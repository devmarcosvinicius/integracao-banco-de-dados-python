import pprint
import os
from pymongo import MongoClient

client = MongoClient(os.environ['MONGO_STRING_CONNECTION'])
db = client.clientes

new_post = [
    {
        "nome": "Marcos Vinicius",
        "cpf": "123456789-01",
        "endereco": "Qr. 555, Rua 555, Numero. 555, Jardim Inga, Luziânia, Goias.",
        "conta": {
            "tipo": "CC",
            "agencia": "0001",
            "num": "5575-0",
            "saldo": 890589.00
        }
    },
    {
        "nome": "Fernanda Pascal",
        "cpf": "123456789-02",
        "endereco": "Qr. 555, Rua 593, Numero. 555 Condomínio Mediterrane, Lago Sul, Distrito Federal.",
        "conta": {
            "tipo": "CC",
            "agencia": "0001",
            "num": "5576-0",
            "saldo": 75589.00
        }
    },
    {
        "nome": "Luisa Frazão",
        "cpf": "123456789-03",
        "endereco": "Qr. 555, Rua 555, Apt. 555 Bloco J Condomínio Porto Rico, St. Sudoeste, Distrito Federal.",
        "conta": {
            "tipo": "CP",
            "agencia": "0001",
            "num": "5577-0",
            "saldo": 55589.00
        }
    }
]

posts = db.posts
posts_ids = posts.insert_many(new_post).inserted_ids

# Recuperação por chave/valor
print("\n\nRecuperação por chave/valor")
pprint.pprint(db.posts.find_one({"nome": "Marcos Vinicius"}))

# Recuperação de documentos dentro de posts
print("\n\nDocumentos dentro de posts")
for post in posts.find():
    pprint.pprint(post)
    print("\n")

print("\n\nQuantidade de contas do tipo CC")
print(posts.count_documents({"conta.tipo": "CC"}))
