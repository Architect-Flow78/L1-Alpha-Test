import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# ТВОЙ ИНВАРИАНТ (БЕЗ ФИЛЬТРОВ И СГЛАЖИВАНИЙ)
def find_nodes_raw(series):
    d = series.diff()
    # Узел — это любая смена направления, даже самая мизерная
    nodes = (d.shift(1) * d < 0)
    return nodes.fillna(False)

st.title("L0-FINAL: ПРЯМОЙ ДЕТЕКТОР")

uploaded = st.file_uploader("ЗАГРУЗИ СВОЙ CSV/TXT ИЗ NASA")

if uploaded:
    # Читаем всё как текст
    raw_text = uploaded.getvalue().decode('utf-8')
    
    # Выцепляем только блок данных между маркерами NASA
    if "$$SOE" in raw_text:
        data_block = raw_text.split("$$SOE")[1].split("$$EOE")[0]
        # Превращаем строки в список чисел (берем последнюю колонку в каждой строке)
        lines = [line.split(',') for line in data_block.strip().split('\n')]
        # Обычно дистанция/координата — это последние значения в строке
        try:
            val_idx = -2 # Для Range (delta) в NASA это предпоследнее поле
            values = [float(l[val_idx]) for l in lines if len(l) > 2]
            
            df = pd.DataFrame({"val": values})
            df['is_node'] = find_nodes_raw(df['val'])
            
            st.success(f"АНАЛИЗ ЗАВЕРШЕН. УЗЛОВ В ПОТОКЕ: {df['is_node'].sum()}")
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df.index, df['val'], color='cyan', label="Сырой поток")
            
            nodes = df[df['is_node']]
            if not nodes.empty:
                ax.scatter(nodes.index, nodes['val'], color='red', s=30, label="УЗЕЛ")
            
            ax.legend()
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"ОШИБКА РАЗБОРА: {e}. NASA поменяла формат?")
    else:
        st.error("ЭТО НЕ ФАЙЛ NASA HORIZONS. НЕТ МЕРКЕРА $$SOE.")
