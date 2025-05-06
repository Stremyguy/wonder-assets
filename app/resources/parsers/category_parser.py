from flask_restful import reqparse

category_post_args = reqparse.RequestParser()
category_post_args.add_argument("title", type=str, required=True)
category_post_args.add_argument("description", type=str, required=True)
category_post_args.add_argument("creator_id", type=int, required=True)
category_post_args.add_argument("role_ids", type=list, required=True)
category_post_args.add_argument("is_private", type=bool)
category_post_args.add_argument("is_testing", type=bool)