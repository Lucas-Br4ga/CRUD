from flask import Flask, request, render_template, redirect, url_for
from datetime import date
import sqlite3
from sqlite3 import Error

app = Flask(__name__)


# 1. Rota para cadastrar produtos
@app.route('/produtos/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        descricao = request.form['descricao']
        precocompra = request.form['precocompra']
        precovenda = request.form['precovenda']
        datacriacao = date.today()

        mensagem = 'Erro - não cadastrado'

        if descricao and precocompra and precovenda and datacriacao:
            registro = (descricao, precocompra, precovenda, datacriacao)
            try:
                conn = sqlite3.connect('database/db-produtos.db')
                sql = '''
                      INSERT INTO produtos(descricao, precocompra, precovenda, datacriacao)
                      VALUES (?, ?, ?, ?) \
                      '''
                cur = conn.cursor()
                cur.execute(sql, registro)
                conn.commit()
                mensagem = 'Sucesso - cadastrado'
            except Error as e:
                print(e)
            finally:
                conn.close()

        return render_template('cadastrar.html', mensagem=mensagem)

    return render_template('cadastrar.html')


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


# 3. Rota para editar um produto
@app.route('/produtos/editar/<int:idproduto>', methods=['GET', 'POST'])
def editar(idproduto):
    # Se o método for POST (atualizar os dados)
    if request.method == 'POST':
        descricao = request.form['descricao']
        precocompra = request.form['precocompra']
        precovenda = request.form['precovenda']

        if descricao and precocompra and precovenda:
            try:
                # Conecta ao banco de dados
                conn = sqlite3.connect('database/db-produtos.db')
                sql = '''
                    UPDATE produtos 
                    SET descricao = ?, precocompra = ?, precovenda = ?
                    WHERE idproduto = ?
                '''
                cur = conn.cursor()
                cur.execute(sql, (descricao, precocompra, precovenda, idproduto))
                conn.commit()

                # Redireciona para a página de listar após a atualização
                return redirect(url_for('listar'))
            except Error as e:
                print(e)
                return render_template('erro.html', mensagem="Erro ao atualizar o produto.")
            finally:
                conn.close()

    # Se o método for GET (exibir o formulário de edição)
    try:
        # Conecta ao banco de dados
        conn = sqlite3.connect('database/db-produtos.db')
        sql = 'SELECT * FROM produtos WHERE idproduto = ?'
        cur = conn.cursor()
        cur.execute(sql, (idproduto,))
        produto = cur.fetchone()

        # Se o produto não for encontrado
        if produto is None:
            return render_template('404.html', mensagem="Produto não encontrado.")

        return render_template('editar.html', produto=produto)

    except Error as e:
        print(e)
        return render_template('404.html', mensagem="Erro ao buscar o produto.")
    finally:
        conn.close()


# 4. Rota para excluir um produto
@app.route('/produtos/deletar/<int:idproduto>', methods=['GET'])
def deletar(idproduto):
    try:
        # Conecta ao banco de dados
        conn = sqlite3.connect('database/db-produtos.db')
        sql = 'DELETE FROM produtos WHERE idproduto = ?'
        cur = conn.cursor()
        cur.execute(sql, (idproduto,))
        conn.commit()

        # Redireciona para a página de listar após a exclusão
        return redirect(url_for('listar'))
    except Error as e:
        print(e)
        return render_template('erro.html', mensagem="Erro ao excluir o produto.")
    finally:
        conn.close()


# 5. Rota de erro para páginas não encontradas
@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)