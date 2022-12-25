from flask import Flask 
from flask import render_template
from flask import request

from bots import Bot1
from students import Student
from dataVisualizers import dataVisualizer

from datetime import date

app = Flask(__name__)

@app.route('/')
def index():
    try:
        username = request.args['u']
        password = request.args['p']
        today = request.args['t'] == "true"

        userData = {
            'uid': username,
            'pwd': password
        }

        bot1 = Bot1(userData = userData)
        bot1.checkInternet()
        bot1.getVitalData()
        bot1.makeLogin()
        bot1.getAttendanceURL()
        
        if today:
            today = date.today().strftime(r"%d-%m-%Y")
            student1 = Student(rawData = bot1.getAttendanceRD(fDate = today, tDate = today))            
        else:
            student1 = Student(rawData = bot1.getAttendanceRD())
    except KeyError as ke:
        return "<h1>Got Error</h1><h1>Argument <i>{arg}</i> Missing</h1>".format(arg = ke.args[0]), 404
    except Exception as exp:
        return "<h1>Got Error</h1><h1><i>{msg}</i></h1>".format(msg = exp), 404

    return render_template('attTable.html', student = student1)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000, debug = True)