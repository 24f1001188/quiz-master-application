from flask import Flask,render_template

app=Flask(__name__)

import configuration as configuration
import models as models
import controllers.routes as routes

if __name__=="__main__":
    app.run(debug=True)