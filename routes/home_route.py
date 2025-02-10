from flask import Blueprint, session, render_template, redirect, url_for

home_route = Blueprint("home",__name__)

@home_route.route("/Home")
def Home():
    if "id" not in session:
        return redirect(url_for("login.FormLogin"))
    
    return render_template("home.html")

@home_route.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.FormLogin'))


