import json
import os
import random
import string

import flask
from flask import Flask, render_template, jsonify, request
from requests import post

import moodle_api

app = Flask(__name__)
moodle_api.URL = "https://eluniver.ugrasu.ru/"
#moodle_api.KEY = "07b1af93609c52da25b89b043b456155"
#course = moodle_api.call(" ", courseid=8026)
@app.route('/json/courses/<id>')
def jsonisator(id):
    return jsonify(moodle_api.call("core_enrol_get_users_courses", userid=id))


@app.route('/json/courses2')
def jsonisator3():
    return jsonify(moodle_api.call('core_webservice_get_site_info')['userid'])

@app.route('/json/course/<id>')
def jsonisator2(id):
    return jsonify(moodle_api.call("core_course_get_contents", courseid=id))

@app.route('/pdf',  methods = ['POST'])
def pdf():
    if request.method == 'POST':
        url = request.form.get('link')
        print(url)

        response = post('https://' + url + '&token=' + moodle_api.KEY)
        fileName = ''.join(random.choice(string.ascii_letters) for i in range(10))
        while fileName in os.listdir():
            fileName = ''.join(random.choice(string.ascii_letters) for i in range(10))
        f = open('static/pdf/'+fileName+'.pdf', 'wb')
        f.write(response.content)
        f.close()
    return flask.redirect('/pdfview/' + fileName)

@app.route('/pdfview/<fileName>')
def pdfview(fileName):
    return render_template('viewPDF.html', content=fileName)

@app.route('/course/<id>')
def GetCourseRes(id):
    course = moodle_api.call("core_course_get_contents", courseid=id)
    c = []
    for item in course:
        item = dict(item)
        modules = []
        for item2 in item['modules']:
            item2 = dict(item2)
            del item2['customdata']
            del item2['onclick']
            if 'description' in item2:
                del item2['description']
            modules.append(item2)

        item['modules'] = modules
        print(modules)
        del item['summary']
        c.append(item)
    c = json.dumps(c, ensure_ascii=True)
    #print(c)
    c = c.replace(r'\"', '')
    return render_template('course.html', content =c, id = id )

@app.route('/')
@app.route('/courses')
def GetCourses():

    userid = (moodle_api.call('core_webservice_get_site_info')['userid'])
    courses = moodle_api.call("core_enrol_get_users_courses", userid=userid)
    c = []
    for item in courses:
        item = dict(item)
        del item['summary']
        c.append(item)

    c = json.dumps(c)
    c = c.replace(r'\"', '')
    return render_template('courses.html', content=c)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        print(str(request.form.get('login')))
        print(str(request.form.get('password')))
        response = post(
            'https://eluniver.ugrasu.ru/login/token.php?username=' + str(request.form.get('login')) + '&password=' + str(request.form.get('password')) + '&service=moodle_mobile_app')
        response = response.json()
        print(str(request.form.get('login')))
        print(str(request.form.get('password')))
        if 'token' in response:
            moodle_api.KEY = response['token']
            print(response['token'])
        else:
            print(response)
            return '<h1>'+ response['error'] + '</h1>'
        return GetCourses()

with app.test_request_context():
    print(os.listdir("static/pdf"))

if __name__ == "__main__":
    app.run(debug=True)
