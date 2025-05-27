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
        ajuste = 'ajuste' in request.form
        produtos_conferido_lojas = 'produtos_conferidos_lojas' in request.form
        divergencia_sistema = 'divergencia_sistema' in request.form
        criador = current_user.username
        nova_conferencia = Produto_Conferido(data_conferencia=data_conferencia,conferente=conferente,
                                             codigo_produto=codigo_produto,nome_do_produto=nome_do_produto,
                                             quantidade_sistema=quantidade_sistema,quantidade_fisico=quantidade_fisico,
                                             quantidade_diferenca=quantidade_diferenca, ajuste=ajuste,
                                             produto_conferido_lojas=produtos_conferido_lojas, divergencia_sistema=divergencia_sistema,
                                             criador=criador)
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
    quantidade = request.form.get('filtro_quantidade', 100000)
    filtroPassando = request.form.get('filtroPassando', 'todos')  # Padrão "todos"

    if not quantidade:
        quantidade = 100000

    query = Produto_Conferido.query.filter(
        Produto_Conferido.data_conferencia >= data_inicial,
        Produto_Conferido.data_conferencia <= data_final,
        Produto_Conferido.quantidade_sistema <= quantidade
    )

    # Aplica o filtro de "Passando" ou "Faltando"
    if filtroPassando == 'passando':
        query = query.filter(Produto_Conferido.quantidade_fisico > Produto_Conferido.quantidade_sistema)
    elif filtroPassando == 'faltando':
        query = query.filter(Produto_Conferido.quantidade_fisico < Produto_Conferido.quantidade_sistema)

    if codigo_produto:
        query = query.filter(Produto_Conferido.codigo_produto == codigo_produto)

    conferencias = query.order_by(Produto_Conferido.data_conferencia.desc()).all()
    totalitens = len(conferencias)

    # Relatório agrupado por conferente (opcional: aplicar mesmo filtro para consistência)
    query_por_conferente = db.session.query(
        Produto_Conferido.conferente, func.count().label('quantidade')
    ).filter(
        Produto_Conferido.data_conferencia >= data_inicial,
        Produto_Conferido.data_conferencia <= data_final
    )

    if filtroPassando == 'passando':
        query_por_conferente = query_por_conferente.filter(
            Produto_Conferido.quantidade_fisico > Produto_Conferido.quantidade_sistema
        )
    elif filtroPassando == 'faltando':
        query_por_conferente = query_por_conferente.filter(
            Produto_Conferido.quantidade_fisico < Produto_Conferido.quantidade_sistema
        )

    conferencias_por_conferente = (
        query_por_conferente.group_by(Produto_Conferido.conferente)
        .order_by(func.count().desc())
        .all()
    )

    return render_template(
        'conferencia/emitir_relatorio.html',
        conferencias=conferencias,
        data_inicial=formatar_data(data_inicial),
        data_final=formatar_data(data_final),
        conferencias_por_conferente=conferencias_por_conferente,
        totalitens=totalitens
    )



@app.route('/conferencia/relatorio_zerados_emitir', methods=['POST'])
@login_required
def conferencia_zerados_relatorio_emitir():
    data_inicial = request.form['data_inicial']
    data_final = request.form['data_final']
    codigo_produto = request.form['codigo_produto']
    if codigo_produto:
        conferencias = Produto_Conferido.query.filter(Produto_Conferido.data_conferencia >= data_inicial,
                                          Produto_Conferido.data_conferencia <=data_final,
                                            Produto_Conferido.codigo_produto==codigo_produto, Produto_Conferido.ajuste==True, Produto_Conferido.divergencia_sistema==False).order_by(Produto_Conferido.data_conferencia.desc()).all()
        conferencias_totais=[]
        for i in conferencias:
            if i.quantidade_sistema > i.quantidade_fisico :
                produto = Produto.query.filter(Produto.codigo_do_produto == i.codigo_produto).first()
                total = (i.quantidade_sistema - i.quantidade_fisico) * produto.preco_do_produto
                conferencias_totais.append({
                    'codigo_produto': i.codigo_produto,
                    'nome_do_produto': i.nome_do_produto,
                    'data_conferencia': i.data_conferencia,
                    'quantidade_sistema': i.quantidade_sistema,
                    'quantidade_fisico': i.quantidade_fisico,
                    'conferente': i.conferente,
                    'criador': i.criador,
                    'ajuste': i.produto_conferido_lojas,
                    'lojas': i.lojas,
                    'total': total
                })

        totalitens = len(conferencias)
        return render_template('conferencia/relatorio_zerados.html', conferencias_totais=conferencias_totais, totalitens= totalitens ,conferencias=conferencias, data_inicial=formatar_data(data_inicial), data_final=formatar_data(data_final))


    conferencias = Produto_Conferido.query.filter(Produto_Conferido.data_conferencia >= data_inicial,
                                        Produto_Conferido.data_conferencia <=data_final,Produto_Conferido.ajuste==True ,Produto_Conferido.divergencia_sistema==False).order_by(
    Produto_Conferido.data_conferencia.desc()).all()
    totalitens = len(conferencias)
    conferencias_totais=[]
    for i in conferencias:
        if i.quantidade_sistema > i.quantidade_fisico:
            produto = Produto.query.filter(Produto.codigo_do_produto == i.codigo_produto).first()
            total = (i.quantidade_sistema - i.quantidade_fisico) * produto.preco_do_produto
            conferencias_totais.append({
                'codigo_produto': i.codigo_produto,
                'nome_do_produto': i.nome_do_produto,
                'data_conferencia': i.data_conferencia,
                'quantidade_sistema': i.quantidade_sistema,
                'quantidade_fisico': i.quantidade_fisico,
                'quantidade_diferenca': i.quantidade_fisico - i.quantidade_sistema,
                'conferente': i.conferente,
                'criador': i.criador,
                'ajuste': i.ajuste,
                'lojas': i.produto_conferido_lojas,
                'total': total
            })
        custo_total = sum(i['total'] for i in conferencias_totais) or 0
    return render_template('conferencia/relatorio_zerados.html',
                           conferencias=conferencias, custo_total=custo_total, conferencias_totais=conferencias_totais,data_inicial=formatar_data(data_inicial),
                           data_final=formatar_data(data_final), totalitens=totalitens)

@app.route('/conferencia/zerados', methods=['GET'])
@login_required
def conferencia_zerados():
    return render_template('conferencia/zerados.html')


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
        panilha_tratada = panilha_bruta[['CODIGO', 'SISTEMA', 'FISICO', 'LOJAS', 'AJUSTE', 'DIVERGENCIA']]
        data_conferencia = request.form['data_conferencia']
        conferente = request.form['conferente']
        criador = current_user.username
        for index, linha in panilha_tratada.iterrows():
            produto = Produto.query.filter(Produto.codigo_do_produto == linha['CODIGO']).first()
            if produto:
                lojas = linha.get('LOJAS', '').strip().lower() == 'sim'
                ajuste = linha.get ('AJUSTE', '').strip().lower() == 'sim'
                divergencia = linha.get('DIVERGENCIA', '').strip().lower() == 'sim'
                nova_conferencia = Produto_Conferido(data_conferencia=data_conferencia,conferente=conferente,
                codigo_produto=produto.codigo_do_produto,nome_do_produto=produto.nome_do_produto,
                quantidade_sistema=Decimal(str(linha['SISTEMA'])),quantidade_fisico=Decimal(str(linha['FISICO'])),
                quantidade_diferenca=(Decimal(str(linha['FISICO']))) - Decimal(str(linha['SISTEMA'])),
                divergencia_sistema=divergencia, produto_conferido_lojas=lojas, ajuste=ajuste,
                criador=criador)
                db.session.add(nova_conferencia)
                db.session.commit()
            else:
                return (f"ERROR NA LINHA, Código: {linha['CODIGO']}, Quantidade Física: {linha['FISICO']}, Quantidade Sistema: {linha['SISTEMA']}")
        db.session.close()
        return redirect(url_for('index_conferencia'))
    conferentes = Funcionarios.query.filter(Funcionarios.funcao=="Estoque")
    return render_template('conferencia/importar_planilha.html', conferentes=conferentes)
