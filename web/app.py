from flask import Flask, Response, request, render_template
from flask_sqlalchemy import SQLAlchemy


app2 = Flask(__name__)
app2.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app2.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:SGuizao123@localhost/armazem'

db = SQLAlchemy(app2)

class Corredor(db.Model):
    corredorId = db.Column(db.Integer, primary_key=True)
    nome_do_corredor = db.Column(db.String(256))

class Produto(db.Model):
    produtoId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produto = db.Column(db.String(256))
    corredorId = db.Column(db.Integer, db.ForeignKey(Corredor.corredorId), primary_key=True)
    data_validade = db.Column(db.Date)
    qtdeKg = db.Column(db.Integer)

@app2.route('/', methods=['POST'])
def index():
  try:
    produto = Produto(
            nome_produto=request.form["nome_produto"], 
            corredorId=request.form["idcorredor"], 
            data_validade=request.form["data_validade"],
            qtdeKg=request.form["qtdeKg"]
            )
    print(produto.data_validade)

    db.session.add(produto)
    db.session.commit()

    return Response("Cadastro Realizado com Sucesso")
  except Exception as e:
        print(e)
        return Response("Erro ao cadastrar")
    
if __name__ == '__main__':
    app2.run(host="localhost", port=5001, debug=True)

app2.run()