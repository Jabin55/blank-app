import os

import anthropic
import streamlit as st

# 모델별 요청 옵션: Haiku 4.5는 effort 설정과 서버 측 fallback을 지원하지 않음
MODELS = {
    "⚖️ Sonnet 5.5 (추천 · 균형)": {
        "model": "claude-sonnet-5-5",
        "output_config": {"effort": "low"},
        "betas": ["server-side-fallback-2026-07-01"],
        "fallbacks": "default",
    },
    "🧠 Opus 5.5 (가장 똑똑함 · 2배 비용)": {
        "model": "claude-opus-5-5",
        "output_config": {"effort": "low"},
        "betas": ["server-side-fallback-2026-07-01"],
        "fallbacks": "default",
    },
    "⚡ Haiku 4.5 (가장 저렴 · 빠름)": {
        "model": "claude-haiku-4-5",
    },
}

PERSONAS = {
    "🤖 만능 도우미": "당신은 친절하고 유능한 AI 도우미입니다. 한국어로 간결하고 정확하게 답하세요.",
    "🏫 우리반 도우미": (
        "당신은 학교 학급의 친절한 도우미 챗봇입니다. 학생과 학부모의 질문에 "
        "쉽고 다정한 한국어로 답하세요. 모르는 학급 일정이나 규칙은 지어내지 말고 "
        "담임 선생님께 확인하라고 안내하세요."
    ),
    "📚 공부 친구": (
        "당신은 학생의 공부를 돕는 튜터입니다. 정답을 바로 알려주기보다 힌트와 "
        "질문으로 학생이 스스로 생각하도록 이끌고, 개념은 쉬운 예시로 설명하세요."
    ),
}

st.set_page_config(page_title="AI 챗봇", page_icon="💬", layout="centered")

# 휴대폰 화면에서 여백을 줄이고 글자를 읽기 좋게 조정
st.markdown(
    """
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 5rem; max-width: 720px; }
    @media (max-width: 640px) {
        .block-container { padding-left: 0.75rem; padding-right: 0.75rem; }
        h1 { font-size: 1.6rem !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_api_key() -> str | None:
    try:
        if "ANTHROPIC_API_KEY" in st.secrets:
            return st.secrets["ANTHROPIC_API_KEY"]
    except FileNotFoundError:
        pass
    return os.environ.get("ANTHROPIC_API_KEY")


with st.sidebar:
    st.header("⚙️ 설정")
    model_label = st.selectbox("AI 모델", list(MODELS))
    persona = st.selectbox("챗봇 성격", list(PERSONAS))
    system_prompt = st.text_area("시스템 프롬프트", PERSONAS[persona], height=150)
    api_key = get_api_key()
    if not api_key:
        api_key = st.text_input("Anthropic API 키", type="password")
    if st.button("🗑️ 대화 지우기", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("💬 AI 챗봇")
st.caption("무엇이든 물어보세요! 왼쪽 위 » 버튼을 눌러 모델과 챗봇 성격을 바꿀 수 있어요.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("메시지를 입력하세요"):
    if not api_key:
        st.warning("API 키가 필요해요. 왼쪽 위 » 메뉴에서 입력하거나 secrets에 설정해 주세요.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    client = anthropic.Anthropic(api_key=api_key)

    def stream_reply():
        with client.beta.messages.stream(
            max_tokens=16000,
            system=system_prompt,
            messages=st.session_state.messages,
            **MODELS[model_label],
        ) as stream:
            yield from stream.text_stream
            if stream.get_final_message().stop_reason == "refusal":
                yield "\n\n죄송해요, 이 요청에는 답변드리기 어려워요."

    with st.chat_message("assistant"):
        try:
            reply = st.write_stream(stream_reply())
        except anthropic.AuthenticationError:
            st.error("API 키가 올바르지 않아요.")
            st.session_state.messages.pop()
            st.stop()
        except anthropic.RateLimitError:
            st.error("요청이 너무 많아요. 잠시 후 다시 시도해 주세요.")
            st.session_state.messages.pop()
            st.stop()
        except anthropic.APIConnectionError:
            st.error("네트워크에 연결할 수 없어요.")
            st.session_state.messages.pop()
            st.stop()
        except anthropic.APIStatusError as e:
            st.error(f"오류가 발생했어요: {e.message}")
            st.session_state.messages.pop()
            st.stop()

    st.session_state.messages.append({"role": "assistant", "content": reply})
