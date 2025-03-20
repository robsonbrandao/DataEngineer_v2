# Carrega as bibliotecas necessárias

import os
import requests
import boto3
from openai import OpenAI
from dotenv import (
    load_dotenv,
)  # Importando a função load_dotenv do pacote python-dotenv

load_dotenv()  # Carregando variáveis de ambiente de um arquivo .env


# Variaveis Reddit
SUBREDDIT = "python"
client_id = os.environ.get("REDDIT_CLIENT_ID")
client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
user_agent = os.environ.get("REDDIT_USER_AGENT")
open_ai_key = os.environ.get("OPENAI_API_KEY")


# Variaveis OpenAI

client = OpenAI()
# Esse código é um exemplo de como obter um token de acesso para a API do Reddit.
# O token de acesso é necessário para fazer solicitações à API do Reddit.
# Para obter um token de acesso, você precisa de um client_id e um client_secret.


# Create an S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)


CSV_PATH = f"{SUBREDDIT}.csv"


# Classificar sentimento
def classificar_sentimento(texto):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Voce é uma inteligencia artificial especializada em detectar sentimentos de textos.",
            },
            {
                "role": "user",
                "content": f"Classifique o sentimento do seguinte texto em 'Positivo', 'Neutro' ou 'Negativo', retorne apenas uma string: {texto}",
            },
        ],
    )
    return completion.choices[0].message.content


# posts_df["sentimento"] = posts_df["selftext"].apply(classificar_sentimento)
# posts_df.head(40)


# # Obtendo acess token
def obter_reddit_acess_token(client_id, client_secret):
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    data = {"grant_type": "client_credentials"}
    headers = {"User-Agent": user_agent}

    response = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth,
        data=data,
        headers=headers,
    )

    # print("Resposta da API:", response.status_code, response.text)  # Adiciona debug
    try:
        return response.json()["access_token"]
    except KeyError:
        raise Exception(f"Erro ao obter token! Resposta da API: {response.json()}")


token = obter_reddit_acess_token(client_id, client_secret)
# print(token)


##**Todos os Endpoints do Reddit**

##reddit.com/dev/api#section_listings


### Pegando os HOT POSTS
# Pegando hot pots de um subreddit
def get_hot_posts(subreddit, token):
    posts_requests = requests.get(
        f"https://oauth.reddit.com/r/{subreddit}/hot",  # Subreddit de onde queremos obter os posts
        headers={
            "User-Agent": user_agent,
            "Authorization": f"bearer {token}",  # Usando o token de acesso para fazer solicitações à API do Reddit
        },
    )
    return posts_requests.json()


# posts = get_hot_posts("python", token)
# import pandas as pd


# Criando dataframe a partir de uma lista de dicionarios
def create_posts_df(posts):
    posts_data = []

    for post in posts["data"]["children"]:
        posts_data.append(
            {
                "id": post["kind"] + "_" + post["data"]["id"],
                "subreddit": post["data"]["subreddit"],
                "kind": post["kind"],
                "title": post["data"]["title"],
                "score": post["data"]["score"],
                "selftext": post["data"]["selftext"],
            }
        )

    return pd.DataFrame(posts_data)


# posts_df = create_posts_df(posts)
# posts_df.head()


# Juntando tudo
import pandas as pd

print("Obtendo token de acesso...")
token = obter_reddit_acess_token(client_id, client_secret)
posts = get_hot_posts(SUBREDDIT, token)

print("Obtendo hot posts")
posts_df = create_posts_df(posts)

print("Classificando sentimentos")
posts_df["sentimento"] = posts_df["selftext"].apply(classificar_sentimento)

print("Salvando {CSV_PATH}")
posts_df.to_csv(CSV_PATH, index=False)


# Escrevendo no S3
print("Escrevendo no S3")
bucket_name = os.environ.get("AWS_S3_BUCKET_NAME")
object_name = CSV_PATH


s3.upload_file(CSV_PATH, bucket_name, f"subreddits/{object_name}")
print("Concluído!")
