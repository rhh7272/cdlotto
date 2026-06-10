import streamlit as st
from dotenv import load_dotenv
import os
import io
import sys
from contextlib import redirect_stdout
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# 환경 변수 로드 (.env 파일에서 OpenAI API 키 로드)
load_dotenv()

# 페이지 기본 설정
st.set_page_config(page_title="파이썬 코드 친절한 리뷰어", page_icon="🐍", layout="wide")

st.title("🐍 친절한 파이썬 코드 리뷰")
st.write("파이썬 코드를 입력하면, 프로그래밍을 모르는 분들도 이해할 수 있도록 쉽고 자세하게 설명해 드리고, 프로그램이 어떻게 단계적으로 실행되는지 알려드립니다.")

# 사용자로부터 코드 입력 받기
code_input = st.text_area("파이썬 코드를 여기에 붙여넣으세요:", height=300, placeholder="ex) \nname = '홍길동'\nprint('안녕하세요, ' + name + '님!')")

if st.button("코드 분석 및 디버깅 시작하기", type="primary"):
    if code_input.strip() == "":
        st.warning("분석할 코드를 입력해 주세요!")
    else:
        with st.spinner("AI가 코드를 꼼꼼히 분석 중입니다... 잠시만 기다려주세요 🤖"):
            try:
                # LLM 모델 초기화 (gpt-4o-mini 사용)
                # 환경변수 OPENAI_API_KEY 가 .env 에 설정되어 있어야 합니다.
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

                # 3. 실제 파이썬 코드 실행 (출력 결과 캡처)
                execution_result = ""
                try:
                    f = io.StringIO()
                    with redirect_stdout(f):
                        exec(code_input, {})
                    execution_result = f.getvalue()
                    if not execution_result:
                        execution_result = "실행이 완료되었으나 출력된 내용이 없습니다."
                except Exception as ex:
                    execution_result = f"실행 중 오류 발생:\n{type(ex).__name__}: {ex}"

                # 결과 화면 출력
                st.divider()
                st.subheader("📖 코드가 무슨 뜻인가요?")
                st.info(explanation_result.content)

                st.divider()
                st.subheader("🔍 프로그램은 어떻게 실행되나요? (단계별 디버깅)")
                st.success(debugging_result.content)

                st.divider()
                st.subheader("▶️ 실제 프로그램 실행 결과")
                if "실행 중 오류 발생" in execution_result:
                    st.error(execution_result)
                else:
                    st.code(execution_result, language="text")

            except Exception as e:
                st.error(f"오류가 발생했습니다. API 키가 제대로 설정되었는지, 인터넷 연결이 정상인지 확인해 주세요.\n\n상세 오류: {e}")
