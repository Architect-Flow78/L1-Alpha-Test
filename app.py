import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- ТВОЙ ИЗНАЧАЛЬНЫЙ ИНСТРУМЕНТ (ORIGINAL L0-FLOW) ---
def compute_derivatives(df, cols, dt=1.0):
    df = df.copy()
    for c in cols:
        df[f"d_{c}"] = df[c].diff() / dt
        df[f"dd_{c}"] = df[f"d_{c}"].diff() / dt
    return df

def toroidal_score(df, cols):
    score = pd.Series(0.0, index=df.index)
    for c in cols:
        score += df[f"d_{c}"].abs()
        score += df[f"dd_{c}"].abs()
    return score

def detect_toroidal_nodes(df, cols, threshold=0.1):
    # Твой метод: узел там, где сумма производных минимальна (точка покоя)
    score = toroidal_score(df, cols)
    # Ищем локальные минимумы через сравнение с соседями
    is_min = (score < score.shift(1)) & (score < score.shift(-1))
    return is_min.fillna(False)

# --- ИНТЕРФЕЙС ---
st.title("🌀 ТВОЙ ИНСТРУМЕНТ: УЗЛЫ КОМПЕНСАЦИИ")

@st.cache_data
def load_nasa_data():
    url = "https://raw.githubusercontent.com/plotly/datasets/master/astronomy_data.csv"
    return pd.read_csv(url)

df_raw = load_nasa_data()
col = 'distance'

# Слайдер для настройки "захвата"
sens = st.slider("Чувствительность захвата узла", 0.01, 1.0, 0.5)

if st.button("▶ НАЙТИ ТОЧКИ ПОКОЯ"):
    df = compute_derivatives(df_raw, [col])
    
    # Ищем точки, где движение "замирает" (экстремумы)
    nodes = detect_toroidal_nodes(df, [col])
    
    st.success(f"Найдено узлов: {nodes.sum()}")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df[col], color='gray', alpha=0.5, label="Орбита")
    
    if nodes.any():
        ax.scatter(df.index[nodes], df.loc[nodes, col], color='red', s=100, label="УЗЕЛ (Компенсация)")
    
    ax.legend()
    st.pyplot(fig)
