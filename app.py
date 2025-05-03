from flask import Flask, request, jsonify
from models import db, Usuario

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bancoDados.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.get_json()
    nome = data.get('nome')
    telefone = data.get('telefone')

    if not nome or not telefone:
        return jsonify({'error': 'Nome e telefone são obrigatórios'}), 400

    novo_usuario = Usuario(nome=nome, telefone=telefone)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'message': 'Usuario criado com sucesso'}), 201

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    usuarios_list = [{'id': usuario.id, 'nome': usuario.nome, 'telefone': usuario.telefone} for usuario in usuarios]
    return jsonify(usuarios_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
