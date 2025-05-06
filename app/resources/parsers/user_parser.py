from flask_restful import reqparse

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("username", type=str, required=True)
user_post_args.add_argument("email", type=str, required=True)
user_post_args.add_argument("password", type=str, required=True)
user_post_args.add_argument("avatar_url", type=str, required=False)
user_post_args.add_argument("bio", type=str, required=False)

user_roles_args = reqparse.RequestParser()
user_roles_args.add_argument("role_names", type=list, location="json", required=True)