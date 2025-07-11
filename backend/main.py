


from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime, timezone, timedelta
import os
from werkzeug.utils import secure_filename
from openai import OpenAI
from models import db, Aluno, Projeto, Setor, Atividade, Atividadealuno, init_db

app = Flask(__name__)

# Configuração para o Railway PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@localhost:5432/npdeas"
app.config['SECRET_KEY'] = "1234"
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Inicializa o banco de dados
init_db(app)

CORS(app)
# Certifique-se de que a pasta de uploads existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Teste de conexão com o banco de dados


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# [Todas as suas rotas existentes continuam aqui...]
# (Copie todas as rotas do seu arquivo original a partir daqui)





# Rotas para upload de imagens
@app.route('/upload/<entity_type>/<int:entity_id>', methods=['POST'])
def upload_file(entity_type, entity_id):
    if 'file' not in request.files:
        return jsonify({'message': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']    
    if file.filename == '':
        return jsonify({'message': 'Nenhum arquivo selecionado'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{entity_type}_{entity_id}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Atualizar a entidade com o caminho da imagem
        if entity_type == 'aluno':
            entity = Aluno.query.get(entity_id)
        elif entity_type == 'projeto':
            entity = Projeto.query.get(entity_id)
        elif entity_type == 'setor':
            entity = Setor.query.get(entity_id)
        elif entity_type == 'atividade':
            entity = Atividade.query.get(entity_id)
        else:
            return jsonify({'message': 'Tipo de entidade inválido'}), 400
        
        if not entity:
            return jsonify({'message': 'Entidade não encontrada'}), 404
        
        # Remove a imagem antiga se existir
        if entity.image_path and os.path.exists(entity.image_path):
            os.remove(entity.image_path)
        
        entity.image_path = filepath
        db.session.commit()
        
        return jsonify({'message': 'Arquivo enviado com sucesso', 'filename': filename}), 200
    else:
        return jsonify({'message': 'Tipo de arquivo não permitido'}), 400

@app.route('/images/<filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Atualizar as rotas existentes para incluir informações de imagem nas respostas
@app.route('/alunos/<int:id>', methods=['GET'])
def get_aluno_by_id(id):
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({'message': 'Aluno não encontrado!'}), 404
    
    aluno_data = {
        'id': aluno.id,
        'nome': aluno.nome,
        'email': aluno.email,
        'setor_id': aluno.setor_id,
        'idade': aluno.idade,
        'bolsista': aluno.bolsista,
        'admin': aluno.admin,
        'ano_entrada': aluno.ano_entrada,
        'linkedin': aluno.linkedin,
        'preferencia': aluno.preferencia,
        'wats': aluno.wats,
        'image_url': f"/images/{os.path.basename(aluno.image_path)}" if aluno.image_path else None
    }
    return jsonify(aluno_data), 200

@app.route('/projetos/<int:id>', methods=['GET'])
def get_projeto_by_id(id):
    projeto = Projeto.query.get(id)
    if not projeto:
        return jsonify({'message': 'Projeto não encontrado!'}), 404
    
    projeto_data = {
        'id': projeto.id,
        'nome': projeto.nome,
        'descricao': projeto.descricao,
        'responsavel': projeto.responsavel,
        'image_url': f"/images/{os.path.basename(projeto.image_path)}" if projeto.image_path else None
    }
    return jsonify(projeto_data), 200

@app.route('/setores/<int:id>', methods=['GET'])
def get_setor_by_id(id):
    setor = Setor.query.get(id)
    if not setor:
        return jsonify({'message': 'Setor não encontrado!'}), 404
    
    setor_data = {
        'id': setor.id,
        'nome': setor.nome,
        'descricao': setor.descricao,
        'projeto_id': setor.projeto_id,
        'image_url': f"/images/{os.path.basename(setor.image_path)}" if setor.image_path else None
    }
    return jsonify(setor_data), 200

@app.route('/atividades/<int:id>', methods=['GET'])
def get_atividade_by_id(id):
    atividade = Atividade.query.get(id)
    if not atividade:
        return jsonify({'message': 'Atividade não encontrada!'}), 404
    
    atividade_data = {
        'id': atividade.id,
        'setor_id': atividade.setor_id,
        'descricao': atividade.descricao,
        'data_inicio': atividade.data_inicio,
        'data_fim_previsto': atividade.data_fim_previsto,
        'data_fim_real': atividade.data_fim_real,
        'status': atividade.status,
        'nivel': atividade.nivel,
        'image_url': f"/images/{os.path.basename(atividade.image_path)}" if atividade.image_path else None
    }
    return jsonify(atividade_data), 200




@app.route('/atividades/<int:atividade_id>/alunos', methods=['GET'])
def get_alunos_por_atividade(atividade_id):

    print(atividade_id)
    alunos = Aluno.query.join(Atividadealuno).filter(Atividadealuno.atividade_id == atividade_id).all()

    resultado = [
        {'id': aluno.id, 'nome': aluno.nome, 'email': aluno.email}
        for aluno in alunos
    ]
    print(resultado)


    return jsonify(resultado)

@app.route('/setores', methods=['POST'])
def setores():
    data = request.json
    setor = Setor(
        nome=data['nome'], descricao=data['descricao'], projeto_id=data['projeto_id']
    )
    db.session.add(setor)
    db.session.commit()
    return jsonify({'message': 'setor criado com sucesso!'}), 201



@app.route('/projetos', methods=['POST'])
def projetos():
    data = request.json
    proejto = Projeto(
        nome=data['nome'], descricao=data['descricao'], responsavel=data['responsavel']
    )
    db.session.add(proejto)
    db.session.commit()
    return jsonify({'id': proejto.id}), 201



@app.route('/register', methods=['POST'])
def register():
    data = request.json
    aluno = Aluno(
        nome=data['nome'], email=data['email'], setor_id=data.get('setor_id'), 
        senha=data['senha'], idade=data['idade'], bolsista=data.get('bolsista', False),   preferencia=data['preferencia'],
        ano_entrada=data['ano_entrada'], linkedin=data.get('linkedin'), wats=data.get('wats'), admin=data.get('admin', False)
    )
    db.session.add(aluno)
    db.session.commit()
    return jsonify({'id': aluno.id}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    aluno = Aluno.query.filter_by(email=data['email']).first()
    
    if aluno and aluno.senha == data['senha']:
        # Inicializa as variáveis como None
        setor_nome = None
        projeto_nome = None
        
        # Se o aluno tem um setor, busca as informações
        if aluno.setor_id:
            setor = Setor.query.get(aluno.setor_id)
            if setor:
                setor_nome = setor.nome
                # Busca o projeto relacionado ao setor
                projeto = Projeto.query.get(setor.projeto_id)
                if projeto:
                    projeto_nome = projeto.nome
        
        return jsonify({
            'id': aluno.id,
            'nome': aluno.nome,
            'email': aluno.email,
            'setorid': aluno.setor_id,
            'setor_nome': setor_nome,
            'projeto_nome': projeto_nome,
            'image_url': f"/images/{os.path.basename(aluno.image_path)}" if aluno.image_path else None
        })
    
    return jsonify({'message': 'Credenciais inválidas'}), 401






@app.route('/atividades', methods=['POST'])
def criar_atividade():
    data = request.json
    atividade = Atividade(
        setor_id=data['setor_id'], descricao=data['descricao'],
        data_fim_previsto=datetime.strptime(data['data_fim_previsto'], '%Y-%m-%d'),
        data_inicio= datetime.now(timezone.utc), status='Pendente', nivel=data['nivel']
    )
    db.session.add(atividade)
    db.session.commit()
    return jsonify({'message': 'Atividade criada com sucesso!'}), 201


@app.route('/atividades/<int:atividade_id>/status', methods=['GET'])
def mudar_status_atividade(atividade_id): 
    print(atividade_id)
    atividade = Atividade.query.filter_by(id=atividade_id).first()
    print(atividade)
    atividade.status = 'concluída'
    atividade.data_fim_real = datetime.now(timezone.utc)  # Método atualizado
    db.session.commit()
    return jsonify({'message': 'Status atualizado com sucesso!'}), 200



@app.route('/atividades/<int:atividade_id>/aluno', methods=['POST'])
def adicionar_aluno_atividade(atividade_id):
    data = request.json
    relacao = Atividadealuno(atividade_id=atividade_id, aluno_id=data['aluno_id'])
    db.session.add(relacao)
    db.session.commit()
    return jsonify({'message': 'Aluno adicionado à atividade!'}), 201


@app.route('/atividadesbyaluno/<int:aluno_id>', methods=['GET'])
def getatvbyaluno(aluno_id):
    # Corrigindo o nome da variável e os campos acessados
    print(aluno_id)
    atividades = Atividade.query.join(Atividadealuno).filter(Atividadealuno.aluno_id == aluno_id).all()
    
    resultado = [
        {
            'id': atividade.id, 
            'descricao': atividade.descricao,
            'data_inicio': atividade.data_inicio,
            'data_fim_previsto': atividade.data_fim_previsto,
            'status': atividade.status,
            'data_fim_real': atividade.data_fim_real,
            'nivel': atividade.nivel
        }
        for atividade in atividades
    ]
    
    print(resultado)

    return jsonify(resultado)


#tirar aluno da atividade   
@app.route('/atividades/<int:atividade_id>/aluno/<int:aluno_id>', methods=['DELETE'])
def remover_aluno_atividade(atividade_id, aluno_id):
    relacao = Atividadealuno.query.filter_by(atividade_id=atividade_id, aluno_id=aluno_id).first()
    if relacao:
        db.session.delete(relacao)
        db.session.commit()
        return jsonify({'message': 'Aluno removido da atividade!'}), 200
    return jsonify({'message': 'Relação não encontrada!'}), 404

@app.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = Aluno.query.all()
    return jsonify([{'id': a.id, 'nome': a.nome, 'email': a.email} for a in alunos])

@app.route('/atividades', methods=['GET'])
def get_atividades():
    atividades = Atividade.query.all()
    return jsonify([
        {'id': at.id, 'descricao': at.descricao, 'status': at.status, 'data_inicio': at.data_inicio, 'data_fim_real': at.data_fim_real, 'nivel':at.nivel}
        for at in atividades])

@app.route('/setores', methods=['GET'])
def get_setores():
    atividades = Setor.query.all()
    return jsonify([
        {'id': at.id, 'descricao': at.descricao, 'nome': at.nome}
        for at in atividades])

@app.route('/projetos', methods=['GET'])
def get_projetos():
    atividades = Projeto.query.all()
    return jsonify([
        {'id': at.id, 'descricao': at.descricao, 'nome': at.nome, 'image_url': f"/images/{os.path.basename(at.image_path)}" if at.image_path else None}
        for at in atividades])





@app.route('/setoresbyp/<int:projetoid>', methods=['GET'])
def setoresbyp(projetoid):
    atividades = Setor.query.filter_by(projeto_id=projetoid).all()
    return jsonify([
        {'id': at.id, 'nome': at.nome, 'descricao': at.descricao}
        for at in atividades])



@app.route('/atividades/setor/<int:setor_id>', methods=['GET'])
def get_atividades_por_setor(setor_id):
    atividades = Atividade.query.filter_by(setor_id=setor_id).all()
    return jsonify([
        {'id': at.id, 'descricao': at.descricao, 'status': at.status, 'data_inicio': at.data_inicio, 'data_fim_real': at.data_fim_real, 'nivel': at.nivel}
        for at in atividades])

        
@app.route('/alunos/horas', methods=['GET'])
def get_horas_trabalhadas_todos():
    alunos = Aluno.query.all()
    resultado = []
    
    for aluno in alunos:
        atividades = Atividade.query.join(Atividadealuno).filter(
            Atividadealuno.aluno_id == aluno.id, 
            Atividade.data_fim_real != None
        ).all()
        
        total_horas = sum([
            (at.data_fim_real - at.data_inicio).total_seconds() / 3600 
            for at in atividades if at.data_fim_real
        ])
        
        # Obter informações do setor e projeto
        setor_nome = None
        projeto_nome = None
        projeto_id = None
        
        if aluno.setor_id:
            setor = Setor.query.get(aluno.setor_id)
            if setor:
                setor_nome = setor.nome
                # Busca o projeto relacionado ao setor
                projeto = Projeto.query.get(setor.projeto_id)
                if projeto:
                    projeto_nome = projeto.nome
                    projeto_id = projeto.id
        
        resultado.append({
            'aluno_id': aluno.id,
            'nome': aluno.nome,
            'email': aluno.email,
            'setor_id': aluno.setor_id,
            'setor_nome': setor_nome,
            'projeto_id': projeto_id,
            'projeto_nome': projeto_nome,
            'horas_trabalhadas': total_horas,
            'horas_meta': aluno.horas_semana  # Corrigido: usando aluno em vez de alunos
        })
    
    return jsonify(resultado)

@app.route('/alunos/setor/<int:setor_id>', methods=['GET'])
def get_alunos_por_setor(setor_id):
    alunos = Aluno.query.filter_by(setor_id=setor_id).all()
    
    resultado = [
        {'id': aluno.id, 'nome': aluno.nome, 'email': aluno.email}
        for aluno in alunos
    ]
    
    return jsonify(resultado)



#adicionar alunos a uma atividade recem criada
@app.route('/atividades/comalunos', methods=['POST'])
def criar_atividade_com_alunos():
    data = request.json
    
    # Criando a atividade
    atividade = Atividade(
        setor_id=data['setor_id'],
        descricao=data['descricao'],
        data_fim_previsto=datetime.strptime(data['data_fim_previsto'], '%d/%m/%Y'),
        data_inicio= datetime.now(timezone.utc),
        status='Pendente',
        nivel=data['nivel']
    )
    db.session.add(atividade)
    db.session.commit()
    
    # Adicionando alunos à atividade
    alunos_ids = data['alunos']

    print('sasas', alunos_ids)


    for aluno_id in alunos_ids:
        relacao = Atividadealuno(atividade_id=atividade.id, aluno_id=aluno_id)
        db.session.add(relacao)
    
    db.session.commit()
    
    return jsonify({'message': 'Atividade criada e alunos adicionados com sucesso!', 'atividade_id': atividade.id}), 201



@app.route('/projeto/comsetoresalunos', methods=['POST'])
def criar_projeto_com_setores_e_alunos():
    data = request.json
    
    # Criando o projeto
    projeto = Projeto(
        nome=data['nome'],
        descricao=data['descricao'],
        responsavel= 'Andre',
     
    )
    db.session.add(projeto)
    db.session.commit()
    
    # Criando setores do projeto
    setores = data['setores']  # A lista de setores passados no parâmetro
    for setor_data in setores:
        setor = Setor(
            nome=setor_data['nome'],
            descricao=setor_data['descricao'],
            projeto_id=projeto.id  # Relacionando o setor ao projeto criado
        )
        db.session.add(setor)
        db.session.commit()
        
       

    db.session.commit()
    
    return jsonify({'message': 'Projeto, setores e alunos criados com sucesso!', 'projeto_id': projeto.id}), 201


@app.route('/alunos/setor-null', methods=['GET'])
def alunos_sem_setor():
    # Consultando os alunos com setor_id como null
    alunos = Aluno.query.filter_by(setor_id=None).all()
    
    # Transformando os resultados em um formato adequado para o JSON
    alunos_data = []
    for aluno in alunos:
        alunos_data.append({
            'id': aluno.id,
            'nome': aluno.nome,
            'email': aluno.email,
            'setor_id': aluno.setor_id
        })
    
    return jsonify({'alunos_sem_setor': alunos_data}), 200



@app.route('/alunos/adicionar/setor', methods=['POST'])
def adicionar_aluno_a_setor():
    data = request.json
    
    aluno_id = data['aluno_id']
    setor_id = data['setor_id']
    horas = data['horas']
    
    # Buscando o aluno pelo ID
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return jsonify({'message': 'Aluno não encontrado!'}), 404
    
    # Buscando o setor pelo ID
    setor = Setor.query.get(setor_id)
    if not setor:
        return jsonify({'message': 'Setor não encontrado!'}), 404
    
    # Atribuindo o aluno ao setor
    aluno.setor_id = setor_id
    aluno.horas_semana = horas
    db.session.commit()

    return jsonify({'message': f'Aluno {aluno.nome} adicionado ao setor {setor.nome} com sucesso!'}), 200













#------------------- INDICADORES ---------------------


# Rotas para os gráficos do dashboard
@app.route('/dashboard/horas-por-projeto', methods=['GET'])
def horas_por_projeto():
    # Calcula horas trabalhadas por projeto
    projetos = Projeto.query.all()
    resultado = []
    
    for projeto in projetos:
        # Encontra todas as atividades relacionadas aos setores do projeto
        atividades = Atividade.query.join(Setor).filter(Setor.projeto_id == projeto.id).all()
        for i in atividades:
            print(i.data_fim_real, i.data_inicio)
        total_horas = sum([
            (at.data_fim_real - at.data_inicio).total_seconds() / 3600 
            for at in atividades if at.data_fim_real
        ])
        
        resultado.append({
            'nome': projeto.nome,
            'horas': round(total_horas, 2)
        })
    
    return jsonify(resultado)

@app.route('/dashboard/distribuicao-atividades', methods=['GET'])
def distribuicao_atividades():
    # Agrupa atividades por status
    atividades = Atividade.query.all()
    
    status_counts = {
        'Concluído': 0,
        'Em Andamento': 0,
        'Pendente': 0
    }
    
    for at in atividades:
        if at.status.lower() == 'concluída':
            status_counts['Concluído'] += 1
        elif at.status.lower() == 'em andamento':
            status_counts['Em Andamento'] += 1
        else:
            status_counts['Pendente'] += 1
    
    return jsonify(status_counts)

@app.route('/dashboard/ranking-alunos', methods=['GET'])
def ranking_alunos():
    # Ranking de alunos por horas trabalhadas
    alunos = Aluno.query.all()
    resultado = []
    
    for aluno in alunos:
        atividades = Atividade.query.join(Atividadealuno).filter(
            Atividadealuno.aluno_id == aluno.id, 
            Atividade.data_fim_real != None
        ).all()
        
        total_horas = sum([
            (at.data_fim_real - at.data_inicio).total_seconds() / 3600 
            for at in atividades if at.data_fim_real
        ])
        
        resultado.append({
            'nome': aluno.nome,
            'horas': round(total_horas, 2),
            'setor': aluno.setor_id if aluno.setor_id else 'Sem setor'
        })
    
    # Ordena por horas (decrescente)
    resultado.sort(key=lambda x: x['horas'], reverse=True)
    
    return jsonify(resultado[:10])  # Retorna apenas os top 10




@app.route('/dashboard/atividades-recentes', methods=['GET'])
def atividades_recentes():
    # Últimas atividades concluídas
    atividades = Atividade.query.filter(
        Atividade.status == 'concluída'
    ).order_by(
        Atividade.data_fim_real.desc()
    ).limit(5).all()
    
    resultado = []
    
    for at in atividades:
        # Obtém os alunos associados à atividade
        alunos = Aluno.query.join(Atividadealuno).filter(
            Atividadealuno.atividade_id == at.id
        ).all()
        
        # Obtém o projeto relacionado
        setor = Setor.query.get(at.setor_id)
        projeto = Projeto.query.get(setor.projeto_id) if setor else None

        resultado.append({
            'nome': at.descricao[:30] + ('...' if len(at.descricao) > 30 else ''),
            'descricao': at.descricao,
            'horas': round((at.data_fim_real - at.data_inicio).total_seconds() / 3600, 2),
            'data': at.data_fim_real.strftime('%Y-%m-%d'),
            'projeto': projeto.nome if projeto else 'Sem projeto',
            'alunos': [
                {
                    'nome': aluno.nome,
                    'img_url': f"/images/{os.path.basename(aluno.image_path)}" if aluno.image_path else None
                }
                for aluno in alunos
            ]
        })
    
    return jsonify(resultado)




# @app.route('/dashboard/atividades-recentes2', methods=['GET'])
# def atividades_recentes2():
#     # Data de 10 dias atrás
#     dez_dias_atras = datetime.now() - timedelta(days=10)
    
#     # Todas as atividades dos últimos 10 dias
#     atividades = Atividade.query.filter(
#         Atividade.data_inicio >= dez_dias_atras
#     ).order_by(
#         Atividade.data_inicio.desc()
#     ).all()
    
#     resultado = []
    
#     for at in atividades:
#         # Determina o status com base nas datas
#         status = at.status.lower()
#         data_atual = datetime.now()
        
#         if status == 'concluída':
#             status_class = 'concluída'
#         else:
#             if at.data_fim_previsto and at.data_fim_previsto < data_atual:
#                 status_class = 'atrasada'
#             else:
#                 status_class = 'pendente'
        
#         # Obtém os alunos associados à atividade
#         alunos = Aluno.query.join(Atividadealuno).filter(
#             Atividadealuno.atividade_id == at.id
#         ).all()
        
#         # Obtém o setor e projeto relacionados
#         setor = Setor.query.get(at.setor_id)
#         projeto = Projeto.query.get(setor.projeto_id) if setor else None
        
#         # Calcula horas (usando data_fim_real se concluída, ou estimativa se pendente/atrasada)
#         if status_class == 'concluída' and at.data_fim_real:
#             horas = round((at.data_fim_real - at.data_inicio).total_seconds() / 3600, 2)
#         else:
#             # Para atividades não concluídas, usa a duração prevista
#             horas = round((at.data_fim_previsto - at.data_inicio).total_seconds() / 3600, 2) if at.data_fim_previsto else 0
        
#         resultado.append({
#             'id': at.id,
#             'nome': at.descricao[:30] + ('...' if len(at.descricao) > 30 else ''),
#             'descricao': at.descricao,
#             'horas': horas,
#             'data_inicio': at.data_inicio.strftime('%Y-%m-%d %H:%M'),
#             'data_fim_previsto': at.data_fim_previsto.strftime('%Y-%m-%d %H:%M') if at.data_fim_previsto else None,
#             'data_fim_real': at.data_fim_real.strftime('%Y-%m-%d %H:%M') if at.data_fim_real else None,
#             'status': status_class,  # Adiciona o status calculado
#             'projeto': projeto.nome if projeto else 'Sem projeto',
#             'setor_image_url': setor.image_path if setor and setor.image_path else None,
#             'alunos': [
#                 {
#                     'nome': aluno.nome,
#                     'img_url': f"/images/{os.path.basename(aluno.image_path)}" if aluno.image_path else None
#                 }
#                 for aluno in alunos
#             ]
#         })
    
#     return jsonify(resultado)


@app.route('/dashboard/atividades-recentes2', methods=['GET'])
def atividades_recentes2():
    dez_dias_atras = datetime.now() - timedelta(days=10)
    data_atual = datetime.now()
    
    atividades = Atividade.query.filter(
        Atividade.data_inicio >= dez_dias_atras
    ).order_by(
        Atividade.data_inicio.desc()
    ).all()
    
    resultado = []
    
    for at in atividades:
        # Classificação do status
        if at.status.lower() == 'concluída':
            status_class = 'concluída'
        elif at.data_fim_previsto and at.data_fim_previsto < data_atual:
            status_class = 'atrasada'
        else:
            status_class = 'pendente'
        
        # Processamento da duração/tempo
        duracao_formatada = ""
        if status_class == 'concluída':
            if at.data_fim_real:
                segundos = (at.data_fim_real - at.data_inicio).total_seconds()
                duracao_formatada = formatar_duracao(segundos)
            else:
                duracao_formatada = "Duração não registrada"
                
        elif status_class == 'pendente':
            if at.data_fim_previsto:
                segundos_restantes = (at.data_fim_previsto - data_atual).total_seconds()
                if segundos_restantes > 0:
                    duracao_formatada = f"Faltam {formatar_duracao(segundos_restantes)}"
                else:
                    duracao_formatada = "Prazo finalizado agora"
            else:
                duracao_formatada = "Sem prazo definido"
                
        elif status_class == 'atrasada':
            if at.data_fim_previsto:
                dias_atraso = (data_atual - at.data_fim_previsto).total_seconds() / 86400
                duracao_formatada = f"Atrasada {round(dias_atraso, 1)} dias"
            else:
                duracao_formatada = "Atrasada (sem prazo definido)"
        
        # Restante do código (alunos, setor, projeto...)
        alunos = Aluno.query.join(Atividadealuno).filter(
            Atividadealuno.atividade_id == at.id
        ).all()
        
        setor = Setor.query.get(at.setor_id)
        projeto = Projeto.query.get(setor.projeto_id) if setor else None
        
        resultado.append({
            'id': at.id,
            'nome': at.descricao[:30] + ('...' if len(at.descricao) > 30 else ''),
            'descricao': at.descricao,
            'tempo': duracao_formatada,  # Campo renomeado para refletir os diferentes tipos
            'status': status_class,
            'data_inicio': at.data_inicio.strftime('%d/%m/%Y %H:%M'),
            'data_fim_previsto': at.data_fim_previsto.strftime('%d/%m/%Y %H:%M') if at.data_fim_previsto else None,
            'data_fim_real': at.data_fim_real.strftime('%d/%m/%Y %H:%M') if at.data_fim_real else None,
            'projeto': projeto.nome if projeto else 'Sem projeto',
            'setor_image_url': setor.image_path if setor and setor.image_path else None,
            'alunos': [
                {
                    'nome': aluno.nome,
                    'img_url': f"/images/{os.path.basename(aluno.image_path)}" if aluno.image_path else None
                }
                for aluno in alunos
            ]
        })
    
    return jsonify(resultado)

def formatar_duracao(segundos):
    """Formata segundos em horas ou dias"""
    segundos = abs(segundos)  # Garante valor positivo
    horas = segundos / 3600
    
    if horas < 24:
        return f"{round(horas, 1)} horas"
    else:
        dias = horas / 24
        if dias < 2:
            return f"{round(dias, 1)} dia"
        else:
            return f"{round(dias, 1)} dias"


@app.route('/alunos-atividades/random', methods=['GET'])
def get_alunos_com_atividades_recentes():
    # Pegar 3 alunos aleatórios
    alunos = Aluno.query.limit(5).all()
    
    resultado = []
    
    for aluno in alunos:
        # Pegar a atividade mais recente do aluno (se existir)
        atividade = (
            Atividade.query
            .join(Atividadealuno)
            .filter(Atividadealuno.aluno_id == aluno.id)
            .order_by(Atividade.data_inicio.desc())
            .first()
        )
        
        # Obter informações do setor e projeto
        setor_nome = None
        projeto_nome = None
        projeto_id = None
        
        if aluno.setor_id:
            setor = Setor.query.get(aluno.setor_id)
            if setor:
                setor_nome = setor.nome
                projeto = Projeto.query.get(setor.projeto_id)
                if projeto:
                    projeto_nome = projeto.nome
                    projeto_id = projeto.id
        
        if atividade:
            resultado.append({
                'nome_aluno': aluno.nome,
                'email_aluno': aluno.email,
                'descricao_atividade': atividade.descricao,
                'status_atividade': atividade.status,
                'data_inicio': atividade.data_inicio.strftime('%d/%m/%Y') if atividade.data_inicio else None,
                'nivel': atividade.nivel, 
                'projeto_nome': projeto_nome,   
                'setor_nome': setor_nome, 
                'image_url': f"/images/{os.path.basename(atividade.image_path)}" if atividade.image_path else None ,
                'image_urlaluno': f"/images/{os.path.basename(aluno.image_path)}" if aluno.image_path else None 

            })
    
    return jsonify(resultado)



@app.route('/dashboard/resumo', methods=['GET'])
def resumo_dashboard():
    # Retorna todos os dados de uma vez para otimização
    return jsonify({
        'horasPorProjeto': horas_por_projeto().json,
        'distribuicaoAtividades': distribuicao_atividades().json,
        'rankingAlunos': ranking_alunos().json,
        'atividadesRecentes': atividades_recentes().json
    })  



def mandarreqiadados(texto):
    historico = []
    minhavari = f""" Voce é um assistente de analise de dados e voce deve fazer uma analise desses dados: {texto}.
    
    Me retorne os setores que mais produziram, os projetos mais engajados, as atividades relaizadas e os alunos destaque e o que fizeram
    
    """

    client = OpenAI(
    organization='org-lUqYZsNk1xF6AeKaAJna72d6',
    project='proj_wW0sxEvXeaNx2K8qX0DgcAJ1',
    api_key = ill
    )
        
    resposta_completa = []  

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=historico,
        stream=True,
    )

    # Acumule as partes da resposta
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            resposta_completa.append(chunk.choices[0].delta.content)
            #print(chunk.choices[0].delta.content, end="")

    # Junte todas as partes da resposta em uma única string
    resposta_final = ''.join(resposta_completa)
    historico.append({"role": "assistant", "content": resposta_final})

    # Retorne a resposta completa
    return resposta_final    

@app.route('/resumoia', methods=['GET'])
def resumo_dashboardia():
    # Retorna todos os dados de uma vez para otimização
    dados = jsonify({
        'horasPorProjeto': horas_por_projeto().json,
        'distribuicaoAtividades': distribuicao_atividades().json,
        'rankingAlunos': ranking_alunos().json,
        'atividadesRecentes': atividades_recentes().json
    })  

    print(dados)
    res = mandarreqiadados(dados)
    return jsonify({"res":res})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas se não existirem
    app.run(debug=True)


    

    

