import sqlite3
from flask import Flask, jsonify, request, send_from_directory
from flasgger import Swagger

app = Flask(__name__, static_url_path='/static', static_folder='../frontend/static')

app.config['SWAGGER'] = {
    'title': 'API de Usuários com SQLite',
    'uiversion': 3
}

swagger = Swagger(app)

def criar_banco():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY, 
            nome TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def encontrar_menor_id_disponivel():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios ORDER BY id ASC")
    ids_existentes = [id[0] for id in cursor.fetchall()]
    conn.close()

    for i in range(1, len(ids_existentes) + 2):
        if i not in ids_existentes:
            return i

criar_banco()

# Rota 1: Cadastrar Usuário (POST)
@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    """
    Cadastra um novo usuário
    ---
    tags:
      - Usuários
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: Usuario
          required:
            - nome
          properties:
            nome:
              type: string
              description: Nome do usuário
    responses:
      201:
        description: Usuário cadastrado com sucesso
    """
    novo_usuario = request.get_json()
    nome = novo_usuario['nome']

    novo_id = encontrar_menor_id_disponivel() 

    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (id, nome) VALUES (?, ?)", (novo_id, nome))
        conn.commit()
        return jsonify({"mensagem": "Usuário cadastrado com sucesso!", "id": novo_id}), 201
    except sqlite3.IntegrityError:
        return jsonify({"mensagem": "Erro: Nome de usuário já existe."}), 400
    finally:
        conn.close()

# Rota 2: Buscar Usuário por ID
@app.route('/buscar_usuario/<int:id>')
def buscar_usuario(id):
    """
    Busca um usuário pelo ID
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do usuário
    responses:
      200:
        description: Usuário encontrado
        schema:
          id: Usuario
          properties:
            id:
              type: integer
            nome:
              type: string
      404:
        description: Usuário não encontrado
    """
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        return jsonify({"id": usuario[0], "nome": usuario[1]})
    else:
        return jsonify({"mensagem": "Usuário não encontrado"}), 404

# Rota 3: Deletar Usuário
@app.route('/deletar_usuario/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    """
    Deleta um usuário pelo ID
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do usuário
    responses:
      200:
        description: Usuário deletado com sucesso
    """
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Usuário deletado com sucesso!"})

# Rota para buscar todos os usuários
@app.route('/buscar_usuario')
def buscar_usuarios():
    """
    Busca todos os usuários
    ---
    tags:
      - Usuários
    responses:
      200:
        description: Lista de usuários
        schema:
          type: array
          items:
            $ref: '#/definitions/Usuario'
    """
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()

    return jsonify([{"id": usuario[0], "nome": usuario[1]} for usuario in usuarios])

# Rota para servir o arquivo index.html (frontend)
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html') 

if __name__ == '__main__':
    app.run(debug=True)
