import streamlit as st
import random
from datetime import datetime

# 페이지 기본 설정
st.set_page_config(page_title="로또 번호 생성기", page_icon="🎲")

# CSS 스타일 정의
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

st.title("🎲 로또 번호 생성기")
st.write("버튼을 누르면 1부터 45까지의 숫자 중 6개의 당첨 번호가 생성됩니다.")

# 번호 생성 버튼
if st.button("로또 번호 생성하기", type="primary"):
    # 1~45 사이의 중복 없는 숫자 6개 생성
    lotto_numbers = random.sample(range(1, 46), 6)
    # 보기 좋게 오름차순으로 정렬
    lotto_numbers.sort()
    
    # 현재 시간 가져오기
    now = datetime.now()
    formatted_time = now.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    
    st.divider()
    
    # 결과 출력
    st.subheader("🎉 생성된 번호")
    
    # 공 모양으로 출력
    balls_html = "<div class='ball-container'>"
    for num in lotto_numbers:
        ball_class = get_ball_class(num)
        balls_html += f"<div class='lotto-ball {ball_class}'>{num}</div>"
    balls_html += "</div>"
    
    st.markdown(balls_html, unsafe_allow_html=True)
    
    st.info(f"🕒 **생성 시간:** {formatted_time}")
