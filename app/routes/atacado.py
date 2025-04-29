from ..main import *


@app.route('/atacado/erros', methods=["GET", "POST"])
@access_level_required(1)
@login_required
def atacado_erros():
    erros = Erros_Atacado.query.filter(
        Erros_Atacado.data_do_erro >= primeiro_dia_mes(),
        Erros_Atacado.data_do_erro <= ultimo_dia_mes()
    ).order_by(
        Erros_Atacado.data_do_erro.desc()).all()

    erros_por_funcionario = db.session.query(
        Erros_Atacado.erro_funcionario,
        func.sum(Erros_Atacado.quantidade_de_erros).label('total_erros'),
    ).filter(
        Erros_Atacado.data_do_erro >= primeiro_dia_mes(),
        Erros_Atacado.data_do_erro <= ultimo_dia_mes()
    ).group_by(
        Erros_Atacado.erro_funcionario
    ).all()

    erros_por_funcionario = db.session.query(
        Erros_Atacado.erro_funcionario,
         func.sum(Erros_Atacado.quantidade_de_erros).label('total_erros'),
    ).filter(
        Erros_Atacado.data_do_erro >= primeiro_dia_mes(),
        Erros_Atacado.data_do_erro <= ultimo_dia_mes()
    ).group_by(
        Erros_Atacado.erro_funcionario
    ).all()


    return render_template("/atacado/erros.html", erros=erros, mes=mes_atual(), erros_por_funcionario=erros_por_funcionario)



@app.route('/atacado/cadastrar_erro', methods=["GET", "POST"])
@access_level_required(1)
@login_required
def cadastrar_atacado_erro():
    funcionarios = Funcionarios.query.filter_by(funcao='Conferente').all()
    if request.method == "POST":
        data_do_erro = request.form["data_do_erro"]
        erro_funcionario = request.form['erro_funcionario']
        erro_cliente = request.form['erro_cliente']
        quantidade_de_erros = request.form['quantidade_de_erros']
        produto_erro = request.form['produto_erro']
        descricao_do_erro = request.form['descricao_do_erro']
        criador = current_user.username
        erro = Erros_Atacado(data_do_erro=data_do_erro, erro_funcionario=erro_funcionario,
                               quantidade_de_erros=quantidade_de_erros, erro_cliente=erro_cliente,
                               produto_erro=produto_erro, descricao_do_erro=descricao_do_erro, criador=criador)
        db.session.add(erro)
        db.session.commit()
        return redirect(url_for("atacado_erros"))
    return render_template("/atacado/cadastrar_erro.html", funcionarios=funcionarios)


@app.route('/atacado/deletar_erro/<int:erro_id>', methods=["post", 'get'])
@login_required
def deletar_erro_atacado(erro_id):
    erro = Erros_Atacado.query.get_or_404(erro_id)
    db.session.delete(erro)
    db.session.commit()
    return redirect(url_for('atacado_erros'))




@app.route('/atacado/erros_relatorio', methods=["GET", "POST"])
@access_level_required(1)
@login_required
def atacado_erros_relatorio():
    if request.method == "POST":
        data_inicial = request.form["data_inicial"]
        data_final = request.form["data_final"]
        erros = Erros_Atacado.query.filter(
            Erros_Atacado.data_do_erro >= data_inicial,
            Erros_Atacado.data_do_erro <= data_final
        ).order_by(
            Erros_Atacado.data_do_erro.desc()).all()
        erros_por_funcionario = db.session.query(
            Erros_Atacado.erro_funcionario,
            func.sum(Erros_Atacado.quantidade_de_erros).label('total_erros')
        ).filter(
            Erros_Atacado.data_do_erro >= data_inicial,
            Erros_Atacado.data_do_erro <= data_final
        ).group_by(
            Erros_Atacado.erro_funcionario
        ).all()

        erros_por_funcionario = db.session.query(
            Erros_Atacado.erro_funcionario,
                func.sum(Erros_Atacado.quantidade_de_erros).label('total_erros'),
        ).filter(
            Erros_Atacado.data_do_erro >= data_inicial,
            Erros_Atacado.data_do_erro <= data_final
        ).group_by(
            Erros_Atacado.erro_funcionario
        ).all()

        return render_template("/atacado/emitir_erro_relatorio.html",
                               mes=mes_atual(),
                               erros=erros, erros_por_funcionario=erros_por_funcionario,
                               data_inicial=formatar_data(data_inicial), data_final=formatar_data(data_final),
                               )
    return render_template('atacado/relatorio_erro.html')

@app.route('/atacado/comparar_erros', methods=['GET', 'POST'])
def atacado_erros_comparar():
    if request.method == "POST":
        data_inicial_1 = request.form["data_inicial1"]
        data_final_1 = request.form["data_final1"]
        data_inicial_2 = request.form["data_inicial2"]
        data_final_2 = request.form["data_final2"]

        erros_por_funcionario = db.session.query(
            Erros_Atacado.erro_funcionario,
                func.sum(Erros_Atacado.quantidade_de_erros).label('total_erros'),
        ).filter(
            Erros_Atacado.data_do_erro >= data_inicial_1,
            Erros_Atacado.data_do_erro <= data_final_1
        ).group_by(
            Erros_Atacado.erro_funcionario
        ).all()

        erros_por_funcionario2 = db.session.query(
            Erros_Atacado.erro_funcionario,
                func.sum(Erros_Atacado.quantidade_de_erros).label('total_erros'),
        ).filter(
            Erros_Atacado.data_do_erro >= data_inicial_2,
            Erros_Atacado.data_do_erro <= data_final_2
        ).group_by(
            Erros_Atacado.erro_funcionario
        ).all()

        array_erros_por_funcionario = []
        for funcionario in erros_por_funcionario:
            for funcionario2 in erros_por_funcionario2:
                if funcionario.erro_funcionario == funcionario2.erro_funcionario:
                    total_erros = funcionario.total_erros + funcionario2.total_erros
                    percentual = calcular_porcentagem( funcionario.total_erros, funcionario2.total_erros)
                    array_erros_por_funcionario.append({'funcionario': funcionario.erro_funcionario,
                        'total_erros_1': funcionario.total_erros, 'total_erros_2': funcionario2.total_erros,
                        'total_erros': total_erros, 'percentual': percentual})

        array_totais = [{'total_erros1': funcionario.total_erros for funcionario in erros_por_funcionario},{
            'total_erros2': funcionario2.total_erros for funcionario2 in erros_por_funcionario2}]
        array_totais.append({'porcentagem': calcular_porcentagem(array_totais[0]['total_erros1'], array_totais[1]['total_erros2'])})
        data_grafico = [array_totais[0]['total_erros1'], array_totais[1]['total_erros2']]

        return render_template('atacado/comparar_erros.html', data_inicial1=formatar_data(data_inicial_1),
        data_final1=formatar_data(data_final_1),array_totais=array_totais, data_inicial2=formatar_data(data_inicial_2),
        data_final2=formatar_data(data_final_2), data_grafico=data_grafico, array_erros_por_funcionario=array_erros_por_funcionario, erros_por_funcionario=erros_por_funcionario,
        erros_por_funcionario2=erros_por_funcionario2, )
    return render_template('atacado/comparar_erros.html')
