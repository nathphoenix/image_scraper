from flask import Flask
from flask_restful import Api
from images import Image_Extractor
from article import Article
import glob, os


app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True
api = Api(app)

@app.route('/')
def homePage():
	return ("Welcome to the image api extractor")

app.secret_key = "nathaniel"

api.add_resource(Image_Extractor, "/images/<path:article_URL>")
api.add_resource(Article, "/article/<path:article_URL>")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
