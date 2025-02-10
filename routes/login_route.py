from controller.loginController import LoginController
from flask import Blueprint, redirect, request, render_template, url_for, flash

login_route = Blueprint("login",__name__)

@login_route.route('/', methods= ["GET"])
def FormLogin():  
    return render_template("FormLogin.html")    

       
@login_route.route('/Login', methods=["POST", "GET"])
def Login():
    controllerLogin = LoginController()
    if request.method == "POST":
        dados = request.form
        success, response  = controllerLogin.Verificar_Login(dados)   

        if not success:
            flash(response, "login")
            return redirect(url_for("login.FormLogin"))

        return redirect(url_for("home.Home"))   

    return redirect(url_for("login.FormLogin"))
