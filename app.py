import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# ТВОЯ МАТЕМАТИКА
def compute_derivatives(df, col):
    df = df.copy()
    # Переводим в числа, если вдруг прочиталось как текст
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=[col])
    df['d'] = df[col].diff()
    df['dd'] = df['d'].diff()
    return df

def find_nodes(df):
    return (df['d'].shift(1) * df['d'] < 0).fillna(False)

st.title("L0-FLOW: ПУСТОЙ ДВИЖОК (NASA EDITION)")

uploaded_file = st.file_uploader("ЗАГРУЗИ СВОЙ CSV ИЗ HORIZONS")

if uploaded_file:
    # Читаем файл целиком как текст, чтобы найти где начинаются данные
    content = uploaded_file.getvalue().decode('utf-8')
    
    # NASA отмечает начало данных строкой $$SOE
    if "$$SOE" in content:
        data_part = content.split("$$SOE")[1].split("$$EOE")[0]
        df_raw = pd.read_csv(io.StringIO(data_part), header=None)
        
        # У NASA в CSV часто нет заголовков в самой таблице, даем временные
        df_raw.columns = [f"col_{i}" for i in range(len(df_raw.columns))]
        
        st.write("Данные NASA загружены. Выбери колонку с цифрами:")
        target_col = st.selectbox("ВЫБЕРИ КОЛОНКУ", df_raw.columns)
        
        if st.button("ПРОГНАТЬ ДАННЫЕ NASA"):
            df = compute_derivatives(df_raw, target_col)
            df['is_node'] = find_nodes(df)
            
            st.write(f"Найдено реальных узлов: {df['is_node'].sum()}")
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df.index, df[target_col], color='cyan', label="Орбита")
            
            if df['is_node'].any():
                ax.scatter(df.index[df['is_node']], df.loc[df['is_node'], target_col], 
                           color='red', s=100, label="УЗЕЛ", zorder=5)
            
            ax.legend()
            st.pyplot(fig)
    else:
        # Если это обычный CSV
        df_raw = pd.read_csv(uploaded_file)
        st.write("Колонки:", df_raw.columns.tolist())
        target_col = st.selectbox("ВЫБЕРИ КОЛОНКУ", df_raw.columns)
        # ... (дальше тот же код кнопки)
