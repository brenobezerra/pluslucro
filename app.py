# 1. Importar as bibliotecas necessárias
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# 2. Configurar a aplicação Flask
app = Flask(__name__)

# 3. Configurar a conexão com o banco de dados PostgreSQL
# SUBSTITUA as informações abaixo pelas suas.
# Formato: 'postgresql://usuario:senha@host:porta/nome_do_banco'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:novasenha@localhost:5432/gastos_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Recomendado para evitar avisos

# 4. Inicializar o objeto SQLAlchemy
db = SQLAlchemy(app)

# 5. Definir o modelo de dados para a sua tabela 'categoria'
# Isso cria uma classe Python que representa sua tabela no banco.
class Categoria(db.Model):
    __tablename__ = 'categoria' # O nome exato da sua tabela no PostgreSQL

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    # Adicione aqui outras colunas que você tenha na tabela 'categoria'

    def __repr__(self):
        return f'<Categoria {self.nome}>'

    # Método para converter o objeto em um dicionário (útil para JSON)
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome
        }

# 6. Criar as Rotas da API

# Rota para obter todas as categorias
@app.route('/categorias', methods=['GET'])
def get_categorias():
    categorias = Categoria.query.all()
    # Converte a lista de objetos Categoria para uma lista de dicionários
    return jsonify([c.to_dict() for c in categorias])

# Rota para criar uma nova categoria
@app.route('/categorias', methods=['POST'])
def create_categoria():
    data = request.get_json() # Pega os dados JSON enviados na requisição
    if not data or 'nome' not in data:
        return jsonify({'erro': 'Nome da categoria é necessário'}), 400

    nova_categoria = Categoria(nome=data['nome'])
    db.session.add(nova_categoria)
    db.session.commit()
    return jsonify(nova_categoria.to_dict()), 201

# Rota para obter uma categoria específica pelo ID
@app.route('/categorias/<int:id>', methods=['GET'])
def get_categoria(id):
    categoria = Categoria.query.get_or_404(id) # Procura pelo ID, retorna 404 se não encontrar
    return jsonify(categoria.to_dict())

# Rota para atualizar uma categoria pelo ID
@app.route('/categorias/<int:id>', methods=['PUT'])
def update_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    data = request.get_json()
    if 'nome' in data:
        categoria.nome = data['nome']

    db.session.commit()
    return jsonify(categoria.to_dict())

# Rota para deletar uma categoria pelo ID
@app.route('/categorias/<int:id>', methods=['DELETE'])
def delete_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({'mensagem': 'Categoria deletada com sucesso'}), 200

# 7. Rodar o servidor da aplicação
if __name__ == '__main__':
    app.run(debug=True)