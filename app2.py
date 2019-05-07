import sys
import subprocess
import socket
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('2.html')

@app.route('/createJobs/', methods=['POST'])
def createJobs():
    host = socket.gethostname()
    print (host)
    ipAddress = request.form.get('ipAddress', 0)
    sportnumber = request.form.get('sportnumber', 0)
    option_val = request.form.get('option_value', 0)
    format_val = request.form.get('format', 0)
    print (ipAddress)
    print (sportnumber)
    print (option_val)


    file = open('job.txt','w')
    file.write('ip_'+ipAddress+'\n')
    file.write('port_'+sportnumber+'\n')
    file.write('mode_'+option_val+'\n')
    file.write('format_'+format_val+'\n')

    #data = {'square': square}
    data = {}
    data = jsonify(data)
    return data


if __name__ == '__main__':
    app.run(debug=True)
