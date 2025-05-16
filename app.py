import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib

# ✅ 한글 폰트 설정
FONT_NAME = "NanumGothic"
FONT_PATH = os.path.join(os.path.dirname(__file__), "NanumGothic.ttf")
matplotlib.rcParams['font.family'] = FONT_NAME
matplotlib.rcParams['axes.unicode_minus'] = False

# ✅ 항목별 이슈 설명 사전
code_explanations = {
    "S12": "국가 인재 양성을 위한 혁신 교육",
    "S15": "인권/행정성 관련 위원회 운영",
    "S22": "산업재해 감소",
    "E7": "물소비량 감소",
    "E1": "에너지 소비 효율화",
    "E4": "온실가스 배출량 산정 및 검증",
    "E10": "물재처리 촉진",
    "G3": "법규준수",
    "E8": "물재활용 증대",
    "S16": "인권/안양 관련 정책 강화",
    "S17": "소수자 우대 정책 확대",
    "E3": "에너지 소비 저감 활동",
    "G2": "산학협력 성과 증진",
    "S1": "문화적 기여 증진",
    "E2": "재생에너지 생산 확대",
    "S10": "개방형 교육 프로그램 확대",
    "S7": "학생 및 교직원의 건강 증진",
    "E6": "공식적인 지속가능발전 조직 운영",
    "G4": "정부 정책 조언 시행",
    "S11": "사회 봉사 프로그램 확대",
    "S5": "학생의 식사 보호",
    "S14": "인권/성평등 교육 강화",
    "S9": "지속가능발전 관련 교육 강화",
    "G5": "이해관계인과 소통 강화",
    "S13": "성차별 철폐",
    "E5": "탄소중립 계획과 활동 증진",
    "E13": "유해물질관리 강화",
    "G6": "연구윤리 강화",
    "G8": "지속가능성 보고서 발간",
    "G7": "SDG 연구나 활동에 직접 참여",
    "S2": "지속가능한 교통 증진",
    "E9": "방류수질관리 강화",
    "E12": "지속가능한 구매",
    "S3": "구성원 주거복지 강화",
    "S18": "지역간 교육 격차 해소 기여",
    "S19": "정규직/고용안정성/차별 조항 철폐",
    "S6": "지속가능한 음식 선택권 보장",
    "E16": "지속가능한 육상생태계 보호",
    "E15": "지속가능한 해양생태계 보호",
}

# ✅ 페이지 기본 설정
st.set_page_config(layout="wide", page_title="ESG IPA Dashboard", page_icon="📊")
st.title("📊 ESG IPA 분석 대시보드")
st.caption("전공종합설계 프로젝트 | 팀원: 박유진, 박현우, 송가영")

# 📁 파일 업로드
uploaded_file = st.file_uploader("📂 Excel 파일을 업로드하세요 (Item, Importance, Performance)", type=["xlsx"])

# 탭 구성
tab1, tab2 = st.tabs(["📊 ESG 분석 대시보드", "🧾 ESG 항목 설명"])

with tab1:
    if uploaded_file:
        df = pd.read_excel(uploaded_file)

        st.subheader("✅ 업로드된 ESG 항목 데이터")
        st.dataframe(df)

        mean_imp = df['Importance'].mean()
        mean_perf = df['Performance'].mean()

        # 전략 분류
        def classify(row):
            if row['Importance'] >= mean_imp and row['Performance'] >= mean_perf:
                return '유지'
            elif row['Importance'] >= mean_imp and row['Performance'] < mean_perf:
                return '개선 우선'
            elif row['Importance'] < mean_imp and row['Performance'] >= mean_perf:
                return '과잉 노력'
            else:
                return '저우선순위'

        df['전략'] = df.apply(classify, axis=1)

        colors = {
            "유지": "green",
            "개선 우선": "red",
            "과잉 노력": "orange",
            "저우선순위": "gray"
        }

        st.subheader("📌 IPA 매트릭스")
        fig, ax = plt.subplots(figsize=(8, 6))
        for _, row in df.iterrows():
            ax.scatter(row['Performance'], row['Importance'], color=colors[row['전략']], s=100)
            ax.text(row['Performance'] + 0.02, row['Importance'], row['Item'], fontsize=9)
        ax.axhline(mean_imp, color='red', linestyle='--')
        ax.axvline(mean_perf, color='blue', linestyle='--')
        ax.set_xlabel('Performance')
        ax.set_ylabel('Importance')
        ax.set_title('IPA 분석 결과')
        st.pyplot(fig)

        st.markdown("### 📋 전략별 분포")
        grouped = df.groupby('전략')['Item'].apply(list).reset_index()
        grouped['개수'] = grouped['Item'].apply(len)
        grouped = grouped[['전략', '개수', 'Item']]
        st.table(grouped)

        st.subheader("📝 전략별 제언 메시지")

        def suggest(strategy):
            if strategy == '유지':
                return "✅ 현재 수준을 유지하세요. 잘 관리되고 있습니다."
            elif strategy == '개선 우선':
                return "🔺 중요도가 높지만 수행도가 낮습니다. 빠른 개선이 필요합니다."
            elif strategy == '과잉 노력':
                return "🟠 중요도에 비해 과도한 자원이 투입되고 있습니다. 자원 재배치를 고려하세요."
            else:
                return "⚪ 현재는 우선순위가 낮습니다. 자원을 집중하지 않아도 됩니다."

        for strategy in ['개선 우선', '유지', '과잉 노력', '저우선순위']:
            filtered = df[df['전략'] == strategy]
            if not filtered.empty:
                with st.expander(f"{strategy} ({len(filtered)}개 항목)", expanded=(strategy == '개선 우선')):
                    for _, row in filtered.iterrows():
                        st.markdown(f"🔹 **{row['Item']}** → {suggest(row['전략'])}")

with tab2:
    st.subheader("🧾 ESG 항목 코드 및 주제 설명")
    code_df = pd.DataFrame({
        "코드": list(code_explanations.keys()),
        "주제": list(code_explanations.values())
    })
    st.dataframe(code_df, use_container_width=True)
