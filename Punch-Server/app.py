
from flask import Flask, render_template, request, send_file, send_from_directory, redirect, url_for, make_response, \
                    g, flash, jsonify
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask_restless import APIManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
from flask_mail import Mail
import json
from io import BytesIO
import os
import eventlet
import eventlet.wsgi
import datetime
import sys
#from paginate import *


eventlet.monkey_patch()

app=Flask(__name__)


file_path = os.path.abspath(os.getcwd()) + "\\DATABASE.db"
APP_ROOT= os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SECRET_KEY']='Sskiekg'

db=SQLAlchemy(app)
mail=Mail(app)


class Person(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    phoneserial = db.Column(db.String(60))
    person_name = db.Column(db.String(120))

class TimeChecked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_name = db.Column(db.String(120))
    phoneserial = db.Column(db.String(60))
    time_recorded=db.Column(db.DateTime())
    in_out = db.Column(db.String(120))

class TimeView(ModelView):
    form_columns=['person_name', 'phoneserial', 'in_out','time_recorded']
    can_delete=False
    can_export=True

db_adapter=SQLAlchemyAdapter(db,TimeChecked)
user_manager=UserManager(db_adapter,app)

admin=Admin(app, template_mode='bootstrap3')
admin.add_view(TimeView(TimeChecked, db.session))
admin.add_view(ModelView(Person, db.session))

apimanager=APIManager(app,flask_sqlalchemy_db=db)
apimanager.create_api(TimeChecked, methods=['GET','POST', 'DELETE'])
apimanager.create_api(Person, methods=['GET','POST', 'DELETE'])

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=="POST":
        json_encoded=request.data.decode("utf-8")
        json_data=json.loads(json_encoded)
        phoneserial=json_data['phoneserial']
        person_name=json_data['person_name']
        in_out=json_data['in_out']
    else:
        phoneserial=request.args.get('phoneserial')
        person_name=request.args.get('person_name')
        in_out=request.args.get('in_out')

    time_recorded=datetime.datetime.now()
    person_reg=Person(phoneserial=phoneserial, person_name=person_name)
    db.session.add(person_reg)
    time_in=TimeChecked(phoneserial=phoneserial, person_name=person_name,in_out=in_out,time_recorded=time_recorded)
    db.session.add(time_in)
    db.session.commit()
    return jsonify({'phoneserial':phoneserial, 'in_out': in_out,'time_recorded':time_recorded})



@app.route('/check', methods=['GET','POST'])
def index():
    if request.method=="POST":
        json_encoded=request.data.decode("utf-8")
        json_data=json.loads(json_encoded)
        phoneserial=json_data['phoneserial']
        in_out=json_data['in_out']
        person_name=json_data['person_name']
    else:
        phoneserial=request.args.get('phoneserial')
        in_out=request.args.get('in_out')
        person_name=request.args.get('person_name') 
    time_recorded=datetime.datetime.now()
    time_in=TimeChecked(person_name=person_name,phoneserial=phoneserial, in_out=in_out,time_recorded=time_recorded)
    db.session.add(time_in)
    db.session.commit()
    return jsonify({'person_name':person_name, 'phoneserial':phoneserial, 'in_out': in_out,'time_recorded':timechecked})

@app.route('/search/', defaults={'page':1}, methods=['GET'])
@app.route('/search/<int:page>', methods=['GET'])
def search(page):
    phone_sn=request.args.get('query')
    records=TimeChecked.query.filter(TimeChecked.phoneserial==phone_sn).order_by(TimeChecked.time_recorded.desc()).paginate(page,10)
    return render_template('search.html', records=records, query=phone_sn)


if __name__=='__main__':
    #app.run(debug=True)
    eventlet.wsgi.server(eventlet.listen(('',8400)), app)