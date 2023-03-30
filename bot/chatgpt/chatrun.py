import io,shutil
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from urllib.parse import quote
import urllib

import openai
import json
import os

# 获取 api
def get_api_key():
    return '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'


openai.api_key = get_api_key()

class ChatGPT:
    def __init__(self, user):
        self.user = user
        self.messages = [{"role": "system", "content": "一个有10年Python开发经验的资深算法工程师"}]
        self.filename = "user_messages.md"

    def ask_gpt(self):
        # q = "用python实现：提示手动输入3个不同的3位数区间，输入结束后计算这3个区间的交集，并输出结果区间"
        rsp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        return rsp.get("choices")[0]["message"]["content"]

    def writeTojson(self, line):
        try:
            # 判断文件是否存在
            if not os.path.exists(self.filename):
                with open(self.filename, "w") as f:
                    # 创建文件
                    pass
            with open(self.filename, 'a+') as f:
                f.writelines(line + "\n")

        except Exception as e:
            print(f"错误代码：{e}")

chat = ChatGPT('ives')


def f_query(q):
    global chat
    # 提问
    chat.writeTojson(f"##【{chat.user}】" + q)

    # 逻辑判断
    if q == "0":
        print("*********退出程序**********")
        return 'ok'
        
    elif q == "1":
        print("**************************")
        print("*********重置对话**********")
        print("**************************")
        chat = ChatGPT('ives')
        return 'ok'

    # 提问-回答-记录
    chat.messages.append({"role": "user", "content": q})
    answer = chat.ask_gpt()
    out = f"【ChatGPT】{answer}"
    print(out)
    chat.writeTojson(out)
    chat.messages.append({"role": "assistant", "content": answer})

    # 限制对话次数
    if len(chat.messages) >= 11:
        print("******************************")
        print("*********强制重置对话**********")
        print("******************************")
        # 写入之前信息
        # chat.writeTojson()
        chat = ChatGPT('ives')

    return answer
        

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        query = query_params.get('query', [None])[0]
        try:
            result = f_query(query)
        except Exception as e:
            result = str(e)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        message = str(result)
        self.wfile.write(bytes(message, "utf8"))
        return
    
    def do_POST(self):
        # mpath, margs = urllib.splitquery(self.path)
        datas = self.rfile.read(int(self.headers['content-length']))
        datas = json.loads(datas)
        print(datas)
        query = datas['q']
        try:
            result = '中国' # result = f_query(q):
        except Exception as e:
            result = str(e)
        self.outputtxt(result)
        return

    def outputtxt(self, content):
        # 指定返回编码
        enc = "UTF-8"
        content = content.encode(enc)
        f = io.BytesIO()
        f.write(content)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)



def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port %d...' % server_address[1])
    httpd.serve_forever()





if __name__ == '__main__':
    #curl http://localhost:8000/?query='你好'
    run()
