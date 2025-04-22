from flask import Flask
from flask import request
from flask import render_template
from datetime import date
import sqlite3
from sqlite3 import Error

#######################################################
# Instância da Aplicação Flask
app = Flask(__name__)

#######################################################
# 1. Rota para cadastrar produtos
@app.route('/produtos/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        # Coletando dados do formulário
        descricao = request.form['descricao']
        precocompra = request.form['precocompra']
        precovenda = request.form['precovenda']
        datacriacao = date.today()

        mensagem = 'Erro - não cadastrado'

        # Verifica se os campos foram preenchidos
        if descricao and precocompra and precovenda and datacriacao:
            registro = (descricao, precocompra, precovenda, datacriacao)
            try:
                # Conecta ao banco de dados
                conn = sqlite3.connect('database/db-produtos.db')
                sql = '''
                    INSERT INTO produtos(descricao, precocompra, precovenda, datacriacao)
                    VALUES (?, ?, ?, ?)
                '''
                cur = conn.cursor()
                cur.execute(sql, registro)
                conn.commit()
                mensagem = 'Sucesso - cadastrado'
            except Error as e:
                print(e)
            finally:
                conn.close()

    # Renderiza a página de cadastro (GET ou após POST)
    return render_template('cadastrar.html')

#######################################################
# 2. Rota para listar produtos
@app.route('/produtos/listar', methods=['GET'])
def listar():
    try:
        conn = sqlite3.connect('database/db-produtos.db')
        sql = 'SELECT * FROM produtos'
        cur = conn.cursor()
        cur.execute(sql)
        registros = cur.fetchall()
        return render_template('listar.html', regs=registros)
    except Error as e:
        print(e)
    finally:
        conn.close()

#######################################################
# 3. Rota de erro para páginas não encontradas
@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404

#######################################################
# Execução da aplicação
if __name__ == '__main__':
    app.run()
