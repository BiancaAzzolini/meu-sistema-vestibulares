from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vestibulares.db'
db = SQLAlchemy(app)

class Prova(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_insc = db.Column(db.String(10), nullable=True)
    data = db.Column(db.String(10), nullable=True)
    hora = db.Column(db.String(10), nullable=True)
    local = db.Column(db.String(100), nullable=True)
    pontuacao_data = db.Column(db.String(10), nullable=True)
    pont_prova = db.Column(db.String(10), nullable=True)
    total_prova = db.Column(db.String(10), nullable=True)

class Simulado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    pontuacao = db.Column(db.String(10), nullable=True)
    total = db.Column(db.String(10), nullable=True)

class QuestaoProva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    cor = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(10), nullable=False) 
    materia = db.Column(db.String(50), nullable=False)
    assunto = db.Column(db.String(50), nullable=True)
    pont = db.Column(db.String(50), nullable=True)
    tot = db.Column(db.String(50), nullable=True)
    prova_id = db.Column(db.Integer, db.ForeignKey("prova.id"), nullable=False)

    prova = db.relationship("Prova", backref=db.backref("questoes", lazy=True))

class QuestaoSimulado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    cor = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(10), nullable=False)
    materia = db.Column(db.String(50), nullable=False)
    assunto = db.Column(db.String(50), nullable=True)
    pont = db.Column(db.String(50), nullable=True)
    tot = db.Column(db.String(50), nullable=True)
    simulado_id = db.Column(db.Integer, db.ForeignKey("simulado.id"), nullable=False)

    simulado = db.relationship("Simulado", backref=db.backref("questoes", lazy=True))

class Estatistica(db.Model):
    id = db.Column(db.Integer, primary_key=True)


with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/provas", methods=["GET", "POST"])
def provas():
    if request.method == "POST":
        nome = request.form["nome"]
        data_insc = request.form.get("data_insc") or None
        data = request.form.get("data") or None
        hora = request.form.get("hora") or None
        local = request.form.get("local") or None
        pontuacao_data = request.form.get("pontuacao_data") or None
        pont_prova = request.form.get("pont_prova") or None
        total_prova = request.form.get("total_prova") or None

        nova_prova = Prova(nome=nome, data_insc=data_insc, data=data, hora=hora, local=local, pontuacao_data=pontuacao_data, pont_prova=pont_prova, total_prova=total_prova)
        db.session.add(nova_prova)
        db.session.commit()

        return redirect("/provas")

    provas_lista = Prova.query.all()
    return render_template("provas.html", provas=provas_lista)

@app.route("/excluir_prova/<int:id>", methods=["POST"])
def excluir_prova(id):
    prova = Prova.query.get(id)
    if prova:
        db.session.delete(prova)
        db.session.commit()
    return redirect("/provas")

@app.route("/excluir_questao_pr/<int:id>/<int:prova_id>", methods=["POST"])
def excluir_questao_pr(id, prova_id):
    questao = QuestaoProva.query.get(id)
    if questao:
        db.session.delete(questao)
        db.session.commit()
    return redirect(url_for("questoes_prova", prova_id=prova_id))

@app.route('/questoes_prova/<int:prova_id>', methods=['GET', 'POST'])
def questoes_prova(prova_id):
    prova = Prova.query.get_or_404(prova_id)

    if request.method == 'POST':
        numero = request.form['numero']
        cor = request.form.get("cor") or None
        status = request.form['status'] 
        materia = request.form.get("materia")
        assunto = request.form.get("assunto") or None
        pont = request.form.get("pont") or None
        tot = request.form.get("tot") or None

        nova_questao = QuestaoProva(numero=numero, cor=cor, status=status, materia=materia, assunto=assunto, pont=pont, tot=tot, prova_id=prova.id)
        db.session.add(nova_questao)
        db.session.commit()
        return redirect(url_for('questoes_prova', prova_id=prova.id))

    questoes = QuestaoProva.query.filter_by(prova_id=prova.id).order_by(QuestaoProva.numero).all()  # Filtrando questões do simulado certo
    return render_template('questoes_prova.html', prova=prova, questoes=questoes)

@app.route('/editar_prova/<int:id>', methods=['GET'])
def editar_prova(id):
    prova = Prova.query.get_or_404(id) 
    return render_template('editar_prova.html', prova=prova) 

@app.route('/editar_prova/<int:id>', methods=['POST'])
def salvar_edicao1(id):
    prova = Prova.query.get_or_404(id)

    prova.nome = request.form["nome"]
    prova.data_insc = request.form.get("data_insc") or None
    prova.data = request.form.get("data") or None
    prova.hora = request.form.get("hora") or None
    prova.local = request.form.get("local") or None
    prova.pontuacao_data = request.form.get("pontuacao_data") or None
    prova.pont_prova = request.form.get("pont_prova") or None
    prova.total_prova = request.form.get("total_prova") or None 

    db.session.commit()
    return redirect(url_for('provas'))

@app.route('/adicionar_prova', methods=['POST'])
def adicionar_prova():
    nome = request.form['nome']
    nova_prova = Prova(nome=nome)
    db.session.add(nova_prova)
    db.session.commit()
    
    return redirect(url_for('questoes_prova', prova_id=nova_prova.id))


@app.route("/simulados", methods=["GET", "POST"])
def simulados():
    if request.method == "POST":
        nome = request.form["nome"]
        pontuacao = request.form.get("pontuacao") or None
        total = request.form.get("total") or None

        novo_simulado = Simulado(nome=nome, pontuacao=pontuacao, total=total)
        db.session.add(novo_simulado)
        db.session.commit()

        return redirect("/simulados")

    simulados_lista = Simulado.query.all()
    return render_template("simulados.html", simulados=simulados_lista)

@app.route("/excluir_simulado/<int:id>", methods=["POST"])
def excluir_simulado(id):
    simulado = Simulado.query.get(id)
    if simulado:
        db.session.delete(simulado)
        db.session.commit()
    return redirect("/simulados")

@app.route("/excluir_questao_sm/<int:id>/<int:simulado_id>", methods=["POST"])
def excluir_questao_sm(id, simulado_id):
    questao = QuestaoSimulado.query.get(id)
    if questao:
        db.session.delete(questao)
        db.session.commit()
    return redirect(url_for("questoes_simulado", simulado_id=simulado_id))

@app.route('/questoes_simulado/<int:simulado_id>', methods=['GET', 'POST'])
def questoes_simulado(simulado_id):
    simulado = Simulado.query.get_or_404(simulado_id)

    if request.method == 'POST':
        numero = request.form['numero']
        cor = request.form.get("cor") or None
        status = request.form['status'] 
        materia = request.form.get("materia")
        assunto = request.form.get("assunto") or None
        pont = request.form.get("pont") or None
        tot = request.form.get("tot") or None

        nova_questao = QuestaoSimulado(numero=numero, cor=cor, status=status, materia=materia, assunto=assunto, pont=pont, tot=tot, simulado_id=simulado.id)
        db.session.add(nova_questao)
        db.session.commit()
        return redirect(url_for('questoes_simulado', simulado_id=simulado.id))

    questoes = QuestaoSimulado.query.filter_by(simulado_id=simulado.id).order_by(QuestaoSimulado.numero).all()  # Filtrando questões do simulado certo
    return render_template('questoes_simulado.html', simulado=simulado, questoes=questoes)

@app.route('/editar_simulado/<int:id>', methods=['GET'])
def editar_simulado(id):
    simulado = Simulado.query.get_or_404(id) 
    return render_template('editar_simulado.html', simulado=simulado) 

@app.route('/editar_simulado/<int:id>', methods=['POST'])
def salvar_edicao2(id):
    simulado = Simulado.query.get_or_404(id)

    simulado.nome = request.form["nome"]
    simulado.pontuacao = request.form.get("pontuacao") or None
    simulado.total = request.form.get("total") or None

    db.session.commit()
    return redirect(url_for('simulados'))

@app.route('/adicionar_simulado', methods=['POST'])
def adicionar_simulado():
    nome = request.form['nome']
    novo_simulado = Simulado(nome=nome)
    db.session.add(novo_simulado)
    db.session.commit()
    
    return redirect(url_for('questoes_simulado', simulado_id=novo_simulado.id))


@app.route('/estatisticas')
def estatisticas():
    estatisticas_simulados = {}
    estatisticas_gerais = {}

    simulados = Simulado.query.all()

    for simulado in simulados:
        estatisticas_simulados[simulado.nome] = {}

        questoes = QuestaoSimulado.query.filter_by(simulado_id=simulado.id).all()

        for questao in questoes:
            materia = questao.materia
            assunto = questao.assunto if questao.assunto else "Sem Assunto"

            # Estatísticas por simulado
            if materia not in estatisticas_simulados[simulado.nome]:
                estatisticas_simulados[simulado.nome][materia] = {}

            if assunto not in estatisticas_simulados[simulado.nome][materia]:
                estatisticas_simulados[simulado.nome][materia][assunto] = {'total': 0, 'acertos': 0}

            estatisticas_simulados[simulado.nome][materia][assunto]['total'] += 1
            if questao.status == "correto":
                estatisticas_simulados[simulado.nome][materia][assunto]['acertos'] += 1

            # Estatísticas gerais (somando tudo)
            if materia not in estatisticas_gerais:
                estatisticas_gerais[materia] = {}

            if assunto not in estatisticas_gerais[materia]:
                estatisticas_gerais[materia][assunto] = {'total': 0, 'acertos': 0}

            estatisticas_gerais[materia][assunto]['total'] += 1
            if questao.status == "correto":
                estatisticas_gerais[materia][assunto]['acertos'] += 1

        # Ordenando os assuntos dentro de cada simulado pela porcentagem de acertos
        for simulado in estatisticas_simulados:
            for materia in estatisticas_simulados[simulado]:
                estatisticas_simulados[simulado][materia] = dict(sorted(
                    estatisticas_simulados[simulado][materia].items(),
                    key=lambda item: (item[1]['acertos'] / item[1]['total']) if item[1]['total'] > 0 else 0,
                    reverse=True
                ))

        # Ordenando os assuntos gerais pela porcentagem de acertos
        for materia in estatisticas_gerais:
            estatisticas_gerais[materia] = dict(sorted(
                estatisticas_gerais[materia].items(),
                key=lambda item: (item[1]['acertos'] / item[1]['total']) if item[1]['total'] > 0 else 0,
                reverse=True
            ))


    return render_template('estatisticas.html', estatisticas_simulados=estatisticas_simulados, estatisticas_gerais=estatisticas_gerais)



def formatar_data(data_str):
    if data_str:  # Verifica se a data existe
        return datetime.strptime(data_str, '%Y-%m-%d').strftime('%d/%m/%Y')
    return ''
 
app.jinja_env.filters['datetimeformat'] = formatar_data


if __name__ == "__main__":
    app.run(debug=True)
