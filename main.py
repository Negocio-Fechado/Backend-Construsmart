from flask import Flask, render_template, request, redirect, url_for
from models import Usuario,Produto,ImagemProduto,Marca
from flask_login import LoginManager,login_user, login_required,logout_user, current_user
from werkzeug.utils import secure_filename
from db import db
import hashlib
import os

app = Flask(__name__)
lm = LoginManager(app)
lm.login_view = 'login'
app.secret_key = "Andre"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:/// database.db"
db.init_app(app)

@lm.user_loader
def user_loader(id):
    usuario = db.session.query(Usuario).filter_by(id=id).first()
    return usuario

def hash(txt):
    hash_obj = hashlib.sha256(txt.encode('utf-8'))
    return hash_obj.hexdigest()
# <-----------Rota home-------------->
@app.route("/")
def home():
    return render_template('main/dashboard/index.html')
# <-----------Rotas de Cadastro-------------->
@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "GET":
        return render_template('main/login/cadastro.html')
    elif request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['pass']


        novo_usuario = Usuario(nome=nome,email=email,senha=hash(senha))
        db.session.add(novo_usuario)
        db.session.commit()

        login_user(novo_usuario)
        return redirect(url_for('home'))
        


@app.route('/cadastrar_produto', methods=['GET','POST'])
@login_required
def cadastrarProduto():

    if request.method == 'POST':
        marca = db.session.query(Marca).all()
        categoria = request.form['categoria']

        nome = request.form['titulo']
        preco = request.form['preco']
        descricao = request.form['descricao']
        imagem = request.files['imagem']
        # tipo = request.form['tipo']
        # id_marca = request.form['id_marca']

        filename = secure_filename(imagem.filename)
        pasta_usuario = os.path.join('static', 'uploads', f'Usuario_{current_user.id}/produtos')
        caminho = f'uploads/Usuario_{current_user.id}/produtos/{filename}'
        os.makedirs(pasta_usuario, exist_ok=True)
        caminho_completo = os.path.join(pasta_usuario, filename)
 # <-----------Salva a imagem no banco-------------->
        imagem.save(caminho_completo)
        img = ImagemProduto(nome=filename,caminho=caminho)
        db.session.add(img)
        db.session.commit()

        id_imagem = img.id
        id_locatario = current_user.id
# <-----------Salva os dados do produto no banco de dados-------------->
        produto = Produto(nome=nome,preco=preco,descricao=descricao,imagem_id=id_imagem,tipo=categoria,locatario_id=id_locatario)
        db.session.add(produto)
        db.session.commit()

        return redirect(url_for('ferramentas'))

    return render_template('main/dashboard/aluguel.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('main/login/login.html')
    elif request.method == "POST":
        email = request.form['email']
        senha = request.form['pass']

        user = db.session.query(Usuario).filter_by(email=email,senha=hash(senha)).first()
        if not user:
            return 'nome ou senha incorretas'
        
        login_user(user)

        return redirect(url_for('home'))

@app.route("/perfil")
def perfil():
    if current_user.is_authenticated:
        return f"Você está logado como {current_user.nome}"
    
    return "Você não está logado"

@app.route('/about')
def about():
    return 'pagina em desenvolvimento'

@app.route('/produtos')
def ferramentas():
    return render_template('main/dashboard/ferramentas.html')        

@app.route('/categoria/<categoria>', methods=['GET','POST'])
def categoria(categoria):
    
    produtos = db.session.query(Produto).filter_by(tipo=categoria).limit(10).all()
    return render_template('main/dashboard/categoria.html', produtos=produtos)


@app.route('/pesquisa/', methods=['GET','POST'])
def pesquisa():
    termo = request.args.get('pesquisar', '').strip()

    resultados = Produto.query.filter(Produto.nome.ilike(f"%{termo}%")).all()

    return render_template('main/dashboard/pesquisa.html', resultados=resultados, termo=termo)
    
@app.route('/consultoria', methods=['GET','POST'])
def consultoria():
    return 'consultoria'


@app.route('/contato', methods=['GET','POST'])
def contato():
    return render_template('main/dashboard/contact.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')

































    
# @app.route("/cadastrar_profissional", methods=["GET","POST"])
# @login_required
# def cadastrarProfissional():
   
#     if request.method == "POST":
#         email = request.form['email']
#         senha = request.form['senha']
#         atuacao = request.form['atuacao']
#         genero = request.form['genero']
#         estado = request.form['estado']
#         cidade = request.form['cidade']
#         data = request.form['date']
#         cpf_cnpj = request.form['cpf_cnpj']
#         celular = request.form['number']

#         profissional = db.session.query(Usuario).filter_by(email=email, senha=hash(senha)).first()

#         if not profissional:
#             return 'erro'

#         else:
#             profissional.genero = genero
#             profissional.estado = estado
#             profissional.cidade = cidade
#             profissional.tipo_usuario = atuacao
#             profissional.cpf_cnpj = cpf_cnpj
#             profissional.celular = celular
#             profissional.data_nascimento = data

#             db.session.commit()
#             return redirect(url_for('home'))

#     return render_template('cadastro_pro.html')