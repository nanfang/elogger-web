from flask import Flask, request, render_template
from flask.helpers import jsonify

from eventlogger.database import redis

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/tasks')
def tasks():
    return render_template('tasks.html', **redis.hgetall('%s:tasks' % _current_user()))

@app.route('/event-log')
def event_log():
    return render_template('event-log.html')

@app.route('/event-log/<int:year>')
def annual_log(year):
    return jsonify(redis.hgetall('%s:event-log:%s' % (_current_user(), year)))

@app.route('/event-log/<int:year>', methods=['POST', 'PUT'])
def save_log(year):
    redis.hset('%s:event-log:%s' % (_current_user(), year), request.form['element_id'], request.form['update_value'])
    return '<pre>' + request.form['update_value'] + '</pre>'

@app.route('/tasks', methods=['POST'])
def save_tasks():
    redis.hmset('%s:tasks' % _current_user(), request.form)
    return ''

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("terry_turtle.png")

def _current_user():
    return 'nanfang'

if __name__ == '__main__':
    app.debug = True
    app.run()

