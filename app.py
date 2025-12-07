import streamlit as st
import random
import json
import os

TOPIC_FILE = "topics.json"

def load_topics():
    if not os.path.exists(TOPIC_FILE):
        return []
    with open(TOPIC_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_topic(question, number_range):
    topics = load_topics()
    topics.append({
        "question": question,
        "range": number_range
    })
    with open(TOPIC_FILE, "w", encoding="utf-8") as f:
        json.dump(topics, f, ensure_ascii=False, indent=4)

st.set_page_config(page_title="라이어 게임", page_icon="🎮", layout="centered")
st.title("🎮 온라인 라이어 게임")

page = st.sidebar.selectbox("메뉴", ["게임 시작", "주제 추가"])

if page == "주제 추가":
    st.header("📝 게임 주제 추가")

    q = st.text_input("1) 질문 입력")
    number_range = st.text_input("2) 숫자범위 입력 (예: 1~100)")

    if st.button("주제 저장"):
        if q.strip() == "" or number_range.strip() == "":
            st.error("모든 항목을 채워주세요.")
        else:
            save_topic(q, number_range)
            st.success("주제가 저장되었습니다!")

    st.subheader("📚 저장된 주제 목록")
    topics = load_topics()
    for i, t in enumerate(topics):
        st.write(f"{i+1}. 질문: {t['question']} / 숫자범위: {t['range']}")

if page == "게임 시작":
    st.header("🎲 게임 설정")

    players = st.number_input("게임 인원 (3~10명)", min_value=3, max_value=10, value=5)
    topics = load_topics()

    if len(topics) == 0:
        st.warning("주제가 없습니다. 먼저 '주제 추가'에서 등록하세요.")
        st.stop()

    selected_topic_index = st.selectbox(
        "게임 주제 선택 (플레이어에게는 비공개)",
        options=list(range(len(topics))),
        format_func=lambda x: f"주제 #{x+1}"
    )

    if st.button("역할 배정 시작"):
        roles = ["라이어", "트롤"] + ["시민"] * (players - 2)
        random.shuffle(roles)

        st.session_state["roles"] = roles
        st.session_state["current_player"] = 1
        st.session_state["topic"] = topics[selected_topic_index]

        st.success("역할 배정 완료!")

    if "roles" in st.session_state:
        st.header(f"{st.session_state['current_player']}번 플레이어 차례")

        if f"checked_{st.session_state['current_player']}" not in st.session_state:
            st.session_state[f"checked_{st.session_state['current_player']}"] = False

        if not st.session_state[f"checked_{st.session_state['current_player']}"]:
            if st.button("👉 역할 확인하기"):
                st.session_state[f"checked_{st.session_state['current_player']}"] = True
        else:
            role = st.session_state["roles"][st.session_state["current_player"]-1]
            topic = st.session_state["topic"]

            st.subheader(f"당신의 역할: {role}")

            if role == "라이어":
                st.warning("라이어는 질문을 볼 수 없습니다.")
                st.info(f"숫자 범위만 볼 수 있음: {topic['range']}")
            else:
                st.success(f"질문: {topic['question']}")
                st.info(f"숫자 범위: {topic['range']}")

            if st.session_state["current_player"] < players:
                if st.button("➡️ 다음 플레이어"):
                    st.session_state["current_player"] += 1
            else:
                st.success("🎉 모든 플레이어가 역할을 확인했습니다!")