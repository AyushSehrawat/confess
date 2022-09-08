import os 

from dotenv import load_dotenv
from deta import Deta
load_dotenv()

deta = Deta(os.getenv("DETA_PROJECT_KEY"))

user = deta.Base("confessioner_users")
posts = deta.Base("confessioner_posts")
