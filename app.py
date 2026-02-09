import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ФУНКЦИЯ "ГРЯЗНОЙ" ОЧИСТКИ (ВЫЦЕПЛЯЕМ ЧИСЛА ИЗ ТЕКСТА)
def force_numeric(series):
    # Превращаем всё в строку, убираем пробелы и пытаемся сделать числом
    return pd.to_numeric(series.astype(str).str.strip(), errors='coerce')

def detect_nodes(series, window):
    if len(series) < window + 2: 
        return pd.Series([False] * len(series))
    # Сглаживание, чтобы не ловить микро-шум
    smooth = series.rolling(window=window, center=True).mean()
    d = smooth.diff()
    return (d.shift(1) * d < 0).fillna(False)

st.set_page_config(page_title="L0-ULTIMATE", layout="wide")
st.title("🌀 ДВИГАТЕЛЬ L0: ПРЯМОЙ ВЗЛОМ ДАННЫХ")

file = st.file_uploader("ЗАГРУЗИ СВОЙ ФАЙЛ NASA")

if file:
    content = file.getvalue().decode('utf-8')
    # NASA разделяет данные запятыми. Разбиваем всё.
    lines = [l.split(',') for l in content.splitlines() if len(l.split(',')) > 2]
    
    if lines:
        df = pd.DataFrame(lines)
        st.write("ПОТОКИ ОБНАРУЖЕНЫ (ПЕРВЫЕ СТРОКИ):")
        st.dataframe(df.head(5))
        
        # Выбор колонки (потока)
        col_options = df.columns.tolist()
        target_col = st.selectbox("ВЫБЕРИ НОМЕР ПОТОКА", col_options, index=min(2, len(col_options)-1))
        
        # Окно сглаживания (для часовых данных NASA ставь 12-24)
        win = st.slider("ЧУВСТВИТЕЛЬНОСТЬ (Сглаживание)", 1, 100, 24)
        
        if st.button("▶ ЗАПУСТИТЬ ПОИСК ИНВАРИАНТОВ"):
            # ЧИСТИМ ДАННЫЕ ВНУТРИ ВЫБРАННОЙ КОЛОНКИ
            clean_series = force_numeric(df[target_col]).dropna().reset_index(drop=True)
            
            if not clean_series.empty:
                nodes = detect_nodes(clean_series, win)
                st.success(f"ПОТОК №{target_col}: НАЙДЕНО УЗЛОВ: {nodes.sum()}")
                
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(clean_series.index, clean_series.values, color='#00ffcc', linewidth=1)
                
                if nodes.any():
                    ax.scatter(clean_series.index[nodes], clean_series.values[nodes], 
                               color='red', s=50, zorder=5, label="УЗЕЛ")
                
                ax.set_title(f"Анализ потока №{target_col}")
                ax.grid(True, alpha=0.1)
                st.pyplot(fig)
            else:
                st.error(f"В колонке №{target_col} реально нет чисел (только текст или даты). Попробуй другую!")
    else:
        st.error("Файл не разбивается на колонки. Попробуй другой формат в Horizons (CSV).")
