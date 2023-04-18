
import streamlit as st
from db_config import Config
from mysql import connector
from recipe import oneFood, foodList
# import webbrowser
# import time


amount_to_emoji = {"1인분" : "🧑",
                "2인분" : "👨🏻‍🤝‍👨🏻",
                "3인분" : "👪",
                "4인분" : "👨‍👩‍👧‍👦"}
difficulty_to_star = {"초보환영" : "⭐",
                    "보통" : "⭐⭐",
                    "어려움" : "⭐⭐⭐"}

def run_query(query):
    conn = connector.connect(**Config) 
    with conn.cursor() as cur:
        cur.execute(query)
        rows= cur.fetchall()
    conn.commit()
    conn.close()

    return rows

def insertFavor(code):
    oneFood(code).insertFavor()

def delFavor(code):
    oneFood(code).delFavor()

def showFoodDetail(code):
  
    # empty1,con1,empty2 = st.columns([0.5,0.77,0.5])
    one = oneFood(code)
    foodcode, name, introduce, subjectcode, subject, typecode, foodtype, cookingtime, amount, difficulty, img = one.getInfo()
    main_ing, sub_ing, sauce = one.getIngredient()
    recipe = one.getRecipe()

    # with empty2 :
    #     st.button("X")

    # with con1 :
    st.markdown('<h1></h1>',unsafe_allow_html=True)
    with st.container(): # 이미지 / 이름 / 분량 / 난이도 / 조리시간
        i1,i2,i3 = st.columns(3)
        with i1:st.write('')
        with i2:st.image(one.getImage()[0][0])
        with i3:st.write('')
       
        c1,c2,c3 = st.columns([0.4,0.4,0.2])
        with c1:st.markdown(f'<span style="font-family:sans-serif; font-weight: bold; color:#61210B; font-size: 40px;"> {one.getImage()[0][1]}  </span>  <span style="font-family:sans-serif; font-weight: bold; color:#FF0000; font-size: 20px;"> {subject} </span>', unsafe_allow_html=True)  
        favorTF,favorTmp=foodList().ourFavor()
        if favorTF:
            st.session_state.userFavor=favorTmp
        else:
            st.session_state.userFavor = []
        
        favorList=[item['RECIPE_ID']for item in st.session_state.userFavor]
        if code in favorList:
            with c3:st.button("💗",on_click=delFavor,args=(code,))
        else:
            with c3:
                st.button("🤍",on_click=insertFavor,args=(code,))

        st.markdown(introduce)

        col1, col2, col3 = st.columns(3)

        with col1 :
            st.markdown(f'<span style="font-weight: bold;">분량</span>', unsafe_allow_html=True)
            st.write(f'{amount_to_emoji[amount]} {amount}')
        with col2 :
            st.markdown(f'<span style="font-weight: bold;">난이도</span>', unsafe_allow_html=True)
            st.write(difficulty_to_star[difficulty])
        with col3 : 
            st.markdown(f'<span style="font-weight: bold;">조리시간</span>', unsafe_allow_html=True)
            st.write(f'⏰ {cookingtime}')


    with st.container(): # 재료
        st.write("----------------")
        co1, co2, co3 = st.columns(3)
        # st.markdown("""<style> div[data-testid="stVerticalBlock"] div[style*="flex-direction: column;"] div[data-testid="stVerticalBlock"] {border: 3px solid grey;} </style>""",unsafe_allow_html=True,)
        with co1 :
            st.markdown(f'<span style="font-weight: bold; text-align: center;">[주재료]</span>', unsafe_allow_html=True)
            for i in main_ing :
                st.write(f"{i[0]}  {i[1]}")
        with co2 :
            st.markdown(f'<span style="font-weight: bold; text-align: center;">[부재료]</span>', unsafe_allow_html=True)
            for i in sub_ing :
                st.write(f"{i[0]}  {i[1]}")
        with co3 :
            st.markdown(f'<span style="font-weight: bold; text-align: center;">[양념]</span>', unsafe_allow_html=True)
            for i in sauce :
                st.write(f"{i[0]}  {i[1]}")
        st.write("------------")

    with st.container() : # 조리법
        st.markdown(f'<span style="font-weight: bold; text-align: center;">조리 방법</span>', unsafe_allow_html=True)
        for i in recipe :
            st.markdown(f'{i[0]}) {i[1]}')
        st.write("------")

    with st.container() : # 유튜브 영상 첨부 도전!
        st.markdown(f'<span style="font-weight: bold; text-align: center;">유튜브 레시피 보러가기</span>', unsafe_allow_html=True)
        st.write(" ")
        with st.spinner("로딩중..."):
            # st.write(one.youtubeVideo())
            st.video(one.youtubeVideo())
