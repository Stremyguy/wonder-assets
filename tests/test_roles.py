from requests import get, post

roles_names = ["user", "creator", "moderator", "admin"]

for role_name in roles_names:
      role = post("http://127.0.0.1:5000/api/roles",
                  json={"name": role_name})

      print(role)