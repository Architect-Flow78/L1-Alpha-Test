import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# ТВОЯ МАТЕМАТИКА (ПОДСТРОЕННАЯ ПОД ЧАСОВЫЕ ДАННЫЕ)
def compute_derivatives(df, col):
    df = df.copy()
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=[col])
    
    # Считаем производную не по 1 точке, а по тренду (чтобы убрать шум)
    df['d'] = df[col].diff()
    return df

def find_nodes(df, window=5):
    # Узел там, где скорость меняет знак, 
    # но смотрим через среднее, чтобы поймать разворот на мелком масштабе
    d_smooth = df['d'].rolling(window=window, center=True).mean()
    return (d_smooth.shift(1) * d_smooth < 0).fillna(False)

st.title("L0-FLOW: АНАЛИЗАТОР NASA (ЧАСОВОЙ)")

uploaded_file = st.file_uploader("ЗАГРУЗИ СВОЙ ЧАСОВОЙ CSV")

if uploaded_file:
    content = uploaded_file.getvalue().decode('utf-8')
    
    if "$$SOE" in content:
        data_part = content.split("$$SOE")[1].split("$$EOE")[0]
        df_raw = pd.read_csv(io.StringIO(data_part), header=None)
        
        # NASA даёт много колонок. Координаты обычно в 2, 3, 4 (X, Y, Z)
        # Если ты качал Range (дистанцию), это обычно колонка 4 или 5
        df_raw.columns = [f"col_{i}" for i in range(len(df_raw.columns))]
        
        st.write("Данные NASA загружены. В почасовых файлах ищи колонку с цифрами:")
        target_col = st.selectbox("ВЫБЕРИ КОЛОНКУ", df_raw.columns)
        
        # Ползунок чувствительности (важно для часовых данных!)
        win = st.slider("Сглаживание (для почасовых данных)", 1, 50, 12)
        
        if st.button("ПРОГНАТЬ ПОЧАСОВЫЕ ДАННЫЕ"):
            df = compute_derivatives(df_raw, target_col)
            df['is_node'] = find_nodes(df, window=win)
            
            st.success(f"Найдено узлов: {df['is_node'].sum()}")
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df.index, df[target_col], color='cyan', label="Траектория")
            
            if df['is_node'].any():
                ax.scatter(df.index[df['is_node']], df.loc[df['is_node'], target_col], 
                           color='red', s=100, label="УЗЕЛ РАЗВОРОТА", zorder=5)
            
            ax.legend()
            st.pyplot(fig)
