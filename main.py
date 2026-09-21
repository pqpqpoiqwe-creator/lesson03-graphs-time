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
    # utf-8-sig: 파일 맨 앞의 BOM 문자 때문에 첫 번째 열 이름이
    # 깨지는 것을 방지하기 위해 사용
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")
    # 날짜 열(하이픈 없는 여덟 자리 숫자)을 실제 날짜 타입으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d")
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
# 구역 2. 기간 내 일관객 합계 상위 5개 영화 비교
# ----------------------------------------------------------------------------
st.header("구역 2. 일관객 합계 상위 5개 영화 비교")

top5_movies = (
    df.groupby("영화명")["일관객"].sum().sort_values(ascending=False).head(5).index
)
top5_df = df[df["영화명"].isin(top5_movies)].sort_values("날짜")

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 상위 5개 영화의 날짜별 일관객 변화",
)
fig2.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra>%{fullData.name}</extra>"
)
fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객(명)",
    legend_title="영화명",
)
# 범례를 클릭하면 해당 영화 선을 켜고 끌 수 있음(Plotly 기본 동작)

st.plotly_chart(fig2, use_container_width=True)

st.text_area(
    "이 그래프로 알 수 있는 것",
    value="",
    placeholder="예: 상위 영화들은 개봉 직후 짧은 기간에 관객이 집중되는 경향을 보인다.",
    key="insight_2",
)

st.divider()

# ----------------------------------------------------------------------------
# 구역 3. (다음 그래프를 위한 자리)
# ----------------------------------------------------------------------------
st.header("구역 3. (준비 중)")
st.caption("다음 그래프가 이 자리에 추가될 예정입니다.")
