from flask import current_app as app
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

mysql = MySQL(cursorclass=DictCursor)
mysql.init_app(app)
nav = [
    {'name': 'Contact Us', 'url': '/contact'},
    {'name': 'Home', 'url': '/index'}
]


@app.route("/")
def home():
    """Landing page."""
    return render_template("home.html",
                           nav=nav,
                           title="Flask Application")


@app.route("/contact")
def contact():
    return render_template("contact.html", nav=nav, title='Flask Application')


@app.route('/index', methods=['GET'])
def index():
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblmlbplayers')
    result = cursor.fetchall()
    return render_template('index.html', nav=nav, title='Flask Application', players=result)


@app.route('/view/<int:player_id>', methods=['GET'])
def record_view(player_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblmlbplayers WHERE id=%s', player_id)
    result = cursor.fetchall()
    return render_template('view.html', nav=nav, title='Flask Application', player=result[0])


@app.route('/edit/<int:player_id>', methods=['GET'])
def form_edit_get(player_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblmlbplayers WHERE id=%s', player_id)
    result = cursor.fetchall()
    return render_template('edit.html', nav=nav, title='Flask Application', player=result[0])


@app.route('/edit/<int:player_id>', methods=['POST'])
def form_update_post(player_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Name'),
                 request.form.get('Team'),
                 request.form.get('Position'),
                 request.form.get('Height'),
                 request.form.get('Weight'),
                 request.form.get('Age'), player_id)
    sql_update_query = """UPDATE tblmlbplayers t SET t.Name = %s, 
    t.Team = %s, t.Position = %s, t.Height = 
    %s, t.Weight = %s, t.Age = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/index", code=302)


@app.route('/players/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', nav=nav, title='Flask Application', )


@app.route('/players/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Name'),
                 request.form.get('Team'),
                 request.form.get('Position'),
                 request.form.get('Height'),
                 request.form.get('Weight'),
                 request.form.get('Age'))
    sql_insert_query = """INSERT INTO 
    tblmlbplayers (Name, Team, Position, Height, Weight, Age) 
    VALUES (%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/index", code=302)


@app.route('/delete/<int:player_id>', methods=['POST'])
def form_delete_post(player_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblmlbplayers WHERE id = %s """
    cursor.execute(sql_delete_query, player_id)
    mysql.get_db().commit()
    return redirect("/index", code=302)


# Get all Data api
@app.route('/api/v1/players', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblmlbplayers')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


# Get Single Data api
@app.route('/api/v1/players/<int:player_id>', methods=['GET'])
def api_retrieve(player_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblmlbplayers WHERE id=%s', player_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


# Edit the Data api
@app.route('/api/v1/players/<int:player_id>', methods=['PUT'])
def api_edit(player_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['Name'], content['Team'], content['Position'],
                 content['Height'], content['Weight'],
                 content['Age'], player_id)
    sql_update_query = """UPDATE tblmlbplayers t SET t.Name = %s, 
    t.Team = %s, t.Position = %s, t.Height = 
    %s, t.Weight = %s, t.Age = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


# Add New Data api
@app.route('/api/v1/players', methods=['POST'])
def api_add() -> str:
    content = request.json
    cursor = mysql.get_db().cursor()
    inputData = (content['Name'], content['Team'], content['Position'],
                 content['Height'], content['Weight'],
                 content['Age'])
    sql_insert_query = """INSERT INTO 
    tblmlbplayers (Name, Team, Position, Height, Weight, Age) 
    VALUES (%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


# Delete the Data api
@app.route('/api/v1/players/<int:player_id>', methods=['DELETE'])
def api_delete(player_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblmlbplayers WHERE id = %s """
    cursor.execute(sql_delete_query, player_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp
