import numpy as np

def preprocess_features(scaler, area):
    """
    Preprocess ONLY the Area feature.
    Returns scaled single feature (Area).
    """
    # log transform area
    area_log = np.log1p(area)

    # scaler expects 2 features: [Area_log, Production_log]
    # set dummy Production_log = 0
    scaled_pair = scaler.transform([[area_log, 0.0]])

    # only scaled area is used
    area_scaled = scaled_pair[0][0]

    return np.array([[area_scaled]])


def predict_single(model, scaler, area):
    """
    Predict production using log+scaled area.
    THEN inverse scale and inverse log the result.
    """
    # --- preprocessing ---
    X = preprocess_features(scaler, area)

    # --- model prediction (still in scaled log space) ---
    y_scaled_log = model.predict(X)[0]

    # --- inverse scaling ---
    # scaler needs 2 columns: [Area_log_scaled, Production_log_scaled]
    inv_input = np.array([[0, y_scaled_log]])   # Area dummy = 0
    _, production_log = scaler.inverse_transform(inv_input)[0]

    # --- inverse log ---
    production_real = np.expm1(production_log)

    return float(production_real)
