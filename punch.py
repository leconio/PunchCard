#!/usr/bin/python3
# encoding:utf-8
import base64
from time import sleep

import requests
from io import BytesIO
import json

from PIL import Image
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

screen_size = ('1440', '900')
screen_size2 = (1440, 900)


class get_chroem:
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
            # service_log_path='/opt/logs/chrome.log',
            desired_capabilities=capabilities)

        if self.window_size is not None:
            self.browser.set_window_size(*self.window_size)
        return self.browser


browser = get_chroem().get_chrome()
browser.get("http://hos.sf-express.com")
login_jsessionid = browser.get_cookie("JSESSIONID")


def get_verify_image():
    browser.execute_script("document.getElementById('username').value = '80002462'")
    browser.execute_script("document.getElementById('password').value = 'Zhangsiwole6'")
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
    if requests.post("http://lecon.io:8000/push", content_json).text == "push success":
        while True:
            code = requests.post("http://lecon.io:8000/getVerifyCode", content_json).text
            if not code:
                print("hold...")
                sleep(10)
            else:
                return code
    else:
        raise IOError


def punch():
    input_btn = browser.find_element_by_id("inputButton")
    input_btn.click()
    print(requests.post("http://lecon.io:8000/success", input_btn.get_attribute("title").encode('utf-8')).text)


def test():
    code = wait_verify_code(get_req_code_json(get_verify_image()))
    print("code :" + code)
    browser.execute_script("document.getElementById('verifyCode').value = '%s'" % code)
    browser.execute_script("login()")
    punch()


if __name__ == '__main__':
    test()
