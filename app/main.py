#!/usr/bin/env python3

import sys
import uvicorn

from app import App
from markup import Document
from model import Model

CONFIG = {
    'upload_route': '/upload',
    'upload_method': 'POST',
    'upload_name': 'file',

    'url_route': '/url',
    'url_method': 'POST',
    'url_name': 'url',

    'images_route': '/images',
    'images_dir': 'images',
    'images_name': 'images',

    'templates_dir': 'templates',
    'js_file': 'script.js',
    # XXX: Relies on the file with JavaScript code.
    'onsubmit': 'return uploadImage(this);',

    'project_name': 'Flower classifier',
    # XXX: Use a less hacky way of distinguishing errors from proper responses,
    # which is also readable for users with disabled JavaScript.
    'error_prefix': 'Error:'
}

def main():
    model = Model(sys.argv[1])  # directory with .pkl

    document = Document(config=CONFIG)

    app = App(debug=False, model=model, document=document, config=CONFIG)

    uvicorn.run(app.app, host='0.0.0.0', port=8000)

if __name__ == '__main__':
    main()
