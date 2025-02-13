from controller.clienteController import ClienteController
from flask import Blueprint, render_template, request, session, flash, redirect, url_for

cliente_route = Blueprint("cliente",__name__)

@cliente_route.route("/FormCadastrarCliente")
def FormCadastrarCliente():
    if "id" not in session:
        return redirect(url_for("login.FormLogin"))
    
    return render_template("formCadastrarCliente.html")

    
@cliente_route.route("/CadastrarCliente", methods=["POST"])
def CadastrarCliente():
    if "id" not in session:
        return redirect(url_for("login.FormLogin"))
    
    controllerCliente = ClienteController()
    response_form = request.form
    id_funcionario = session["id"]
    
    message = controllerCliente.Cadastrar(response_form, id_funcionario)
    flash(message, "cadastrarCliente")
    return redirect(url_for("cliente.FormCadastrarCliente"))






@cliente_route.route("/ListarClientes")
def ListarClientes():
    if "id" not in session:
        return redirect(url_for("login.FormLogin"))
    
    controllerCliente = ClienteController()
    success, reponse, clientes, filhos, id_func = controllerCliente.ListarClientes()

    if success == False:
        flash(reponse, "listar-error")
        return redirect(url_for("home.Home"))
    return render_template("listarClientes.html", clientes=clientes, filhos=filhos, id_func=id_func)


@cliente_route.route("/ListarTodosClientes")
def ListarTodosClientes():
    if "id" not in session:
        return redirect(url_for("login.FormLogin"))
    
    controllerCliente = ClienteController()
    success, reponse, clientes, filhos = controllerCliente.ListarTodosClientes()

    if success == False:
        flash(reponse, "listar-error")
        return redirect(url_for("home.Home"))
    return render_template("listarTodosClientes.html", clientes=clientes, filhos=filhos)
    



@cliente_route.route('/FormAtualizarCliente/<int:id>', methods=["POST", "GET"])
def FormAtualizarCliente(id):
    if "id" not in session:
        return redirect(url_for("login.FormLogin"))
    
    controllerCliente = ClienteController()
    success, reponse, clientes, filhos, casado, TemFilho, nfilhos = controllerCliente.GetClienteAtualizar(id)

    if success == False:
        flash(reponse, "listarAtualizar-error")
        return redirect(url_for("home.Home"))
    
    return render_template("formAtualizar.html", resultado1=clientes, resultado2=filhos, casado=casado, filho=TemFilho, nfilhos=nfilhos, id_cliente=id)
    


@cliente_route.route('/AtualizarCliente/<int:id>', methods=["POST"])
def AtualizarCliente(id):
    if "id" not in session:
        return redirect(url_for("login.FormLogin"))
    
    controllerCliente = ClienteController()
    response_form = request.form
    message = controllerCliente.AtualizarClientee(response_form, id)
    flash(message, "Atualiazar")

    return redirect(url_for("cliente.ListarClientes"))

@cliente_route.route('/DeletarCliente/<int:id>', methods=["POST", "GET"])
def DeletarCliente(id):
    if "id" not in session:
        return redirect(url_for("login.FormLogin"))
    
    controllerCliente = ClienteController()
    message = controllerCliente.DeletarCliente(id)
    flash(message)
    
    return redirect(url_for("cliente.ListarClientes"))
    
