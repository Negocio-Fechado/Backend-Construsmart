from flask import Flask,render_template, request, redirect, url_for
from db import db
from models import Usuario, Produto
import hashlib

app = Flask(__name__)
app.secret_key = "Andre"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:/// database.db"
db.init_app(app)


def hash(txt):
    hash_obj = hashlib.sha256(txt.encode('utf-8'))
    return hash_obj.hexdigest()


@app.route("/")
def base():
    return render_template('admin/base.html')

@app.route("/admin/listar_usuario")
def listarUsuario():
    usuario = db.session.query(Usuario).all()
    return render_template('admin/listar_usuario.html', usuario=usuario)


@app.route("/admin/listar_ferramenta")
def listarFerramenta():
    ferramentas = db.session.query(Produto).all()
    return render_template('admin/listar_ferramenta.html', ferramentas=ferramentas)


@app.route("/admin/cadastrar_usuario", methods=['GET','POST'])
def cadastrarUsuario():
        if request.method == 'GET':
          return render_template('admin/cadastrar_usuario.html')
        if request.method == 'POST':
            nome = request.form['nome']
            sobrenome = request.form['sobrenome']
            data = request.form["data"]
            email = request.form["email"]
            senha = request.form["pass"]

            novo_usuario = Usuario(nome=nome,sobrenome=sobrenome,data=data,email=email,senha=hash(senha))
            db.session.add(novo_usuario)
            db.session.commit()


            return redirect(url_for('listarUsuario'))

@app.route("/admin/excluir_usuario/<int:id>", methods=['POST'])
def excluirUsuario(id):
        usuario = db.session.query(Usuario).filter_by(id=id).first()
        db.session.delete(usuario)
        db.session.commit()
        return redirect(url_for('listarUsuario'))


@app.route("/admin/excluir_ferramenta/<int:id>", methods=['POST'])
def excluirFerramenta(id):
        ferramenta = db.session.query(Produto).filter_by(id=id).first()
        db.session.delete(ferramenta)
        db.session.commit()
        return redirect(url_for('listarFerramenta'))



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
