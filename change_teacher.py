from playwright.sync_api import BrowserContext

from page_init import init_page


def change_teacher(ctx: BrowserContext, course_id: str) -> None:
    course_page = ctx.new_page()
    init_page(course_page)
    course_page.goto(f"https://lms.ouchn.cn/course/{course_id}/ng#")
    if (
        course_page.locator(".change-teacher").locator("span").inner_text()
        != "辅导老师"
    ):
        course_page.locator(".change-teacher").click()
        course_page.locator(".teacher-list").get_by_text("辅导老师").click()
        course_page.wait_for_timeout(5000)
    course_page.close()
