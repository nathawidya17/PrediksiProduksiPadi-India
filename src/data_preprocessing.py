import numpy as np

def preprocess_features(encoder, scaler, state, district, season, area):
        """Preprocess input features into scaled numpy array.

        Supports two encoder formats:
        - An encoder object with a `.transform([[state, district, season]])` method (e.g.,
            an sklearn transformer that encodes multiple columns at once).
        - A dict mapping column names to per-column label encoder objects (e.g.,
            `{"State_Name": LabelEncoder(...), "District_Name": ..., "Season": ...}`),
            where each encoder has `.transform([value])`.
        """

        # Categorical encode: accept either a transformer or a dict of encoders
        if hasattr(encoder, "transform") and callable(getattr(encoder, "transform")):
                encoded = encoder.transform([[state, district, season]])[0]
        else:
                # Assume dict-like with keys matching column names
                s1 = encoder["State_Name"].transform([state])[0]
                s2 = encoder["District_Name"].transform([district])[0]
                s3 = encoder["Season"].transform([season])[0]
                encoded = [s1, s2, s3]

        # Log1p area
        area_log = np.log1p(area)

        # The saved MinMaxScaler was fitted on two columns: [Area, Production].
        # During model construction we only need the scaled Area (production is a dummy 0),
        # so pass a 2-column array and take the first value back.
        area_scaled_pair = scaler.transform([[area_log, 0.0]])
        area_scaled = area_scaled_pair[0][0]

        # Build final feature vector in the same column order used by the model:
        # [State_enc, District_enc, Season_enc, Area_scaled]
        X = list(encoded) + [area_scaled]
        X = np.array(X).reshape(1, -1)

        return X
