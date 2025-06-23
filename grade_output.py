from page_init import init_page
from playwright.sync_api import BrowserContext


def grade_output(ctx: BrowserContext, href: str, course_name: str) -> None:
    course_id = href.split("/")[2]
    course_page = ctx.new_page()
    init_page(course_page)
    course_page.goto(f"https://lms.ouchn.cn/course/{course_id}/ng#/score")
    course_page.locator(".ivu-btn.ivu-btn-default").nth(1).hover()
    course_page.locator(".ivu-dropdown-item").first.click()
    with course_page.expect_download() as download_info:
        course_page.locator("a.operation").first.click()

    download = download_info.value
    # 保存文件并指定文件名
    download.save_as(f"./grade/{course_name}.xlsx")  # 明确指定文件名和扩展名

    print(f"成绩已保存: {course_name}.xlsx")
    course_page.close()
