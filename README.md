# 프로젝트 기획

## 프로젝트 개요

| 프로젝트 목적 | 본인만의 레시피를 공유해서 건강한 식탁을 만들기 위함|
| --- | --- |
| 프로젝트 기간 | 5/22 - 6/15 |
| 발표 날짜 | 6/16 |
| 팀명 | 현준 식탁 |
| 주제 | 레시피 공유 웹사이트 |

## 기술 스택

<div align="center">
	<img src="https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=HTML5&logoColor=white"/>
	<img src="https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=CSS3&logoColor=white"/>
	<img src="https://img.shields.io/badge/JAVASCRIPT-F7DF1E?style=for-the-badge&logo=Javascript&logoColor=white"/>
  <img src="https://img.shields.io/badge/TAILWIND CSS-06B6D4?style=for-the-badge&logo=TAILWIND CSS&logoColor=white"/>
  <img src="https://img.shields.io/badge/JQUERY-0769AD?style=for-the-badge&logo=JQUERY&logoColor=white"/>
	<br>
	<img src="https://img.shields.io/badge/DJANGO-092E20?style=for-the-badge&logo=django&logoColor=white">
	<img src="https://img.shields.io/badge/PYTHON-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>
	<br>
  <img src="https://img.shields.io/badge/FIGMA-F24E1E?style=for-the-badge&logo=FIGMA&logoColor=white"/>
</div>

## 개발 역할 분담

| 이름 | 역할 |
| --- | --- |
| [박현준](https://github.com/DT-HYUNJUN) | 조장, FRONT |
| [감수지](https://github.com/SoozieKam) | BACK |
| [김범서](https://github.com/lemon-lime-honey) | BACK |
| [박태양](https://github.com/pty9714) | FULL |
| [한선진](https://github.com/badajinsee) | FRONT |

## 주제 사전 조사 & 분석

[우리의 식탁](https://wtable.co.kr/recipes)

[만개의 레시피](https://www.10000recipe.com/)

[Baking a Moment](https://bakingamoment.com/)

## 서비스 주요 기능

<details>
  <summary> 회원관리 </summary>
  <div>
    - 회원가입
    - 로그인 / 소셜 로그인
    - 로그아웃
    - 회원 프로필
    - 팔로잉
  </div>
</details>

<details>
<summary> 레시피 </summary>
<div>
  - 레시피 별 검색 (이름 , 재료, 조리기구)
  - 날씨 별 레시피 추천
  - 나만의 냉장고 기능 (재료 추가로 레시피 제공)
  - 리뷰 작성 (댓글)
  - 북마크
  - 좋아요
</div>
</details>

<details>
<summary>커뮤니티</summary>
<div>
  - 멀티 이미지 첨부
  - 댓글
  - 좋아요
</div>
</details>

## 모델(Model) 설계 ERD

![ERD](readme_img/ERD.png)

## 화면(Template) 설계

<details>
  <summary>사전 설계</summary>
  <div>
    <img src="readme_img/pre1.png">
    <img src="readme_img/pre2.png">
  </div>
</details>


<details>
  <summary>메인</summary>
  <div>
  <img src="readme_img/index.png">
  </div>
</details>

<details>
<summary>회원가입 / 로그인 / 마이페이지</summary>
<div>
  - 회원가입
  <img src="readme_img/">
  - 로그인
  <img src="readme_img/login.png">
  - 마이페이지
  <img src="readme_img/mypage.png">
</div>
</details>

<details>
<summary>레시피 목록</summary>
<div>
  - 레시피 목록
  <img src="readme_img/recipes.png">
  - 장비별 목록
  <img src="readme_img/equips.png">
</div>
</details>

<details>
<summary>레시피 상세</summary>
<div>
  <img src="readme_img/recipes_detail.png">
</div>
</details>

<details>
<summary>검색</summary>
<div>
  - 검색
  <img src="readme_img/search.png">
  - 키워드로 검색
  <img src="readme_img/search_name.png">
  - 재료로 검색
  <img src="readme_img/search_ingrd.png">
</div>
</details>


<details>
<summary>냉장고</summary>
<div>
  <img src="readme_img/fridge.png">
</div>
</details>

<details>
<summary>커뮤니티</summary>
<div>
  - 목록
  <img src="readme_img/communities.png">
  - 상세
  <img src="readme_img/communities_detail.png">
</div>
</details>