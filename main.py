import os
import requests

USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 "
    + "(KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"
)


def login():
    """使用账号密码登陆 NSSCTF"""
    resp = requests.post(
        "https://www.nssctf.cn/api/user/login/",
        headers={"User-Agent": USER_AGENT},
        data={
            "username": os.environ["NSSCTF_USERNAME"],
            "password": os.environ["NSSCTF_PASSWORD"],
        },
    )
    cookies = dict(resp.cookies)
    cookies["token"] = resp.json()["data"]["token"]
    return cookies


def get_coin_num(cookies):
    """获取金币数量"""
    resp = requests.get(
        "https://www.nssctf.cn/api/user/info/opt/setting/",
        headers={"User-Agent": USER_AGENT},
        cookies=cookies,
    )
    data = resp.json()
    if data["code"] != 200:
        return None
    return data.get("data", {}).get("coin", None)


def main():
    cookies = login()
    coin_num = get_coin_num(cookies)
    if coin_num is None:
        print("签到失败")
    else:
        print(f"签到成功，当前金币数量为 {coin_num}")


if __name__ == "__main__":
    main()
