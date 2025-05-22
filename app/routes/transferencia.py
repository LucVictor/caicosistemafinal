from ..main import *
from ..models.models import Transferencia, Tipos_Transferencias


@app.route('/transferencia/', methods=['GET'])
@login_required
def index_transferencia():
    criador = current_user.username
    transferencias = Transferencia.query.filter(Transferencia.data >= primeiro_dia_mes(),
                                          Transferencia.data <= ultimo_dia_mes()).order_by(
        Transferencia.data.desc()).all()
    transferencias_por_comprador = (db.session.query(Transferencia.comprador, func.count().label('quantidade'))
    .filter(
        Transferencia.data >= primeiro_dia_mes(),
        Transferencia.data <= ultimo_dia_mes(),
    )
    .group_by(Transferencia.comprador)
    .order_by(func.count().desc())
    .all())

    transferencias_por_tipo = (db.session.query(Transferencia.tipo, func.count().label('quantidade'))
    .filter(
        Transferencia.data >= primeiro_dia_mes(),
        Transferencia.data <= ultimo_dia_mes(),
    )
    .group_by(Transferencia.tipo)
    .order_by(func.count().desc())
    .all())

    if transferencias_por_comprador:
        compradores, qtd_transferencias = zip(*transferencias_por_comprador)
    else:
        compradores, qtd_transferencias = [], []
    if transferencias_por_tipo:
        tipos, quantidades = zip(*transferencias_por_tipo)
    else:
        tipos, quantidades = [], []


    total_transferencias = len(transferencias)
    return render_template('transferencia/index.html', tipos=tipos, quantidades=quantidades, compradores=compradores, qtd_transferencias=qtd_transferencias, transferencias_por_tipo=transferencias_por_tipo, transferencias_por_comprador=transferencias_por_comprador, total_transferencias=total_transferencias, criador=criador, transferencias=transferencias, mes=mes_atual())



@app.route('/transferencia/cadastrar', methods=['POST'])
@login_required
def transferencia_cadastrar():
    if request.method == 'POST':
        data = request.form['data']
        comprador = request.form['comprador']
        tipo = request.form['tipo']
        loja = request.form['loja']
        pedido = request.form['pedido']
        obs = request.form['obs']
        criador = current_user.username
        nova_transferencia = Transferencia(data=data, pedido=pedido, comprador=comprador, tipo=tipo, loja=loja, obs=obs,
                                             criador=criador)
        db.session.add(nova_transferencia)
        db.session.commit()
        db.session.close()
        return redirect(url_for('index_transferencia'))

@app.route('/transferencia/cadastro', methods=['GET'])
@login_required
def transferencia_cadastro():
    compradores = Funcionarios.query.filter(Funcionarios.funcao=="Comprador")
    tipos = Tipos_Transferencias.query.all()
    return render_template('transferencia/cadastrar.html', compradores=compradores, tipos=tipos)


@app.route('/transferencia/relatorio', methods=['GET'])
@login_required
def transferencia_relatorio():
    return render_template('transferencia/relatorio.html')

@app.route('/transferencia/tipos', methods=['GET', 'POST'])
@login_required
def cadastrar_tipos_transferencia():
    if request.method == 'POST':
        nome = request.form['nome'].capitalize()
        novo_tipo = Tipos_Transferencias(nome=nome)
        db.session.add(novo_tipo)
        db.session.commit()
        return render_template('transferencia/cadastrar_tipos.html', sucesso='Cadastrado com Sucesso')
    return render_template('transferencia/cadastrar_tipos.html')



@app.route('/transferencia/relatorio_emitir', methods=['POST'])
@login_required
def emitir_relatorio_transferencia():
    data_inicial = request.form['data_inicial']
    data_final = request.form['data_final']

    transferencias = Transferencia.query.filter(Transferencia.data >= data_inicial, Transferencia.data <= data_final).order_by(
        Transferencia.data.desc()).all()
    total_transferencias = len(transferencias)

    transferencias_por_tipo = (db.session.query(Transferencia.tipo, func.count().label('quantidade'))
    .filter(
        Transferencia.data >= data_inicial,
        Transferencia.data <= data_final,
    )
    .group_by(Transferencia.tipo)
    .order_by(func.count().desc())
    .all())

    transferencias_por_comprador = (db.session.query(Transferencia.comprador, func.count().label('quantidade'))
    .filter(
        Transferencia.data >= data_inicial,
        Transferencia.data <= data_final,
    )
    .group_by(Transferencia.comprador)
    .order_by(func.count().desc())
    .all())
    tipos, quantidades = zip(*transferencias_por_tipo)
    compradores, qtd_transferencias  = zip(*transferencias_por_comprador)

    print(transferencias_por_tipo)
    print(tipos)
    return render_template('transferencia/emitir_relatorio.html',compradores=compradores, qtd_transferencias=qtd_transferencias ,tipos=tipos, quantidades=quantidades, transferencias_por_tipo=transferencias_por_tipo, data_inicial=formatar_data(data_inicial), data_final=formatar_data(data_final), transferencias_por_comprador=transferencias_por_comprador, total_transferencias=total_transferencias, transferencias=transferencias)


@app.route('/transferencia/deletar/<int:id>', methods=['GET'])
@login_required
def transferencia_deletar(id):
    transferencia = Transferencia.query.get_or_404(id)
    if transferencia:
        db.session.delete(transferencia)
        db.session.commit()
        return redirect(url_for('index_transferencia'))
    return redirect(url_for('index_transferencia'))
