import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# ЧИСТАЯ МАТЕМАТИКА (БЕЗ ПРИМЕСЕЙ)
def analyze_flow(df, col, window):
    df = df.copy()
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=[col]).reset_index(drop=True)
    
    # Производная (скорость изменения)
    df['d'] = df[col].diff()
    
    # Поиск узлов через смену знака (сглаживаем, чтобы не ловить шум)
    d_smooth = df['d'].rolling(window=window, center=True).mean()
    df['is_node'] = (d_smooth.shift(1) * d_smooth < 0).fillna(False)
    return df

st.title("L0-ENGINE: ТОЛЬКО ТВОИ ДАННЫЕ")

uploaded_file = st.file_uploader("ЗАГРУЗИ CSV (HORIZONS)", type=["csv", "txt"])

if uploaded_file:
    content = uploaded_file.getvalue().decode('utf-8')
    
    # Чистим мусор NASA (ищем маркер начала данных)
    if "$$SOE" in content:
        raw_data = content.split("$$SOE")[1].split("$$EOE")[0]
        df = pd.read_csv(io.StringIO(raw_data), header=None)
    else:
        df = pd.read_csv(uploaded_file)
    
    # Показываем, что реально внутри файла
    st.write("Колонки (выбери ту, где числа):", df.columns.tolist())
    target_col = st.selectbox("КОЛОНКА", df.columns)
    
    # Чувствительность: чем меньше окно, тем больше узлов (даже мусорных)
    win = st.slider("ЧУВСТВИТЕЛЬНОСТЬ (Окно)", 1, 100, 5)
    
    if st.button("ПРОГНАТЬ МОЙ ФАЙЛ"):
        res = analyze_flow(df, target_col, win)
        
        st.success(f"В ТВОЕМ ФАЙЛЕ НАЙДЕНО УЗЛОВ: {res['is_node'].sum()}")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(res.index, res[target_col], color='cyan', label="Траектория")
        
        nodes = res[res['is_node'] == True]
        if not nodes.empty:
            ax.scatter(nodes.index, nodes[target_col], color='red', s=60, label="УЗЕЛ")
        
        ax.legend()
        st.pyplot(fig)
else:
    st.warning("ДВИГАТЕЛЬ ПУСТ. ЖДУ ТВОЙ ФАЙЛ.")
