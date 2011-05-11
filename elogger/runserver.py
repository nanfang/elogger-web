from flask.globals import session
from elogger import app
from elogger.database import redis

@app.context_processor
def inject_direction():
    direction=redis.get('direction:'+session['username'])
    return dict(direction=direction)

app.secret_key = 'hello'
app.run(debug=True)

