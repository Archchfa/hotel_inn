import streamlit as st
import requests
import time
import json
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Загрузка отелей", layout="wide")
st.title("Сбор данных по отелям")

url = st.text_input(
    "Укажите ссылку на API:",
    value="https://tourism.fsa.gov.ru/api/v1/resorts/hotels/showcase",
    help="Актуальная ссылка на 15 мая: https://tourism.fsa.gov.ru/api/v1/resorts/hotels/showcase"
)

start = st.button("Начать загрузку")

if start and url:
    rows = []
    page = 0
    limit = 20
    progress_text = st.empty()
    progress_bar = st.progress(0)
    
    with st.spinner("Загрузка данных..."):
        while True:
            try:
                response = requests.get(url, params={"page": page, "limit": limit}, timeout=10)
            except requests.exceptions.RequestException as e:
                st.error(f"Ошибка при запросе: {e}")
                break
                
            if response.status_code != 200:
                st.error(f"Ошибка на странице {page}: {response.status_code}")
                break
                
            try:
                data = response.json()
            except json.JSONDecodeError:
                st.error("Ошибка при разборе JSON")
                break
                
            hotels = data.get("data")
            if not hotels:
                st.success("Данные загружены полностью")
                break
                
            rows.extend(hotels)
            progress_text.text(f"Страница {page} — загружено {len(hotels)} объектов")
            progress_bar.progress(min((page + 1)*limit, 1000)/1000)  # пример прогресса
            
            page += 1
            time.sleep(0.5)
    
    if rows:
        df = pd.json_normalize(rows)
        pd.set_option("display.max_columns", None)
        st.write("Пример данных:")
        st.dataframe(df.head())
        
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Скачать результат (CSV)",
            data=csv,
            file_name="hotels.csv",
            mime="text/csv"
        )
