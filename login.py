import streamlit as st
from db_config import Config
from mysql import connector
from streamlit.source_util import get_pages,_on_pages_changed
import json
from pathlib import Path

if 'login_id' not in st.session_state : st.session_state.login_id =''
if 'login_pw' not in st.session_state : st.session_state.login_pw =''
if 'username' not in st.session_state : st.session_state.username =''
if 'userFavor' not in st.session_state : st.session_state.userFavor = []

DEFAULT_PAGE = "MainHome.py"

class Login():

    def init_connection(self):
        self.conn = connector.connect(**Config)
        return self.conn
    
    def run_query(self,query):
        conn=self.init_connection()     
        with conn.cursor() as cur:
            cur.execute(query)
            rows= cur.fetchall()
        conn.commit()
        conn.close()

        return rows
    
    def login(self,id,pw): #로그인
        query = f'select userName,userFavor from user where userId = "{id}" and userPw ="{pw}";'
        rows = self.run_query(query)
        if rows:
            userName=rows[0][0]
            userFavor=rows[0][1]
            return userName,userFavor
        else:
            return 'nouser',''
        
    def reg_member(self,username,id,pw,age,gender): #회원정보 DB 저장
        query = f"insert into user(userName,userId,userPw,age,gender) values('{username}','{id}','{pw}','{age}','{gender}');"
        self.run_query(query)

    def reg_id_check(self,id): #회원가입 아이디 중복 체크
        query= f'select * from user where userId = "{id}";'
        rows=self.run_query(query)
        if rows:
            return False #사용불가
        else:
            return True #사용가능
        
    ###로그인 페이지###
        
    def loginBtnClick(self): #로그인 버트
        st.session_state.error_message=''
        if not str(st.session_state.input_id) :
            st.session_state.error_message = "ID를 입력해주세요."
            
        elif not str(st.session_state.input_pw) :
            st.session_state.error_message = "PASSWORD를 입력해주세요."
        
        else :
            username,userfavor=self.login(st.session_state.input_id,st.session_state.input_pw)
            if username != 'nouser':
                st.session_state.login_id=st.session_state.input_id
                st.session_state.login_pw=st.session_state.input_pw
                st.session_state.username = username
                st.session_state.userfavor = userfavor
                self.loginSuccess()

            else :
                st.session_state.error_message = "등록된 정보가 없습니다. 재확인하거나 회원가입바랍니다.🚨"

    def goRegClick(self):
        st.session_state.error_message=''
        st.session_state.mainpage = 'reg_member' #회원가입 페이지로 이동

    def regBtnClick(self):
        if not str(st.session_state.reg_id) or not str(st.session_state.reg_pw) or not str(st.session_state.reg_name) or not str(st.session_state.reg_pw_check):
            st.session_state.error_message ="🚨 모든 정보를 입력해주세요. 🚨"  

        elif not self.reg_id_check(st.session_state.reg_id) :
            st.session_state.error_message ="🚨 중복된 아이디입니다. 다시 입력해주세요. 🚨"
            
        elif st.session_state.reg_pw != st.session_state.reg_pw_check :
            st.session_state.error_message ="🚨 비밀번호가 일치하지 않습니다.🚨"

        else:
            st.session_state.error_message=''
            st.session_state.username=st.session_state.reg_name
            st.session_state.login_id=st.session_state.reg_id
            st.session_state.login_pw=st.session_state.reg_pw
            st.session_state.mainpage = 'reg_mem_info' #회원 세부정보 페이지 이동

    def regInfoBtnClick(self):
        if not str(st.session_state.reg_age) or not str(st.session_state.reg_gender):
            st.session_state.error_message ="🚨 모든 정보를 입력해주세요. 🚨" 

        else:
            st.session_state.error_message=''
            self.reg_member(st.session_state.username,st.session_state.login_id,st.session_state.login_pw,st.session_state.reg_age,st.session_state.reg_gender)
            self.loginSuccess()

    def loginSuccess(self):
        st.session_state.mainpage = 'login_check'
        st.balloons()

        

    def show_login_page(self):
        # st.markdown(f'<h1 style="background-color:#A7DCDC;border-radius:2%;text-align: center;">오늘은 내가 요리사 👩‍🍳</h1>', unsafe_allow_html=True)
        ##페이지 만들기
        ph = st.empty()
        #로그인 페이지        
        if st.session_state.mainpage == 'login':
            with ph.container():
                    with st.form("login_form"):
                        col1, col2,col3 = st.columns(3)
                        with col1 : st.write(' ')
                            
                        with col2:
                                st.text_input("ID",key='input_id')
                                st.text_input("PASSWORD",key='input_pw',type='password')
                                st.form_submit_button('로그인',use_container_width=True,on_click=self.loginBtnClick) #로그인 시도
                                st.form_submit_button('회원가입',use_container_width=True,on_click=self.goRegClick) #회원가입 페이지로 이동
                            
                        with col3 : st.write(' ')

        ## 회원가입 Page 1
        elif st.session_state.mainpage == 'reg_member':
            with st.form("reg_mem_form"):
                st.markdown("<h3 style='text-align: center;'>회원가입</h3>", unsafe_allow_html=True)
                col1, col2,col3 = st.columns(3)
                with col1 : st.write(' ')
                with col2:
                        st.text_input("이름",key='reg_name')
                        st.text_input("ID",key='reg_id')
                        st.text_input("PASSWORD",key='reg_pw',type='password')
                        st.text_input("비밀번호 재입력",key='reg_pw_check',type='password')
                        st.form_submit_button('가입하기',use_container_width=True,on_click=self.regBtnClick) #너비 늘리기

                with col3 : st.write(' ')
        ## 회원가입 Page 2 ; 상세정보 입력
        elif st.session_state.mainpage == 'reg_mem_info':
            with st.form("reg_mem_info"):
                st.markdown(f"<h3 style='text-align: center;'> {st.session_state.username}님의 정보를 입력해주세요. </h3>", unsafe_allow_html=True)
                col1, col2,col3 = st.columns(3)
                with col1 : st.write(' ')
                with col2:
                        st.text_input("나이",key='reg_age')
                        st.radio("성별",('여자','남자'),key='reg_gender')
                        st.form_submit_button('가입하기',use_container_width=True,on_click=self.regInfoBtnClick) #너비 늘리기 
                with col3 : st.write(' ')

    #로그인 x 시 페이지 감추기 
    def clear_all_but_first_page(self):
        current_pages = get_pages(DEFAULT_PAGE)

        if len(current_pages.keys()) == 1:
            return
        self.get_all_pages()

        # # Remove all but the first page
        key, val = list(current_pages.items())[0]
        current_pages.clear()
        current_pages[key] = val

        _on_pages_changed.send()

    def get_all_pages(self):
        default_pages = get_pages(DEFAULT_PAGE)

        pages_path = Path("pages.json")

        if pages_path.exists():
            saved_default_pages = json.loads(pages_path.read_text())
        else:
            saved_default_pages = default_pages.copy()
            pages_path.write_text(json.dumps(default_pages, indent=4))

        return saved_default_pages


    def show_all_pages(self):
        current_pages = get_pages(DEFAULT_PAGE)

        saved_pages = self.get_all_pages()

        missing_keys = set(saved_pages.keys()) - set(current_pages.keys())

        # Replace all the missing pages
        for key in missing_keys:
            current_pages[key] = saved_pages[key]

        _on_pages_changed.send()