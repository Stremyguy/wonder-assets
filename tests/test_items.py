from requests import get, post, delete

# item = post("http://127.0.0.1:5000/api/items",
#             json={"title": "3D MODEL 1",
#                   "description": "3D MODEL 1!",
#                   "images": ["animation01.jpg",
#                              "flow_thumbnail.jpg",
#                              "Group-1-480x270.jpg"],
#                   "item_url": "items/1.zip",
#                   "model_file_url": "my_model.zip"
#                   "type_id": 1,
#                   "category_id": 45,
#                   "creator_id": 1,
#                   "is_private": False,
#                   "can_download": True})

print(delete("http://127.0.0.1:5000/api/items/6").json())

# print(item.json())
# categories = delete("http://127.0.0.1:5000/api/categories/2")
# print(post("http://127.0.0.1:5000/api/categories/3"))
