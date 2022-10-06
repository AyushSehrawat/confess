from deta import Deta
deta = Deta()
user = deta.Base("confessioner_users")
posts = deta.Base("confessioner_posts")