import streamlit as st
from db_config import Config
# from mysql import connector
from datetime import date, datetime
import time
from recipe import rfg


st.set_page_config(page_title="나의 냉장고", page_icon="🛒",layout='wide')
if 'checktmp' not in st.session_state: st.session_state.checktmp = True
if 'userRfg' not in st.session_state: rfg().get_userRfg()

def delItem(id):
    rfg().delItem(id)

st.markdown(f'<h1 style="background-color:#A7DCDC;border-radius:2%;text-align: center;">오늘은 내가 요리사 👩‍🍳</h1>', unsafe_allow_html=True)
st.markdown(f'<h3 style="background-color:#A7DCDC;border-radius:2%;text-align: center;"> 나의 냉장고 🛒</h3>',unsafe_allow_html=True)

listTabs = ["조회", "추가","수정"]
whitespace = 24
tabs = st.tabs([s.center(whitespace,"\u2001") for s in listTabs])

with tabs[0]:
   userRfg=st.session_state.userRfg
   st.markdown("#### 나의 냉장고 속 재료 🥕")
   if userRfg!=[]:
        today=datetime.now().date()
        for i in range(0,len(userRfg),2):
                item1=userRfg[i]
                try: item2=userRfg[i+1]
                except: item2=''
                col1,col2=st.columns(2)
                with col1:
                    dday='D-'+str(item1['expiryDate']-today).split(' days')[0]
                    dday=dday.replace('--','+').replace('day, 0:00:00','')
                    if item1['expiryDate'] == date(2099,12,31):
                        st.markdown(f"<h4>{item1['itemName']}</h4>", unsafe_allow_html=True)
                        st.info(f"개수 : {item1['itemNum']}개",icon='✅')
                    elif item1['expiryDate'] == today :
                        st.markdown(f"<h4>{item1['itemName']}   D-DAY</h4>", unsafe_allow_html=True)
                        st.error(f"유통기한 : {item1['expiryDate']}  ✅개수 : {item1['itemNum']}개",icon='📆')
                    elif item1['expiryDate'] < today :
                            st.markdown(f"<h4>{item1['itemName']}   {dday}</h4>", unsafe_allow_html=True)
                            st.error(f"유통기한 : {item1['expiryDate']}  ✅개수 : {item1['itemNum']}개",icon='📆')    
                    else:
                        st.markdown(f"<h4>{item1['itemName']}   {dday}</h4>", unsafe_allow_html=True)
                        st.info(f"유통기한 : {item1['expiryDate']}  ✅개수 : {item1['itemNum']}개",icon='📆')

                    st.button('삭제',key='delItemBtn'+str(item1['id']),use_container_width=True,args=(item1['id'],),on_click=delItem)

                with col2:
                    try:
                        dday='D-'+str(item2['expiryDate']-today).split(' days')[0]
                        dday=dday.replace('--','+').replace('day, 0:00:00','')
                        if item2['expiryDate'] == date(2099,12,31):
                            st.markdown(f"<h4>{item2['itemName']}</h4>", unsafe_allow_html=True)
                            st.info(f"{item2['itemNum']}개",icon='✅')
                        elif item2['expiryDate'] == today :
                            st.markdown(f"<h4>{item2['itemName']}   D-DAY</h4>", unsafe_allow_html=True)
                            st.error(f"유통기한 : {item2['expiryDate']}  ✅개수 : {item2['itemNum']}개",icon='📆')
                        elif item2['expiryDate'] < today :
                            st.markdown(f"<h4>{item2['itemName']}   {dday}</h4>", unsafe_allow_html=True)
                            st.error(f"유통기한 : {item2['expiryDate']}  ✅개수 : {item2['itemNum']}개",icon='📆')                           
                        else:
                            st.markdown(f"<h4>{item2['itemName']}   {dday}</h4>", unsafe_allow_html=True)
                            st.info(f"유통기한 : {item2['expiryDate']}  ✅개수 : {item2['itemNum']}개",icon='📆')
                    
                        st.button('삭제',key='delItemBtn'+str(item2['id']),use_container_width=True,args=(item2['id'],),on_click=delItem)
                    except:
                        st.write('')
                st.markdown('----')

   else:
        st.write()
        st.markdown(f"<h3>냉장고가 비어있어요 😥 재료를 추가해주세요! </h3>", unsafe_allow_html=True)
        st.image('https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2F20160810_238%2Fnaolby_1470803155141pMhNE_JPEG%2F12.jpg&type=sc960_832',use_column_width='always')

with tabs[1]:
    st.markdown("#### 재료 추가하기 ➕")
    ingred=rfg().getMyIngred()
    expiryDate=date(2099,12,31)
       
    col1, col2 = st.columns(2)
    with col1:
        itemName=st.selectbox('재료 추가하기',ingred)
    with col2: 
        itemNum = st.number_input("수량",step=1,min_value=1)

    ex_check=st.checkbox('유통기한 있음',value=True)
    if ex_check:
        expiryDate = st.date_input("유통기한")

    submitted = st.button("추가하기",use_container_width=True)
    if submitted:
        rfg().addIngred(itemName,expiryDate,itemNum)
        if expiryDate== date(2099,12,31):
            st.success(f'{itemName} : {itemNum}개 추가되었습니다.',icon='🔔')
        else:
            st.success(f'{itemName} : {itemNum}개 추가되었습니다. (유통기한 : {expiryDate})',icon='🔔')  

        time.sleep(1.5)
        st.experimental_rerun()

with tabs[2]:
    rfg().get_userRfg()
    st.markdown("#### 재료 수정하기 🔧")
    userRfg=st.session_state.userRfg
    ingred=[ row['itemName'] for row in userRfg]    
    if ingred!=[]:
        col1, col2 = st.columns(2)
        itemName=st.selectbox('나의 냉장고 속 재료',ingred)

        for item in userRfg : 
            if item['itemName']==itemName:
                moditem=item
                break

        moditemNum = st.number_input("수량",value=moditem['itemNum'],step=1,min_value=1,key='moditemNum')
        if moditem['expiryDate']==date(2099,12,31):
            ex_check=st.checkbox('유통기한 있음',value=False,key='modCheck1')
            if ex_check:
                mod_ex=st.date_input("유통기한",key='modexpiryDate1')
            else: 
                mod_ex=date(2099,12,31)
        else:
            ex_check=st.checkbox('유통기한 있음',value=True,key='modCheck2')
            if ex_check:
                mod_ex=st.date_input("유통기한",value=moditem['expiryDate'],key='modexpiryDate2')
            else: 
                mod_ex=date(2099,12,31)

        modsubmitted = st.button("수정하기",use_container_width=True,key='modItemBtn')
        if modsubmitted:
            rfg().modIngred(moditemNum,mod_ex,moditem)
            if mod_ex== date(2099,12,31):
                st.success(f'{itemName}의 수량 : {moditemNum}개, 유통기한 : 없음 으로 수정되었습니다.',icon='🔔')
            else:
                st.success(f'{itemName}의 수량 : {moditemNum}개, 유통기한 : {mod_ex} 로 수정되었습니다.',icon='🔔')  

            time.sleep(1.5)
            st.experimental_rerun()

    else:
        st.write()
        st.markdown(f"<h3>냉장고가 비어있어요 😥 재료를 추가해주세요! </h3>", unsafe_allow_html=True)
        st.image('https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2F20160810_238%2Fnaolby_1470803155141pMhNE_JPEG%2F12.jpg&type=sc960_832',use_column_width='always')




    # st.button('수정',key='modItemBtn'+str(item1['id']),use_container_width=True,args=(item1['id'],item1['itemName'],item1['itemNum'],item1['expiryDate'],),on_click=modItem)

    # ex_check=st.checkbox('유통기한 있음',value=True)
    # if ex_check:
    #     expiryDate = st.date_input("유통기한")

    # submitted = st.button("추가하기",use_container_width=True)
    # if submitted:
    #     run_query(f"insert into userRfg(itemName,expiryDate,itemNum,userId) values('{itemName}','{expiryDate}','{itemNum}','{st.session_state.login_id}')")
    #     if ex_check:
    #         st.markdown(f"(유통기한 : {expiryDate})")
    #     st.experimental_rerun() 
        
