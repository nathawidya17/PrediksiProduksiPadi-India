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

    # Data dummy area (sesuai kode asli Anda)
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

    # Menghitung Persentase Pertumbuhan untuk Data Pendukung
    df_pred['Growth (%)'] = df_pred['Production'].pct_change() * 100
    avg_growth = df_pred['Growth (%)'].mean()

    # --- Bagian Visualisasi ---
    st.subheader("Visualisasi Prediksi Produksi Padi India")
    plot_combined_chart(df_pred)
    
    st.divider() # Garis pemisah visual

    # --- Bagian Storytelling / Insight ---
    st.subheader("Analisis Tren Produksi")
    
    # Menggunakan st.markdown dengan HTML agar bisa atur warna (putih) dan ukuran font
    st.markdown(
        f"""
        <div style="
            background-color: #3174f0; 
            padding: 20px; 
            border-radius: 10px;
            color: white;
            font-size: 18px;
            line-height: 1.6;
            margin-bottom: 20px;
        ">
            <strong style="font-size: 22px;"> Kesimpulan Prediksi:</strong>
            <br><br>
            Berdasarkan grafik di atas, terlihat jelas bahwa <strong>hasil prediksi produksi padi cenderung naik dari tahun ke tahun</strong> ({start_year} - {end_year}). 
            Peningkatan luas area tanam memberikan dampak positif yang signifikan terhadap hasil panen.
            <br><br>
            Selain itu, jika kita melihat laju pertumbuhannya, <strong>persentase kenaikan produksi cenderung positif tiap tahunnya dan menunjukan pola yang mulai stabil</strong>. 
            Hal ini mengindikasikan bahwa produktivitas pertanian diprediksi akan terus terjaga seiring dengan bertambahnya waktu dan luas lahan.
        </div>
        """,
        unsafe_allow_html=True
    )