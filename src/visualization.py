import plotly.graph_objects as go
import streamlit as st

def plot_combined_chart(df):

    # ==========================
    # Hitung persentase perubahan
    # ==========================
    percent_change = [0.0]
    for i in range(1, len(df)):
        prev = df["Production"].iloc[i-1]
        curr = df["Production"].iloc[i]
        if prev > 0:
            change = ((curr - prev) / prev) * 100
        elif curr > 0:
            change = 100.0
        else:
            change = 0.0
        percent_change.append(change)

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
        text=[f"{v:,.2f}" for v in df["Production"]],
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(color="black", size=15),
        hovertemplate=
            "<b>Tahun</b>: %{x}<br>"
            "<b>Produksi</b>: %{y:,.2f} Ton<br>"
            "<extra></extra>"
    ))

    # ==========================
    # 2️⃣ LINE — Warna Dinamis (Hijau / Merah)
    # ==========================
    for i in range(1, len(df)):
        color = "green" if df["Production"].iloc[i] >= df["Production"].iloc[i-1] else "red"

        fig.add_trace(go.Scatter(
            x=df["Year"].iloc[i-1:i+1],
            y=df["Production"].iloc[i-1:i+1],
            mode="lines+markers",
            line=dict(color=color, width=3),
            marker=dict(size=8),
            showlegend=False,
            hovertemplate=
                "<b>Tahun</b>: %{x}<br>"
                "<b>Produksi</b>: %{y:,.2f} Ton<br>"
                "<extra></extra>"
        ))

    # ==========================
    # 3️⃣ TEXT — Persentase Perubahan
    # ==========================
    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["Production"],
        mode="text",
        text=[f"{p:.1f}%" if i > 0 else "" for i, p in enumerate(df["Percent_Change"])],
        textposition="top center",
        showlegend=False
    ))

    # ==========================
    # Layout
    # ==========================
    fig.update_layout(
        title="📊 Prediksi Produksi Padi",
        xaxis_title="Tahun",
        yaxis_title="Produksi (Ton)",
        barmode="overlay",
        template="plotly_white",
        legend=dict(x=0.01, y=0.99),
        margin=dict(t=80)
    )

    st.plotly_chart(fig, use_container_width=True)
