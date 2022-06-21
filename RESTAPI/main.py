from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test999.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    views = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, likes = {likes}, views = {views})"



video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help = "dfsdf")
video_put_args.add_argument("likes", type=int, help = "dfsdf")
video_put_args.add_argument("views", type=int, help = "dfsdf" )

resource_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'likes' : fields.Integer,
    'views' : fields.Integer,

}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        print("sdfsdf")
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            print("doesn't exist")

        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        video = VideoModel(id=video_id, name=args['name'], likes=args['likes'], views=args['views'] )
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            print(video_id)
            abort(409, message= "not unique video id")
        db.session.add(video)
        db.session.commit()
        return {video_id:args}



api.add_resource(Video, "/video/<int:video_id>")


if __name__ =="__main__":
    app.run(debug=True)
