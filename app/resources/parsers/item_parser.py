from flask_restful import reqparse

item_post_args = reqparse.RequestParser()
item_post_args.add_argument("title", type=str, required=True)
item_post_args.add_argument("short_description", type=str, required=False)
item_post_args.add_argument("full_description", type=str, required=False)
item_post_args.add_argument("item_url", type=str, required=True)
item_post_args.add_argument("type_id", type=int, required=True)
item_post_args.add_argument("category_id", type=int, required=True)
item_post_args.add_argument("creator_id", type=int, required=True)
item_post_args.add_argument("is_private", type=bool)
item_post_args.add_argument("can_download", type=bool)