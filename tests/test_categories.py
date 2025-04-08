from requests import get, post

"""Creating a new category"""
new_category_data = {
    "title": "Category test 1",
    "description": "Description of the first category",
    "is_testing": True
}

new_category = post("http://127.0.0.1:5000/api/categories",
                    json=new_category_data).json()
print(new_category)

"Get all the existing categories"
categories = get("http://127.0.0.1:5000/api/categories").json()
print(categories)
