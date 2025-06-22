import os

from flask import Flask, render_template, request
from lexicon import Stemmer

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    

    @app.route("/", methods=["GET", "POST"])
    def index():
        output = None
        input = request.form.get("content")
        if input:
            lang = request.form.get("language")
            try:
                threshold = int(request.form.get("threshold", 0))
            except ValueError:
                threshold = 1
            g = Stemmer(lang)
            output = g.count_words_from_text(input, thresh=threshold)
        return render_template('index.html', output=output)

    return app