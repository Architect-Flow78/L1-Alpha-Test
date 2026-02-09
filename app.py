import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- ЛОГИКА МЕЛЬНИКА ---
def compute_derivatives(df, cols, dt=1.0):
    df = df.copy()
    for c in cols:
        df[f"d_{c}"] = df[c].diff() / dt
        df[f"dd_{c}"] = df[f"d_{c}"].diff() / dt
    return df

def detect_toroidal_nodes(df, col):
    # Узел — это экстремум, где скорость меняет направление (точка замирания)
    d = df[f"d_{col}"]
    nodes = (d.shift(1) * d < 0) # Смена знака скорости
    return nodes.fillna(False)

# --- ИНТЕРФЕЙС ---
st.title("🌀 ТВОЙ ИНСТРУМЕНТ: УЗЛЫ КОМПЕНСАЦИИ")

# Вшитые данные, чтобы не было ошибок загрузки
t = np.linspace(0, 100, 500)
dist = 384400 + 20000 * np.sin(t) * np.exp(-0.005 * t) # Реалистичная затухающая орбита
df_raw = pd.DataFrame({"отсчет": t, "дистанция": dist})

col = "дистанция"

if st.button("▶ НАЙТИ ТОЧКИ ПОКОЯ"):
    df = compute_derivatives(df_raw, [col])
    nodes = detect_toroidal_nodes(df, col)
    
    st.success(f"Найдено узлов: {nodes.sum()}")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df[col], color='gray', alpha=0.5, label="Орбита")
    
    if nodes.any():
        ax.scatter(df.index[nodes], df.loc[nodes, col], color='red', s=100, label="УЗЕЛ (Компенсация)")
    
    ax.legend()
    st.pyplot(fig)
