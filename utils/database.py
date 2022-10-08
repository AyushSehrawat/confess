import os, sys
from deta import Deta

from dotenv import load_dotenv

load_dotenv()

try:
    if os.environ["DETA_PROJECT_KEY"]:
        deta = Deta(os.environ["DETA_PROJECT_KEY"])
except KeyError:
    deta = Deta()
user = deta.Base("confessioner_users")
posts = deta.Base("confessioner_posts")