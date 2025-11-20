import streamlit as st
import pandas as pd
import numpy as np

from src.utils import load_css
from src.loaders import load_json_files, load_all_models
from src.model import predict_single, predict_year_range
from src.visualization import plot_combined_chart

st.set_page_config(page_title="Prediksi Produksi Padi", layout="wide")

# Load CSS
load_css("assets/style.css")

# Load JSON: state -> district & season
state_dict, season_list = load_json_files()

# Load model, scaler, encoder
model, scaler, encoder = load_all_models()

st.title("📈 Sistem Prediksi Padi India")


# ================= INPUT =================
# Tampilkan input state, district, season dalam satu baris
col_state, col_district, col_season = st.columns(3)
with col_state:
    state = st.selectbox("🌎 Pilih State", list(state_dict.keys()))
with col_district:
    district = st.selectbox("🏙️ Pilih District", state_dict[state])
with col_season:
    season = st.selectbox("🌤️ Pilih Season", season_list)

# Tahun awal minimal 2016
col1, col2 = st.columns(2)
with col1:
    start_year = st.number_input("Tahun Awal", min_value=2016, max_value=2100, value=2016, step=1)
with col2:
    end_year = st.number_input("Tahun Akhir", min_value=start_year, max_value=2100, value=2020, step=1)


# ================= INPUT AREA PER TAHUN =================
st.subheader("🌾 Masukkan Area per Tahun (ha)")
year_range = list(range(start_year, end_year + 1))
area_values = {}

# Tampilkan input area per tahun dalam beberapa kolom agar lebih ringkas
cols = st.columns(min(4, len(year_range)))
for idx, year in enumerate(year_range):
    col = cols[idx % len(cols)]
    with col:
        area_values[year] = st.number_input(
            f"Area {year}",
            min_value=1.0,
            key=f"area_{year}",
            step=1.0,
            format="%.2f",
            label_visibility="visible"
        )

submit = st.button("Prediksi")

# ================= PREDIKSI =================
if submit:
    rows = []
    for year in year_range:
        pred_value = predict_single(
            model=model,
            scaler=scaler,
            encoder=encoder,
            state=state,
            district=district,
            season=season,
            area=area_values[year]
        )

        rows.append({
            "Year": year,
            "Area": area_values[year],
            "Production": pred_value
        })

    df_pred = pd.DataFrame(rows)

    # ================= OUTPUT =================
    st.subheader("📊 Visualisasi Hasil Prediksi")
    plot_combined_chart(df_pred)
