import streamlit as st
import random
import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# 환경 변수 로드 (.env 파일에서 OpenAI API 키 로드)
load_dotenv()

# 페이지 기본 설정은 전체 앱에서 한 번만 호출 가능합니다.
st.set_page_config(page_title="코드리뷰 & 로또생성)", page_icon="✨", layout="wide")

# 로또 공 CSS 스타일 정의
st.markdown("""
<style>
.lotto-ball {
    display: inline-block;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    text-align: center;
    line-height: 60px;
    font-size: 24px;
    font-weight: bold;
    color: white;
    margin: 10px 5px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    text-shadow: 1px 1px 2px rgba(0,0,0,0.4);
}
.ball-yellow { background-color: #fbc400; color: #333; text-shadow: none; }
.ball-blue { background-color: #69c8f2; }
.ball-red { background-color: #ff7272; }
.ball-gray { background-color: #aaaaaa; }
.ball-green { background-color: #b0d840; }
.ball-container {
    text-align: center;
    margin-top: 10px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

def get_ball_class(number):
    if number <= 10:
        return "ball-yellow"
    elif number <= 20:
        return "ball-blue"
    elif number <= 30:
        return "ball-red"
    elif number <= 40:
        return "ball-gray"
    else:
        return "ball-green"

st.title("✨ 친절한 파이썬 코드 리뷰 & 로또 번호 생성기")

# 탭 생성
tab1, tab2 = st.tabs(["🐍 파이썬 코드 리뷰", "🎲 로또 번호 생성기"])

# ----------------- 첫 번째 탭: 파이썬 코드 리뷰 -----------------
with tab1:
    st.header("🐍 비전공자를 위한 친절한 파이썬 코드 리뷰")
    st.write("파이썬 코드를 입력하면, 프로그래밍을 모르는 분들도 이해할 수 있도록 쉽고 자세하게 설명해 드리고, 프로그램이 어떻게 단계적으로 실행되는지 알려드립니다.")

    # 세션 상태 초기화
    if "explanation_result" not in st.session_state:
        st.session_state.explanation_result = None
    if "debugging_result" not in st.session_state:
        st.session_state.debugging_result = None

    # 사용자로부터 코드 입력 받기
    code_input = st.text_area("파이썬 코드를 여기에 붙여넣으세요:", height=300, placeholder="ex) \nname = '홍길동'\nprint('안녕하세요, ' + name + '님!')")

    # 버튼에 고유한 key 지정
    if st.button("코드 분석 및 디버깅 시작하기", type="primary", key="code_review_btn"):
        if code_input.strip() == "":
            st.warning("분석할 코드를 입력해 주세요!")
        else:
            with st.spinner("AI가 코드를 꼼꼼히 분석 중입니다... 잠시만 기다려주세요 🤖"):
                try:
                    # LLM 모델 초기화 (gpt-4o-mini 사용)
                    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

                    # 1. 쉬운 코드 설명 프롬프트
                    explanation_prompt = PromptTemplate.from_template(
                        """당신은 프로그래밍을 전혀 모르는 비전공자에게 파이썬을 가르치는 친절한 선생님입니다.
                        아래의 파이썬 코드를 보고, 일상 생활의 비유를 들어서 최대한 쉽고 자세하게 설명해주세요.
                        전문 용어 사용은 자제하고, 부득이하게 사용할 경우 반드시 쉬운 설명을 덧붙여 주세요.

                        [파이썬 코드]
                        {code}

                        [친절한 설명]"""
                    )
                    
                    # 2. 단계별 디버깅/실행 과정 프롬프트
                    debugging_prompt = PromptTemplate.from_template(
                        """당신은 파이썬 프로그램의 실행 과정을 추적하는 친절한 디버거입니다.
                        아래의 파이썬 코드가 실행될 때, 첫 번째 줄부터 마지막 줄까지 어떤 순서로 실행되는지 단계별로 설명해주세요.
                        변수의 값이 어떻게 저장되고 변하는지, 어떤 조건에서 어떤 결과가 나오는지 초보자가 직관적으로 이해하기 쉽게 구체적으로 설명해주세요.

                        [파이썬 코드]
                        {code}

                        [단계별 실행 과정 (디버깅)]"""
                    )

                    # 체인 구성 및 실행
                    explanation_chain = explanation_prompt | llm
                    debugging_chain = debugging_prompt | llm

                    explanation_result = explanation_chain.invoke({"code": code_input})
                    debugging_result = debugging_chain.invoke({"code": code_input})

                    # 결과를 세션 상태에 저장
                    st.session_state.explanation_result = explanation_result.content
                    st.session_state.debugging_result = debugging_result.content

                except Exception as e:
                    st.error(f"오류가 발생했습니다. API 키가 제대로 설정되었는지, 인터넷 연결이 정상인지 확인해 주세요.\n\n상세 오류: {e}")

    # 저장된 결과 출력
    if st.session_state.explanation_result:
        st.divider()
        st.subheader("📖 코드가 무슨 뜻인가요?")
        st.info(st.session_state.explanation_result)

    if st.session_state.debugging_result:
        st.divider()
        st.subheader("🔍 프로그램은 어떻게 실행되나요? (단계별 디버깅)")
        st.success(st.session_state.debugging_result)

# ----------------- 두 번째 탭: 로또 번호 생성기 -----------------
with tab2:
    st.header("🎲 로또 번호 생성기")
    st.write("버튼을 누르면 1부터 45까지의 숫자 중 6개의 당첨 번호가 생성됩니다.")

    # 세션 상태 초기화
    if "lotto_html" not in st.session_state:
        st.session_state.lotto_html = None
    if "lotto_time" not in st.session_state:
        st.session_state.lotto_time = None

    # 번호 생성 버튼 (버튼에 고유한 key 지정)
    if st.button("로또 번호 생성하기", type="primary", key="lotto_btn"):
        # 1~45 사이의 중복 없는 숫자 6개 생성
        lotto_numbers = random.sample(range(1, 46), 6)
        # 보기 좋게 오름차순으로 정렬
        lotto_numbers.sort()
        
        # 현재 시간 가져오기
        now = datetime.now()
        formatted_time = now.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
        
        # 공 모양으로 출력
        balls_html = "<div class='ball-container'>"
        for num in lotto_numbers:
            ball_class = get_ball_class(num)
            balls_html += f"<div class='lotto-ball {ball_class}'>{num}</div>"
        balls_html += "</div>"
        
        # 세션 상태에 저장
        st.session_state.lotto_html = balls_html
        st.session_state.lotto_time = formatted_time

    # 저장된 결과 출력
    if st.session_state.lotto_html:
        st.divider()
        st.subheader("🎉 생성된 번호")
        st.markdown(st.session_state.lotto_html, unsafe_allow_html=True)
        st.info(f"🕒 **생성 시간:** {st.session_state.lotto_time}")
