import plotly.graph_objects as go
import streamlit as st

def plot_combined_chart(df):
    # ==========================
    # Hitung persentase perubahan
    # ==========================
    percent_change = [0.0]
    has_increase = False
    has_decrease = False

    for i in range(1, len(df)):
        prev = df["Production"].iloc[i-1]
        curr = df["Production"].iloc[i]
        change = ((curr - prev) / prev) * 100 if prev > 0 else (100.0 if curr > 0 else 0.0)
        percent_change.append(change)
        
        # Cek apakah ada data naik atau turun untuk manajemen legenda
        if change >= 0:
            has_increase = True
        else:
            has_decrease = True

    df["Percent_Change"] = percent_change

    fig = go.Figure()

    # ==========================
    # 1️⃣ BAR — Produksi
    # ==========================
    fig.add_trace(go.Bar(
        x=df["Year"],
        y=df["Production"],
        name="Produksi (Bar)",
        marker=dict(color="lightskyblue", opacity=0.9),
        text=[f"{v:,.2f} Ton" for v in df["Production"]],
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(color="black", size=15),
        hovertemplate="<b>Tahun</b>: %{x}<br><b>Produksi</b>: %{y:,.2f} Ton<extra></extra>"
    ))

    # ==========================
    # 2️⃣ LINE - Informasi
    # ==========================
    if has_increase:
        fig.add_trace(go.Scatter(
            x=[None], y=[None], mode='lines+markers',
            line=dict(color="green", width=3),
            marker=dict(size=8),
            name="Persentase (Naik)", # Label yang Anda minta
            showlegend=True
        ))
    
    if has_decrease:
        fig.add_trace(go.Scatter(
            x=[None], y=[None], mode='lines+markers',
            line=dict(color="red", width=3),
            marker=dict(size=8),
            name="Persentase (Turun)",
            showlegend=True
        ))

    # ==========================
    # 3️⃣ LINE - Garis
    # ==========================
    for i in range(1, len(df)):
        # Ganti ke "blue" jika naik, "red" jika turun
        is_up = df["Production"].iloc[i] >= df["Production"].iloc[i-1]
        color = "green" if is_up else "red"

        fig.add_trace(go.Scatter(
            x=df["Year"].iloc[i-1:i+1],
            y=df["Production"].iloc[i-1:i+1],
            mode="lines+markers",
            line=dict(color=color, width=3),
            marker=dict(size=8),
            showlegend=False, # Sembunyikan per segmen agar legenda tidak berantakan
            hoverinfo="skip" # Agar tidak double hover dengan Bar
        ))

    # ==========================
    # 4️⃣ TEXT — Label Persentase
    # ==========================
    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["Production"],
        mode="text",
        text=[f"{p:+.1f}%" if i > 0 else "" for i, p in enumerate(df["Percent_Change"])],
        textposition="top center",
        showlegend=False,
        textfont=dict(size=12, color="white") # Sesuaikan warna teks jika background gelap
    ))

    # ==========================
    # Layout
    # ==========================
    fig.update_layout(
        title="📊 Prediksi Produksi Padi",
        xaxis_title="Tahun",
        yaxis_title="Produksi (Ton)",
        template="plotly_dark", # Menggunakan dark mode agar mirip screenshot Anda
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(0,0,0,0)" # Transparan
        ),
        margin=dict(t=80)
    )

    st.plotly_chart(fig, use_container_width=True)