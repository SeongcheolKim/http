from playwright.async_api import async_playwright
import asyncio

async def auto_reply(instance_number, url, article_no):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = await context.new_page()

        # 1. 주어진 URL로 이동
        await page.goto(url+f"&no={article_no}", wait_until="domcontentloaded", timeout=60000)

        print(f"인스턴스 {instance_number}: 게시글 번호: {article_no}")

        # 4. 동적으로 생성된 ID로 댓글 작성자 이름, 비밀번호, 댓글 입력
        name_field_id = f"#name_{article_no}"
        password_field_id = f"#password_{article_no}"
        memo_field_id = f"#memo_{article_no}"

        # 강제로 클릭하거나 스크롤을 사용하여 필드를 클릭 가능하게 함
        await page.locator(f"#btn_gall_nick_name_x_{article_no}").click(force=True)
        await page.locator(name_field_id).scroll_into_view_if_needed()
        await page.fill(name_field_id, "ㅇㅇ")  # 댓글 작성자 이름
        await page.wait_for_timeout(2000)
        await page.locator(password_field_id).scroll_into_view_if_needed()
        await page.fill(password_field_id, "1111")  # 비밀번호 입력
        await page.wait_for_timeout(2000)
        await page.locator(memo_field_id).scroll_into_view_if_needed()
        await page.fill(memo_field_id, f"test: {instance_number}")  # 댓글 내용 수정
        await page.wait_for_timeout(2000)
        # 등록 버튼 클릭
        await page.locator("button.btn_svc.repley_add").click(force=True)

        # 추천 버튼 클릭 및 팝업 처리 추가
        dialog_message = None
        dialog_event = asyncio.Event()

        async def handle_dialog(dialog):
            nonlocal dialog_message
            dialog_message = dialog.message
            await dialog.accept()
            dialog_event.set()

        page.on("dialog", lambda dialog: asyncio.create_task(handle_dialog(dialog)))

        await page.locator("button.btn_recom_up").click(force=True)

        # 다이얼로그를 기다립니다 (최대 5초)
        try:
            await asyncio.wait_for(dialog_event.wait(), timeout=5.0)
            print(f"인스턴스 {instance_number}: 팝업 메시지: {dialog_message}")
        except asyncio.TimeoutError:
            print(f"인스턴스 {instance_number}: 팝업이 나타나지 않았습니다.")

        # 6. 작업이 완료되었으므로 브라우저를 닫음
        await asyncio.sleep(5)
        await browser.close()

# 메인 함수 수정
async def main():
    # 동시에 실행할 인스턴스 수 설정
    instance_count = 1
    
    # URL과 article_no 설정
    url = "https://gall.dcinside.com/board/view/?id=baseball_ab2"
    article_no = "8675634"  # 예시 값, 실제 사용 시 적절한 값으로 변경해야 함
    
    # 여러 인스턴스를 동시에 실행
    tasks = [auto_reply(i, url, article_no) for i in range(instance_count)]
    await asyncio.gather(*tasks)

# 비동기 실행
asyncio.run(main())
