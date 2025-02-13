from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from controller.filhoController import FilhoController

filho_route = Blueprint("filho",__name__)


@filho_route.route("/FormCadastrarFilho/<int:id>",methods=["POST", "GET"])
def FormCadastrarFilho(id):
    if "id" not in session:
        return redirect(url_for("login.FormLogin"))
    
    return render_template("formCadastrarFilhos.html", id_cliente=id)
    

@filho_route.route("/CadastrarFilho/<int:id>", methods=["POST", "GET"])
def CadastrarFilho(id):
    controllerFilho = FilhoController()
    response_form = request.form
    print(response_form)
    message = controllerFilho.Cadastrar(response_form, id)
    flash(message)

    return redirect(url_for("cliente.ListarClientes"))



@filho_route.route("/FormAtualizarFilho/<int:id>", methods=["POST", "GET"])
def FormAtualizarFilho(id):
    if "id" not in session:
        return redirect(url_for("login.FormLogin"))
    
    controllerFilho = FilhoController()
    filho = controllerFilho.GetFilho(id)  # Objeto do banco
    print("--------------------------------------------------------")
    print(filho)

    return render_template("formAtualizarFilho.html", dado=filho)


@filho_route.route("/AtualizarFilho/<int:id>", methods=["POST", "GET"])
def AtualizarFilho(id):
    if "id" not in session:
        return redirect(url_for("login.FormLogin"))
    
    controllerFilho = FilhoController()
    response_form = request.form
    message = controllerFilho.AtualizarFilho(id, response_form)
    flash(message)

    return redirect(url_for("cliente.ListarClientes"))


@filho_route.route("/DeletarFilho/<int:id>", methods=["POST", "GET"])
def DeletarFilho(id):
    if "id" not in session:
        return redirect(url_for("login.FormLogin"))

    controllerFilho = FilhoController()
    message = controllerFilho.DeletarFilho(id)
    flash(message)
    
    return redirect(url_for("cliente.ListarClientes"))