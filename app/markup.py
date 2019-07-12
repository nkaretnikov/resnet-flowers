import os

import dominate
import dominate.tags as tags
import dominate.util as util
import jinja2

# XXX: No accessiblity support.
# https://getbootstrap.com/docs/4.3/getting-started/accessibility
# https://developer.mozilla.org/en-US/docs/Web/Accessibility

class Document:
    def noscript(self):
        with tags.noscript():
            with tags.div(cls='container'):
                with tags.div(cls='row mt-3 justify-content-center'):
                    with tags.div(cls='col-md-8 col-lg-6'):
                        with tags.div(
                                 cls='alert alert-warning text-center',
                                 role='alert'):
                            util.text('Enable JavaScript for better experience')

    def image(self, src, alt):
        with tags.figure(cls='figure'):
            tags.img(cls='figure-img img-fluid rounded', src=src, alt=alt)
            with tags.figcaption(
                    cls='figure-caption',
                    # Requires browser-specific hyphens to work in different browsers.
                    style=('-webkit-hyphens: auto; '
                           '-moz-hyphens: auto; '
                           '-ms-hyphens: auto; '
                           'hyphens: auto;')):
                util.text(alt)

    def upload_form(self):
        with tags.form(
            id=self.config['upload_name'],
            onsubmit=self.config['onsubmit'],
            enctype='multipart/form-data',
            method=self.config['upload_method'],
            action=self.config['upload_route'],
            cls='card p-3 bg-light'):

            tags.h5('Upload an image', cls='card-title')

            with tags.div(cls='form-group row'):
                with tags.div(cls='col-12'):
                    # This requires JavaScript to show the filename.
                    # https://github.com/Johann-S/bs-custom-file-input
                    #
                    # 'style' is necessary to avoid overlapping in Safari and
                    # Chrome on iOS:
                    # https://github.com/twbs/bootstrap/issues/26933
                    with tags.div(cls='custom-file', style='overflow: hidden;'):
                        tags.input(
                            type='file', cls='custom-file-input p-1 rounded',
                            id=self.config['upload_name'], name=self.config['upload_name'])
                        tags.label(
                            'Choose file', fr=self.config['upload_name'],
                            cls='custom-file-label bg-light')

            with tags.div(cls='form-group row'):
                with tags.div(cls='col-3'):
                    with tags.button(type='submit', cls='btn btn-primary'):
                        util.text('Submit')

    def url_form(self):
        with tags.form(
            id=self.config['url_name'],
            onsubmit=self.config['onsubmit'],
            method=self.config['url_method'],
            action=self.config['url_route'],
            cls='card p-3 bg-light'):

            tags.h5('Load an image from a URL', cls='card-title')

            with tags.div(cls='form-group row'):
                with tags.div(cls='col-12'):
                    tags.input(
                        type='url', cls='form-control p-1 bg-light rounded',
                        name=self.config['url_name'], placeholder='https://example.com/image.png')

            with tags.div(cls='form-group row'):
                with tags.div(cls='col-3'):
                    with tags.button(type='submit', cls='btn btn-primary'):
                        util.text('Submit')

    def __init__(self, config):
        self.config = config

        env = jinja2.Environment(
                  loader=jinja2.FileSystemLoader(self.config['templates_dir']),
                  trim_blocks=True)
        self.script = env.get_template(self.config['js_file']).render(**self.config)

        self.document = dominate.document(title=self.config['project_name'])
        self.document['lang'] = 'en'

        self.images = []
        for image_file in os.listdir(self.config['images_dir']):
            dir_image_file = os.path.join(self.config['images_dir'], image_file)
            if os.path.isfile(dir_image_file):
                src = '{}/{}'.format(self.config['images_route'], image_file)
                alt = os.path.splitext(
                          image_file.capitalize()
                              .replace('-', ' ')
                              .replace('_', ' '))[0]
                self.images.append((src, alt))
        self.images.sort(key=lambda x: x[1])

        with self.document.head:
            tags.meta(charset='utf-8')
            tags.meta(
                name='viewport',
                content='width=device-width, initial-scale=1, shrink-to-fit=no')
            # Bootstrap CSS.
            tags.link(
                rel='stylesheet',
                href='https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
                integrity='sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T',
                crossorigin='anonymous')
            # Fonts.
            tags.link(
                rel='stylesheet',
                href='https://fonts.googleapis.com/css?family=Dancing+Script&display=swap')

        with self.document:
            self.noscript()

            with tags.script():
                util.text(self.script, escape=False)

            with tags.div(id='root'):
                with tags.div(cls='container'):
                    with tags.div(cls='row mb-3 mt-3'):
                        with tags.div(cls='col'):

                            with tags.div(cls='card'):
                                with tags.div(cls='card-body'):
                                    with tags.h1(cls='display-5', style="font-family: 'Dancing Script', cursive;"):
                                        with tags.span(cls='text-capitalize'):
                                            util.text(self.config['project_name'])

                                    with tags.p(cls='lead'):
                                        util.text('Use machine learning to classify flowers! The ')
                                        tags.a('fast.ai library', href='https://docs.fast.ai')
                                        util.text(' was used to ')
                                        tags.a('train', href='https://github.com/nkaretnikov/resnet-flowers')
                                        util.text(' a ')
                                        tags.a('residual', href='https://arxiv.org/pdf/1512.03385.pdf')
                                        util.text(' ')
                                        tags.a('neural network', href='http://cs231n.github.io/convolutional-networks')
                                        util.text(' on the ')
                                        tags.a('Flower Color Images', href='https://www.kaggle.com/olgabelitskaya/flower-color-images')
                                        util.text(' dataset to recognize the classes below.')

                                    tags.hr(cls='my-4')

                                    with tags.div(cls='container'):
                                        with tags.div(cls='row mb-1'):
                                            for src, alt in self.images:
                                                with tags.div(cls='col-6 col-sm-4 col-md-3 col-lg-2'):
                                                    self.image(src=src, alt=alt)

                    with tags.div(cls='row mb-1'):
                        with tags.div(cls='col-md-9 col-lg-7 col-xl-6'):
                            self.upload_form()

                    with tags.div(cls='row mb-3'):
                        with tags.div(cls='col-md-9 col-lg-7 col-xl-6'):
                            self.url_form()

            # Optional JavaScript for Bootstrap.
            tags.script(
                src='https://code.jquery.com/jquery-3.3.1.slim.min.js',
                integrity='sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo',
                crossorigin='anonymous')
            tags.script(
                src='https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js',
                integrity='sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1',
                crossorigin='anonymous')
            tags.script(
                src='https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js',
                integrity='sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM',
                crossorigin='anonymous')

            # Show the filename when using 'custom-file'.
            tags.script(
                src='https://cdn.jsdelivr.net/npm/bs-custom-file-input/dist/bs-custom-file-input.min.js',
                integrity='sha384-wbycNUwFmhRaoqw8zOxtEdIA5kWW1MUAV4bXEfNNOk0e5HmG3AaNRvOHFjWNAAQb',
                crossorigin='anonymous')
            with tags.script():
                util.text('$(document).ready(function () { bsCustomFileInput.init() })')
