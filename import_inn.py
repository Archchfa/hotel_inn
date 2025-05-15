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
    output = StringIO()
    page = 0
    limit = 20
    with st.spinner("Загрузка..."):
        while True:
            r = requests.get(url, params={"page": page, "limit": limit})
            if r.status_code != 200:
                st.error(f"Ошибка {r.status_code}")
                break
            d = r.json()
            items = d.get("data")
            if not items:
                break
            output.write(r.text + "\n")
            page += 1
            time.sleep(0.5)
        st.success("Загрузка завершена")

    raw = output.getvalue()
    parts = raw.strip().split('\n')
    hotels = []
    for part in parts:
        try:
            obj = json.loads(part)
            if 'data' in obj:
                hotels.extend(obj['data'])
        except json.JSONDecodeError:
            continue

    df = pd.json_normalize(hotels)
    pd.set_option('display.max_columns', None)

    st.write("Пример данных:")
    st.dataframe(df.head())

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Загрузить результат", csv, file_name="hotels.csv", mime="text/csv")
