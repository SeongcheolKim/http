from playwright.sync_api import sync_playwright

def auto_reply_to_first_post():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = context.new_page()

        # 1. 게시글 리스트 페이지로 이동
        page.goto("https://gall.dcinside.com/board/lists/?id=baseball_ab2", wait_until="domcontentloaded", timeout=60000)

        # 2. 첫 번째 게시글 클릭
        first_post_selector = "tr.ub-content.us-post td.gall_tit.ub-word a"
        page.wait_for_selector(first_post_selector)
        page.click(first_post_selector)

        # 3. 게시글의 댓글 섹션에서 data-article-no 속성으로 동적 ID 찾기
        page.wait_for_selector("div.view_comment")
        article_no = page.get_attribute("div.view_comment div.comment_wrap", "data-article-no")

        if article_no is None:
            print("data-article-no를 찾을 수 없습니다.")
            return

        print(f"게시글 번호: {article_no}")

        # 4. 동적으로 생성된 ID로 댓글 작성자 이름, 비밀번호, 댓글 입력
        name_field_id = f"#name_{article_no}"
        password_field_id = f"#password_{article_no}"
        memo_field_id = f"#memo_{article_no}"

        # 강제로 클릭하거나 스크롤을 사용하여 필드를 클릭 가능하게 함
        page.locator(f"#btn_gall_nick_name_x_{article_no}").click(force=True)
        for i in range(5):
            page.locator(name_field_id).scroll_into_view_if_needed()
            page.fill(name_field_id, "ㅇㅇ")  # 댓글 작성자 이름
            page.wait_for_timeout(2000)
            page.locator(password_field_id).scroll_into_view_if_needed()
            page.fill(password_field_id, "1111")  # 비밀번호 입력
            page.wait_for_timeout(2000)
            page.locator(memo_field_id).scroll_into_view_if_needed()
            page.fill(memo_field_id, f"{i+1}")  # 댓글 내용 입력
            page.wait_for_timeout(2000)
            # 등록 버튼 클릭
            page.locator("button.btn_svc.repley_add").click(force=True)

        # 6. 작업이 완료되었으므로 브라우저를 닫음
        page.wait_for_timeout(5000)
        browser.close()

# 함수 실행
auto_reply_to_first_post()
