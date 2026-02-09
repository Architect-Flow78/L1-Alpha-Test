import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# ФУНКЦИЯ-ДЕТЕКТОР (ЧИСТАЯ МАТЕМАТИКА)
def detect_nodes(series, window):
    if len(series) < window + 2: 
        return pd.Series([False] * len(series))
    smooth = series.rolling(window=window, center=True).mean()
    d = smooth.diff()
    return (d.shift(1) * d < 0).fillna(False)

st.set_page_config(page_title="L0-ULTIMATE-FIX", layout="wide")
st.title("🌀 ДВИГАТЕЛЬ L0: ПРЯМОЙ СКАНЕР ЧИСЕЛ")

file = st.file_uploader("ЗАГРУЗИ СВОЙ ФАЙЛ NASA (CSV или TXT)")

if file:
    content = file.getvalue().decode('utf-8')
    lines = content.splitlines()
    
    table_data = []
    for line in lines:
        # Ищем ВСЕ числа в строке (целые и с точкой)
        # Регулярное выражение найдет числа даже если они зажаты текстом
        nums = re.findall(r"[-+]?\d*\.\d+|\d+", line)
        if len(nums) > 1: # Если в строке больше одного числа - это наши данные
            table_data.append([float(n) for n in nums])
    
    if table_data:
        df = pd.DataFrame(table_data)
        st.write("ЧИСЛОВЫЕ ПОТОКИ ОБНАРУЖЕНЫ:")
        st.dataframe(df.head(5))
        
        col_options = df.columns.tolist()
        # В файлах NASA координаты обычно идут после даты (это колонки с индексами 3, 4, 5 и т.д.)
        target_col = st.selectbox("ВЫБЕРИ НОМЕР ПОТОКА", col_options, index=min(len(col_options)-1, 3))
        
        win = st.slider("СГЛАЖИВАНИЕ (Масштаб)", 1, 100, 12)
        
        if st.button("▶ НАЙТИ УЗЛЫ В ЭТОМ ПОТОКЕ"):
            series = df[target_col]
            nodes = detect_nodes(series, win)
            
            st.success(f"ПОТОК №{target_col}: НАЙДЕНО УЗЛОВ: {nodes.sum()}")
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(series.index, series.values, color='#00ffcc', linewidth=1, label="Траектория")
            
            if nodes.any():
                ax.scatter(series.index[nodes], series.values[nodes], 
                           color='red', s=40, zorder=5, label="УЗЕЛ")
            
            ax.grid(True, alpha=0.1)
            ax.legend()
            st.pyplot(fig)
    else:
        st.error("В этом файле ВООБЩЕ не найдено чисел. Либо файл пустой, либо формат совсем дикий.")

st.info("Совет: Пробуй разные номера потоков. В NASA координаты — это обычно средние колонки.")
