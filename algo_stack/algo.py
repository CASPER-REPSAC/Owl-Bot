import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os

async def crawling(lists, ctx):
    url = "https://www.acmicpc.net/problem/{}"
    check = False
    result = {}

    for num in lists:
        try:
            tmp = int(num)
        except ValueError:
            check = True
            break
    if check:
        return "[!] 숫자만 입력해 주세요."

    for i in range(len(lists)):
        try:
            result[i] = {
                "problem_description" : "",
                "problem_input" : "",
                "problem_output" : "",
                "problem_url" : "",
                "problem_idx" : ""
            }
            res = requests.get(url.format(lists[i]), headers = fakeUserAgent())
            html = BeautifulSoup(res.content, "html.parser")

            result[i]["problem_description"] = html.select('#problem_description')[0].text
            result[i]["problem_input"] = html.select('#problem_input')[0].text
            result[i]["problem_output"] = html.select('#problem_output')[0].text
            result[i]["problem_url"] = url.format(lists[i])
            result[i]["problem_idx"] = lists[i]

        except IndexError:
            check = True
            break
    if check:
        return "[!] 입력한 숫자 중, 존재하지 않는 문제가 있습니다."

    await sendMessage(ctx, "[*] 크롤링 완료.")
    editReadMe(result)
    await sendMessage(ctx, "[*] README.md 파일 수정 완료.")
    createDir(lists, result)
    await sendMessage(ctx, "[*] 문제 폴더 생성 완료.")
    commit()
    await sendMessage(ctx, "[*] commit 완료.")
    await sendMessage(ctx, "[*] 끝~")

def editReadMe(crawling_data):
    f = open("../algorithm-stack/baekjoon/README.md", 'r', encoding='UTF8')
    data = f.read()
    f.close()

    form = """- [date]
    [prob_list]
  - [empty]
    """

    prob_list = ''
    for i in range(len(crawling_data)):
        prob = "- [{}번](https://github.com/CASPER-REPSAC/algorithm-stack/tree/main/baekjoon/{})\n    "
        prob_list += prob.format(crawling_data[i]["problem_idx"], crawling_data[i]["problem_idx"])

    form = form.replace("[prob_list]", prob_list)
    form = form.replace("[date]", datetime.today().strftime("%Y.%m.%d"))
    data = data.replace("- [empty]", form)

    f = open("../algorithm-stack/baekjoon/README.md", 'w', encoding='UTF8')
    f.write(data)
    f.close()

def createDir(lists, crawling_data):
    path = "../algorithm-stack/baekjoon/"

    for i in range(len(lists)):
        try:
            if not os.path.exists(path + lists[i]):
                os.makedirs(path + lists[i])
                f = open(path + lists[i] + "/README.md", 'w', encoding='UTF8')
                data = "# [{}]({})\n\n{}\n\n{}\n\n{}".format(lists[i], crawling_data[i]["problem_url"], crawling_data[i]["problem_description"], crawling_data[i]["problem_input"], crawling_data[i]["problem_output"])
                f.write(data)
                f.close()
        except OSError:
            pass

def commit():
    os.chdir("../algorithm-stack/")
    os.system("git add .")
    os.system("git commit -m \"Add algo problem (Bot)\"")
    os.system("git push origin main")

async def sendMessage(ctx, message):
    await ctx.send(message)

def fakeUserAgent():
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }