import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

def clean_and_find_data(uploaded_file):
    content = uploaded_file.getvalue().decode('utf-8')
    if "$$SOE" in content:
        # Берем только то, что между маркерами NASA
        data_block = content.split("$$SOE")[1].split("$$EOE")[0]
        df = pd.read_csv(io.StringIO(data_block), header=None, low_memory=False)
        # Оставляем только числовые колонки
        df = df.apply(pd.to_numeric, errors='coerce')
        return df.dropna(axis=1, how='all').reset_index(drop=True)
    return pd.read_csv(uploaded_file).apply(pd.to_numeric, errors='coerce')

st.title("🌀 L0-FLOW: ПРЯМАЯ ДЕТЕКЦИЯ")

file = st.file_uploader("ЗАГРУЗИ СВОЙ CSV")

if file:
    df = clean_and_find_data(file)
    
    if not df.empty:
        st.write("Доступные числовые векторы:", df.columns.tolist())
        # Выбираем колонку, где больше всего "движухи"
        default_col = df.std().idxmax()
        target = st.selectbox("ВЫБЕРИ ВЕКТОР", df.columns, index=int(default_col))
        
        # Считаем производную
        series = df[target].interpolate()
        diff = series.diff()
        
        # УЗЕЛ: там, где скорость d меняет знак
        nodes = (diff.shift(1) * diff < 0).fillna(False)
        
        st.success(f"НАЙДЕНО УЗЛОВ В ТВОИХ ДАННЫХ: {nodes.sum()}")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(series.index, series.values, color='#00ffcc', label="Траектория")
        
        if nodes.any():
            ax.scatter(series.index[nodes], series.values[nodes], 
                       color='red', s=40, label="УЗЕЛ КОМПЕНСАЦИИ", zorder=5)
        
        ax.grid(True, alpha=0.2)
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("В файле не найдено числовых данных между $$SOE и $$EOE")
