"""
Datenaufbereitung für Trend-Visualisierung (VERBESSERT)
Liest monatliche Keyword-Daten ein, aggregiert auf Quartalsebene,
nutzt normalisierte keyword_pct Werte und erzeugt vereinfachtes JavaScript.
"""

import os
import pandas as pd
import json
from datetime import datetime


def prepare_trend_data():
    """
    Hauptfunktion zur Datenaufbereitung.
    """
    
    # Pfade definieren
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "Trends_Data")
    
    input_file = os.path.join(data_dir, "keyword_monthly_normalized.csv")
    output_json = os.path.join(script_dir, "trend_data_quarterly.json")
    output_js = os.path.join(script_dir, "script.js")
    
    # ====== SCHRITT 1: CSV einlesen ======
    print("\n" + "="*60)
    print("TREND-DATENAUFBEREITUNG (VERBESSERT)")
    print("="*60)
    
    try:
        df = pd.read_csv(input_file, encoding='utf-8')
        print(f"\n✓ CSV-Datei geladen: {input_file}")
        print(f"  → {len(df)} Zeilen eingelesen")
    except FileNotFoundError:
        print(f"\n✗ FEHLER: CSV-Datei nicht gefunden: {input_file}")
        return False
    except Exception as e:
        print(f"\n✗ FEHLER beim Laden der CSV: {str(e)}")
        return False
    
    # ====== SCHRITT 2: Spalten prüfen ======
    print("\n--- Datenstruktur ---")
    required_cols = ['year_month', 'tech_keyword', 'industry_keyword', 'keyword_pct']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"\n✗ FEHLER: Erforderliche Spalten fehlen: {missing_cols}")
        print(f"Gefunden: {list(df.columns)}")
        return False
    print(f"✓ Alle erforderlichen Spalten vorhanden")
    
    # ====== SCHRITT 3: Daten bereinigen ======
    df_clean = df.copy()
    
    # Datum konvertieren
    df_clean['date'] = pd.to_datetime(df_clean['year_month'], format='%Y-%m', errors='coerce')
    
    # Keywords kombinieren: tech_keyword > industry_keyword
    df_clean['keyword'] = df_clean.apply(
        lambda row: (row['tech_keyword'] if pd.notna(row['tech_keyword']) and str(row['tech_keyword']).strip() != ''
                     else (row['industry_keyword'] if pd.notna(row['industry_keyword']) and str(row['industry_keyword']).strip() != ''
                           else None)),
        axis=1
    )
    
    # ====== SCHRITT 4: Ungültige Zeilen filtern ======
    df_clean = df_clean.dropna(subset=['date', 'keyword', 'keyword_pct'])
    df_clean = df_clean[df_clean['keyword'].astype(str).str.strip() != '']
    print(f"\n✓ Nach Bereinigung: {len(df_clean)} gültige Zeilen")
    
    # ====== SCHRITT 5: Quartale erzeugen ======
    df_clean['year'] = df_clean['date'].dt.year
    df_clean['quarter'] = df_clean['date'].dt.quarter
    df_clean['quarter_label'] = df_clean['year'].astype(str) + '-Q' + df_clean['quarter'].astype(str)
    
    # ====== SCHRITT 6: Aggregieren auf Quartalsebene ======
    # WICHTIG: keyword_pct Mittelwert (nicht Summe!)
    df_quarterly = df_clean.groupby(['quarter_label', 'keyword']).agg({
        'keyword_pct': 'mean',  # Durchschnittlicher Prozentsatz pro Quartal
        'year': 'first',
        'quarter': 'first'
    }).reset_index()
    
    # ====== SCHRITT 7: Chronologisch sortieren ======
    df_quarterly['sort_key'] = df_quarterly['year'] * 10 + df_quarterly['quarter']
    df_quarterly = df_quarterly.sort_values('sort_key').reset_index(drop=True)
    df_quarterly = df_quarterly.drop(columns=['sort_key'])
    
    print(f"✓ Daten auf Quartalsebene aggregiert")
    print(f"  → {len(df_quarterly['keyword'].unique())} unterschiedliche Keywords")
    print(f"  → Metrik: keyword_pct (durchschnittlich pro Quartal)")
    
    # ====== SCHRITT 8: JSON erzeugen ======
    output_data = {
        'metadata': {
            'generated': datetime.now().isoformat(),
            'total_keywords': int(df_quarterly['keyword'].nunique()),
            'quarters_count': int(df_quarterly['quarter_label'].nunique()),
            'metric': 'keyword_pct (normalisiert, %)',
            'date_range': {
                'from': str(df_quarterly['quarter_label'].iloc[0]),
                'to': str(df_quarterly['quarter_label'].iloc[-1])
            }
        },
        'data': []
    }
    
    # Daten strukturieren
    for _, row in df_quarterly.iterrows():
        output_data['data'].append({
            'keyword': str(row['keyword']),
            'quarter': str(row['quarter_label']),
            'keyword_pct': round(float(row['keyword_pct']), 2),
            'year': int(row['year']),
            'quarter_num': int(row['quarter'])
        })
    
    # JSON speichern
    try:
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"\n✓ JSON gespeichert: {output_json}")
    except Exception as e:
        print(f"\n✗ FEHLER beim Speichern der JSON: {str(e)}")
        return False
    
    # ====== SCHRITT 9: Verbessertes JavaScript generieren ======
    try:
        json_string = json.dumps(output_data, ensure_ascii=False, indent=2)
        
        js_template = f'''/*
  Trend-Visualisierung - Script (VERBESSERT)
  Automatisch generiert von prepare_trend_data.py
  Quartalweise Keyword-Trends mit normalisierte Werten (keyword_pct)
*/

// Eingebettete Trenddaten
const trendData = {json_string};

// ===== KONFIGURATION =====
let selectedKeywords = [];
const maxKeywords = 5;

// DOM-Elemente
const keywordsList = document.getElementById('keywordsList');
const resetButton = document.getElementById('resetButton');
const chart = document.getElementById('chart');
const chartWrapper = document.getElementById('chartWrapper');
const warningMessage = document.getElementById('warningMessage');
const emptyStateMessage = document.getElementById('emptyStateMessage');

// ===== HILFSFUNKTIONEN =====

/**
 * Extrahiert alle Keywords
 */
function getAllKeywords() {{
    const keywords = new Set();
    trendData.data.forEach(item => keywords.add(item.keyword));
    return Array.from(keywords).sort();
}}

/**
 * Extrahiert alle Quartale in chronologischer Reihenfolge
 */
function getAllQuarters() {{
    const quarters = new Set();
    trendData.data.forEach(item => quarters.add(item.quarter));
    return Array.from(quarters).sort((a, b) => {{
        const [yearA, qA] = a.split('-Q').map(x => parseInt(x));
        const [yearB, qB] = b.split('-Q').map(x => parseInt(x));
        if (yearA !== yearB) return yearA - yearB;
        return qA - qB;
    }});
}}

/**
 * Holt Daten für ein Keyword
 */
function getDataForKeyword(keyword) {{
    return trendData.data
        .filter(item => item.keyword === keyword)
        .sort((a, b) => {{
            const [yearA, qA] = a.quarter.split('-Q').map(x => parseInt(x));
            const [yearB, qB] = b.quarter.split('-Q').map(x => parseInt(x));
            if (yearA !== yearB) return yearA - yearB;
            return qA - qB;
        }});
}}

/**
 * Erstellt Checkboxen für Keyword-Auswahl
 */
function populateKeywordsList() {{
    const keywords = getAllKeywords();
    keywordsList.innerHTML = '';
    
    if (keywords.length === 0) {{
        keywordsList.classList.add('empty');
        keywordsList.innerHTML = '<div class="loading">Keine Keywords gefunden</div>';
        return;
    }}
    
    keywords.forEach(keyword => {{
        const wrapper = document.createElement('div');
        wrapper.className = 'keyword-checkbox-wrapper';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = `kw-${{keyword}}`;
        checkbox.value = keyword;
        checkbox.addEventListener('change', handleKeywordChange);
        
        const label = document.createElement('label');
        label.htmlFor = `kw-${{keyword}}`;
        label.textContent = keyword;
        
        wrapper.appendChild(checkbox);
        wrapper.appendChild(label);
        keywordsList.appendChild(wrapper);
    }});
    
    // Wähle standardmäßig erstes Keyword aus
    if (keywords.length > 0) {{
        const firstCheckbox = document.getElementById(`kw-${{keywords[0]}}`);
        if (firstCheckbox) {{
            firstCheckbox.checked = true;
            selectedKeywords = [keywords[0]];
        }}
    }}
}}

/**
 * Behandelt Änderungen in der Checkbox-Auswahl
 */
function handleKeywordChange(event) {{
    const checkedBoxes = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'));
    const selected = checkedBoxes.map(box => box.value);
    
    // Max. 5 Keywords
    if (selected.length > maxKeywords) {{
        // Rückgängig machen
        event.target.checked = false;
        showWarning(`⚠️ Maximum {{maxKeywords}} Keywords gleichzeitig. Bitte ein anderes deselektieren.`);
        return;
    }}
    
    selectedKeywords = selected;
    hideWarning();
    updateChart();
}}

/**
 * Zeigt Warnung an
 */
function showWarning(message) {{
    warningMessage.textContent = message;
    warningMessage.style.display = 'block';
}}

/**
 * Versteckt Warnung
 */
function hideWarning() {{
    warningMessage.style.display = 'none';
}}

/**
 * Setzt Auswahl zurück
 */
function resetSelection() {{
    const keywords = getAllKeywords();
    if (keywords.length > 0) {{
        // Alle Checkboxen deselektieren
        document.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
        
        // Erstes Keyword auswählen
        const firstCheckbox = document.getElementById(`kw-${{keywords[0]}}`);
        if (firstCheckbox) {{
            firstCheckbox.checked = true;
            selectedKeywords = [keywords[0]];
        }}
        hideWarning();
        updateChart();
    }}
}}

/**
 * Generiert dynamischen Chart-Titel
 */
function getChartTitle() {{
    if (selectedKeywords.length === 0) {{
        return 'Keine Keywords ausgewählt';
    }} else if (selectedKeywords.length === 1) {{
        return `Trendentwicklung: ${{selectedKeywords[0]}}`;
    }} else {{
        return `Keyword Trend Comparison (Quarterly)`;
    }}
}}

/**
 * Aktualisiert das Chart
 */
function updateChart() {{
    // Empty State prüfen
    if (selectedKeywords.length === 0) {{
        emptyStateMessage.style.display = 'block';
        chartWrapper.style.display = 'none';
        return;
    }}
    
    emptyStateMessage.style.display = 'none';
    chartWrapper.style.display = 'block';
    
    const quarters = getAllQuarters();
    const traces = [];
    const colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'];
    
    // Trace pro ausgewähltem Keyword
    selectedKeywords.forEach((keyword, index) => {{
        const keywordData = getDataForKeyword(keyword);
        
        // Mapping Quartale -> Werte
        const valuesByQuarter = {{}};
        keywordData.forEach(item => {{
            valuesByQuarter[item.quarter] = item.keyword_pct;
        }});
        
        // Arrays erstellen
        const yValues = quarters.map(q => valuesByQuarter[q] || 0);
        
        traces.push({{
            x: quarters,
            y: yValues,
            mode: 'lines+markers',
            name: keyword,
            type: 'scatter',
            line: {{
                color: colors[index % colors.length],
                width: 2.5
            }},
            marker: {{
                size: 5
            }},
            hovertemplate: '<b>%{{fullData.name}}</b><br>' +
                          'Quartal: %{{x}}<br>' +
                          'Share: %{{y:.2f}}%<br>' +
                          '<extra></extra>'
        }});
    }});
    
    const layout = {{
        title: {{
            text: getChartTitle(),
            font: {{ size: 18 }},
        }},
        xaxis: {{
            title: 'Quartal',
            tickangle: -45
        }},
        yaxis: {{
            title: 'Market Share (%)',
            zeroline: false
        }},
        hovermode: 'x unified',
        margin: {{ l: 70, r: 30, t: 100, b: 100 }},
        plot_bgcolor: '#f9f9f9',
        paper_bgcolor: '#ffffff',
        legend: {{
            orientation: 'v',
            x: 1.02,
            y: 1
        }},
        responsive: true
    }};
    
    Plotly.newPlot(chart, traces, layout, {{ responsive: true }});
}}

// ===== EVENT LISTENER =====
resetButton.addEventListener('click', resetSelection);

// ===== INITIALISIERUNG =====
window.addEventListener('DOMContentLoaded', function() {{
    populateKeywordsList();
    updateChart();
    console.log('✓ Visualisierung initialisiert');
    console.log(`  Keywords: {{getAllKeywords().length}}`);
    console.log(`  Quartale: {{getAllQuarters().length}}`);
    console.log(`  Metrik: {{trendData.metadata.metric}}`);
}});
'''
        
        with open(output_js, 'w', encoding='utf-8') as f:
            f.write(js_template)
        print(f"✓ JavaScript generiert: {output_js}")
        
    except Exception as e:
        print(f"\n✗ FEHLER beim JavaScript-Generator: {str(e)}")
        return False
    
    # ====== ABSCHLUSS ======
    print("\n" + "="*60)
    print("ERFOLGREICH ABGESCHLOSSEN")
    print("="*60)
    print(f"\nErgebnisse:")
    print(f"  ✓ {len(df_quarterly)} Quartal-Einträge verarbeitet")
    print(f"  ✓ {len(df_quarterly['keyword'].unique())} unterschiedliche Keywords")
    print(f"  ✓ Metrik: Normalisierte Werte (keyword_pct mit Durchschnitt)")
    print(f"  ✓ Zeitraum: {df_quarterly['quarter_label'].iloc[0]} bis {df_quarterly['quarter_label'].iloc[-1]}")
    print(f"\nGenerierte Dateien:")
    print(f"  ✓ Daten: trend_data_quarterly.json")
    print(f"  ✓ Logik: script.js")
    print(f"\nÖffnen Sie 'index.html' im Browser!")
    print("="*60 + "\n")
    
    return True


if __name__ == "__main__":
    success = prepare_trend_data()
    exit(0 if success else 1)
