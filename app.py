import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="TOR-Phase Analyzer", layout="wide")
st.title("🛸 Toroidal Phase: Линия Истины")

uploaded_file = st.file_uploader("Загрузи файл NASA (CSV)", type="csv")

if uploaded_file is not None:
    try:
        # Пытаемся прочитать файл, игнорируя строки с текстом в начале
        # sep=None заставляет pandas самому угадать: запятая там или точка с запятой
        df = pd.read_csv(uploaded_file, comment='#', skip_blank_lines=True, sep=None, engine='python')
        
        # Если в первой колонке все еще текст, пробуем найти первую цифровую строку
        if df.empty:
            st.error("Файл пустой или не распознан.")
        else:
            st.success("Файл успешно прожеван!")
            
            # Выбираем только колонки, где есть числа
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if not numeric_cols:
                st.error("В файле нет числовых данных! Проверь формат.")
            else:
                col_name = st.selectbox("Выбери колонку с данными (частота/скорость)", numeric_cols)
                
                real_data = df[col_name].dropna().values
                
                # ИДЕАЛЬНЫЙ ТОР-ПРОГНОЗ
                omega_0 = real_data[0]
                ideal_path = [omega_0]
                
                # Коэффициент K — это твоя "вилка". Давай вынесем его в слайдер,
                # чтобы ты мог с телефона его подкрутить и увидеть резонанс!
                K = st.sidebar.slider("Коэффициент связи K", 0.0, 0.001, 0.000001, format="%.8f")
                
                for i in range(1, len(real_data)):
                    w = ideal_path[-1]
                    # ТВОЯ ФОРМУЛА: a = w^(4/3)
                    accel = abs(w)**(1.33333333) 
                    w_next = w + (K * accel)
                    ideal_path.append(w_next)
                
                ideal_path = np.array(ideal_path)
                
                # ВЫЧИТАНИЕ (Просушка)
                diff = real_data - ideal_path
                
                # Рисуем график
                st.subheader(f"Разница: Реальность NASA минус Твой Идеал")
                st.line_chart(diff)
                
                st.write(f"Последнее отклонение: {diff[-1]:.10f}")

    except Exception as e:
        st.error(f"Б****, опять ошибка: {e}")
        st.write("Попробуй открыть файл в блокноте на телефоне и посмотри, нет ли там лишнего текста сверху.")
