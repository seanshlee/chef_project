import streamlit as st
from db_config import Config
from mysql import connector
from googleapiclient.discovery import build
from datetime import datetime 
import requests
from PIL import Image
import io
from collections import Counter
# from googleapiclient.errors import HttpError
# from oauth2client.tools import argparser
import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
import time
# import foodDetail

DEVELOPER_KEY = "AIzaSyCnNCe7nXXLJ0yGzkfkRFVej4eEeSxndZs"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)


def run_query(query):
    conn = connector.connect(**Config) 
    with conn.cursor() as cur:
        cur.execute(query)
        rows= cur.fetchall()
    conn.commit()
    conn.close()
    return rows

amount_to_emoji = {"1인분" : "🧑",
                "2인분" : "👨🏻‍🤝‍👨🏻",
                "3인분" : "👪",
                "4인분" : "👨‍👩‍👧‍👦"}
difficulty_to_star = {"초보환영" : "⭐",
                    "보통" : "⭐⭐",
                    "어려움" : "⭐⭐⭐"}


class oneFood() :

    def __init__(self,code) :
        self.code = code

    def getImage(self) :
        query = f'SELECT 이미지URL,RECIPE_NM FROM recipeInfo WHERE RECIPE_ID = "{self.code}";'
        result = run_query(query)
        return result
    
    def getInfo(self) :
        query = f'SELECT * FROM recipeInfo WHERE RECIPE_ID = "{self.code}";'
        result = run_query(query)
        return result[0]       

    def getIngredient(self) :
        main_ing = []
        sub_ing = []
        sauce = []
        query = f'SELECT * FROM recipeIngred WHERE RECIPE_ID = "{self.code}";'
        result = run_query(query)
        for i in result : # 재료 종류별로 리스트 생성
            if i[4] == "주재료" :
                main_ing.append((i[1], i[2]))
            if i[4] == "부재료" :
                sub_ing.append((i[1], i[2]))
            if i[4] == "양념" :
                sauce.append((i[1], i[2]))
        for li in [main_ing,sub_ing,sauce] : # 안필요할 경우 X
            if len(li) == 0 :
                li.append(("X",""))
        return main_ing, sub_ing, sauce

    def getRecipe(self) :
        query = f'SELECT 요리설명순서,요리설명 FROM recipeProcess WHERE RECIPE_ID = "{self.code}";'
        result = run_query(query)
        result.sort(key = lambda x : x[0])
        return result
    
    def youtubeVideo(self) :
        query = f'SELECT RECIPE_URL FROM recipeVideo WHERE RECIPE_ID = "{self.code}";'
        url = run_query(query)
        return url[0][0]
        # query = f'SELECT RECIPE_NM FROM recipeInfo WHERE RECIPE_ID = "{self.code}";'
        # name = run_query(query)[0][0]
        # search_response=youtube.search().list(
        #     q = f"{name}", #채널 십오야
        #     order = 'relevance',
        #     part = 'id',
        #     maxResults = 3).execute()
        # videoID = search_response['items'][0]["id"]["videoId"]
        # url = f'https://www.youtube.com/watch?v={videoID}'
        # return url

    def insertFavor(self) :
        query1 = f"SELECT userFavor FROM user WHERE userId ='{st.session_state.login_id}'" # 기존 UserFavor 정보
        rows = run_query(query1)

        if rows[0][0] != None :
            userfavor = rows[0][0]
            userfavor += f"{self.code};"
        else :
            userfavor = f"{self.code};"

        query = f"UPDATE user SET userFavor='{userfavor}' WHERE userId='{st.session_state.login_id}';" # UserFavor 업데이트
        rows = run_query(query)
        # nm=self.getInfo()['RECIPE_NM']
        nm=self.getInfo()[1]

        placeholder = st.empty()
        with placeholder.container():
            st.info(f"선호 레시피에 '{nm}' 추가되었습니다.",icon='💌')
            time.sleep(2)
        placeholder.empty()

    def delFavor(self):
        query = f"SELECT userFavor FROM user WHERE userId ='{st.session_state.login_id}'" # 기존 UserFavor 정보
        rows = run_query(query)

        userfavor = rows[0][0]
        userfavor=userfavor.replace(f"{self.code};","")
        query = f"UPDATE user SET userFavor='{userfavor}' WHERE userId='{st.session_state.login_id}';" # UserFavor 업데이트
        rows = run_query(query)
        nm=self.getInfo()[1]

        placeholder = st.empty()
        with placeholder.container():
            st.info(f"선호 레시피에서 '{nm}' 삭제되었습니다.",icon='💔')
            time.sleep(2)
        placeholder.empty()


    
class foodList():

    def seasonal(self): #제철 음식 
        now = datetime.now()
        query = f"SELECT 품목명, 품목분류 FROM seasonal_menu WHERE 월별='{now.month}월';"
        rows = run_query(query)

        fruit = [row[0] for row in rows if '과일' in row[1] or '과실' in row[1]]
        fruit2 = ','.join(fruit)
        vegi =   [row[0] for row in rows if '과일' not in row[1] and '과실' not in row[1]]
        vegi2 = ','.join(vegi)

        return now.month,fruit2,vegi2
    
    def ourFavor(self):
        query2 = f"SELECT userFavor FROM user WHERE userId='{st.session_state.login_id}';"
        rows = run_query(query2)

        #### 좋아요를 누른 메뉴가 있는 경우 
        if rows[0][0] is None or rows[0][0]=='':  #좋아요를 누른 메뉴가 없을 경우, user 들이 좋아요 많이 누른 Best 메뉴 추천. 
            query4 = f"SELECT userFavor FROM user;"
            rows_ = run_query(query4)

            # 쿼리 실행 결과에서 빈도 파악할 리스트 생성
            rows_list = [i for row in rows_ if row[0] is not None for i in row[0].split(';')]
            
            # 리스트 내 요소별 빈도 파악
            freq = Counter(rows_list)
            del(freq[""])
            freq=sorted(freq.items(), key = lambda x: x[1],reverse=True)[:3]
            top3=[x[0] for x in freq]
            query = f"SELECT RECIPE_ID,RECIPE_NM, RECIPE_INFO, 유형분류, 음식분류, 조리시간, 분량, 난이도, 이미지URL FROM recipeInfo WHERE RECIPE_ID IN {tuple(top3)};"    
            rows = run_query(query)
            tf=False
        
        elif rows[0][0] is not None:
            # user가 좋아하는 레시피
            rows2 = [i[0] for i in rows][0].split(';') #['180344', '195428', '120476']
        # recipe_ids = ",".join([f'{id_}' for id_ in rows2]) #rows2 리스트의 요소들 빼서 '' 붙이기
            query3 = f"SELECT RECIPE_ID,RECIPE_NM, RECIPE_INFO, 유형분류, 음식분류, 조리시간, 분량, 난이도, 이미지URL FROM recipeInfo WHERE RECIPE_ID IN {tuple(rows2)};"    
            rows = run_query(query3)
            tf=True
    

        ourFavor=[]
        col=['RECIPE_ID','RECIPE_NM', 'RECIPE_INFO', '유형분류', '음식분류', '조리시간', '분량','난이도', '이미지URL']
        for row in rows:
            tmp={}
            for idx,c in enumerate(col):
                tmp[c]=row[idx]
            ourFavor.append(tmp)
        return tf,ourFavor
    

    def randomFood(self,rows) : #오늘의 메뉴
        randomResult=[]
        col=['RECIPE_ID','RECIPE_NM', 'RECIPE_INFO', '유형분류', '음식분류', '조리시간', '분량','난이도', '이미지URL']
        for row in rows:
            tmp={}
            for idx,c in enumerate(col):
                tmp[c]=row[idx]
            randomResult.append(tmp)
        return randomResult
    
    def searchFood(self,foodcategory1,foodcategory2,cook_time,difficulty): #요리 검색
        query = f"select RECIPE_ID,RECIPE_NM, RECIPE_INFO, 유형분류, 음식분류, 조리시간, 분량, 난이도, 이미지URL from recipeInfo where 유형분류 = '{foodcategory1}' and 음식분류 = '{foodcategory2}' and 조리시간 <= {int(cook_time.split('분')[0])} and 난이도 = '{difficulty}';"   
        rows = run_query(query)
        if not rows :
            st.write('')
            st.markdown("<h6>해당 조건에 맞는 검색 결과가 없습니다. 😥</h6>", unsafe_allow_html=True) #1
        elif rows :
            st.write('')
            st.markdown(f"<h6>🔎 {foodcategory1}-{foodcategory2} 검색결과 : {len(rows)}건</h6>", unsafe_allow_html=True) #항목별로 건수 보여주기 
            searchResult=[]
            col=['RECIPE_ID','RECIPE_NM', 'RECIPE_INFO', '유형분류', '음식분류', '조리시간', '분량','난이도', '이미지URL']
            for row in rows:
                tmp={}
                for idx,c in enumerate(col):
                    tmp[c]=row[idx]
                searchResult.append(tmp)
            return searchResult


    def showFoodList(self,foodList):
        for idx,item in enumerate(foodList):
            st.markdown('----')
            col1,col2=st.columns([0.4,0.7])
            with col1:
                st.write('')
                r = requests.get(item['이미지URL'])
                img = Image.open(io.BytesIO(r.content)).resize((225, 225), Image.ANTIALIAS)
                st.image(img,use_column_width=True)
            with col2:
                st.markdown(f"<h3>{item['RECIPE_NM']} </h3>",unsafe_allow_html=True)
                st.info(f"{item['RECIPE_INFO']}",icon='👩‍🍳')
                cc1,cc2,cc3,cc4,cc5 = st.columns(5)
                with cc1:
                    st.markdown(f'<span style="font-weight: bold;">분량</span>', unsafe_allow_html=True)
                    st.write(f'{amount_to_emoji[item["분량"]]} {item["분량"]}')
                with cc2 :
                    st.write('')
                with cc3 :
                    st.markdown(f'<span style="font-weight: bold;">난이도</span>', unsafe_allow_html=True)
                    st.write(difficulty_to_star[item['난이도']])
                with cc4 : 
                    st.write('')
                with cc5:
                    st.markdown(f'<span style="font-weight: bold;">조리시간</span>', unsafe_allow_html=True)
                    st.write(f'⏰ {item["조리시간"]}')
                code=item['RECIPE_ID']
                click=st.button("상세보기", key='detailBtn'+str(idx),use_container_width=True,on_click=self.getDetail,args=(code,))
                if click:
                    return True

    def getDetail(self,code):
        st.session_state.code=code
        # return True
    

class rfg():
    def get_userRfg(self):
        rows=run_query(f"select itemName,expiryDate,itemNum,id from userRfg where userId = '{st.session_state.login_id}'")
        userRfg=[{'itemName':row[0],'expiryDate':row[1],'itemNum':row[2],'id':row[3]} for row in rows]
        st.session_state.userRfg=userRfg
        return userRfg

    def delItem(self,id):
        run_query(f"delete from userRfg where userId = '{st.session_state.login_id}' and id = {id};")
        self.get_userRfg()


    def getMyIngred(self):
        rows=run_query(f"select IRDNT_NM from ingred")
        ingred=[row[0] for row in rows]
        return ingred

    def addIngred(self,itemName,expiryDate,itemNum):
        run_query(f"insert into userRfg(itemName,expiryDate,itemNum,userId) values('{itemName}','{expiryDate}','{itemNum}','{st.session_state.login_id}')")
        self.get_userRfg()

    def modIngred(self,moditemNum,mod_ex,moditem):
        run_query(f"UPDATE userRfg SET itemNum='{moditemNum}',expiryDate='{mod_ex}' where userId = '{st.session_state.login_id}' and id = {moditem['id']};")
        self.get_userRfg()

    def searchFood(self,ingred):
        if len(ingred) > 1 :
            rows= run_query(f"select RECIPE_ID,IRDNT_NM from recipeIngred where IRDNT_NM in {tuple(ingred)};")
        else:
            rows= run_query(f"select RECIPE_ID,IRDNT_NM from recipeIngred where IRDNT_NM = '{ingred[0]}';")
        rows=list(set(rows))
        tmp=[row[0] for row in rows]
        freq = Counter(tmp)
        freq=sorted(freq.items(), key = lambda x: x[1],reverse=True)[:10]
        freq=[ x[0] for x in freq if x[1]==len(ingred)]
        result={x:[] for x in freq}
        for row in rows:
            if row[0] in freq:
                result[row[0]].append(row[1])
        searchResult=[]
        col=['RECIPE_ID','RECIPE_NM', 'RECIPE_INFO', '유형분류', '음식분류', '조리시간', '분량','난이도', '이미지URL']
        for food in list(result.keys()):
            query = f"select RECIPE_ID,RECIPE_NM, RECIPE_INFO, 유형분류, 음식분류, 조리시간, 분량, 난이도, 이미지URL from recipeInfo where RECIPE_ID = {food};" 
            rows=run_query(query)
            row=rows[0]
            tmp={}
            for idx,c in enumerate(col):
                tmp[c]=row[idx]
            searchResult.append(tmp)
        return searchResult


        # query = f"select RECIPE_ID,RECIPE_NM, RECIPE_INFO, 유형분류, 음식분류, 조리시간, 분량, 난이도, 이미지URL from recipeInfo where RECIPE_ID inv{list(result.keys())};"   
        # rows = run_query(query)
        # if not rows :
        #     st.write('')
        #     st.markdown("<h6>해당 조건에 맞는 검색 결과가 없습니다. 😥</h6>", unsafe_allow_html=True) #1
        # elif rows :
        #     st.write('')
        #     searchResult=[]
        #     col=['RECIPE_ID','RECIPE_NM', 'RECIPE_INFO', '유형분류', '음식분류', '조리시간', '분량','난이도', '이미지URL']
        #     for row in rows:
        #         tmp={}
        #         for idx,c in enumerate(col):
        #             tmp[c]=row[idx]
        #         searchResult.append(tmp)
        #     return searchResult
  

