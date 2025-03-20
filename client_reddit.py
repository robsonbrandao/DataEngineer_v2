import praw
import pandas as pd


class ClientReddit:
    def __init__(self, client_id, client_secret, username, password, user_agent):
        """
        Inicializa o objeto da classe ClientReddit com as credenciais de acesso à API do Reddit.
        :param client_id: str: ID do cliente da API do Reddit
        :param client_secret: str: Chave secreta do cliente da API do Reddit
        :param username: str: Nome de usuário do Reddit
        :param password: str: Senha do Reddit
        :param user_agent: str: Nome do aplicativo que está fazendo a solicitação

        """

        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent,
        )

    def get_hot_posts(self, subreddit_name, limit=10):
        """
        Obtém os hot posts de um subreddit.
        :param subreddit_name: str: Nome do subreddit
        :param limit: int: Número de posts a serem retornados
        :return: list: Lista de posts
        """
        subreddit = self.reddit.subreddit(subreddit_name)
        posts = []
        for post in subreddit.hot(limit=limit):
            posts.append(
                {
                    "id": post.id,
                    "ups": post.ups,
                    "downs": post.downs,
                    "upvote_ratio": post.upvote_ratio,
                    "subreddit": post.subreddit.display_name,
                    "title": post.title,
                    "score": post.score,
                    "created_utc": post.created_utc,
                    "url": post.url,
                    "selftext": post.selftext
                    
                }
            )
        return pd.DataFrame(posts)
