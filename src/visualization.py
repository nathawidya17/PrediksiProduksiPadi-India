import plotly.graph_objects as go
import streamlit as st

def plot_combined_chart(df):
    # Hitung persentase perubahan dibanding tahun sebelumnya
    percent_change = [0.0]  # Tahun pertama tidak ada perubahan
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

    # Bar chart
    fig.add_trace(go.Bar(
        x=df["Year"],
        y=df["Production"],
        name="Produksi (Bar)",
        marker_color="lightskyblue"
    ))

    # Line chart di atas bar chart
    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["Production"],
        mode="lines+markers+text",
        name="Produksi (Line)",
        line=dict(color="crimson", width=3),
        marker=dict(size=8),
        text=[f"{p:.1f}% ↑" if i>0 else "" for i,p in enumerate(df["Percent_Change"])],
        textposition="top center"
    ))

    fig.update_layout(
        title="📊 Prediksi Produksi Padi",
        xaxis_title="Tahun",
        yaxis_title="Produksi (Ton)",
        barmode="overlay",
        template="plotly_white",
        legend=dict(x=0.01, y=0.99)
    )

    st.plotly_chart(fig, use_container_width=True)
