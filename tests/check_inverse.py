from src.loaders import load_all_models
from src.data_preprocessing import preprocess_features
import numpy as np
import json

model, scaler, encoder = load_all_models()
state_dist = json.load(open('data/state_district.json'))
state = list(state_dist.keys())[0]
district = state_dist[state][0]
season = json.load(open('data/season_list.json'))[0]
area = 100.0

print('sample:', state, district, season, area)
X = preprocess_features(encoder, scaler, state, district, season, area)
print('prepared X shape:', X.shape)
raw_pred = model.predict(X)[0]
print('model raw prediction:', raw_pred)

# Try inverse by assuming model predicts scaled production (MinMax scaled)
# We need to craft a 2-col array [area_log, pred_scaled] but scaler was fitted on raw area_log and production (maybe log1p(production)).
area_log = np.log1p(area)
try:
    inv = scaler.inverse_transform([[area_log, raw_pred]])
    print('scaler.inverse_transform result:', inv)
    possible_prod_value = inv[0][1]
    print('possible production value (may be log1p):', possible_prod_value)
    try:
        print('after expm1:', np.expm1(possible_prod_value))
    except Exception as e:
        print('expm1 failed:', e)
except Exception as e:
    print('scaler.inverse_transform failed:', e)

# Also try treating raw_pred as log1p directly
try:
    print('treating raw_pred as log1p -> expm1:', np.expm1(raw_pred))
except Exception as e:
    print('expm1 on raw_pred failed:', e)
