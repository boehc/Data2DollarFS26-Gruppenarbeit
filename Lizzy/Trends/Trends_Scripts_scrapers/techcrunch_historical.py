import scrapy


class TechcrunchHistoricalSpider(scrapy.Spider):
    name = "techcrunch_historical"
    allowed_domains = ["techcrunch.com"]
    # Multiple category URLs to scrape
    start_urls = [
        "https://techcrunch.com/category/startups/",
        "https://techcrunch.com/category/venture/",
        "https://techcrunch.com/category/apps/",
        "https://techcrunch.com/category/artificial-intelligence/",
        "https://techcrunch.com/category/security/",
    ]
    
    # Max articles per category per month
    MAX_PER_CATEGORY_MONTH = 50
    
    # Custom settings for politeness
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 5,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Track collected article URLs across all pages for deduplication
        self.collected_urls = set()
        # Track which categories have hit pre-2023 content
        self.stop_categories = set()
        # Track per-category per-month counts: key is "category_url|YYYY-MM"
        self.category_month_counts = {}
        # Category name mapping
        self.category_names = {
            "https://techcrunch.com/category/startups/": "startups",
            "https://techcrunch.com/category/venture/": "venture",
            "https://techcrunch.com/category/apps/": "apps",
            "https://techcrunch.com/category/artificial-intelligence/": "ai",
            "https://techcrunch.com/category/security/": "security",
        }

    def start_requests(self):
        """Yield requests for each category URL with metadata."""
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse,
                meta={'category_url': url})

    def parse(self, response):
        """Extract article links from listing page and follow next page if needed."""
        category_url = response.meta.get('category_url', response.url)
        if category_url in self.stop_categories:
            return
        
        self.logger.info(f"Parsing: {response.url} (Collected: {len(self.collected_urls)})")
        
        # Extract article links using exact selector
        article_links = response.css('a.post-block__title__link::attr(href)').getall()
        
        # Fallback selector
        if not article_links:
            article_links = response.css('h3 a::attr(href)').getall()
        
        # Process article links with deduplication
        new_links_count = 0
        found_pre_2023_article = False
        
        for link in article_links:
            article_url = response.urljoin(link)
            
            # Filter: TechCrunch domain, exclude videos/events, not already collected
            if ("techcrunch.com" in article_url and 
                "/video/" not in article_url and 
                "/events/" not in article_url and
                article_url not in self.collected_urls):
                
                # Add to collected set
                self.collected_urls.add(article_url)
                new_links_count += 1
                
                # Yield request to parse full article (with date filter in parse_article)
                yield scrapy.Request(
                    article_url,
                    callback=self.parse_article,
                    errback=self.errback_parse_article,
                    meta={'category_url': category_url}
                )
        
        self.logger.info(f"Found {new_links_count} new articles on this page. Total collected: {len(self.collected_urls)}")
        
        # Progress checkpoint every 100 articles
        if len(self.collected_urls) % 100 == 0:
            total = sum(self.category_month_counts.values())
            self.logger.info(f"✓ Progress: {len(self.collected_urls)} new articles | {total} within caps")
        
        # Follow next page if category hasn't hit pre-2023 articles
        if category_url not in self.stop_categories:
            next_page = response.css('a.wp-block-query-pagination-next::attr(href)').get()
            
            if next_page:
                next_url = response.urljoin(next_page)
                self.logger.info(f"✓ Following next page: {next_url}")
                
                yield scrapy.Request(
                    next_url,
                    callback=self.parse,
                    meta={'category_url': category_url}
                )
            else:
                self.logger.warning(f"⚠️  No next page link found. Stopping at {len(self.collected_urls)} articles")
        else:
            self.logger.info(f"Category {category_url} stopped (pre-2023 or already stopped)")

    def parse_article(self, response):
        """Extract article details from individual article pages."""
        
        # Extract title
        title = response.css('h1::text').get()
        if title:
            title = title.strip()
        
        # Extract publication date FIRST for date filtering
        publication_date = response.css('time::attr(datetime)').get()
        if publication_date:
            publication_date = publication_date.strip()
        
        # Extract year from publication_date
        year = None
        if publication_date:
            year = publication_date[:4]
        
        # DATE FILTER: Only yield articles from 2023, 2024, 2025
        if not year:
            self.logger.warning(f"No date found: {response.url}")
            return
        
        try:
            year_int = int(year)
        except ValueError:
            self.logger.warning(f"Invalid year format: {year} for {response.url}")
            return
        
        # Skip articles from 2027 or later
        if year_int > 2026:
            self.logger.info(f"Skipping 2027+ article: {response.url}")
            return
        
        # Stop crawling further if we hit 2022 or earlier
        if year_int < 2023:
            self.logger.info(f"Found pre-2023 article (year {year}): {response.url}")
            category_url = response.meta.get('category_url', '')
            self.stop_categories.add(category_url)
            self.logger.info(f"Stopping {category_url} - hit pre-2023 content")
            return
        
        # Get category info and apply per-category per-month cap
        category_url = response.meta.get('category_url', '')
        category_name = self.category_names.get(category_url, 'unknown')
        year_month = publication_date[:7]  # e.g. "2023-04"
        
        # Check per-category per-month cap
        cap_key = f"{category_url}|{year_month}"
        current_count = self.category_month_counts.get(cap_key, 0)
        
        if current_count >= self.MAX_PER_CATEGORY_MONTH:
            self.logger.info(f"Cap reached: {category_name} {year_month} ({current_count}/50)")
            return
        
        # Safety total cap
        total = sum(self.category_month_counts.values())
        if total >= 10000:
            self.logger.info("Safety cap of 10000 reached")
            return
        
        # Update counter
        self.category_month_counts[cap_key] = current_count + 1
        
        # Log when month-category is complete
        if current_count + 1 == self.MAX_PER_CATEGORY_MONTH:
            new_total = sum(self.category_month_counts.values())
            self.logger.info(f"✓ {category_name} {year_month} complete | Total: {new_total}")
        
        # Extract author
        author = response.css('a[rel="author"]::text').get()
        if not author:
            author = response.css('.article-byline a::text').get()
        if author:
            author = author.strip()
        
        # Extract article excerpt
        article_excerpt = response.css('meta[name="description"]::attr(content)').get()
        if article_excerpt:
            article_excerpt = article_excerpt.strip()
        
        # Extract article text from all paragraphs - try multiple selectors
        article_text = ""
        
        # Try first selector: div.entry-content p::text
        article_paragraphs = response.css('div.entry-content p::text').getall()
        if article_paragraphs:
            article_text = " ".join([p.strip() for p in article_paragraphs if p.strip()])
        
        # Fallback to second selector if first didn't work
        if not article_text:
            article_paragraphs = response.css('div.wp-block-post-content p::text').getall()
            if article_paragraphs:
                article_text = " ".join([p.strip() for p in article_paragraphs if p.strip()])
        
        # Fallback to third selector if second didn't work
        if not article_text:
            article_paragraphs = response.css('article div[class*="content"] p ::text').getall()
            if article_paragraphs:
                article_text = " ".join([p.strip() for p in article_paragraphs if p.strip()])
        
        # Fallback to fourth selector
        if not article_text:
            article_paragraphs = response.css('div.article-content p ::text').getall()
            if article_paragraphs:
                article_text = " ".join([p.strip() for p in article_paragraphs if p.strip()])
        
        # Fallback to fifth selector
        if not article_text:
            article_paragraphs = response.css('article p ::text').getall()
            if article_paragraphs:
                article_text = " ".join([p.strip() for p in article_paragraphs if p.strip()])
        
        # Return extracted data as a dictionary
        yield {
            "source": "TechCrunch",
            "category": category_name,
            "source_type": "startup_news",
            "title": title,
            "url": response.url,
            "publication_date": publication_date,
            "year": year,
            "year_month": year_month,
            "author": author,
            "article_excerpt": article_excerpt,
            "article_text": article_text,
            "trend_type": "hard_trend",
        }
        
        self.logger.info(f"Parsed ({year}): {title[:60]}")

    def errback_parse_article(self, failure):
        """Handle errors during article parsing."""
        self.logger.error(f"Error parsing article: {failure.request.url}")
