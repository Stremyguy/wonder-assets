from requests import post, delete

# 2. Now create new type (will get id=1)
current_type = post("http://127.0.0.1:5000/api/types",
                  json={
                      "name": "Texture Pack",
                      "icon_url": "images/icons/icon_texture.png"
                  })
print("New type response:", current_type.json())