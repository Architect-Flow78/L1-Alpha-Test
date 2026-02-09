import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. ТВОЙ ИНВАРИАНТ С ЧУВСТВИТЕЛЬНОСТЬЮ
def detect_nodes(series, window):
    # Убираем None и переводим в числа
    s = pd.to_numeric(series, errors='coerce').dropna().reset_index(drop=True)
    if len(s) < window: return s, pd.Series([False]*len(s))
    
    # Сглаживаем, чтобы не считать "шум" за узлы
    smooth = s.rolling(window=window, center=True).mean()
    d = smooth.diff()
    nodes = (d.shift(1) * d < 0).fillna(False)
    return s, nodes

st.set_page_config(page_title="L0-ENGINE: FINAL", layout="wide")
st.title("🌀 ДВИГАТЕЛЬ L0: РЕАЛЬНЫЙ ПОТОК")

file = st.file_uploader("ЗАГРУЗИ CSV/TXT ИЗ NASA")

if file:
    content = file.getvalue().decode('utf-8')
    # Ищем блок между $$SOE и $$EOE
    if "$$SOE" in content:
        data_block = content.split("$$SOE")[1].split("$$EOE")[0]
        # Читаем фиксированно: в NASA данные обычно через запятую
        lines = [l.strip().split(',') for l in data_block.strip().split('\n') if len(l) > 10]
        df = pd.DataFrame(lines)
    else:
        # Если маркеров нет, берем всё что есть
        lines = [l.strip().split(',') for l in content.splitlines() if len(l) > 1]
        df = pd.DataFrame(lines)

    if not df.empty:
        st.write("ТАБЛИЦА ВОССТАНОВЛЕНА:")
        st.dataframe(df.head(5))
        
        # В NASA за 2026 год (как на скрине) координаты обычно в колонках 2, 3, 4
        target_idx = st.selectbox("ВЫБЕРИ ПОТОК (Числа)", df.columns, index=min(2, len(df.columns)-1))
        
        # Слайдер фильтрации шума
        win = st.slider("МАСШТАБ (Сглаживание)", 1, 100, 24)
        
        if st.button("▶ ВЫЯВИТЬ СТРУКТУРУ"):
            clean_series, nodes = detect_nodes(df[target_idx], win)
            
            st.success(f"НАСТОЯЩИХ УЗЛОВ ВЫЯВЛЕНО: {nodes.sum()}")
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(clean_series.index, clean_series.values, color='#00ffcc', label="Траектория")
            
            if nodes.any():
                ax.scatter(clean_series.index[nodes], clean_series.values[nodes], 
                           color='red', s=40, label="УЗЕЛ", zorder=5)
            
            ax.grid(True, alpha=0.1)
            ax.legend()
            st.pyplot(fig)
    else:
        st.error("Файл пустой или не распознан.")
