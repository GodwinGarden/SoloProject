from flask_app import app

from flask_app.controllers import visitors, gardens

if __name__=="__main__":
    app.run(debug=True)