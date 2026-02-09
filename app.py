import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ТВОЙ ИНВАРИАНТ (ЖЕСТКАЯ ДЕТЕКЦИЯ)
def detect_nodes(series):
    # Скорость (дифференциал)
    d = series.diff()
    # Узел — точка, где скорость меняет знак (разворот)
    return (d.shift(1) * d < 0).fillna(False)

st.title("🌀 L0-ENGINE: ПРЯМОЙ СКАНЕР")

file = st.file_uploader("ЗАГРУЗИ СВОЙ ФАЙЛ (ЛЮБОЙ ФОРМАТ)")

if file:
    content = file.getvalue().decode('utf-8')
    lines = content.splitlines()
    
    all_data = []
    for line in lines:
        # Разбиваем строку по запятым или пробелам и ищем числа
        parts = line.replace(',', ' ').split()
        numeric_parts = []
        for p in parts:
            try:
                numeric_parts.append(float(p))
            except:
                continue
        if len(numeric_parts) > 0:
            all_data.append(numeric_parts)
    
    if all_data:
        df = pd.DataFrame(all_data)
        st.write("Обнаружены числовые потоки (колонки):")
        st.dataframe(df.head(5))
        
        # Выбираем колонку, где самые большие числа (обычно это дистанция или координаты)
        target = st.selectbox("ВЫБЕРИ КОЛОНКУ С ДАННЫМИ", df.columns)
        
        if st.button("▶ ИСКАТЬ УЗЛЫ В ПОТОКЕ"):
            series = df[target]
            nodes = detect_nodes(series)
            
            st.success(f"НАЙДЕНО УЗЛОВ: {nodes.sum()}")
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(series.index, series.values, color='#00ffcc', label="Данные")
            
            if nodes.any():
                ax.scatter(series.index[nodes], series.values[nodes], 
                           color='red', s=40, label="УЗЕЛ")
            
            ax.grid(True, alpha=0.1)
            ax.legend()
            st.pyplot(fig)
    else:
        st.error("В файле вообще не найдено чисел. Проверь файл!")
