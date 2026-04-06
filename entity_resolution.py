import pandas as pd
from rapidfuzz import fuzz

# 1. INCARCA DATELE
df = pd.read_csv('presales_data_sample.csv')
print(f"Date incarcate: {len(df)} randuri, {df['input_row_key'].nunique()} companii")

# 2. FUNCTII
def clean(val):
    if pd.isna(val):
        return ""
    val = str(val).strip().lower()
    for suffix in [' a/s', ' as', ' aps', ' gmbh', ' ltd', ' limited',
                   ' sdn bhd', ' pte ltd', ' inc', ' llc', ' sa', ' ab',
                   ' oy', ' nuf', ' berhad', ' co ltd', ' pte', ' plc',
                   ' ag', ' bv', ' nv', ' spa', ' srl', ' kft']:
        val = val.replace(suffix, '').strip()
    return val

def score_candidate(row):
    name_ratio = fuzz.token_sort_ratio(clean(row['input_company_name']), clean(row['company_name'])) / 100
    name_partial = fuzz.partial_ratio(clean(row['input_company_name']), clean(row['company_name'])) / 100
    name_score = max(name_ratio, name_partial)
    country_score = 1.0 if clean(row['input_main_country']) == clean(row['main_country']) else 0.0
    city_score = fuzz.token_sort_ratio(clean(row['input_main_city']), clean(row['main_city'])) / 100
    street_score = fuzz.token_sort_ratio(clean(row['input_main_street']), clean(row['main_street'])) / 100
    total = (name_score * 0.40) + (country_score * 0.35) + (city_score * 0.15) + (street_score * 0.10)
    return round(total, 3), round(name_score, 3), country_score

# 3. APLICA SCORING
print("Calculez scoruri...")
df['auto_score'], df['name_score'], df['country_score'] = zip(*df.apply(score_candidate, axis=1))

# 4. GASESTE BEST MATCH
results = []

for key, group in df.groupby('input_row_key'):
    best_idx = group['auto_score'].idxmax()
    best = group.loc[best_idx]
    
    name_s = best['name_score']
    country_s = best['country_score']
    total_s = best['auto_score']
    
    if name_s >= 0.80 and country_s == 1.0 and total_s >= 0.75:
        status = 'AUTO HIGH'
    elif name_s >= 0.65 and country_s == 1.0:
        status = 'AUTO MEDIUM'
    elif total_s >= 0.55:
        status = 'REVIEW'
    else:
        status = 'NO MATCH'
    
    results.append({
        'input_row_key': int(key),
        'input_company': group.iloc[0]['input_company_name'],
        'input_country': group.iloc[0]['input_main_country'],
        'input_city': group.iloc[0]['input_main_city'],
        'suggested_match': best['company_name'],
        'match_country': best['main_country'],
        'match_city': best['main_city'],
        'website': best['website_url'],
        'score': total_s,
        'status': status,
        'notes': ''
    })

results_df = pd.DataFrame(results).sort_values('input_row_key')

# 5. STATISTICI
print("\n=== REZULTATE ===")
print(results_df['status'].value_counts())

# 6. EXPORT
results_df.to_excel('entity_resolution_results.xlsx', index=False)
print("\nFisier salvat: entity_resolution_results.xlsx")