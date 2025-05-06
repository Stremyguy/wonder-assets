from requests import get, post, delete

# print(get("http://127.0.0.1:5000/api/categories/5").json())
# "Get all the existing categories"
# categories = post("http://127.0.0.1:5000/api/categories",
#                   json={"title": "3D models",
#                         "description": "The description of the 1st category",
#                         "creator_id": 1,
#                         "is_private": False,
#                         "is_testing": False})
# print(categories.json())
# categories = delete("http://127.0.0.1:5000/api/categories/2")
# print(post("http://127.0.0.1:5000/api/categories/3"))
