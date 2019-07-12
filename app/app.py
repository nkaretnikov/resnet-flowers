import traceback

import aiohttp
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, PlainTextResponse
from starlette.staticfiles import StaticFiles

# XXX: There is no way to limit the size by default:
# https://github.com/aio-libs/aiohttp/issues/2638
#
# XXX: Note: 'self._body' is cached (as in the upstream code), so this will
# return the first value for repeated calls.
async def read(self, n: int = -1) -> bytes:
    """
    Read up to 'n' bytes of the response payload.

    If 'n' is -1 (default), read the entire payload.
    """
    if self._body is None:
        try:
            if n is -1:
                self._body = await self.content.read()
            else:
                chunks = []
                i = 0
                while i < n:
                    chunk = await self.content.read(n=n - i)
                    if not chunk:
                        break
                    chunks.append(chunk)
                    i += len(chunk)

                self._body = b''.join(chunks)

            for trace in self._traces:
                await trace.send_response_chunk_received(self._body)

        except BaseException:
            self.close()
            raise
    elif self._released:
        raise aiohttp.ClientConnectionError('Connection closed')

    return self._body


class App:
    def __init__(self, debug, model, document, config):
        self.config = config

        self.app = Starlette(debug=debug)
        self.app.mount(
            self.config['images_route'],
            StaticFiles(directory=self.config['images_dir']),
            name=self.config['images_name'])

        self.model = model
        self.document = document

        self.num_bytes = 10_000_000  # 10 MB

        self.app.add_route(
            path='/',
            route=self.homepage)

        self.app.add_route(
            path=self.config['upload_route'],
            route=self.upload,
            methods=[self.config['upload_method']])

        self.app.add_route(
            path=self.config['url_route'],
            route=self.url,
            methods=[self.config['url_method']])

        # Errors must be prefixed to be properly colored by the frontend.
        self.error_internal = (
            '{} something went wrong'.format(self.config['error_prefix']))

        self.error_empty_file = '{} empty file'.format(self.config['error_prefix'])

        self.error_failed_to_get_url = (
            '{} failed to get URL'.format(self.config['error_prefix']))

        self.error_invalid_url = '{} invalid URL'.format(self.config['error_prefix'])

    async def homepage(self, _request):
        try:
            response = str(self.document.document)
            return HTMLResponse(response)
        except:
            traceback.print_exc()
            return PlainTextResponse(self.error_internal)

    async def upload(self, request):
        try:
            form = await request.form()
            content = await form[self.config['upload_name']].read(self.num_bytes)
            if not content:
                return PlainTextResponse(self.error_empty_file)
            return PlainTextResponse(self.model.classify(content))
        except:
            traceback.print_exc()
            return PlainTextResponse(self.error_internal)

    async def url(self, request):
        try:
            form = await request.form()
            url = form[self.config['url_name']]
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status != 200:
                            return PlainTextResponse(self.error_failed_to_get_url)
                        content = await read(response, n=self.num_bytes)
                        return PlainTextResponse(self.model.classify(content))
            except aiohttp.ClientConnectionError:
                return PlainTextResponse(self.error_failed_to_get_url)
            except aiohttp.client_exceptions.InvalidURL:
                return PlainTextResponse(self.error_invalid_url)
        except:
            traceback.print_exc()
            return PlainTextResponse(self.error_internal)
