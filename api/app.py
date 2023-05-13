from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import _mysql_connector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:SGuizao123@localhost/armazem'

db = SQLAlchemy(app)

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
    
    
#######
#SELECT
#######

#Selecionar todos os corredores
@app.route("/corredores", methods=["GET"])
def selectAllCorredores():
    corredores_objs = Corredor.query.all()
    corredores_json = [corredor.to_json() for corredor in corredores_objs]
    print(corredores_json)
    
    return response(200, "corredores", corredores_json, "ok")

#Selecionar todos os produtos
@app.route("/produtos", methods=["GET"])
def selectAllProdutos():
    produtos_objs = Produto.query.all()
    produtos_json = [produto.to_json() for produto in produtos_objs]
    print(produtos_json)

    return response(200, "produtos", produtos_json)

#Selecionar produto por id
@app.route("/produtos/<produtoId>", methods=["GET"])
def selectById(produtoId):
    produto_obj = Produto.query.filter_by(produtoId = produtoId).first()
    produto_json = produto_obj.to_json()
    print(produto_json)

    return Response(json.dumps(produto_json))


########
#INSERT#
########

#Insere um novo registro no banco de dados
@app.route("/produtos", methods=["POST"])
def insertProdutct():
    body = request.get_json()

    try:
       produto = Produto(
            nome_produto=body["nome_produto"], 
            corredorId=body["corredorId"], 
            data_validade=body["data_validade"],
            qtdeKg=body["qtdeKg"]
            )
       db.session.add(produto)
       db.session.commit()

       return response(201, "produto", produto.to_json(), "Registro inserido com sucesso")
    except Exception as e:
        print(e)
        return response(400, "produto", {}, "Erro ao inserir registro")


########
#UPDATE#
########

#Atualiza um registro
@app.route("/produtos/<produtoId>", methods=["PUT"])
def updateProduct(produtoId):
    produto_obj = Produto.query.filter_by(produtoId = produtoId).first()
    body = request.get_json()

    try:
       produto_obj.nome_produto = body["nome_produto"]
       produto_obj.corredorId = body["corredorId"]
       produto_obj.data_validade = body["data_validade"]
       produto_obj.qtdeKg = body["qtdeKg"]

       db.session.add(produto_obj)
       db.session.commit()

       return response(200, "produto", produto_obj.to_json(), "Atualizado com sucesso")
    except Exception as e:
        print(e)
        return response(400, "produto", {}, "Erro ao atualizar")


########
#DELETE#
########

#Deleta um registro
@app.route("/produtos/<produtoId>", methods=["DELETE"])
def deleteProduct(produtoId):
        produto_obj = Produto.query.filter_by(produtoId = produtoId).first()

        try:
           db.session.delete(produto_obj)
           db.session.commit()
           return response(200, "produto", produto_obj.to_json(), "Deletado com sucesso")
        except Exception as e:
           print(e)
           return response(400, "produto", {}, "Erro ao deletar")

def response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body[mensagem] = mensagem
    
    return Response(json.dumps(body), status=status, mimetype="application/json")

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)


app.run()
