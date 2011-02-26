from flask import Flask, request, render_template


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/tasks')
def tasks():
    return render_template('tasks.html')

@app.route('/tasks', methods=['POST'])
def save_tasks():
    print(request.form['inbox'])
    return 'success'

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("terry_turtle.png")


if __name__ == '__main__':
    app.debug = True
    app.run()

