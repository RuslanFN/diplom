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

        response = post(url + '&token=' + moodle_api.KEY)
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
    course = json.dumps(course)
    course = json.loads(course)
    return render_template('course.html',id = id, contents=course )

@app.route('/courses')
def GetCourses():
    userid = (moodle_api.call('core_webservice_get_site_info')['userid'])
    courses = moodle_api.call("core_enrol_get_users_courses", userid=userid)
    courses = json.dumps(courses)
    courses = json.loads(courses)
    return render_template('courses.html', contents=courses)

@app.route('/')
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
        return flask.redirect('/courses')

with app.test_request_context():
    print(os.listdir("static/pdf"))

if __name__ == "__main__":
    app.run(debug=True)
