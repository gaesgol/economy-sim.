streamlit_app.py

import streamlit as st import pandas as pd import matplotlib.pyplot as plt import json import random from datetime import datetime

초기 데이터 로드

def load_data(): with open("data.json", "r", encoding="utf-8") as f: return json.load(f)

def save_data(data): with open("data.json", "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)

countries = load_data()

국가 선택

st.sidebar.header("정책 조정") selected_country = st.sidebar.selectbox("국가", list(countries.keys()))

money = st.sidebar.slider("통화량", 500, 5000, countries[selected_country]["통화량"]) interest = st.sidebar.slider("금리", 0.0, 10.0, float(countries[selected_country]["금리"])) tax = st.sidebar.slider("세율", 0, 50, countries[selected_country]["세율"])

if st.sidebar.button("정책 적용"): countries[selected_country]["통화량"] = money countries[selected_country]["금리"] = interest countries[selected_country]["세율"] = tax countries[selected_country]["환율"] = round(random.uniform(0.8, 1.2), 2) gdp = int((money * (1 - tax/100)) * (1 + interest/100)) countries[selected_country]["GDP"] = gdp countries[selected_country]["기록"].append([datetime.now().strftime("%H:%M:%S"), gdp]) save_data(countries) st.success("정책이 적용되었습니다.")

무역 시뮬레이션

st.header("무역 시뮬레이션") col1, col2 = st.columns(2) with col1: exporter = st.selectbox("수출국", list(countries.keys()), key="exp") with col2: importer = st.selectbox("수입국", list(countries.keys()), key="imp")

products = list(countries[exporter]["특산품"].keys()) product = st.selectbox("상품", products) quantity = st.slider("수량", 1, 100, 10)

if st.button("무역 요청"): if exporter == importer: st.warning("같은 국가끼리는 무역할 수 없습니다.") else: price = countries[exporter]["특산품"][product] exchange_rate = countries[importer]["환율"] / countries[exporter]["환율"] total_cost = int(price * quantity * exchange_rate) threshold = int(countries[importer]["GDP"] * 0.05) if total_cost <= threshold: countries[exporter]["GDP"] += total_cost countries[importer]["GDP"] -= total_cost st.success(f"{importer}이(가) {exporter}에게 {product} {quantity}개 구매 ({total_cost})") save_data(countries) else: st.info(f"{importer}이(가) 거래를 거절했습니다. ({total_cost} > 허용한도 {threshold})")

경제력 그래프

st.header("국가별 경제력 비교") df = pd.DataFrame(countries).T st.bar_chart(df["GDP"])

시계열 변화

st.header("GDP 시계열 변화") fig, ax = plt.subplots() for name, data in countries.items(): if data["기록"]: times, gdps = zip(*data["기록"]) ax.plot(times, gdps, label=name) ax.legend() st.pyplot(fig)

