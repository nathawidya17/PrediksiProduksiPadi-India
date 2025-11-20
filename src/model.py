import numpy as np
import pandas as pd

# Use the preprocessing helper which expects the encoder and scaler
# objects that are loaded from `models/` (via `src.loaders`).
from .data_preprocessing import preprocess_features


# ==========================
# PREDIKSI RANGE TAHUN
# ==========================
def predict_year_range(model, scaler, encoder, state, district, season, start_year, end_year, area):
    years = list(range(start_year, end_year + 1))
    predictions = []

    for yr in years:
        # prepare input and get model output (model likely predicts scaled production)
        X = preprocess_features(encoder, scaler, state, district, season, area)
        pred_scaled = model.predict(X)[0]

        # compute scaled area used with the scaler (scaler was fitted on [Area_log, Production_log])
        area_log = np.log1p(area)
        area_scaled = scaler.transform([[area_log, 0.0]])[0][0]

        # inverse the MinMax scaling for production by providing the pair [area_scaled, pred_scaled]
        try:
            inv_pair = scaler.inverse_transform([[area_scaled, pred_scaled]])
            prod_log = inv_pair[0][1]
            prod = np.expm1(prod_log)
        except Exception:
            # fallback: if scaler/inverse doesn't match, try treating model output as log1p directly
            prod = float(np.expm1(pred_scaled))

        predictions.append(prod)

    return pd.DataFrame({"Year": years, "Production": predictions})


# ==========================
# PREDIKSI SINGLE INPUT
# ==========================
def predict_single(model, scaler, encoder, state, district, season, area):
    X = preprocess_features(encoder, scaler, state, district, season, area)
    pred_scaled = model.predict(X)[0]

    # compute scaled area used with the scaler
    area_log = np.log1p(area)
    area_scaled = scaler.transform([[area_log, 0.0]])[0][0]

    # inverse the MinMax scaling for production by providing the pair [area_scaled, pred_scaled]
    try:
        inv_pair = scaler.inverse_transform([[area_scaled, pred_scaled]])
        prod_log = inv_pair[0][1]
        prod = np.expm1(prod_log)
    except Exception:
        # fallback: treat model output as log1p of production
        prod = float(np.expm1(pred_scaled))

    return float(prod)


# NOTE:
# The previous implementation built a pandas DataFrame and tried to call
# per-column `.transform()` on `encoder[...]` objects. The repository
# stores `labelencode.pkl` and `minmax.pkl` as objects that are consumed
# by `src.data_preprocessing.preprocess_features` (single `.transform` on
# the encoder and then scaler.transform on the full feature vector). To
# keep behaviour consistent we now reuse that helper.
