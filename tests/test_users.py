from requests import get, post, put

"Get all the existing categories"
users = get("http://127.0.0.1:5000/api/users/1")
print(users.json())

# user = post("http://127.0.0.1:5000/api/users",
#             json={"username": "John Smith",
#                   "email": "johnsmith@gmail.com",
#                   "password": "john12345"}).json()

# print(user)

# users = put("http://127.0.0.1:5000/api/users/3",
#             json={"role_names": ["user", "moderator"]})

# print(users.json())