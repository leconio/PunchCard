#!/usr/bin/python3
# encoding:utf-8
import base64
import json
import sys
from io import BytesIO
from time import sleep

import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

screen_size = ('1440', '900')
screen_size2 = (1440, 900)

HOST = "punch.leconio.com"
PORT = 8000

# 0 签到
# other 签退
punch_mode = 0


class Chrome:
    def __init__(self, *args, **kwargs):
        self.browser = None
        self.args = args
        self.kwargs = kwargs
        self.window_size = None

    def get_chrome(self):
        chrome_driver_path = "/Users/spawn/PycharmProjects/PunchCard/chromedriver"
        chrome_option = webdriver.ChromeOptions()
        self.window_size = screen_size
        chrome_option.add_argument('no-sandbox')
        chrome_option.add_argument('--headless')
        # 配置忽略ssl错误
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptSslCerts'] = True
        capabilities['acceptInsecureCerts'] = True
        self.browser = webdriver.Chrome(
            chrome_driver_path,
            chrome_options=chrome_option,
            service_log_path='./chrome.log',
            desired_capabilities=capabilities)

        if self.window_size is not None:
            self.browser.set_window_size(*self.window_size)
        return self.browser


browser = Chrome().get_chrome()
browser.implicitly_wait(10)
browser.get("http://hos.sf-express.com")
login_jsessionid = browser.get_cookie("JSESSIONID")


def get_verify_image():
    browser.execute_script("document.getElementById('username').value = '80002462'")
    browser.execute_script("document.getElementById('password').value = 'Zhangsiwole8'")
    verify_img = browser.find_element_by_class_name("yzmImg")

    browser.save_screenshot('/Users/spawn/PycharmProjects/PunchCard/tmp1.png')
    location = verify_img.location
    size = verify_img.size
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    buffered = BytesIO()
    img = Image.open('/Users/spawn/PycharmProjects/PunchCard/tmp1.png').resize(screen_size2)
    img.save('/Users/spawn/PycharmProjects/PunchCard/tmp2.png', format="PNG")
    img = Image.open('/Users/spawn/PycharmProjects/PunchCard/tmp2.png').crop((left, top, right, bottom))
    img.thumbnail((60, 60))
    img.save(buffered, format="PNG")
    # img.save("test.png", format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def get_req_code_json(img_b64):
    return json.dumps({
        "alert": "新消息来了",
        "title": "^_^",
        "extras": {
            "img": img_b64
        }
    })


def wait_verify_code(content_json):
    result = requests.post("http://%s:%s/push" % (HOST, PORT), content_json).text
    hold = 0  # 100s必须有结果，不然就结束
    if result == "push success":
        while hold < 10:
            code = requests.post("http://%s:%s/getVerifyCode" % (HOST, PORT), content_json).text
            if not code:
                print("hold...")
                hold += 1
                sleep(10)
            else:
                return code
    elif result == "0":
        print("已经执行成功")
        exit(0)
    else:
        raise IOError


def punch():
    browser.execute_script('document.getElementById("inputButton").click()')
    print(requests.post("http://%s:%s/success" % (HOST, PORT), "签到成功".encode('utf-8')).text)


def punch_out():
    browser.execute_script('document.getElementById("outputButton").click()')
    print(requests.post("http://%s:%s/success" % (HOST, PORT), "签退成功".encode('utf-8')).text)


def test():
    try:
        code = wait_verify_code(get_req_code_json(get_verify_image()))
        print("code :" + code)
        browser.execute_script("document.getElementById('verifyCode').value = '%s'" % code)

        locator = (By.ID, 'loginForm')
        WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located(locator))
        browser.execute_script("login()")
        if punch_mode == 0:
            punch()
        else:
            punch_out()
    except requests.exceptions.ConnectionError:
        test()


if __name__ == '__main__':
    punch_mode = len(sys.argv)
    test()
