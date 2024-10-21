import streamlit as st
from streamlit_chat import message
import openai
import os

# OpenAI API 키 설정
openai.api_key = os.environ.get('OPENAI_API_KEY')  # 환경 변수에서 API 키 가져오기

# 시스템 지침 정의
system_instruction1 = ''' 
너는 의료지식이 풍부한 진로 가이드 챗봇이야.  
- 너의 최종 목표는 고등학생들에게 간호사에 대해 알려줘야 해. 
- 고등학생들과 대화를 하니 최대한 쉬운 단어로 질문해야 해. 
- 너무 과목에 치우치지 말고 성격이나 취미, 장점, 단점 등 진로에 도움 될 만한 질문을 적절하게 생성해.
'''

# 세션 스테이트 초기화
if 'messages' not in st.session_state:
    st.session_state['messages'] = [{
        "role": "assistant",
        "content": '나는 간호사 챗봇이야. 간호사에 대한 궁금한 점이 있니?'
    }]

if 'stop' not in st.session_state:
    st.session_state['stop'] = False

def chat(text):
    messages = [{"role": "system", "content": system_instruction1}]
    messages.extend(st.session_state['messages'])

    user_turn = {"role": "user", "content": text}
    messages.append(user_turn)
    st.session_state['messages'].append(user_turn)

    try:
        # OpenAI API 호출
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages
        )
        assistant_messages = response['choices'][0]['message']['content']
    except Exception as e:
        assistant_messages = "죄송합니다, 요청 처리 중 오류가 발생했습니다."
        st.error(f"Error: {str(e)}")

    assistant_turn = {"role": "assistant", "content": assistant_messages}
    st.session_state['messages'].append(assistant_turn)

    return assistant_messages

# Streamlit 앱 타이틀
st.title('ChatGPT-ED 진로 가이드 챗봇')

if not st.session_state['stop']:
    row1 = st.container()
    row2 = st.container()

    with row2:
        with st.form('form', clear_on_submit=True):
            input_text = st.text_input('You', placeholder='질문을 입력하세요...')
            submitted = st.form_submit_button('Send')
            if submitted and input_text:
                chat(input_text)

    with row1:
        for i, msg_obj in enumerate(st.session_state['messages']):
            msg = msg_obj['content']
            is_user = (i % 2 == 1)  # 질문/응답 구분
            message(msg, is_user=is_user, key=i)
