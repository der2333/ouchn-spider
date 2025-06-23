import logging
from playwright.sync_api import sync_playwright, Request

from change_teacher import change_teacher
from grade_output import grade_output
from page_init import init_page
from request import send_request

user_cookie = ""


def intercept_request(request: Request) -> None:
    global user_cookie
    # 获取请求头中的Cookie
    if "https://lms.ouchn.cn/api/my-grades" in request.url:
        header = request.all_headers()
        user_cookie = header["cookie"]


def main():
    global user_cookie
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            # executable_path="/Users/fyf/Library/Caches/ms-playwright/chromium-1161/chrome-mac/Chromium.app/Contents/MacOS/Chromium",
            executable_path="C:\\Users\\13388\\AppData\\Local\\ms-playwright\\chromium-1161\\chrome-win\\chrome.exe",
        )
        ctx = browser.new_context(accept_downloads=True)

        # 初始化首页
        index_page = ctx.new_page()
        init_page(index_page)

        index_page.on("request", intercept_request)
        index_page.goto("https://lms.ouchn.cn/user/courses#/")
        index_page.locator("#loginName").fill("79295025@qq.com")
        index_page.locator("#password").fill("he6656852")
        index_page.locator("#agreeCheckBox").click()
        index_page.locator("#form_button").click()

        # 填写用户信息用户
        input("进入课程页面后按回车继续...")

        index_page.locator("#course-role-select_ms").click()
        index_page.locator("#ui-multiselect-3-course-role-select-option-2").click()

        if index_page.locator(".select2-choice").is_visible():
            index_page.locator(".select2-choice").click()
            index_page.locator(".select2-results-dept-0").last.click()
            index_page.wait_for_timeout(3000)

        courses = index_page.locator("a.ng-binding.ng-scope").all()

        # 批量发送导出成绩表的请求
        for course in courses:
            href = course.get_attribute("href")
            if href is None:
                continue
            course_id = href.split("/")[2]
            try:
                change_teacher(ctx, course_id)  # 切换辅导老师
            except Exception:
                pass

            send_request(user_cookie, course_id)

        # 批量下载导出的成绩表
        for course in courses:
            href = course.get_attribute("href")
            if href is None:
                continue
            course_name = course.inner_text()
            try:
                grade_output(ctx, href, course_name)
            except Exception:
                logging.warning(f"下载 {course_name} 成绩表失败")

        # 关闭浏览器
        ctx.close()
        input("结束")


if __name__ == "__main__":
    main()
