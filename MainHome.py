import streamlit as st
from db_config import Config
from login import Login
import hydralit_components as hc
import foodDetail
from recipe import foodList
import time

st.set_page_config(page_title="오늘은 내가 요리사",page_icon="👩‍🍳",layout='wide')
st.markdown(f'<h1 style="background-color:#A7DCDC;border-radius:2%;text-align: center;">오늘은 내가 요리사 👩‍🍳</h1>', unsafe_allow_html=True)
if 'mainpage' not in st.session_state: st.session_state.mainpage = 'login'
if 'recipePage' not in st.session_state : st.session_state.recipePage = ''

def empty():
    placeholder.empty()
    time.sleep(1)

Login().clear_all_but_first_page() #로그인 화면 보여주기
Login().show_login_page()

placeholder= st.empty()
## 로그인 완료
if st.session_state.mainpage == 'login_check':
 
    Login().show_all_pages()
    # url = f"{st.get_url()}/?my_var=42"
    # st.markdown("[Link](url)")

    # if st.session_state.page1 == 0:
    with placeholder.container():  
        st.markdown(f"<h5 style='text-align: center;background-color:#A7DCDC;'> {st.session_state.username}님 오늘도 맛있는 하루 되세요😆👍 </h5>", unsafe_allow_html=True)
        st.markdown("""## """)
        ### 제철메뉴 추천 파트 ###
        month,fruit,vegi=foodList().seasonal()
        st.markdown(f"<h5 style='text-align: center;background-color:#DCDCDC; padding-top: 10px;'> {month}월의 제철메뉴 📅 </h5>", unsafe_allow_html=True)
        st.markdown(f"<h5 style='text-align: left;background-color:#F0FFF0; padding-top: 10px;'> 🍒 {month}월의 제철 과일</h5>", unsafe_allow_html=True) 
        st.markdown(f"<h6 style='text-align: left;background-color:#F0FFF0; padding-left: 10px;'> {fruit}</h6>", unsafe_allow_html=True) 
        st.markdown(f"<h5 style='text-align: left;background-color:#F0FFF0; padding-top: 10px;'> 🥦 {month}월의 제철 채소</h5>", unsafe_allow_html=True)  
        st.markdown(f"<h6 style='text-align: left;background-color:#F0FFF0; padding-left: 10px;'> {vegi}</h6>", unsafe_allow_html=True) 
        
        favorTF,favorTmp=foodList().ourFavor()

        if favorTF:
            st.session_state.userFavor=favorTmp
            st.write('')
            st.markdown(f"<h5 style='text-align: center;background-color:#F8F8FF; padding-top: 10px;'> {st.session_state.username}님이 좋아하는 레시피 ❤</h5>", unsafe_allow_html=True)  
            click=foodList().showFoodList(st.session_state.userFavor)

        else:
            st.session_state.userFavor = []
            st.session_state.bestFavor=favorTmp
            st.write('')
            st.markdown(f"<h5 style='text-align: center;background-color:#F8F8FF; padding-top: 10px;'> BEST 메뉴 추천! 🍜 </h5>", unsafe_allow_html=True)  
            click=foodList().showFoodList(st.session_state.bestFavor) 

    if click:
        # st.session_state.page1=1
        # st.markdown('<h1>33</h1>', unsafe_allow_html=True)
        empty()
        with placeholder.container():
            foodDetail.showFoodDetail(st.session_state.code)

    # elif st.session_state.page1 == 1:
    #     empty()
    #     with placeholder.container():
    #         foodDetail.showFoodDetail(st.session_state.code)
    
# elif st.session_state.recipepage == 'detailPage':
#     foodDetail.showFoodDetail(st.session_state.code)

con = st.container()
if 'error_message' in st.session_state and st.session_state.error_message:
    con.error(st.session_state.error_message)