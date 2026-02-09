import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ФУНКЦИЯ ОЧИСТКИ И ПОИСКА
def get_clean_data(df, col_idx):
    # Забираем колонку и чистим от всего, что не число
    series = df[col_idx].astype(str).str.replace(' ', '')
    series = pd.to_numeric(series, errors='coerce').dropna().reset_index(drop=True)
    return series

def detect_nodes(series, window):
    if len(series) < window + 2: 
        return pd.Series([False] * len(series))
    # Сглаживание для часовых данных
    smooth = series.rolling(window=window, center=True).mean()
    d = smooth.diff()
    return (d.shift(1) * d < 0).fillna(False)

st.set_page_config(page_title="L0-FIXED", layout="wide")
st.title("🌀 ДВИГАТЕЛЬ L0: ПРЯМОЙ ДОСТУП")

file = st.file_uploader("ЗАГРУЗИ СВОЙ ФАЙЛ NASA")

if file:
    content = file.getvalue().decode('utf-8')
    
    # Режем файл жестко по запятым, игнорируя пустые строки
    lines = [l.split(',') for l in content.splitlines() if len(l.split(',')) > 3]
    
    if lines:
        df = pd.DataFrame(lines)
        st.write("ТАБЛИЦА ПРОЧИТАНА. ПОТОКИ ДОСТУПНЫ:")
        st.dataframe(df.head(5))
        
        # Теперь тут будут ВСЕ колонки, которые нашел код
        col_options = df.columns.tolist()
        target_col = st.selectbox("ВЫБЕРИ НОМЕР ПОТОКА (Пробуй 2, 3 или 4)", col_options)
        
        win = st.slider("МАСШТАБ (Сглаживание)", 1, 100, 12)
        
        if st.button("▶ ИСКАТЬ УЗЛЫ"):
            clean_series = get_clean_data(df, target_col)
            
            if not clean_series.empty:
                nodes = detect_nodes(clean_series, win)
                st.success(f"ПОТОК {target_col}: НАЙДЕНО УЗЛОВ: {nodes.sum()}")
                
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(clean_series.index, clean_series.values, color='#00ffcc')
                
                if nodes.any():
                    ax.scatter(clean_series.index[nodes], clean_series.values[nodes], 
                               color='red', s=40, zorder=5)
                
                ax.grid(True, alpha=0.1)
                st.pyplot(fig)
            else:
                st.error("В этом потоке нет чисел. Выбери другой номер.")
    else:
        st.error("Не удалось разбить файл на колонки. Проверь формат.")
