# chef_project

'농림수산식품교육문화정보원' 공공데이터를 활용하여 사용자에게 요리 레시피를 알력주는 웹 입니다. 

음식 종류, 조리시간, 난이도 별 레시피 검색이 가능하며 개인별 냉장고 관리기능을 추가하여 보유한 재료들로 가능한 레시피를 추천해드립니다.

## 💡 아이디어 도출배경
* 항상 메뉴를 정하지 못하는 사람들에게 메뉴를 추천
* 먹고 싶은 음식 종류 , 조리 가능한 시간, 난이도 별로 레시피 검색 가능
* 개인별 냉장고 재료를 등록해두면 보유한 재료들로 가능한 레시피 추천
* 냉장고 내 재료들의 수량 및 유통기한 관리

## ⭐ 주요 기능
* 제철 메뉴 및 사용자가 평소에 담아둔 레시피 제공
* 조건에 맞는 레시피 추천
* 오늘의 메뉴 랜덤 추천
* 나의 냉장고 속 재료들의 수량 및 유통기한 관리 기능 제공

## 🔎 활용 데이터
농림수산식품교육문화정보원 공공데이터 포털 오픈 API 이용 

  * __제철 농산물 상세정보 (seosonal_menu)__ : 제철 음식 추천에 필요한 제철 농산물 데이터
  * __레시피 기본 정보 (recipeInfo)__ : 음식별 간단한 설명 및 조리시간 / 난이도 / 대표 이미지 등의 데이터
  * __레시피 과정 정보 (recipeProcess)__ : 레시피별 순서와 과정을 담은 데이터
  * __레시피 재료 정보 (recipeIngred)__ : 레시피별 사용되는 재료의 양과 종류 등의 데이터
    * __재료 데이터 (ingred)__ : 이용되는 모든 재료 코드 

## 기술 스택
* Front
  * Streamlit : Python 기반 AIops 도구
* Backend
  * Python, docker, mySQL

## 개발기간
* 2023-04-11 ~ 2023-04-17 (1주)

## 📚 파일 구조

##### 📦chef_project-main

#####  ┣ 📂pages
 
#####  ┃ ┣ 1_모두의 레시피.py
 
#####  ┃ ┗ 2_나의 냉장고.py
 
#####  ┣ foodDetail.py
 
#####  ┣ login.py
 
#####  ┣ MainHome.py
#####  ┗ recipe.py
 
 
 
 
 ## 📑 DB 테이블 구조
 
 #### Docker를 이용한 DB 공유
![image](https://user-images.githubusercontent.com/88521667/232651653-2ffee586-b89f-48f7-bca2-c5825a47a2f3.png)
