from flask_restful import reqparse

type_post_args = reqparse.RequestParser()
type_post_args.add_argument("name", type=str, required=True)
type_post_args.add_argument("icon_url", type=str, required=True)