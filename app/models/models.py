from ..main import *
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo_do_produto = db.Column(db.Integer, nullable=False)
    nome_do_produto = db.Column(db.String(300), nullable=False)
    preco_do_produto = db.Column(db.DECIMAL(10, 2), nullable=False)
    codigo_de_barras = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f'<{self.nome_do_produto}>'

class Produto_Vencimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo_do_produto = db.Column(db.Integer, nullable=False)
    nome_do_produto = db.Column(db.String(300), nullable=False)
    quantidade = db.Column(db.DECIMAL(10, 2), nullable=False)
    data_de_vencimento = db.Column(db.Date)
    data_de_insercao = db.Column(db.Date)
    atualizacao = db.Column(db.Date)
    criador = db.Column(db.String(300), nullable=True)


class Produto_Avaria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo_do_produto = db.Column(db.Integer, nullable=False)
    nome_do_produto = db.Column(db.String(300), nullable=False)
    preco_do_produto = db.Column(db.DECIMAL(10, 2), nullable=False)
    quantidade = db.Column(db.DECIMAL(10, 2), nullable=False)
    preco_total = db.Column(db.DECIMAL(10, 2), nullable=False)
    data_de_insercao = db.Column(db.Date)
    criador = db.Column(db.String(300), nullable=True)
    tipodeavaria = db.Column(db.String(300), nullable=True)
    origem = db.Column(db.String(300), nullable=True)
    usoeconsumo = db.Column(db.String(300), nullable=True)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    acesso = db.Column(db.String(250), nullable=False)

class Volume_de_Vendas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo_do_produto = db.Column(db.Integer, nullable=False)
    mediames = db.Column(db.DECIMAL, nullable=False)

class Entrega(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_da_entrega = db.Column(db.Date, nullable=False)
    motorista = db.Column(db.String(250), nullable=False)
    caminhao = db.Column(db.String(250), nullable=False)
    ajudante = db.Column(db.String(250), nullable=False)
    conferente = db.Column(db.String(250), nullable=True)
    rota = db.Column(db.String(250), nullable=False)
    quantidade_de_entregas = db.Column(db.Integer, nullable=False)
    tempo_total = db.Column(db.Time, nullable=False)
    tempo_total_entrega = db.Column(db.Time, nullable=False)
    tempo_medio_total = db.Column(db.Time, nullable=False)
    tempo_medio_entrega = db.Column(db.Time, nullable=False)
    resultado_tempo = db.Column(db.String(250), nullable=False)
    reentregas = db.Column(db.Integer, nullable=True)
    entreganrealizadas = db.Column(db.Integer, nullable=True)
    odometro_inicial = db.Column(db.Integer, nullable=True)
    odometro_final = db.Column(db.Integer, nullable=True)
    rodagem = db.Column(db.Integer, nullable=True)

class Rotas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rota = db.Column(db.String(250), unique=True, nullable=False)
    tempo_medio_rota = db.Column(db.Time, nullable=False)


class Funcionarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(250), unique=True, nullable=False)
    funcao = db.Column(db.String(250), nullable=False)

    @classmethod
    def motorista(cls, nome):
        return cls(nome=nome, funcao='Motorista')

    @classmethod
    def ajudante(cls, nome):
        return cls(nome=nome, funcao='Ajudante')

    @classmethod
    def estoque(cls, nome):
        return cls(nome=nome, funcao='Estoque')

    @classmethod
    def vendedor(cls, nome):
        return cls(nome=nome, funcao='Vendedor')

    @classmethod
    def conferente(cls, nome):
        return cls(nome=nome, funcao='Conferente')

    @classmethod
    def faturista(cls, nome):
        return cls(nome=nome, funcao='Faturista')

class Erros_Vendas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_do_erro = db.Column(db.Date, nullable=False)
    erro_funcionario = db.Column(db.String(250), nullable=False)
    erro_cliente = db.Column(db.String(250), nullable=False)
    quantidade_de_erros = db.Column(db.Integer, nullable=False)
    motorista_da_entrega = db.Column(db.String(250), nullable=False)
    produto_erro = db.Column(db.String(250), nullable=False)
    descricao_do_erro = db.Column(db.String(1000), nullable=True)
    criador = db.Column(db.String(250), nullable=True)

class Erros_Logistica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_do_erro = db.Column(db.Date, nullable=False)
    erro_funcionario = db.Column(db.String(250), nullable=False)
    erro_cliente = db.Column(db.String(250), nullable=False)
    quantidade_de_erros = db.Column(db.Integer, nullable=False)
    motorista_da_entrega = db.Column(db.String(250), nullable=False)
    rota_da_entrega = db.Column(db.String(250), nullable=False)
    produto_erro = db.Column(db.String(250), nullable=False)
    descricao_do_erro = db.Column(db.String(1000), nullable=True)
    criador = db.Column(db.String(250), nullable=True)
    tipo_do_erro = db.Column(db.String(250), nullable=True)

class Erros_Atacado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_do_erro = db.Column(db.Date, nullable=False)
    erro_funcionario = db.Column(db.String(250), nullable=False)
    erro_cliente = db.Column(db.String(250), nullable=False)
    quantidade_de_erros = db.Column(db.Integer, nullable=False)
    produto_erro = db.Column(db.String(250), nullable=False)
    descricao_do_erro = db.Column(db.String(1000), nullable=True)
    criador = db.Column(db.String(250), nullable=True)

class Produto_Conferido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_conferencia = db.Column(db.Date, nullable=False)
    conferente = db.Column(db.String(250), nullable=False)
    codigo_produto = db.Column(db.String(250), nullable=False)
    nome_do_produto = db.Column(db.String(250), nullable=False)
    quantidade_sistema = db.Column(db.DECIMAL(10,3), nullable=False)
    quantidade_fisico = db.Column(db.DECIMAL(10,3), nullable=False)
    quantidade_diferenca= db.Column(db.DECIMAL(10,3), nullable=False)
    criador = db.Column(db.String(250), nullable=True)
    produto_trocado =  db.Column(db.Boolean, default=False, nullable=True)
    divergencia_sistema = db.Column(db.Boolean, default=False, nullable=True)
    produto_conferido_lojas= db.Column(db.Boolean, default=False, nullable=True)
    ajuste = db.Column(db.Boolean, default=False, nullable=True)

class Caminhao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identificao =  db.Column(db.Integer, nullable=False)
    placa =  db.Column(db.String(250), nullable=False)

class Recebimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_recebimento = db.Column(db.Date, nullable=False)
    conferente = db.Column(db.String(250), nullable=False)
    quantidade_notas = db.Column(db.Integer, nullable=False)
    estoques = db.Column(db.Boolean, nullable=False)
    prateleiras = db.Column(db.Boolean, nullable=False)
    produto_novo = db.Column(db.Boolean, nullable=False)
    criador = db.Column(db.String(250), nullable=True)
    foto = db.Column(db.String(250), nullable=True)

class Transferencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    comprador = db.Column(db.String(250), nullable=False)
    pedido = db.Column(db.Integer, nullable=False)
    loja = db.Column(db.String(250), nullable=False)
    tipo = db.Column(db.String(250), nullable=False)
    obs = db.Column(db.Text, nullable=True)
    criador = db.Column(db.String(250), nullable=False)

class Tipos_Transferencias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(250), unique=True, nullable=False)
