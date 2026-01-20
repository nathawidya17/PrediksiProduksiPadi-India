import streamlit as st
import pandas as pd

from src.utils import load_css
from src.loaders import load_all_models
from src.model import predict_single
from src.visualization import plot_combined_chart

st.set_page_config(page_title="Prediksi Produksi Padi", layout="wide")

# Load CSS
load_css("assets/style.css")

# Load model & scaler
model, scaler = load_all_models()

st.title("Sistem Prediksi Produksi Padi India")

# ================= INPUT TAHUN =================

col1, col2 = st.columns(2)
with col1:
    start_year = st.number_input(
        "Tahun Awal",
        min_value=2016,
        max_value=2100,
        value=2016,
        step=1
    )

with col2:
    end_year = st.number_input(
        "Tahun Akhir",
        min_value=start_year,
        max_value=2100,
        value=2020,
        step=1
    )

submit = st.button("Tampilkan Prediksi")

# ================= PREDIKSI =================

if submit:
    year_range = list(range(start_year, end_year + 1))
    rows = []

    AREA_BY_YEAR = {
        2016: 100,
        2017: 150,
        2018: 200,
        2019: 300,
        2020: 350,
        2021: 400,
        2022: 450,
        2023: 500,
        2024: 600,
        2025: 650,
        2026: 700,
        2027: 750,
        2028: 800,
        2029: 900,
        2030: 950,
    }

    for year in year_range:
        area = AREA_BY_YEAR.get(year)

        if area is None:
            st.error(f"Data area untuk tahun {year} tidak tersedia")
            st.stop()

        pred_value = predict_single(
            model=model,
            scaler=scaler,
            area=area
        )

        rows.append({
            "Year": year,
            "Area (ha)": area,
            "Production": pred_value
        })

    df_pred = pd.DataFrame(rows)

    st.subheader("Visualisasi Prediksi Produksi Padi India")
    plot_combined_chart(df_pred)

    
