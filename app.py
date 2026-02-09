import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- ТВОЙ ОРИГИНАЛЬНЫЙ КОД (L1-Emergence) ---
def compute_derivatives(df, col):
    df = df.copy()
    df['d'] = df[col].diff()
    df['dd'] = df['d'].diff()
    return df

def find_nodes(df):
    # Твой инвариант: узел там, где скорость меняет вектор
    return (df['d'].shift(1) * df['d'] < 0).fillna(False)

st.title("🌀 ТЕСТ ГЕОМЕТРИИ: ТОР (L0-FLOW)")

# Генерируем движение по Тору (две частоты: вращение и обход)
t = np.linspace(0, 10, 1000)
# Координата X движения по поверхности тора
# (R + r*cos(v)) * cos(u)
x_torus = (3 + np.cos(5 * t)) * np.cos(t) 

df = pd.DataFrame({"time": t, "torus_x": x_torus})

st.write("Сейчас мы запустим алгоритм на идеальной модели Тора.")

if st.button("👁 ВЫЯВИТЬ УЗЛЫ ТОРЫ"):
    df = compute_derivatives(df, "torus_x")
    df['is_node'] = find_nodes(df)
    
    nodes_count = df['is_node'].sum()
    st.success(f"На геометрии Тора обнаружено узлов: {nodes_count}")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['time'], df['torus_x'], color='white', alpha=0.3, label="Траектория Тора")
    
    # Рисуем узлы
    if nodes_count > 0:
        ax.scatter(df.loc[df['is_node'], 'time'], df.loc[df['is_node'], 'torus_x'], 
                   color='red', s=50, label="УЗЕЛ КОМПЕНСАЦИИ", zorder=5)
    
    ax.set_title("Паттерн 'Дыхания' Тора")
    ax.legend()
    st.pyplot(fig)
    
    st.write("Смотри на красные точки. Если они выстроились в ровный ритм — значит "
             "алгоритм видит структуру. Это и есть твоя 'Альфа-решетка'.")
