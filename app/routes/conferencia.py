from ..main import *
from sqlalchemy import func
from ..models.models import Produto_Conferido
@app.route('/conferencia/', methods=['GET'])
@login_required
def index_conferencia():
    criador = current_user.username
    conferencias = Produto_Conferido.query.filter(Produto_Conferido.data_conferencia >= primeiro_dia_mes(),
                                          Produto_Conferido.data_conferencia <= ultimo_dia_mes(), Produto_Conferido.data_conferencia == data_agora()).order_by(
        Produto_Conferido.data_conferencia.desc()).all()
    totalitens = len(conferencias)
    return render_template('conferencia/index.html', totalitens=totalitens, criador=criador, conferencias=conferencias, mes=mes_atual())



@app.route('/conferencia/cadastrar', methods=['POST'])
@login_required
def conferencia_cadastrar():
    if request.method == 'POST':
        data_conferencia = request.form['data_conferencia']
        conferente = request.form['conferente']
        codigo_produto = request.form['codigo_produto']
        nome_do_produto = request.form['nome_do_produto']
        quantidade_sistema = request.form['quantidade_sistema']
        quantidade_fisico = request.form['quantidade_fisico']
        quantidade_diferenca = Decimal(quantidade_fisico) - Decimal(quantidade_sistema)
        criador = current_user.username
        nova_conferencia = Produto_Conferido(data_conferencia=data_conferencia,conferente=conferente, 
                                             codigo_produto=codigo_produto,nome_do_produto=nome_do_produto,
                                             quantidade_sistema=quantidade_sistema,quantidade_fisico=quantidade_fisico,
                                             quantidade_diferenca=quantidade_diferenca,criador=criador)
        db.session.add(nova_conferencia)
        db.session.commit()
        db.session.close()
        return redirect(url_for('index_conferencia'))
    return render_template('conferencia/procurar.html', conferencias=conferencias, mes=mes_atual())


@app.route('/conferencia/procurar', methods=['GET'])
@login_required
def conferencia_procurar():
    return render_template('conferencia/procurar.html')


@app.route('/conferencia/cadastro', methods=['POST'])
@login_required
def conferencia_cadastro():
    codigo = request.form['codigo']
    if codigo:
        produto = Produto.query.filter(Produto.codigo_do_produto == codigo).first()
        conferentes = Funcionarios.query.filter(Funcionarios.funcao=="Estoque")
        return render_template('conferencia/cadastrar.html', produto=produto, conferentes=conferentes)
    return render_template('conferencia/procurar.html')


@app.route('/conferencia/relatorio', methods=['GET'])
@login_required
def conferencia_relatorio():
    return render_template('conferencia/relatorio.html')


@app.route('/conferencia/relatorio_emitir', methods=['POST'])
@login_required
def conferencia_relatorio_emitir():
    data_inicial = request.form['data_inicial']
    data_final = request.form['data_final']
    codigo_produto = request.form['codigo_produto']
    if codigo_produto:
        conferencias = Produto_Conferido.query.filter(Produto_Conferido.data_conferencia >= data_inicial,
                                          Produto_Conferido.data_conferencia <=data_final,
                                            Produto_Conferido.codigo_produto==codigo_produto).order_by(Produto_Conferido.data_conferencia.desc()).all()
        totalitens = len(conferencias)
        itens_por_conferente = conferencias = Produto_Conferido.query.filter(Produto_Conferido.data_conferencia >= data_inicial,
                                          Produto_Conferido.data_conferencia <=data_final,
                                            Produto_Conferido.codigo_produto==codigo_produto).order_by(Produto_Conferido.data_conferencia.desc()).all()

        return render_template('conferencia/emitir_relatorio.html', totalitens= totalitens ,conferencias=conferencias, data_inicial=formatar_data(data_inicial), data_final=formatar_data(data_final))
    conferencias = Produto_Conferido.query.filter(Produto_Conferido.data_conferencia >= data_inicial,
                                        Produto_Conferido.data_conferencia <=data_final).order_by(
    Produto_Conferido.data_conferencia.desc()).all()
    totalitens = len(conferencias)
    conferencias_por_conferente = (
    db.session.query(Produto_Conferido.conferente, func.count().label('quantidade'))
    .filter(
        Produto_Conferido.data_conferencia >= data_inicial,
        Produto_Conferido.data_conferencia <= data_final,
    )
    .group_by(Produto_Conferido.conferente)
    .order_by(func.count().desc())  # opcional, ordena do maior pro menor
    .all()
)
    return render_template('conferencia/emitir_relatorio.html',
                           conferencias=conferencias, data_inicial=formatar_data(data_inicial), 
                           data_final=formatar_data(data_final), conferencias_por_conferente=conferencias_por_conferente, totalitens=totalitens)


@app.route('/conferencia/deletar/<int:id>', methods=['GET'])
@login_required
def conferencia_deletar(id):
    conferencia = Produto_Conferido.query.get_or_404(id)
    if conferencia:
        db.session.delete(conferencia)
        db.session.commit()
        return redirect(url_for('index_conferencia'))
    return redirect(url_for('index_conferencia'))



@app.route('/conferencia/planilha', methods=['GET', 'POST'])
def conferencia_planilha():
    if request.method == 'POST':
        file = request.files['planilha']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'tabela_planilha.xlsx'))
        panilha_bruta = pd.read_excel('app/static/uploads/tabela_planilha.xlsx')
        panilha_tratada = panilha_bruta[['CODIGO', 'SISTEMA', 'FISICO']]
        data_conferencia = request.form['data_conferencia']
        conferente = request.form['conferente']
        criador = current_user.username
        for index, linha in panilha_tratada.iterrows():
            produto = Produto.query.filter(Produto.codigo_do_produto == linha['CODIGO']).first()
            if produto:
                nova_conferencia = Produto_Conferido(data_conferencia=data_conferencia,conferente=conferente, 
                codigo_produto=produto.codigo_do_produto,nome_do_produto=produto.nome_do_produto,
                quantidade_sistema=Decimal(str(linha['SISTEMA'])),quantidade_fisico=Decimal(str(linha['FISICO'])),
                quantidade_diferenca=(Decimal(str(linha['FISICO']))) - Decimal(str(linha['SISTEMA'])),criador=criador)
                db.session.add(nova_conferencia)
                db.session.commit()
            else:
                return (f"ERROR NA LINHA, {linha['CODIGO'], {linha['FISICO']}, {linha['SISTEMA']}}")
        db.session.close()
        return redirect(url_for('index_conferencia'))
    conferentes = Funcionarios.query.filter(Funcionarios.funcao=="Estoque")
    return render_template('conferencia/importar_planilha.html', conferentes=conferentes)
