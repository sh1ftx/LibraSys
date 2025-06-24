from pymongo import MongoClient

# Conecta ao MongoDB local
client = MongoClient("mongodb://localhost:27017/")

# Banco de dados
db = client["biblioteca"]

# Coleções
colecao_livros = db["livros"]
colecao_historico = db["historico"]

def inicializar_indices():
    # Índice único no título + autor + ano pode ser criado, opcional para evitar duplicatas exatas
    colecao_livros.create_index(
        [("titulo", 1), ("autor", 1), ("ano", 1)], unique=False
    )
    colecao_historico.create_index("livro_id")
    colecao_historico.create_index("data")

if __name__ == "__main__":
    # Inicializa índices se necessário
    inicializar_indices()
    print("Índices criados/confirmados no banco.")
