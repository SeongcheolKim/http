# 자동 댓글 작성봇(특정 사이트 한정)
특정 사이트의 원하는 게시글에 자동으로 댓글을 작성
## requirements
python\
asyncio\
playwright
## 사용방법
test.py의 main 함수에 url과 article_no를 입력하여 python 으로 실행
## 개선점
1. 실행 프로그램으로 변환
2. 각 인스턴스 별로 추천 버튼을 눌렀을 때 추천 수가 정상적으로 작동하게 변경(현재 여러 인스턴스여도 추천에 제약이 발생)
