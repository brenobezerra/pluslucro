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

# 5. Definir o modelo de dados para a sua tabela 'pilar'
# Isso cria uma classe Python que representa sua tabela no banco.
class Pilar(db.Model):
    __tablename__ = 'pilar' # O nome exato da sua tabela no PostgreSQL

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    # Adicione aqui outras colunas que você tenha na tabela 'pilar'

    def __repr__(self):
        return f'<Pilar {self.nome}>'

    # Método para converter o objeto em um dicionário (útil para JSON)
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome
        }

# 6. Criar as Rotas da API

# Rota para obter todas as pilares
@app.route('/pilares', methods=['GET'])
def get_pilares():
    pilares = Pilar.query.all()
    # Converte a lista de objetos Pilar para uma lista de dicionários
    return jsonify([p.to_dict() for p in pilares])

# Rota para criar uma nova pilar
@app.route('/pilares', methods=['POST'])
def create_pilar():
    data = request.get_json() # Pega os dados JSON enviados na requisição
    if not data or 'nome' not in data:
        return jsonify({'erro': 'Nome do pilar é necessário'}), 400

    novo_pilar = Pilar(nome=data['nome'])
    db.session.add(novo_pilar)
    db.session.commit()
    return jsonify(novo_pilar.to_dict()), 201

# Rota para obter uma pilar específica pelo ID
@app.route('/pilares/<int:id>', methods=['GET'])
def get_pilar(id):
    pilar = Pilar.query.get_or_404(id) # Procura pelo ID, retorna 404 se não encontrar
    return jsonify(pilar.to_dict())

# Rota para atualizar uma pilar pelo ID
@app.route('/pilares/<int:id>', methods=['PUT'])
def update_pilar(id):
    pilar = Pilar.query.get_or_404(id)
    data = request.get_json()
    if 'nome' in data:
        pilar.nome = data['nome']

    db.session.commit()
    return jsonify(pilar.to_dict())

# Rota para deletar uma pilar pelo ID
@app.route('/pilares/<int:id>', methods=['DELETE'])
def delete_pilar(id):
    pilar = Pilar.query.get_or_404(id)
    db.session.delete(pilar)
    db.session.commit()
    return jsonify({'mensagem': 'Pilar deletado com sucesso'}), 200

# 7. Rodar o servidor da aplicação
if __name__ == '__main__':
    app.run(debug=True)