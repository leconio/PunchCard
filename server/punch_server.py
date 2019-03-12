#!/usr/bin/python3
# encoding:utf-8

import io
import json
import sys
from http.server import HTTPServer, CGIHTTPRequestHandler
from socketserver import ThreadingMixIn
import time
import requests
from requests.auth import HTTPBasicAuth


class ThreadingHttpServer(ThreadingMixIn, HTTPServer):
    """
    多线程
    """
    pass


verifyCode = ""

TODAY = ""


class FDHTTPRequestHandler(CGIHTTPRequestHandler):

    def get_req_code_json(self, content):
        return json.dumps({
            "alert": "",
            "title": content
        })

    def do_POST(self):
        global verifyCode
        global TODAY
        print(self.path)
        if self.path == "/push":
            if time.strftime("%Y-%m-%d", time.localtime()) == TODAY:
                self.html("0")
            else:
                post_data = self.rfile.read(int(self.headers['Content-Length']))
                result = "error"
                try:
                    self.send_push(json.loads(post_data.decode()))
                    result = "push success"
                except EOFError as e:
                    print(e)
                self.html(result)
        elif self.path == "/success":
            post_data = self.rfile.read(int(self.headers['Content-Length'])).decode()
            self.html("msg: " + post_data)
            self.send_push(json.loads(self.get_req_code_json(post_data)))
            TODAY = time.strftime("%Y-%m-%d", time.localtime())
            print("通知客户端 success")
        elif self.path == "/getVerifyCode":
            # 机器请求验证码
            print("getVerifyCode success")
            self.html(verifyCode)
            verifyCode = ""
        elif self.path == "/setVerifyCode":
            # 客户端把验证码发送过来
            post_data = self.rfile.read(int(self.headers['Content-Length']))
            verifyCode = json.loads(post_data.decode())['msg']
            print("setVerifyCode success")
            self.html(json.dumps({"msg": "success"}))

    def send_push(self, content_json):
        push_data = json.dumps({
            'platform': 'all',
            'audience': 'all',
            'notification': {
                "android": content_json
            }
        })
        print(push_data)
        auth = HTTPBasicAuth("04aca7c29259d962c82dc23a", "21cbe7bd0d59b55524775086")
        resp = requests.post("https://api.jpush.cn/v3/push", data=push_data, auth=auth)
        print(resp.text)

    def html(self, content):
        # 指定返回编码
        enc = "UTF-8"
        f = io.BytesIO()
        f.write(content.encode(enc))
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()
        else:
            self.send_response(400)


def test(port, HandlerClass=FDHTTPRequestHandler,
         ServerClass=ThreadingHttpServer, protocol="HTTP/1.0", bind=""):
    server_address = (bind, port)

    HandlerClass.protocol_version = protocol
    with ServerClass(server_address, HandlerClass) as httpd:
        sa = httpd.socket.getsockname()
        serve_message = "Serving HTTP on {host} port {port} (http://{host}:{port}/) ..."
        print(serve_message.format(host=sa[0], port=sa[1]))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        test(8000)
    else:
        port = sys.argv[1]
        try:
            port = int(port)
        except ValueError:
            raise ValueError("后边只能跟着端口")
        if port > 65535 or port < 1:
            raise ValueError("端口范围错误，只能在端口区间之中")
        test(port)
