
import os
from flask import Flask, request, jsonify
from flask.wrappers import Response
from display import Display
from PIL import Image


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    display = Display()

    @app.route('/', methods=['POST'])
    def draw():
        if display.Busy():
            return  Response(response="display is busy, wait", status=425)
        if 'black' not in request.files:
            return Response(response="No file part", status=400)
        black = request.files['black']
     
        blackImg = Image.open(black)
        if blackImg.size != display.size():
            return Response(response=f'incorrect black image size {blackImg.size}', status=400)
        redImg = display.get_clear_image()
        if "red" in request.files.keys() and request.files["red"].filename != '':
            red = request.files["red"]
            redImg = Image.open(red)
            if redImg.size != display.size():
                return Response(response=f'incorrect red image size {redImg.size}', status=400)
        display.draw_image(blackImg, redImg)

        return Response(status=200)

    return app