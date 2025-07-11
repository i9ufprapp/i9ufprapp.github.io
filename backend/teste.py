import requests
import json
from datetime import datetime, timedelta
import os
from pathlib import Path

BASE_URL = "http://127.0.0.1:5000"

# Diretório com imagens de exemplo (crie este diretório e adicione algumas imagens)
IMAGES_DIR = Path(r"C:/Users/anajs/OneDrive/Documentos/server/i9ufprapp.github.io/backend/test_images")
os.makedirs(IMAGES_DIR, exist_ok=True)

# Função auxiliar para formatar datas
def format_date(date):
    return date.strftime('%Y-%m-%d')

# Função para fazer upload de imagem (agora usando FormData)
def upload_image(entity_type, entity_id, image_path):
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (image_path.name, f, 'image/jpeg')}
            response = requests.post(
                f"{BASE_URL}/upload/{entity_type}/{entity_id}", 
                files=files
            )
            return response.json()
    except Exception as e:
        print(f"Erro ao enviar imagem: {str(e)}")
        return None

# Criar projetos com imagens
projetos_data = [
    {
        "nome": "Ciência Para Todos", 
        "descricao": "Projeto Ciência Para Todos", 
        "responsavel": "Andre",
        "image_path": IMAGES_DIR / "projeto1.jpg"
    },
    {
        "nome": "Iniciativa Startup Experience", 
        "descricao": "Projeto Iniciativa Startup Experience", 
        "responsavel": "Andre",
        "image_path": IMAGES_DIR / "projeto2.jpg"
    }
]

for projeto in projetos_data:
    # Primeiro cria o projeto
    projeto_data = {k: v for k, v in projeto.items() if k != 'image_path'}
    response = requests.post(f"{BASE_URL}/projetos", json=projeto_data)
    projeto_id = response.json().get('id')
    print(f"Projeto criado: {response.json()}")
    
    # Faz upload da imagem se existir
    if projeto_id and projeto['image_path'].exists():
        print(f"Enviando imagem para projeto {projeto_id}...")
        upload_response = upload_image('projeto', projeto_id, projeto['image_path'])
        print(f"Imagem do projeto {projeto_id} upload: {upload_response}")

# Criar setores para cada projeto com imagens
setores_data = [
    {"nome": "DHO", "descricao": "Setor de DHO", "projeto_id": 1, "image_path": IMAGES_DIR / "dho.jpg"},
    {"nome": "TI", "descricao": "Setor de TI", "projeto_id": 1, "image_path": IMAGES_DIR / "ti.jpg"},
    {"nome": "Marketing", "descricao": "Setor de Marketing", "projeto_id": 1, "image_path": IMAGES_DIR / "marketing.jpg"},
    {"nome": "DHO", "descricao": "Setor de DHO", "projeto_id": 2, "image_path": IMAGES_DIR / "dho.jpg"},
    {"nome": "TI", "descricao": "Setor de TI", "projeto_id": 2, "image_path": IMAGES_DIR / "ti.jpg"},
    {"nome": "Marketing", "descricao": "Setor de Marketing", "projeto_id": 2, "image_path": IMAGES_DIR / "marketing.jpg"}
]

for setor in setores_data:
    # Primeiro cria o setor
    setor_data = {k: v for k, v in setor.items() if k != 'image_path'}
    response = requests.post(f"{BASE_URL}/setores", json=setor_data)
    setor_id = response.json().get('id')
    print(f"Setor criado: {response.json()}")
    
    # Faz upload da imagem se existir
    if setor_id and setor['image_path'].exists():
        print(f"Enviando imagem para setor {setor_id}...")
        upload_response = upload_image('setor', setor_id, setor['image_path'])
        print(f"Imagem do setor {setor_id} upload: {upload_response}")

# Cadastrar alunos com fotos
alunos_data = [
    {
        "nome": "Ana Souza",
        "email": "ana.souza@example.com",
        "setor_id": 1,
        "preferencia": "Design",
        "senha": "ana123",
        "idade": 24,
        "bolsista": False,
        "ano_entrada": 2022,
        "linkedin": "https://linkedin.com/in/ana-souza",
        "wats": "11999887766",
        "admin": False,
        "image_path": IMAGES_DIR / "aluno1.jpg"
    },
    {
        "nome": "Carlos Pereira",
        "email": "carlos.pereira@example.com",
        "setor_id": 2,
        "preferencia": "Programação",
        "senha": "carlos456",
        "idade": 23,
        "bolsista": True,
        "ano_entrada": 2021,
        "linkedin": "https://linkedin.com/in/carlos-pereira",
        "wats": "11988776655",
        "admin": False,
        "image_path": IMAGES_DIR / "aluno2.jpg"
    },
    {
        "nome": "JV",
        "email": "JV@gmail.com",
        "setor_id": 3,
        "preferencia": "Comunicação",
        "senha": "123",
        "idade": 25,
        "bolsista": True,
        "ano_entrada": 2023,
        "linkedin": "https://linkedin.com/in/fernanda-lima",
        "wats": "11977665544",
        "admin": True,
        "image_path": IMAGES_DIR / "aluno3.jpg"
    }
]

for aluno in alunos_data:
    # Primeiro cria o aluno
    aluno_data = {k: v for k, v in aluno.items() if k != 'image_path'}
    response = requests.post(f"{BASE_URL}/register", json=aluno_data)
    aluno_id = response.json().get('id')
    print(f"Aluno criado: {response.json()}")
    
    # Faz upload da foto se existir
    if aluno_id and aluno['image_path'].exists():
        print(f"Enviando imagem para aluno {aluno_id}...")
        upload_response = upload_image('aluno', aluno_id, aluno['image_path'])
        print(f"Foto do aluno {aluno_id} upload: {upload_response}")

# Testar login
login_data = {"email": "JV@gmail.com", "senha": "123"}
login_response = requests.post(f"{BASE_URL}/login", json=login_data)
print("Login:", login_response.json())

# Criar atividades individuais com imagens
atividades_data = [
    {
        "setor_id": 1,
        "descricao": "Desenvolver um novo sistema",
        "data_fim_previsto": format_date(datetime.now() + timedelta(days=30)),
        "nivel": "facil",
        "image_path": IMAGES_DIR / "atividade1.jpg"
    },
    {
        "setor_id": 3,
        "descricao": "Publicação no linkedin",
        "data_fim_previsto": format_date(datetime.now() + timedelta(days=15)),
        "nivel": "medio",
        "image_path": IMAGES_DIR / "atividade2.jpg"
    }
]

for atividade in atividades_data:
    # Primeiro cria a atividade
    atividade_data = {k: v for k, v in atividade.items() if k != 'image_path'}
    response = requests.post(f"{BASE_URL}/atividades", json=atividade_data)
    atividade_id = response.json().get('id')
    print(f"Atividade criada: {response.json()}")
    
    # Faz upload da imagem se existir
    if atividade_id and atividade['image_path'].exists():
        print(f"Enviando imagem para atividade {atividade_id}...")
        upload_response = upload_image('atividade', atividade_id, atividade['image_path'])
        print(f"Imagem da atividade {atividade_id} upload: {upload_response}")

# Criar atividades com alunos associados
atividade_com_alunos_data = {
    "setor_id": 1,
    "descricao": "Planejamento estratégico",
    "data_fim_previsto": "30/06/2024",
    "nivel": "dificil",
    "alunos": [1, 2],
    "image_path": IMAGES_DIR / "atividade3.jpg"
}

# Primeiro cria a atividade
response = requests.post(f"{BASE_URL}/atividades/comalunos", 
                        json={k: v for k, v in atividade_com_alunos_data.items() if k != 'image_path'})
atividade_id = response.json().get('atividade_id')
print("Atividade com alunos:", response.json())

print(atividade_com_alunos_data['image_path'])
# Faz upload da imagem se existir
if atividade_id:
    print(f"Enviando imagem para atividade {atividade_id}...")
    upload_response = upload_image('atividade', atividade_id, atividade_com_alunos_data['image_path'])
    print(f"Imagem da atividade {atividade_id} upload: {upload_response}")






# # Criar projeto completo com setores e alunos
# projeto_completo_data = {
#     "nome": "Projeto Integrador",
#     "descricao": "Projeto multidisciplinar integrando todos os setores",
#     "setores": [
#         {
#             "nome": "Coordenação", 
#             "descricao": "Setor de coordenação geral",
#             "image_path": IMAGES_DIR / "coordenacao.jpg"
#         },
#         {
#             "nome": "Operações", 
#             "descricao": "Setor de operações",
#             "image_path": IMAGES_DIR / "operacoes.jpg"
#         },
#         {
#             "nome": "Comunicação", 
#             "descricao": "Setor de comunicação",
#             "image_path": IMAGES_DIR / "comunicacao.jpg"
#         }
#     ],
#     "image_path": IMAGES_DIR / "projeto3.jpg"
# }

# # Primeiro cria o projeto
# projeto_data = {
#     "nome": projeto_completo_data["nome"],
#     "descricao": projeto_completo_data["descricao"],
#     "responsavel": "Admin",
#     "setores": [
#         {k: v for k, v in setor.items() if k != 'image_path'} 
#         for setor in projeto_completo_data["setores"]
#     ]
# }

# response = requests.post(f"{BASE_URL}/projeto/comsetoresalunos", json=projeto_data)
# projeto_id = response.json().get('projeto_id')
# print("Projeto completo:", response.json())

# # Faz upload da imagem do projeto se existir
# if projeto_id and projeto_completo_data['image_path'].exists():
#     print(f"Enviando imagem para projeto {projeto_id}...")
#     upload_response = upload_image('projeto', projeto_id, projeto_completo_data['image_path'])
#     print(f"Imagem do projeto {projeto_id} upload: {upload_response}")

# # Faz upload das imagens dos setores criados
# setores_criados = requests.get(f"{BASE_URL}/setoresbyp/{projeto_id}").json()
# for setor_data, setor_criado in zip(projeto_completo_data["setores"], setores_criados):
#     if setor_criado['id'] and setor_data['image_path'].exists():
#         print(f"Enviando imagem para setor {setor_criado['id']}...")
#         upload_response = upload_image('setor', setor_criado['id'], setor_data['image_path'])
#         print(f"Imagem do setor {setor_criado['id']} upload: {upload_response}")

# Testar rotas GET básicas
print("\nTestando rotas GET:")
print("Alunos:", requests.get(f"{BASE_URL}/alunos").json())
print("Atividades:", requests.get(f"{BASE_URL}/atividades").json())
print("Setores:", requests.get(f"{BASE_URL}/setores").json())
print("Projetos:", requests.get(f"{BASE_URL}/projetos").json())

# Concluir algumas atividades
print("\nConcluindo atividades:")
for atividade_id in [1, 2]:
    print(f"Concluindo atividade {atividade_id}:", requests.get(f"{BASE_URL}/atividades/{atividade_id}/status").json())

# Testar rotas de dashboard
print("\nTestando rotas de dashboard:")
print("Horas por projeto:", requests.get(f"{BASE_URL}/dashboard/horas-por-projeto").json())
print("Distribuição atividades:", requests.get(f"{BASE_URL}/dashboard/distribuicao-atividades").json())
print("Ranking alunos:", requests.get(f"{BASE_URL}/dashboard/ranking-alunos").json())
print("Atividades recentes:", requests.get(f"{BASE_URL}/dashboard/atividades-recentes").json())
print("Resumo dashboard:", requests.get(f"{BASE_URL}/dashboard/resumo").json())
print("Resumo IA:", requests.get(f"{BASE_URL}/resumoia").json())