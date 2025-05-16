import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import numpy as np

# ✅ 한글 폰트 설정
FONT_NAME = "NanumGothic"
FONT_PATH = os.path.join(os.path.dirname(__file__), "NanumGothic.ttf")
matplotlib.rcParams["font.family"] = FONT_NAME
matplotlib.rcParams["axes.unicode_minus"] = False

# ✅ 페이지 설정
st.set_page_config(layout="wide", page_title="ESG IPA Analyzer", page_icon="📊")

# ✅ 제목
st.title("📊 ESG IPA 분석 대시보드")
st.caption("전공종합설계 프로젝트 | 팀원: 박유진, 박현우, 송가영")
st.markdown("---")

# ✅ 파일 업로드
uploaded_file = st.file_uploader("📂 엑셀 파일을 업로드하세요 (Item, Importance, Performance)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    mean_imp = df["Importance"].mean()
    mean_perf = df["Performance"].mean()

    def classify(row):
        if row["Importance"] >= mean_imp and row["Performance"] >= mean_perf:
            return "유지"
        elif row["Importance"] >= mean_imp and row["Performance"] < mean_perf:
            return "개선 우선"
        elif row["Importance"] < mean_imp and row["Performance"] >= mean_perf:
            return "과잉 노력"
        else:
            return "저우선순위"

    df["전략"] = df.apply(classify, axis=1)

    # 전략별 색상
    colors = {
        "유지": "green",
        "개선 우선": "red",
        "과잉 노력": "orange",
        "저우선순위": "gray"
    }

    # 전략별 제언
    def suggest(strategy):
        if strategy == '유지':
            return "✅ 현재 수준을 유지하세요. 잘 관리되고 있습니다."
        elif strategy == '개선 우선':
            return "🔺 중요도가 높지만 수행도가 낮습니다. 빠른 개선이 필요합니다."
        elif strategy == '과잉 노력':
            return "🟠 중요도에 비해 과도한 자원이 투입되고 있습니다. 자원 재배치를 고려하세요."
        else:
            return "⚪ 현재는 우선순위가 낮습니다. 자원을 집중하지 않아도 됩니다."

    df['제언'] = df['전략'].apply(suggest)

    # ✅ 탭 구성
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 IPA 결과", "🗂️ 전략 분석", "🔎 전략 필터링/수정", "🧾 항목 코드 설명", "📁 분석 데이터 저장"
    ])

    # 📊 IPA 결과
    with tab1:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("🎯 IPA 그래프")
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

        with col2:
            st.subheader("🧮 기준값")
            st.metric("평균 중요도", f"{mean_imp:.2f}")
            st.metric("평균 수행도", f"{mean_perf:.2f}")
            st.markdown("🔴 평균 Importance (Red Line)<br>🔵 평균 Performance (Blue Line)", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        ### ℹ️ IPA 매트릭스 해석
        - 🔵 **유지**: 중요도와 수행도 모두 높음 → 유지
        - 🔺 **개선 우선**: 중요도 높음, 수행도 낮음 → **보완 필요**
        - 🟠 **과잉 노력**: 수행도 높음, 중요도 낮음 → 자원 재배치 고려
        - ⚪ **저우선순위**: 둘 다 낮음 → 낮은 우선순위
        """)

    # 🗂️ 전략 분석
    with tab2:
        st.subheader("📋 전략별 항목 및 제언")
        for strategy in ['개선 우선', '유지', '과잉 노력', '저우선순위']:
            filtered = df[df['전략'] == strategy]
            if not filtered.empty:
                with st.expander(f"{strategy} ({len(filtered)}개 항목)", expanded=True if strategy == '개선 우선' else False):
                    for _, row in filtered.iterrows():
                        st.markdown(f"🔹 **{row['Item']}** → {row['제언']}")

    # 🔎 전략 필터링 및 항목 수정
    with tab3:
        st.subheader("✏️ 전략 수정 및 필터링")
        filtered_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        st.write("수정된 데이터를 아래에서 저장할 수 있습니다.")

    # 🧾 항목 코드 설명
    with tab4:
        st.subheader("🧾 ESG 항목 코드 설명")
        item_descriptions = {
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
            # ... 필요 시 더 추가 가능
        }
        for code, desc in item_descriptions.items():
            st.markdown(f"**{code}**: {desc}")

    # 📁 분석 기록 저장
    with tab5:
        st.subheader("📁 분석 결과 저장")
        save_df = filtered_df if 'filtered_df' in locals() else df
        csv = save_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 분석결과 CSV 다운로드", csv, "esg_analysis_result.csv", "text/csv")
