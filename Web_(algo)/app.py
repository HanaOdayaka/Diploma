from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import importjson
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
import usage
import ast

app = Flask(__name__)

uploads_dir = '/home/MatasovaV/mysite/static'

p = 0
flo_points = 0
charging_points = 0
watering = 0

url_r = 'https://api.jsonbin.io/v3/b/65ababe5dc746540189730d9'
url_p = 'https://api.jsonbin.io/v3/b/65ababd41f5677401f21c189'
headers = {'X-Access-Key' : '$2a$10$URLCktrLOPS5OTOI4N4GguKYaHHOIfGPSye6ScFo8qTlz1y92UJQm'}


pfile = requests.get(url_p, json=None, headers=headers)

robots_headings = ("Робот", "Батарея", "Задания")
plants_headings = ("Растение", "Состояние")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/robots')
def robots():
    rfile = requests.get(url_r, json=None, headers=headers)
    rdata, pdata = importjson.imports(rfile.text, pfile.text)
    return render_template('robots.html', headings = robots_headings, data = rdata)

@app.route('/plants')
def plants():
    return render_template('plants.html', headings = plants_headings, data = pdata)

@app.route('/planning')
def planning():
    return render_template('planning_naming.html')

@app.route('/plane')
def plane():
    return render_template('planning.html')

@app.route('/plants_coords')
def plants_coords():
    return render_template('plants_coords.html', p=p)

@app.route('/j')
def j():
    return """<html><head>
              <title>Website for OrangePi</title>
              <link rel = "stylesheet" href = "/static/style.css" />
              <link href='https://fonts.googleapis.com/css?family=Raleway' rel='stylesheet'>
              <link rel="shortcut icon" href="{{ url_for('static', filename='favicon.png') }}">
              <body><h1>Monitoring</h1>

              <h2 id="h2">Планирование</h2>
              <div class="id" id="container"></div>
              <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js" type="text/javascript"></script>
              <script>
              var js = jQuery.noConflict();
              var $mainContainer = js("#container");
              const queryString = window.location.search;
              const urlParams = new URLSearchParams(queryString);
              const id = urlParams.get('id')
              document.getElementById("h2").innerHTML = id.toString();
              var newDiv = js('<img src="' + id.toString() + '.png" alt="id" width="500" height="500">');
              $mainContainer.append(newDiv);
              </script>
              </body></html>"""

@app.route('/doc')
def doc():
    return render_template('doc.html')

@app.route('/cont')
def cont():
    return render_template('cont.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/planning_on_map')
def planning_on_map():
    return render_template('planning_on_map.html', p=flo_points)

@app.route('/final_path_planning')
def final_path_planning():
    global charging_points, p, flo_points
    ch = ast.literal_eval(charging_points)[0]
    p1 = ast.literal_eval(p)
    flo1 = ast.literal_eval(flo_points)
    flo1.append(ch)
    path = usage.main(p1, flo1, ch)
    return render_template('final_path_planning.html',p = path,pp=ch,ppp=p1)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    global p
    if request.method == 'POST':

        profile = request.files['file']
        profile.save(os.path.join(uploads_dir, secure_filename(profile.filename)))

        p = request.form['poly_points']
        return

@app.route('/upload2', methods=['POST', 'GET'])
def upload2():
    global flo_points
    if request.method == 'POST':

        profile = request.files['file']
        profile.save(os.path.join(uploads_dir, secure_filename(profile.filename)))

        flo_points = request.form['points']
        return

@app.route('/upload3', methods=['POST', 'GET'])
def upload3():
    global charging_points
    if request.method == 'POST':

        profile = request.files['file']
        profile.save(os.path.join(uploads_dir, secure_filename(profile.filename)))

        charging_points = request.form['ch_points']
        return

@app.route('/upload4', methods=['POST', 'GET'])
def upload4():
    global watering
    if request.method == 'POST':

        watering = request.form['watering']
        return

if __name__ == "__main__":
    app.run(debug = True)
