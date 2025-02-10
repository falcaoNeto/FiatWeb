from flask import Flask
from routes.cliente_route import cliente_route
from routes.filho_route import filho_route
from routes.home_route import home_route
from routes.login_route import login_route
from routes.carro_route import carro_route
from dotenv import load_dotenv
import os
from datetime import timedelta
load_dotenv()

SECRET_KEY_SESSION = os.getenv('SECRET_KEY_SESSION')



app = Flask(__name__)
app.secret_key = SECRET_KEY_SESSION

app.config["SESSION_PERMANENT"] = False 
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=15)

app.register_blueprint(login_route)
app.register_blueprint(home_route)
app.register_blueprint(cliente_route)
app.register_blueprint(filho_route)
app.register_blueprint(carro_route)



if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

