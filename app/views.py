#-*- coding: utf-8 -*-
#!E:\python\python.exe


from flask import render_template, Flask, redirect, flash, session, request, make_response
from app import app
from .forms import LoginForm
from .redis_model import CRedis
from .python_db   import *
import json
import sys
import time


@app.route('/', methods = ['GET', 'POST'])
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    redis_model = CRedis()

    user = redis_model.get('user')
    if not user:
        sys.exit()    


    user_array = json.loads(user)
    
    #如果session有值得话
    if request.cookies.get('username') == 'zhang':
        return redirect('/index')

    #登录成功后
    if form.validate_on_submit():
          
        if (user_array.get('username') == request.form['username']) and (user_array.get('password') == request.form['password']):

            session['username'] = request.form['username']
            redis_model.set(request.form['username'],request.form['username'])  

            response = make_response(redirect('/list_log'))
            response.set_cookie('username',request.form.get("username"))
       
            return response
        else:
            str = '登录失败'
            flash(str.decode('utf8'))
            return redirect('/login')
  
    html = make_response(render_template('login.html',
        title = 'Sign In',
        form = form))
    
    return html


@app.route('/index')
def index():

    redis_model = CRedis()
    username = redis_model.get('zhang')
    return 'Hello,%s'% username


@app.route('/list_log')
def list_log():

    limit_num = request.args.get('limit_num','')
    id        = request.args.get('id','')
    today_num  = request.args.get('today_num',1)
  
    
    if id:
        where_sql = {'id':id}
    else:
        where_sql = {}

    if today_num:
        previous = (int(today_num) -  1) * 10
    else:
        previous = 0



    if limit_num:
        limit_sql = str(previous)+','+str(limit_num)
    else :
        limit_sql = str(previous)+',10'

    mysql_model = LinkMysql()
    accept_list = mysql_model._select('sos_api_accept_log','*',where_sql,' id desc ',limit_sql)
    if accept_list:
        for_list = list(accept_list)
        for k,i in enumerate(for_list):
       
            for_list[k] = list(for_list[k])
            time_local = 0
            time_local = time.localtime(int(for_list[k][4]))

            if str(for_list[k][5]).find('Android') != -1:
                for_list[k].append(u'安卓')
            elif str(for_list[k][5]).find('iPhone') != -1:
                for_list[k].append(u'苹果')
            else:
                for_list[k].append(u'电脑端')

            for_list[k][4] = time.strftime("%Y-%m-%d %H:%M:%S",time_local)

    
    html = make_response(
		render_template(
		'list.html',
        title = 'Sign In',
        list  = for_list,
        id = id,
        limit_num = limit_num,  
        previous = int(today_num) - 1,
        next     = int(today_num) + 1,
		))
    return html
    
@app.route('/list_log_display')
def list_log_display():

    log_id =  request.args.get('log_id')
    type   =  request.args.get('type')
    mysql_model = LinkMysql()
    accept_list = mysql_model._find('sos_api_accept_log','*',{'id':log_id})
    
    html = make_response(
		render_template(
		'list_log_display.html',
        title = 'Sign In',
        accept_list = accept_list,
        type  = int(type),
		))
    return html



