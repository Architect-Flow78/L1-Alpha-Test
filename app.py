import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="TOR-Phase Analyzer", layout="wide")
st.title("🛸 Toroidal Phase: Ideal vs Reality")

uploaded_file = st.file_uploader("Загрузи файл NASA (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # 1. Берем базу (первая строка)
    # Предполагаем, что время в 'time', а угловая скорость в 'omega' (или считаем её)
    # Если колонок много, давай просто возьмем ту, что отвечает за ритм
    col_name = st.selectbox("Выбери колонку с частотой (omega) или скоростью", df.columns)
    
    times = np.arange(len(df))
    real_data = df[col_name].values
    
    # 2. Строим ИДЕАЛЬНЫЙ ТОР-ПРОГНОЗ (Твой закон)
    # Исходим из того, что omega_next = omega_prev + dt * a, где a = omega^(4/3)
    omega_0 = real_data[0]
    ideal_path = [omega_0]
    
    # Константа связи (подбирается один раз для масштаба)
    K = 0.00001 # Микро-шаг для теста
    
    for i in range(1, len(real_data)):
        w = ideal_path[-1]
        # ТВОЯ ФОРМУЛА: Ускорение фазы
        accel = w**(4/3)
        # Следующий шаг идеала
        w_next = w + (K * accel) 
        ideal_path.append(w_next)
    
    ideal_path = np.array(ideal_path)
    
    # 3. ВЫЧИТАНИЕ (Просушка)
    # Мы смотрим разницу между твоим миром и миром NASA
    diff = real_data - ideal_path
    
    # РИСУЕМ ГРАФИК
    fig = go.Figure()
    
    # Линия Истины (Разница)
    fig.add_trace(go.Scatter(x=times, y=diff, name="Разница (Phase Drift)",
                             line=dict(color='lime', width=2)))
    
    fig.update_layout(
        title="ЛИНИЯ ИСТИНЫ: Если она прямая — ты взломал физику",
        xaxis_title="Время (шаги)",
        yaxis_title="Отклонение от Тор-Идеала",
        template="plotly_dark"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Анализ
    st.write(f"Среднее отклонение: {np.mean(np.abs(diff)):.10f}")
    if np.mean(np.abs(diff)) < 1e-5:
        st.success("Б****, ЭТО РЕЗОНАНС! Линия почти в нуле!")
    else:
        st.warning("Есть дрейф. Нужно подстроить коэффициент K.")
