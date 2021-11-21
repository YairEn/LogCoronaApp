from datetime import datetime, timedelta
from typing import Any

import bcrypt
from flask import g, json, redirect, render_template, request, session, url_for
from LogCorona.exceptions import UserAlreadyExist
from LogCorona.log_corona import (add_peoples_data, add_user, delete_log, get_log_data_by_user_id_and_filter_param,
                                  get_peoples_by_user_id, get_username_data_by_id, get_username_data_by_username,
                                  update_log)
from LogCorona.models import CoronaLog
from LogCorona.utlis import extract_peoples_data
from LogCorona.validators import validate_inputs
from LogCorona import app, db, app_logger


@app.before_request
def before_request() -> None:
    """
    This func activate the database and the global user every request
    :return: None
    """
    try:
        db.connect()
    except Exception as err:
        app_logger.fatal(err)
    g.user = None

    if 'user_id' in session:
        user = get_username_data_by_id(session['user_id'])
        g.user = user


@app.teardown_request
def db_close(exc: Any) -> None:
    """
    This func close the db after every end of request
    :param exc:
    :return: None
    """
    if not db.is_closed():
        try:
            db.close()
        except Exception as err:
            app_logger.fatal(err)


@app.route("/", methods=["GET"])
def home():
    """
    This func is the home route
    :return: home_login page or the index page
    """
    if g.user is not None:
        return render_template("home_login.j2", user_name=g.user.username)
    return render_template("index.j2")


@app.route("/register", methods=["POST", "GET"])
def register():
    """
    This func register the new users to the app
    :return: login or back to the register
    """
    if request.method == "POST":
        first_name = request.form['registerFirstName'].strip()
        last_name = request.form['registerLastName'].strip()
        username = request.form['registerUsername'].strip()
        password = request.form['registerPassword'].strip()

        if validate_inputs(first_name, last_name, username, password):
            result = 'One or more of your inputs is empty Please fill the fields'
            return render_template('register.j2', result=result)
        else:
            try:
                add_user(first_name, last_name, username, password)
            except UserAlreadyExist as err:
                app_logger.warning(err.msg)
                return render_template('register.j2', result=err.msg)
            else:
                app_logger.info('New user added')
                return redirect(url_for('login'))
    else:
        return render_template('register.j2')


@app.route('/login', methods=["POST", "GET"])
def login():
    """
    This func login the users to the app
    :return: login page is the users unauthorized to enter or log_corona_main page instead
    """
    if request.method == "POST":
        username = request.form['loginUsername'].strip().encode('utf-8')
        password = request.form['loginPassword'].strip().encode('utf-8')

        if validate_inputs(username, password):
            msg = 'Username or password are empty'
            return render_template('login.j2', msg=msg)
        else:
            session.pop('user_id', None)

            user = get_username_data_by_username(username)
            if user is not None:
                if bcrypt.checkpw(password, user.password.encode('utf-8')):
                    session['user_id'] = user.user_id
                    peoples = json.dumps(get_peoples_by_user_id(user.user_id))
                    app_logger.info('User logged in')
                    return redirect(url_for('log_corona_main', people=peoples))
            msg = 'Username or password are incorrect'
            return render_template('login.j2', msg=msg)
    return render_template('login.j2')


@app.route('/log_corona_main', methods=["POST", "GET"])
def log_corona_main():
    """
    This func it is the main page that add new logs to the db
    :return: home page or current pagei
    """
    if g.user is not None:
        if request.method == "POST":
            first_name = request.form['first_name'].strip()
            last_name = request.form['last_name'].strip()
            location = request.form['location'].strip()
            comment = request.form['comment'].strip()

            if validate_inputs(first_name):
                return render_template('log_corona_main.j2')
            else:
                add_peoples_data(g.user.user_id, first_name, last_name, location, comment)
                log_data = get_log_data_by_user_id_and_filter_param(g.user.user_id, CoronaLog.create_date > (
                        datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'))

                return render_template('log_corona_main.j2', log_data=log_data)
        log_data = []
        return render_template('log_corona_main.j2', log_data=log_data)
    return redirect(url_for('home'))


@app.route('/logout', methods=["GET"])
def logout():
    """
    This func logout the user and delete the user from the g object
    :return: home page
    """
    if g.user is not None:
        session['user_id'] = None
    return redirect(url_for('home'))


@app.route('/stat', methods=["POST", "GET"])
def stat():
    """
    This func show the status of the logs to the user
    and provide delete and update logs option
    :return: no_stat page(page_without logs), current_page, and home page
    """
    if g.user is not None:
        if request.method == "POST":
            peoples_data, ids_to_work_on = extract_peoples_data(dict(request.form))
            if peoples_data.get('Delete'):
                for log_id in ids_to_work_on:
                    delete_log(log_id)
            else:
                for log_id in ids_to_work_on:
                    update_log(log_id, peoples_data.get(log_id))

        logs_data = get_log_data_by_user_id_and_filter_param(g.user.user_id)
        if len(logs_data) == 0:
            return render_template('stat_no_data.j2')
        return render_template('stat.j2', logs_data=logs_data)
    return redirect(url_for("home"))
