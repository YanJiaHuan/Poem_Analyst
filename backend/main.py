# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 16:44:45 2020
laptop backend involving rule engine
@author: 77433
"""
# from backend import *
from flask import Flask, Response, request
import json
# import sqlite3 as sql
#from url_explain import main_op
from flask_cors import *  # 跨域支持
app = Flask(__name__)
CORS(app)

job = [i for i in range(0, 17364)]


@app.route('/', methods=['POST', 'GET'])
def respond():
    req = request.form
    print(req)
    req = req.to_dict()
    print(req)
    final = []

    # for i in req.keys():
    #     try:
    #         a = int(req[i])
    #         final.append(a)
    #     except:
    #         final.append(req[i])
    # print(final)

    # job = [i for i in range(0, 17364)]

    # # telecommuting,country,Type,experience,education,function,mbti
    # ideal = SelectionIdeal(job, final)
    # print("len(ideal)", len(ideal))

    # suitable = SelectionSuitable(job, final)
    # print("len(suitable)", len(suitable))

    # ideal_job = random.choice(ideal)
    # suitable_job = random.choice(suitable)
    # print(ideal_job, suitable_job)

    # resp = []
    # resp.append(title[ideal_job])
    # resp.append(MBTI_comment(ideal_job, final)[0])
    # resp.append(description(final[5]))

    # resp.append(title[suitable_job])
    # resp.append(MBTI_comment(ideal_job, final)[1])
    # resp.append(MBTI_comment(ideal_job, final)[2])

    resp = []
    # 刘郎去，阮郎行，惆怅恨难平。
    resp_1 = trans(req)
    resp_2 = allusion1(req)
    resp_3 = allusion2(req)

    # 秦州刺史窦滔妻，彭城令苏道之女，有才学，织锦制回文诗，以赎夫罪。
    # resp_1 = [
    #     '秦 州 刺 史 窦 禹 的 妻 子 ， 彭 城 县 令 苏 道 之 女 有 才 智 。 织 锦 制 成 回 文 诗 写 赠 送 夫 人 以 赎 其 罪 。']
    # resp_2 = ['Allusion 1: 织锦    0.97', 'Allusion 2: 关关    0.661', 'Allusion 3: 挑锦字    0.64', 'Allusion 4: 锦荐    0.639', 'Allusion 5: 锦筵    0.563',
    #           'Allusion 6: 特地    0.472', 'Allusion 7: 拌（pan1）    0.454', 'Allusion 8: 越南    0.421', 'Allusion 9: 故故    0.417', 'Allusion 10: 醮坛    0.41']
    # resp_3 = ['1. Allusions: 织锦',
    #           '2. Background and meaning: 织锦(zhī iin) literally means "weaving brocade". It is an allusion to an ancient story about a woman named zhuo wenjun, who was skilled in weavina brocade. In the storv. she was forced to marrv a man she did not love. but she expressed her emotions through her poetry and brocade weaving. The phrase 织锦 is often used in poetry to describe the intricate and beautiful weaving of emotions and thoughts into the fabric of the verse.']

    for i in range(0, len(resp_1)):
        resp.append(resp_1[i])
    for i in range(0, len(resp_3)):
        resp_3_temp = resp_3[i].split(":", 1)
        # print(resp_3_temp)
        resp.append(resp_3_temp[1])
    for i in range(0, len(resp_2)):
        resp.append(resp_2[i])

    print(resp)

    return Response(json.dumps(resp), status=200, content_type="application/json")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
