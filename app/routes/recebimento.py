from ..main import *
from sqlalchemy import func
from ..models.models import Recebimento


@app.route('/recebimento/', methods=['GET'])
@login_required
def index_recebimento():
    recebimentos = Recebimento.query.filter(Recebimento.data_recebimento >= primeiro_dia_mes(), Recebimento.data_recebimento <= ultimo_dia_mes()).order_by(
        Recebimento.data_recebimento.desc()).all()
    total_recebimento = len(recebimentos)
    recebimento_por_conferente = (db.session.query(Recebimento.conferente, func.count().label('quantidade'))
    .filter(
        Recebimento.data_recebimento >= primeiro_dia_mes(),
        Recebimento.data_recebimento <= ultimo_dia_mes(),
    )
    .group_by(Recebimento.conferente)
    .order_by(func.count().desc())  # opcional, ordena do maior pro menor
    .all())
    return render_template('recebimento/index.html', recebimento_por_conferente=recebimento_por_conferente, total_recebimento=total_recebimento, recebimentos=recebimentos)

@app.route('/recebimento/cadastrar', methods=['GET', 'POST'])
@login_required
def recebimento_cadastrar():
    if request.method == 'POST':
        data_recebimento = request.form['data_recebimento']
        quantidade_notas = request.form['quantidade_notas']
        estoque = request.form['estoque'].lower() == 'true'
        prateleiras = request.form['prateleiras'].lower() == 'true'
        produto_novo = request.form['produto_novo'].lower() == 'true'
        conferente = request.form['conferente']
        criador = current_user.username
        file = request.files['foto_prancheta']
        novo_recebimento = Recebimento(data_recebimento=data_recebimento,
            conferente=conferente, quantidade_notas=quantidade_notas, estoques=estoque,
            prateleiras=prateleiras, produto_novo=produto_novo, criador=criador)
        db.session.add(novo_recebimento)
        db.session.commit()
        ext = os.path.splitext(file.filename)[1]  # obtém a extensão, incluindo o ponto (ex: .jpg, .xlsx)
        filename = f'recebimento_{novo_recebimento.id}{ext}'
        novo_recebimento.foto = filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER_PRANCHETA'], secure_filename(filename))
        file.save(filepath)
        db.session.add(novo_recebimento)
        db.session.commit()
        db.session.close()
        return redirect(url_for('index_recebimento'))
    conferentes = Funcionarios.query.filter(Funcionarios.funcao=="Estoque")
    return render_template('recebimento/cadastrar.html', conferentes=conferentes)


@app.route('/recebimento/relatorio', methods=['GET'])
@login_required
def relatorio_recebimento():
    return render_template('recebimento/relatorio.html')

@app.route('/recebimento/relatorio_emitir', methods=['POST'])
@login_required
def emitir_relatorio_recebimento():
    data_inicial = request.form['data_inicial']
    data_final = request.form['data_final']
    recebimentos = Recebimento.query.filter(Recebimento.data_recebimento >= data_inicial, Recebimento.data_recebimento <= data_final).order_by(
        Recebimento.data_recebimento.desc()).all()
    total_recebimento = len(recebimentos)
    recebimento_por_conferente = (db.session.query(Recebimento.conferente, func.count().label('quantidade'))
    .filter(
        Recebimento.data_recebimento >= data_inicial,
        Recebimento.data_recebimento <= data_final,
    )
    .group_by(Recebimento.conferente)
    .order_by(func.count().desc())  # opcional, ordena do maior pro menor
    .all())

    return render_template('recebimento/emitir_relatorio.html', data_inicial=formatar_data(data_inicial), data_final=formatar_data(data_final), recebimentos=recebimentos, recebimento_por_conferente=recebimento_por_conferente, total_recebimento=total_recebimento)


@app.route('/recebimento/deletar/<int:id>', methods=['GET'])
@login_required
def recebimento_deletar(id):
    recebimento = Recebimento.query.get_or_404(id)
    if recebimento:
        db.session.delete(recebimento)
        db.session.commit()
        return redirect(url_for('index_recebimento'))
    return redirect(url_for('index_recebimento'))
