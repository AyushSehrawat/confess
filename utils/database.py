import os, sys
from deta import Deta

deta = Deta(os.environ["SECRET_KEY"])
user = deta.Base("confessioner_users")
posts = deta.Base("confessioner_posts")