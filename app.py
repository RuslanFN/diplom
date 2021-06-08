from flask import Flask, render_template, jsonify, url_for
import moodle_api
import json
import ast

app = Flask(__name__)
moodle_api.URL = "https://eluniver.ugrasu.ru/"
moodle_api.KEY = "07b1af93609c52da25b89b043b456155"
course = moodle_api.call("core_course_get_contents", courseid=8026)
@app.route('/json/courses')
def jsonisator():
    return jsonify(moodle_api.call("core_enrol_get_users_courses", userid=146024))

@app.route('/json/course/<id>')
def jsonisator2(id):
    return jsonify(moodle_api.call("core_course_get_contents", courseid=id))

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
    c = json.dumps(c)
    #print(c)
    c = c.replace(r'\"', '')
    return render_template('course.html', content =c )

@app.route('/assign')
def assign():
    return render_template('assign.html')
@app.route('/')
@app.route('/courses')
def GetCourses():
    courses = moodle_api.call("core_enrol_get_users_courses", userid=146024)
    c = []
    for item in courses:
        item = dict(item)
        del item['summary']
        c.append(item)

    c = json.dumps(c)
    return render_template('courses.html', content=c)

with app.test_request_context():
    print(url_for('GetCourseRes', id=12))

if __name__ == "__main__":
    app.run(debug=True)
