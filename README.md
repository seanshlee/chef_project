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

<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=black"> (Python 기반 AIops 도구)

* Backend

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=black"> <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=MySQL&logoColor=black">

## 📚 파일 구조

##### 📦chef_project-main
 
#####  ┣ MainHome.py : 메인페이지
 
 #####  ┣ 📂pages
 
#####  ┃ ┣ 1_모두의 레시피.py 
 
#####  ┃ ┗ 2_나의 냉장고.py
#####  ┣ foodDetail.py : 음식 세부 조리법 페이지 구현
 
#####  ┣ login.py : 로그인, 회원가입 기능 구현
 
#####  ┗ recipe.py : 여러 페이지를 위한 기능을 클래스 별로 나누어 구현
 
 
 ## 📑 DB 테이블 구조
 
 #### Docker를 이용한 DB 공유
![image](https://user-images.githubusercontent.com/88521667/232651653-2ffee586-b89f-48f7-bca2-c5825a47a2f3.png)


## 개발개요
* 개발 기반 : 2023-04-11 ~ 2023-04-17 (1주)
* 개발 인원 : 3명


## 웹 사이트 시안영상
https://user-images.githubusercontent.com/95599133/232660671-5f589f89-6f03-4cce-9505-683e9396e8bb.mp4
