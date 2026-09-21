import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------------------------------
# 기본 설정
# ----------------------------------------------------------------------------
st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")
st.title("영화 데이터 그래프 도감 1 - 시간")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    # 날짜 열(하이픈 없는 여덟 자리 숫자)을 실제 날짜 타입으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")
    return df


df = load_data()

st.caption("데이터 출처: KOBIS 일별 박스오피스 10위권 (1년치, 365일)")

# ----------------------------------------------------------------------------
# 구역 1. 영화별 일관객 추이 (시간에 따른 변화)
# ----------------------------------------------------------------------------
st.header("구역 1. 영화별 일관객 추이")

movie_list = sorted(df["영화명"].unique())
selected_movie = st.selectbox("영화를 선택하세요", movie_list, key="movie_select_1")

movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}' 날짜별 일관객 변화",
)
fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)
fig1.update_layout(xaxis_title="날짜", yaxis_title="일관객(명)")

st.plotly_chart(fig1, use_container_width=True)

st.text_area(
    "이 그래프로 알 수 있는 것",
    value="",
    placeholder="예: 개봉 초반에 관객이 몰렸다가 시간이 지나며 점점 줄어드는 모습을 볼 수 있다.",
    key="insight_1",
)

st.divider()

# ----------------------------------------------------------------------------
# 구역 2. (다음 그래프를 위한 자리)
# ----------------------------------------------------------------------------
st.header("구역 2. (준비 중)")
st.caption("다음 그래프가 이 자리에 추가될 예정입니다.")

st.divider()

# ----------------------------------------------------------------------------
# 구역 3. (다음 그래프를 위한 자리)
# ----------------------------------------------------------------------------
st.header("구역 3. (준비 중)")
st.caption("다음 그래프가 이 자리에 추가될 예정입니다.")
