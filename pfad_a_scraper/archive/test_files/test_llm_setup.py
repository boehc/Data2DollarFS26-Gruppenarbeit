"""
Test script to verify LLM analyzer setup.
Checks API key, dependencies, and runs a single article test.
"""

import sys
import os
import json

def test_api_key():
    """Test if API key is set."""
    print("1️⃣  Testing OpenAI API Key...")
    api_key = os.environ.get('OPENAI_API_KEY')
    
    if not api_key:
        print("   ❌ OPENAI_API_KEY not set!")
        print("   Fix: export OPENAI_API_KEY='your-key-here'")
        return False
    
    if len(api_key) < 20:
        print("   ⚠️  API key seems too short. Is it correct?")
        return False
    
    print(f"   ✅ API key found (starts with: {api_key[:7]}...)")
    return True


def test_dependencies():
    """Test if required packages are installed."""
    print("\n2️⃣  Testing Dependencies...")
    
    missing = []
    
    try:
        import openai
        print("   ✅ openai package installed")
    except ImportError:
        print("   ❌ openai package missing")
        missing.append("openai")
    
    try:
        import pandas
        print("   ✅ pandas package installed")
    except ImportError:
        print("   ❌ pandas package missing")
        missing.append("pandas")
    
    if missing:
        print(f"\n   Install missing packages:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    return True


def test_input_file():
    """Test if input file exists and is valid."""
    print("\n3️⃣  Testing Input File...")
    
    input_file = 'data/startupticker_articles_for_llm.json'
    
    if not os.path.exists(input_file):
        print(f"   ❌ Input file not found: {input_file}")
        return False
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)
        
        print(f"   ✅ Input file valid: {len(articles)} articles found")
        
        # Check first article structure
        if articles:
            first = articles[0]
            required_keys = ['article_text', 'publication_date', 'year']
            missing_keys = [k for k in required_keys if k not in first]
            
            if missing_keys:
                print(f"   ⚠️  Missing keys in articles: {missing_keys}")
                return False
            
            print(f"   ✅ Article structure valid")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error reading input file: {e}")
        return False


def test_api_connection():
    """Test actual API connection with a minimal call."""
    print("\n4️⃣  Testing OpenAI API Connection...")
    
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        
        # Simple test call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'API works!' in JSON format"}
            ],
            max_tokens=10,
            response_format={"type": "json_object"}
        )
        
        result = response.choices[0].message.content
        print(f"   ✅ API connection successful!")
        print(f"   Response: {result}")
        return True
        
    except Exception as e:
        print(f"   ❌ API connection failed: {str(e)}")
        
        error_msg = str(e).lower()
        if 'api key' in error_msg or 'authentication' in error_msg:
            print("   → Check your API key")
        elif 'rate limit' in error_msg:
            print("   → Rate limit exceeded, wait a moment")
        elif 'insufficient' in error_msg or 'quota' in error_msg:
            print("   → Insufficient credits on your OpenAI account")
        
        return False


def test_single_extraction():
    """Test extraction on a single article."""
    print("\n5️⃣  Testing Single Article Extraction...")
    
    try:
        from openai import OpenAI
        
        # Load one article
        with open('data/startupticker_articles_for_llm.json', 'r', encoding='utf-8') as f:
            articles = json.load(f)
        
        if not articles:
            print("   ⚠️  No articles to test")
            return False
        
        article = articles[0]
        print(f"   Testing with: {article.get('title', 'Unknown')[:60]}...")
        
        # Simple extraction prompt
        prompt = f"""Extract the startup name from this article. Return only JSON.

Article: {article['article_text'][:1000]}

Return:
{{
  "startup_name": "extracted name or null"
}}"""
        
        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a data extraction assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=100,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        extracted_name = result.get('startup_name', 'null')
        
        print(f"   ✅ Extraction successful!")
        print(f"   Extracted name: {extracted_name}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Extraction failed: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("="*70)
    print("🧪 LLM ANALYZER SETUP TEST")
    print("="*70)
    
    tests = [
        ("API Key", test_api_key),
        ("Dependencies", test_dependencies),
        ("Input File", test_input_file),
        ("API Connection", test_api_connection),
        ("Single Extraction", test_single_extraction),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
            
            if not result:
                print(f"\n⚠️  Test '{name}' failed. Fix this before continuing.\n")
                break
                
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {str(e)}\n")
            results.append((name, False))
            break
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}  {name}")
    
    all_passed = all(r for _, r in results)
    
    if all_passed:
        print("\n✅ ALL TESTS PASSED!")
        print("\nYou're ready to run the analyzer:")
        print("   python3 8_llm_article_analyzer.py")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("\nFix the issues above before running the analyzer.")
        print("See LLM_ANALYZER_README.md for help.")
    
    print("="*70)
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
