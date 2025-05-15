import streamlit as st
import requests

try:
    r = requests.get("https://tourism.fsa.gov.ru/api/v1/resorts/hotels/showcase", timeout=5)
    st.write(f"Статус ответа: {r.status_code}")
except Exception as e:
    st.error(f"Ошибка подключения: {e}")
