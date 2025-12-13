import streamlit as st
import pandas as pd

from src.utils import load_css
from src.loaders import load_all_models
from src.model import predict_single
from src.visualization import plot_combined_chart

st.set_page_config(page_title="Prediksi Produksi Padi", layout="wide")

# Load CSS
load_css("assets/style.css")

# Load model & scaler (TANPA encoder)
model, scaler = load_all_models()

st.title("Sistem Prediksi Padi India")

# ================= INPUT TAHUN =================

col1, col2 = st.columns(2)
with col1:
    start_year = st.number_input("Tahun Awal", min_value=2016, max_value=2100, value=2016, step=1)
with col2:
    end_year = st.number_input("Tahun Akhir", min_value=start_year, max_value=2100, value=2020, step=1)


# ================= INPUT AREA PER TAHUN =================
st.subheader("Masukkan Area per Tahun (ha)")

year_range = list(range(start_year, end_year + 1))
area_values = {}

cols = st.columns(min(4, len(year_range)))
for idx, year in enumerate(year_range):
    col = cols[idx % len(cols)]
    with col:
        area_values[year] = st.number_input(
            f"Area {year}",
            min_value=1.0,
            key=f"area_{year}",
            step=1.0,
            format="%.2f"
        )

submit = st.button("Prediksi")

# ================= PREDIKSI =================

if submit:
    rows = []

    for year in year_range:
        pred_value = predict_single(
            model=model,
            scaler=scaler,
            area=area_values[year]
        )

        rows.append({
            "Year": year,
            "Area": area_values[year],
            "Production": pred_value
        })

    df_pred = pd.DataFrame(rows)

    # ================= OUTPUT =================
    st.subheader("Visualisasi Hasil Prediksi")
    plot_combined_chart(df_pred)
