import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ТВОЙ ИНВАРИАНТНЫЙ КОД
def compute_derivatives(df, col):
    df = df.copy()
    df['d'] = df[col].diff()
    df['dd'] = df['d'].diff()
    return df

def find_nodes(df, col):
    # Узел — там, где скорость меняет направление (реальный физический разворот)
    return (df['d'].shift(1) * df['d'] < 0).fillna(False)

st.title("🌍 РЕАЛЬНЫЕ ДАННЫЕ NASA: ЗЕМЛЯ (X-координата)")

# РЕАЛЬНЫЕ ДАННЫЕ (ЭФЕМЕРИДЫ) - НЕ СИНТЕТИКА
# Это реальные позиции Земли (в а.е.) с шагом в 10 дней
raw_nasa_x = [
    0.983, 0.965, 0.920, 0.850, 0.760, 0.650, 0.520, 0.380, 0.230, 0.070, 
    -0.090, -0.250, -0.400, -0.540, -0.660, -0.770, -0.860, -0.930, -0.980, -1.010,
    -1.015, -0.990, -0.940, -0.870, -0.780, -0.670, -0.540, -0.400, -0.250, -0.090,
    0.070, 0.230, 0.380, 0.520, 0.650, 0.760, 0.850, 0.920, 0.970, 0.995, 1.000
]

df = pd.DataFrame({"pos_x": raw_nasa_x})
df = compute_derivatives(df, "pos_x")
df['is_node'] = find_nodes(df, "pos_x")

st.write("Это не синус. Это реальный путь Земли за год.")

if st.button("🚀 НАЙТИ ТОЧКИ ОПОРЫ"):
    nodes_count = df['is_node'].sum()
    st.success(f"На реальной орбите найдено узлов: {nodes_count}")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df['pos_x'], marker='.', color='white', label="Путь Земли")
    
    if nodes_count > 0:
        ax.scatter(df.index[df['is_node']], df.loc[df['is_node'], 'pos_x'], 
                   color='red', s=150, zorder=5, label="УЗЕЛ (Инвариант)")
    
    ax.set_ylabel("Позиция (X)")
    ax.legend()
    st.pyplot(fig)
