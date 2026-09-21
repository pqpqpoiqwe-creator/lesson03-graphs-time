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
# 구역 3. 날짜별 10위권 일관객 합계
# ----------------------------------------------------------------------------
st.header("구역 3. 날짜별 10위권 일관객 합계")

daily_total = df.groupby("날짜", as_index=False)["일관객"].sum()
daily_total = daily_total.sort_values("날짜")

# 합계가 가장 컸던 날 3일
top3_days = daily_total.sort_values("일관객", ascending=False).head(3)

fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="날짜별 박스오피스 10위권 일관객 합계",
)
fig3.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계 일관객: %{y:,}명<extra></extra>"
)
fig3.update_layout(xaxis_title="날짜", yaxis_title="일관객 합계(명)")

# 최고치 3일을 점으로 표시하고 날짜 라벨을 붙임
fig3.add_scatter(
    x=top3_days["날짜"],
    y=top3_days["일관객"],
    mode="markers+text",
    text=top3_days["날짜"].dt.strftime("%Y-%m-%d"),
    textposition="top center",
    marker=dict(size=10, color="red"),
    name="합계 최고 3일",
)

st.plotly_chart(fig3, use_container_width=True)

st.text_area(
    "이 그래프로 알 수 있는 것",
    value="",
    placeholder="예: 신작이 몰리는 특정 날짜에 전체 관객 합계가 크게 튀는 경향이 있다.",
    key="insight_3",
)

st.divider()

# ----------------------------------------------------------------------------
# 구역 4. 영화별 일관객 합계 TOP 10
# ----------------------------------------------------------------------------
st.header("구역 4. 영화별 일관객 합계 TOP 10")

movie_stats = df.groupby("영화명", as_index=False).agg(
    총일관객=("일관객", "sum"),
    top10진입일수=("날짜", "count"),
)
top10_movies = movie_stats.sort_values("총일관객", ascending=False).head(10)
# 관객이 많은 영화가 위로 오도록 오름차순으로 정렬해 그래프에 전달
top10_movies = top10_movies.sort_values("총일관객", ascending=True)

fig4 = px.bar(
    top10_movies,
    x="총일관객",
    y="영화명",
    orientation="h",
    custom_data=["top10진입일수"],
    title="일관객 합계 TOP 10 영화",
)
fig4.update_traces(
    hovertemplate=(
        "영화명: %{y}<br>"
        "총 일관객: %{x:,}명<br>"
        "10위권 진입 일수: %{customdata[0]}일<extra></extra>"
    )
)
fig4.update_layout(
    xaxis_title="일관객 합계(명)",
    yaxis_title="영화명",
    yaxis=dict(categoryorder="total ascending"),  # 관객 많은 영화가 위로
)

st.plotly_chart(fig4, use_container_width=True)

st.text_area(
    "이 그래프로 알 수 있는 것",
    value="",
    placeholder="예: 상위권 영화들은 대체로 10위권에 오래 머무르며 꾸준히 관객을 모았다.",
    key="insight_4",
)

st.divider()

# ----------------------------------------------------------------------------
# 구역 5. 월 x 요일 일관객 합계 히트맵
# ----------------------------------------------------------------------------
st.header("구역 5. 월 x 요일별 일관객 합계")

WEEKDAY_ORDER = ["월", "화", "수", "목", "금", "토", "일"]
WEEKDAY_MAP = {0: "월", 1: "화", 2: "수", 3: "목", 4: "금", 5: "토", 6: "일"}

heat_df = df.copy()
heat_df["월"] = heat_df["날짜"].dt.month
heat_df["요일"] = heat_df["날짜"].dt.dayofweek.map(WEEKDAY_MAP)

heat_pivot = (
    heat_df.groupby(["월", "요일"])["일관객"]
    .sum()
    .reset_index()
    .pivot(index="월", columns="요일", values="일관객")
    .reindex(columns=WEEKDAY_ORDER)
    .sort_index()
)

fig5 = px.imshow(
    heat_pivot,
    color_continuous_scale="Reds",
    aspect="auto",
    labels=dict(x="요일", y="월", color="일관객 합계"),
    title="월 x 요일별 일관객 합계 히트맵",
)
fig5.update_traces(
    hovertemplate="월: %{y}월<br>요일: %{x}요일<br>일관객 합계: %{z:,}명<extra></extra>"
)
fig5.update_layout(xaxis_title="요일", yaxis_title="월")

st.plotly_chart(fig5, use_container_width=True)

st.text_area(
    "이 그래프로 알 수 있는 것",
    value="",
    placeholder="예: 주말(토·일)에 색이 진해, 주중보다 관객이 많이 몰리는 경향을 볼 수 있다.",
    key="insight_5",
)

st.divider()

# ----------------------------------------------------------------------------
# 구역 6. (다음 그래프를 위한 자리)
# ----------------------------------------------------------------------------
st.header("구역 6. (준비 중)")
st.caption("다음 그래프가 이 자리에 추가될 예정입니다.")
