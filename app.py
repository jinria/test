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

# 🎯 페이지 기본 설정
st.set_page_config(layout="centered", page_title="ESG IPA Dashboard", page_icon="📊")

# 🎯 제목
st.title("📊 ESG IPA 분석 대시보드")
st.caption("전공종합설계 프로젝트 | 팀원: 박유진, 박현우, 송가영")
st.markdown("---")

# 📁 파일 업로드
uploaded_file = st.file_uploader("📂 엑셀 파일을 업로드하세요 (Item, Importance, Performance)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("✅ 업로드된 ESG 항목 데이터")
    st.dataframe(df)

    # 평균 계산
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

    # 전략별 색상
    colors = {
        "유지": "green",
        "개선 우선": "red",
        "과잉 노력": "orange",
        "저우선순위": "gray"
    }

    # 📊 IPA 그래프
    st.subheader("📌 IPA 매트릭스")
    fig, ax = plt.subplots(figsize=(8, 6))
    for _, row in df.iterrows():
        ax.scatter(row['Performance'], row['Importance'], color=colors[row['전략']], s=100)
        ax.text(row['Performance'] + 0.02, row['Importance'], row['Item'], fontsize=9)
    ax.axhline(mean_imp, color='red', linestyle='--')
    ax.axvline(mean_perf, color='blue', linestyle='--')
    ax.set_xlabel('Performance')
    ax.set_ylabel('Importance')
    ax.set_title('IPA Result')
    st.pyplot(fig)

    # ℹ️ 해석 가이드
    st.markdown("---")
    st.markdown("""
    ### ℹ️ IPA 매트릭스 해석
    - 🔵 **유지**: 중요도와 수행도 모두 높음 → 유지
    - 🔺 **개선 우선**: 중요도 높음, 수행도 낮음 → **보완 필요**
    - 🟠 **과잉 노력**: 수행도 높음, 중요도 낮음 → 자원 재배치 고려
    - ⚪ **저우선순위**: 둘 다 낮음 → 낮은 우선순위
    """)
    st.markdown("---")

    # 📋 전략별 항목 분포 요약
    st.subheader("📋 전략별 항목 분포")
    grouped = df.groupby('전략')['Item'].apply(list).reset_index()
    grouped['개수'] = grouped['Item'].apply(len)
    grouped = grouped[['전략', '개수', 'Item']]
    st.table(grouped)

    # 📝 전략별 제언 메시지
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
            with st.expander(f"{strategy} ({len(filtered)}개 항목)", expanded=True if strategy == '개선 우선' else False):
                for _, row in filtered.iterrows():
                    st.markdown(f"🔹 **{row['Item']}** → {suggest(row['전략'])}")