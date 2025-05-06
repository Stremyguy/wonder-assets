from flask_restful import reqparse

role_post_args = reqparse.RequestParser()
role_post_args.add_argument("name", type=str, required=True)