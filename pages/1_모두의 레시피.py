import streamlit as st
from db_config import Config
from mysql import connector
import foodDetail
import random
from recipe import foodList,rfg
import hydralit_components as hc
import time


st.set_page_config(page_title="모두의 레시피", page_icon="🍜",layout='wide')

if 'random_numbers' not in st.session_state: st.session_state.random_numbers = []
if 'random_ids' not in st.session_state: st.session_state.random_ids = []

# @st.cache_resource
# def load_page():
#     if 'recipePage' not in st.session_state or st.session_state.recipePage!='base': st.session_state.recipePage = 'base'

amount_to_emoji = {"1인분" : "🧑",
                "2인분" : "👨🏻‍🤝‍👨🏻",
                "3인분" : "👪",
                "4인분" : "👨‍👩‍👧‍👦"}
difficulty_to_star = {"초보환영" : "⭐",
                    "보통" : "⭐⭐",
                    "어려움" : "⭐⭐⭐"}

def empty():
    placeholder.empty()
    time.sleep(1)

def run_query(query):
    conn = connector.connect(**Config) 
    with conn.cursor() as cur:
        cur.execute(query)
        rows= cur.fetchall()
    conn.commit()
    conn.close()

    return rows

@st.cache_resource
def getRandom() :
    query = f"select RECIPE_ID from recipeInfo;"    
    st.session_state.random_ids = run_query(query)
    st.session_state.random_numbers = [random.randrange(1,len(st.session_state.random_ids)) for i in range(6)] # 랜덤 번호

    col=['RECIPE_ID','RECIPE_NM', 'RECIPE_INFO', '유형분류', '음식분류', '조리시간', '분량','난이도', '이미지URL']      
    query = f"select RECIPE_ID,RECIPE_NM, RECIPE_INFO, 유형분류, 음식분류, 조리시간, 분량, 난이도, 이미지URL from recipeInfo where RECIPE_ID IN {tuple(st.session_state.random_numbers)};"    
    rows = run_query(query) # 랜덤 번호의 데이터
    return rows

###########페이지###########
st.markdown(f'<h1 style="background-color:#A7DCDC;border-radius:2%;text-align: center;">오늘은 내가 요리사 👩‍🍳</h1>', unsafe_allow_html=True)
st.markdown(f'<h3 style="background-color:#A7DCDC;border-radius:2%;text-align: center;"> 모두의 레시피 🍜</h3>',unsafe_allow_html=True)
menu_data = [
    {'id':'search','icon': "🔎", 'label':"레시피 조회"},
    {'id':'myFood','icon':'🍚','label':'냉장고 털기'}
    ]

over_theme = {'txc_inactive': '#5D5D5D','menu_background':'#A7DCDC','txc_active':'black'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='오늘의 메뉴 추천',
    hide_streamlit_markers=True, #will show the st hamburger as well as the navbar now!
    sticky_nav=True, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)

placeholder = st.empty()

if menu_id =='오늘의 메뉴 추천':

    with placeholder.container():  
        st.markdown('<h1></h1>',unsafe_allow_html=True)
        st.markdown(f"<h3 style='border-radius:2%;text-align: center;'> 오늘의 메뉴를 추천해드려요! </h3>",unsafe_allow_html=True) #2
        rows = getRandom()
        st.session_state.randomResult=foodList().randomFood(rows)
        click=foodList().showFoodList(st.session_state.randomResult)
    if click:
        empty()
        with placeholder.container():
            foodDetail.showFoodDetail(st.session_state.code)
        # foodDetail.showFoodDetail(st.session_state.code)
    # if st.session_state.recipePage == 'detailPage':w
    #     placeholder1.empty()
    #     foodDetail.showFoodDetail(st.session_state.code)

elif menu_id =='search':
    ###########레시피 조회 사이드바################
    foodcategory1 = st.sidebar.selectbox(
    "음식 카테고리 대분류를 선택해주세요",('한식', '퓨전', '서양', '이탈리아', '일본', '중국', '동남아시아')
    )
    query1 = f"select 음식분류 from recipeInfo where 유형분류='{foodcategory1}';"
    mid = run_query(query1) # mid = 위에서 선택된 유형분류에 해당하는 음식분류만 가져오는 query1 실행 결과
    # mid의 요소를 중복없이 set으로 뽑아서 리스트로 만들어서 sidebar.selectbox에 넣기
    foodcategory2 = st.sidebar.selectbox("음식 카테고리 중분류를 선택해주세요",list(set([i[0] for i in mid])))

    query2 = f"select 조리시간 from recipeInfo where 유형분류='{foodcategory1}' and 음식분류='{foodcategory2}';"
    ct = run_query(query2) # ct = 위에서 선택된 유형분류, 음식분류에 해당하는 조리시간만 가져오는 query2 실행 결과
    # ct의 요소를 중복없이 set으로 뽑아서 리스트로 만든 후 오름차순 정렬
    cook_time = st.sidebar.selectbox("조리시간을 선택해주세요",sorted(list(set([i[0]+' 이하' for i in ct]))))

    query3 = f"select 난이도 from recipeInfo where 유형분류='{foodcategory1}' and 음식분류='{foodcategory2}' and 조리시간 <= {int(cook_time.split('분')[0])};"
    diff = run_query(query3) # diff = 위에서 선택된 유형분류, 음식분류, 조리시간(선택한 시간 이하)에 해당하는 난이도만 가져오는 query3 실행 결과
    difficulty = st.sidebar.selectbox("조리 난이도를 선택해주세요",list(set([i[0] for i in diff])))

    with st.sidebar:
        searchBtn=st.button("조회하기",use_container_width=True)

    if searchBtn: #선택완료 버튼을 누르면 실행
        st.session_state.recipePage='searchPage'
        # st.experimental_rerun()

    st.session_state.searchResult=foodList().searchFood(foodcategory1,foodcategory2,cook_time,difficulty)
    placeholder = st.empty()
    with placeholder.container():  
        click=foodList().showFoodList(st.session_state.searchResult)

    if click:
        empty()
        with placeholder.container():
            foodDetail.showFoodDetail(st.session_state.code)

elif menu_id =='myFood':
    st.markdown('<h1></h1>',unsafe_allow_html=True)
    st.markdown(f"<h3 style='border-radius:2%;text-align: center;'> 냉장고 속 재료를 사용해보세요! </h3>",unsafe_allow_html=True) #2
    userRfg=rfg().get_userRfg()
    ingred=[ row['itemName'] for row in userRfg]   
    options = st.multiselect("활용할 재료 선택하기",ingred)
    click=False
    if options:
        myResult=rfg().searchFood(options)
        if myResult == [] :
            txt=str(options).replace('[','').replace(']','')
            st.markdown(f"<h3> {txt} 로는 할 수 있는 요리가 없어요! 😥  </h3>", unsafe_allow_html=True)
        else:
            txt=str(options).replace('[','').replace(']','')
            st.markdown(f"<h3> {txt} 로 할 수 있는 요리입니다! 😋 </h3>", unsafe_allow_html=True)
            placeholder = st.empty()
            with placeholder.container():  
                click=foodList().showFoodList(myResult)

    if click:
        empty()
        with placeholder.container():
            foodDetail.showFoodDetail(st.session_state.code)

    
# elif st.session_state.recipePage == 'blank':
#     st.write('')