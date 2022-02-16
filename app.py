from distutils.log import debug
import os
import dcm_reader
from os.path import join, dirname, realpath

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/dcm/')


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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

    # route to index
    @app.route('/', methods=['GET'])
    @app.route('/index', methods=('GET', 'POST'))
    def index():
      if request.method == 'GET':
        return render_template('index.html')

      if request.method == 'POST':
        # get files
        file = request.files['filetosave']
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # save files
        file.save(filepath)
        
        return 'Finished uploading'

    # route to index
    @app.route('/render', methods=('GET', 'POST'))
    def render():
        if request.method == 'GET':
            return 'KEKW'
        
        if request.method == 'POST':
            # read the files
            dcm_reader.read()
            return 'Finished rendering'

    return app