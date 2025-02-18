from flask import Blueprint, redirect, render_template, session, url_for, request, flash
from controller.carroController import CarroController

carro_route = Blueprint("carro",__name__)

@carro_route.route("/FormCadastrarCarro", methods=["GET", "POST"])
def FormCadastrarCarro():   
    if "id" not in session:
        return redirect(url_for("login.FormLogin"))
    
    return render_template("formCadastrarCarro.html")



@carro_route.route("/CadastrarCarro", methods=["POST"])
def CadastrarCarro():
    if "id" not in session:
        return redirect(url_for("login.FormLogin"))
    
    respnse_form = request.form

    controllerCarro = CarroController()
    message = controllerCarro.cadastrar(respnse_form)
    print(message)

    return redirect(url_for("carro.FormCadastrarCarro"))
    
    

@carro_route.route("/ListarCarros", methods=["GET", "POST"])
def ListarCarros():
    if "id" not in session:
        return redirect(url_for("login.FormLogin"))
    
    controllerCarro = CarroController()
    success, message, carros = controllerCarro.ListarCarros()
    
    
    return render_template("ListarCarros.html",  Carros=carros)



@carro_route.route("/DeletarCarro/<int:id>", methods=["GET", "POST"])
def DeletarCarro(id):
    if "id" not in session:
        return redirect(url_for("login.FormLogin"))
    
    controllerCarro = CarroController()
    message = controllerCarro.DeletarCarro(id)
    print(message)
    
    return redirect(url_for("carro.ListarCarros"))

@carro_route.route("/AtualizarCarro/<int:id>", methods=["POST"])
def AtualizarCarro(id):
    if "id" not in session:
        return redirect(url_for("login.FormLogin"))
    
    controllerCarro = CarroController()
    response_form = request.form
    message = controllerCarro.AtualizarCarros(id, response_form)
    print(message)
    return redirect(url_for("carro.ListarCarros"))

@carro_route.route("/FormAtualizarCarro/<int:id>", methods=["GET", "POST"])
def FormAtualizarCarro(id):

    if "id" not in session:
        return redirect(url_for("login.FormLogin"))
    
    controllerCarro = CarroController()
    carro = controllerCarro.VisualizarCarroDados(id)  # Objeto do banco

    return render_template("formAtualizarDados.html", dado=carro)


@carro_route.route("/DeletarDado/<int:id>/", methods=["GET", "POST"])
def DeletarDado(id):
    if "id" not in session:
        return redirect(url_for("login.FormLogin"))
    
    controllerCarro = CarroController()
    message = controllerCarro.DeletarDado(id)
    print(message)
    
    return redirect(url_for("carro.ListarCarros"))


@carro_route.route("/FormCadastrarDado/<int:id>", methods=["GET", "POST"])
def FormCadastrarDado(id):
    if "id" not in session:
        return redirect(url_for("login.FormLogin"))
    
    modelo = request.args.get("modelo")
    
    return render_template("formCadastrarDados.html", id_carro=id, modelo=modelo)


@carro_route.route("/CadastrarDado/<int:id>", methods=["POST"])
def CadastrarDado(id):
    if "id" not in session:
        return redirect(url_for("login.FormLogin"))
    
    respnse_form = request.form
    modelo = request.args.get("modelo")

    controllerCarro = CarroController()
    message = controllerCarro.CadastrarDado(id, modelo, respnse_form)
    print(message)

    return redirect(url_for("carro.ListarCarros"))
