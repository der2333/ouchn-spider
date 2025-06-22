import json
import logging
import requests

logging.basicConfig(level=logging.INFO)


def send_request(cookie: str, course_id: str) -> None:
    base_url = f"https://lms.ouchn.cn/api/course/{course_id}/score/export/excel"
    params = {
        "column": "only",
        "conditions": json.dumps(
            {  # 将字典转换为 JSON 字符串
                "org_ids": [],
                "grade_ids": [],
                "class_ids": [],
                "section_ids": [],
                "keyword": "",
                "department_ids": [],
            }
        ),
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    }

    # 发送 GET 请求
    response = requests.get(base_url, params=params, headers=headers)

    # 检查响应
    if response.status_code == 200:
        logging.info("请求成功")
    else:
        print(f"请求失败，状态码：{response.status_code}")
        logging.error(response.text)  # 查看错误信息
