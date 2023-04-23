# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 16:44:45 2020
laptop backend involving rule engine
@author: 77433
"""
from backend import *
from flask import Flask, Response, request
import json
import sqlite3 as sql
# from url_explain import main_op
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

    for i in req.keys():
        try:
            a = int(req[i])
            final.append(a)
        except:
            final.append(req[i])
    print(final)

    job = [i for i in range(0, 17364)]

    # telecommuting,country,Type,experience,education,function,mbti
    ideal = SelectionIdeal(job, final)
    print("len(ideal)", len(ideal))

    suitable = SelectionSuitable(job, final)
    print("len(suitable)", len(suitable))

    ideal_job = random.choice(ideal)
    suitable_job = random.choice(suitable)
    print(ideal_job, suitable_job)

    resp = []
    resp.append(title[ideal_job])
    resp.append(MBTI_comment(ideal_job, final)[0])
    resp.append(description(final[5]))

    resp.append(title[suitable_job])
    resp.append(MBTI_comment(ideal_job, final)[1])
    resp.append(MBTI_comment(ideal_job, final)[2])

    print(resp)

    return Response(json.dumps(resp), status=200, content_type="application/json")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
