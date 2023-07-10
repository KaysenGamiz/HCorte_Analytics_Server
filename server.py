from flask import Flask
from routes.cortes_route import cortes_blueprint
from routes.users_route import users_blueprint

# Flask Server
app = Flask(__name__)

app.register_blueprint(cortes_blueprint, url_prefix='/cortes')
app.register_blueprint(users_blueprint, url_prefix='/users')


if __name__ == '__main__':
    app.run(port=7070)
