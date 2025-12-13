import plotly.graph_objects as go
import streamlit as st

def plot_combined_chart(df):

    # Hitung persentase perubahan
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
    # 1️⃣ BAR — tampilkan angka hasil prediksi di atas bar
    # ==========================
    fig.add_trace(go.Bar(
    x=df["Year"],
    y=df["Production"],
    name="Produksi (Bar)",
    marker=dict(color="lightskyblue", opacity=0.9),

    # angka produksi ditampilkan di dalam bar
    text=[f"{v:,.2f}" for v in df["Production"]],
    textposition="inside",
    insidetextanchor="middle",
    textfont=dict(color="black", size=15),

    hovertemplate="<b>Tahun</b>: %{x}<br>"
                  "<b>Produksi</b>: %{y:,.2f} Ton<br>"
))

    # ==========================
    # 2️⃣ LINE — persentase perubahan tiap tahun
    # ==========================
    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["Production"],
        mode="lines+markers+text",
        name="Produksi (Line)",
        line=dict(color="crimson", width=3),
        marker=dict(size=8),
        text=[f"{p:.1f}%" if i>0 else "" for i,p in enumerate(df["Percent_Change"])],
        textposition="top center",
        hovertemplate="<b>Tahun</b>: %{x}<br>"
                      "<b>Produksi</b>: %{y:,.2f} Ton<br>"
                      "<b>Perubahan</b>: %{text}<br>"
    ))

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
    