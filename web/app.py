from flask import Flask, Response, request, render_template
from flask_sqlalchemy import SQLAlchemy


app2 = Flask(__name__)
app2.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app2.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:SGuizao123@localhost/armazem'

db = SQLAlchemy(app2)

class Corredor(db.Model):
    corredorId = db.Column(db.Integer, primary_key=True)
    nome_do_corredor = db.Column(db.String(256))

    def to_json(self):
        return {"corredorId": self.corredorId, 
                "nome_do_corredor": self.nome_do_corredor
                }

class Produto(db.Model):
    produtoId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produto = db.Column(db.String(256))
    corredorId = db.Column(db.Integer, db.ForeignKey(Corredor.corredorId), primary_key=True)
    data_validade = db.Column(db.Date)
    qtdeKg = db.Column(db.Integer)

    def to_json(self):
        return {"produtoId": self.produtoId, 
                "nome_produto": self.nome_produto, 
                "corredorId": self.corredorId, 
                "data_validade": str(self.data_validade),
                "qtdeKg": self.qtdeKg
                }
                

#Página inicial
@app2.route('/')
def home():
    fruits = ['apple','orange', 'wine']
    return render_template("index.html",fruits=fruits)

#Retorna uma página para cadastro
@app2.route('/insert')
def insert():
    return render_template("form.html")

#Retorna uma página para deleção
@app2.route('/delete')
def delete():
    return render_template("formDelete.html")

#Retorna página com todos os corredores
@app2.route('/selectCorredores')
def selCorredor():
    corredores_objs = Corredor.query.all()
    return render_template('select.html',corredores_objs=corredores_objs)

#Retorna página com todos os corredores
@app2.route('/selectProdutos')
def selProdutos():
    produtos_objs = Produto.query.all()
    return render_template('selectP.html', produtos_objs=produtos_objs)

#Seleciona produto por Id
@app2.route('/selectById')
def selProductById():
    return render_template('formId.html')

@app2.route('/updateById')
def upById():
    return render_template('formUpdate.html')



#Realiza cadastro
@app2.route('/register', methods=['POST'])
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
  
#Pegar por Id
@app2.route('/getById', methods=['GET','POST'])
def getPById():
    produto_obj = Produto.query.filter_by(produtoId = request.form['produtoId']).first()
    return render_template('byId.html', produto_obj=produto_obj)

#Deleta por Id
@app2.route('/deleteById', methods=['POST'])
def deleteById():
    produto_obj = Produto.query.filter_by(produtoId = request.form['produtoId']).first()
    try:
        db.session.delete(produto_obj)
        db.session.commit()

        return Response("Deletado com sucesso")
    except Exception as e:
        print(e)
        return Response("Erro ao deletar")
    
#Auxílio de atualização
@app2.route('/update1', methods=['POST'])
def getUpById():
    produto_obj = Produto.query.filter_by(produtoId = request.form['produtoId']).first()
    return render_template('formUpdate2.html', produto_obj=produto_obj)

#Realiza atualização
@app2.route('/update', methods=['POST'])
def updateId():
    produto_obj = Produto.query.filter_by(produtoId = request.form['produtoId']).first()
    try:
       produto_obj.nome_produto = request.form["nome_produto"]
       produto_obj.corredorId = request.form["idcorredor"]
       produto_obj.data_validade = request.form["data_validade"]
       produto_obj.qtdeKg = request.form["qtdeKg"]

       db.session.add(produto_obj)
       db.session.commit()

       return Response("Atualizado com sucesso")
    except Exception as e:
        print(e)
        return Response("Erro ao atualizar")


    
if __name__ == '__main__':
    app2.run(host="localhost", port=5001, debug=True)

app2.run()