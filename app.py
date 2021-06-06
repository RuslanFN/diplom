from flask import Flask, render_template, jsonify
import moodle_api
import json

app = Flask(__name__)
moodle_api.URL = "https://eluniver.ugrasu.ru/"
moodle_api.KEY = "07b1af93609c52da25b89b043b456155"
course = moodle_api.call("core_course_get_contents", courseid=8026)
@app.route('/json')
def index2():
    return jsonify(moodle_api.call("mod_assign_get_submissions", assignid=248075))

@app.route('/')
def index():
    return render_template('index.html', content = json.dumps(course, ensure_ascii=False))

@app.route('/assign')
def assign(id):
    return render_template('assign.html', id = id)

if __name__ == "__main__":
    app.run(debug=True)
