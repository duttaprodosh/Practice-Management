from flask import Flask

from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root:root@localhost/baseballdb'
db = SQLAlchemy(app)



from app import routes, models
#login = LoginManager(app)

if __name__  == '__main__':
    app.run(debug=True)












