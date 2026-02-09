import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ТВОЯ МАТЕМАТИКА
def compute_derivatives(df, col):
    df = df.copy()
    df['d'] = df[col].diff()
    df['dd'] = df['d'].diff()
    return df

def find_nodes(df):
    # Узел там, где скорость меняет знак
    return (df['d'].shift(1) * df['d'] < 0).fillna(False)

# ИНТЕРФЕЙС
st.title("L0-FLOW: ПУСТОЙ ДВИЖОК")

uploaded_file = st.file_uploader("ЗАГРУЗИ СВОЙ CSV")

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)
    st.write("Колонки в твоем файле:", df_raw.columns.tolist())
    
    target_col = st.selectbox("ВЫБЕРИ КОЛОНКУ ДЛЯ АНАЛИЗА", df_raw.columns)
    
    if st.button("ПРОГНАТЬ МОИ ДАННЫЕ"):
        df = compute_derivatives(df_raw, target_col)
        df['is_node'] = find_nodes(df)
        
        st.write(f"Найдено узлов: {df['is_node'].sum()}")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df.index, df[target_col], color='cyan', label="Твои данные")
        
        if df['is_node'].any():
            ax.scatter(df.index[df['is_node']], df.loc[df['is_node'], target_col], 
                       color='red', s=100, label="УЗЕЛ")
        
        ax.legend()
        st.pyplot(fig)
