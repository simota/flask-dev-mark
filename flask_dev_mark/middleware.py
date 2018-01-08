class TagGenerator(object):

    STYLE = """<style>.github-fork-ribbon,.github-fork-ribbon.red{background-color:#a00}.github-fork-ribbon{position:absolute;padding:2px 0;background-image:-webkit-gradient(linear,left top,left bottom,from(rgba(0,0,0,0)),to(rgba(0,0,0,.15)));background-image:-webkit-linear-gradient(top,rgba(0,0,0,0),rgba(0,0,0,.15));background-image:-moz-linear-gradient(top,rgba(0,0,0,0),rgba(0,0,0,.15));background-image:-ms-linear-gradient(top,rgba(0,0,0,0),rgba(0,0,0,.15));background-image:-o-linear-gradient(top,rgba(0,0,0,0),rgba(0,0,0,.15));background-image:linear-gradient(to bottom,rgba(0,0,0,0),rgba(0,0,0,.15));-webkit-box-shadow:0 2px 3px 0 rgba(0,0,0,.5);-moz-box-shadow:0 2px 3px 0 rgba(0,0,0,.5);box-shadow:0 2px 3px 0 rgba(0,0,0,.5);font:700 13px "Helvetica Neue",Helvetica,Arial,sans-serif;z-index:9999;pointer-events:auto;opacity:1;transition:opacity .25s ease-in-out;-moz-transition:opacity .25s ease-in-out;-webkit-transition:opacity .25s ease-in-out}.github-fork-ribbon:hover{opacity:.2}.github-fork-ribbon.green{background-color:#090}.github-fork-ribbon.black{background-color:#333}.github-fork-ribbon.orange{background-color:#f80}.github-fork-ribbon .github-fork-ribbon-text,.github-fork-ribbon .github-fork-ribbon-text:hover{color:#fff;text-decoration:none;text-shadow:0 -1px rgba(0,0,0,.5);text-align:center;cursor:pointer;width:200px;line-height:20px;display:inline-block;padding:2px 0;border-width:1px 0;border-style:dotted;border-color:#fff;border-color:rgba(255,255,255,.7)}.github-fork-ribbon-wrapper{width:150px;height:150px;position:absolute;overflow:hidden;top:0;z-index:9999;pointer-events:none}.github-fork-ribbon-wrapper.fixed{position:fixed}.github-fork-ribbon-wrapper.left{left:0}.github-fork-ribbon-wrapper.right{right:0}.github-fork-ribbon-wrapper.left-bottom{position:fixed;top:inherit;bottom:0;left:0}.github-fork-ribbon-wrapper.right-bottom{position:fixed;top:inherit;bottom:0;right:0}.github-fork-ribbon-wrapper.right .github-fork-ribbon{top:42px;right:-43px;-webkit-transform:rotate(45deg);-moz-transform:rotate(45deg);-ms-transform:rotate(45deg);-o-transform:rotate(45deg);transform:rotate(45deg)}.github-fork-ribbon-wrapper.left .github-fork-ribbon{top:42px;left:-43px;-webkit-transform:rotate(-45deg);-moz-transform:rotate(-45deg);-ms-transform:rotate(-45deg);-o-transform:rotate(-45deg);transform:rotate(-45deg)}.github-fork-ribbon-wrapper.left-bottom .github-fork-ribbon{top:80px;left:-43px;-webkit-transform:rotate(45deg);-moz-transform:rotate(45deg);-ms-transform:rotate(45deg);-o-transform:rotate(45deg);transform:rotate(45deg)}.github-fork-ribbon-wrapper.right-bottom .github-fork-ribbon{top:80px;right:-43px;-webkit-transform:rotate(-45deg);-moz-transform:rotate(-45deg);-ms-transform:rotate(-45deg);-o-transform:rotate(-45deg);transform:rotate(-45deg)}</style>"""

    RIBBON_TAG = """<div class="github-fork-ribbon-wrapper right fixed" onclick="this.style.display='none'" title=""><div class="github-fork-ribbon red"><span class="github-fork-ribbon-text">{env}</span></div></div>"""

    def __init__(self, env):
        self._env = env

    @property
    def size(self):
        tags = [
            '({0})'.format(self._env), self.STYLE,
            self.RIBBON_TAG.format(env=self._env)
        ]
        return len(''.join(tags))

    def generate(self, body):
        body = self._replace_title(body)
        body = self._append_style(body)
        body = self._append_dev_mark(body)
        return body

    def _replace_title(self, body):
        return body.replace('</title>', '({0})</title>'.format(self._env))

    def _append_style(self, body):
        return body.replace('</head>', '{0}</head>'.format(self.STYLE))

    def _append_dev_mark(self, body):
        tag = self.RIBBON_TAG.format(env=self._env)
        return body.replace('</body>', '{0}</body>'.format(tag))


def _is_html(header):
    return (header[0] == 'Content-Type' and header[1] == 'text/html')


class DevMark(object):
    def __init__(self, app, env):
        self.app = app
        self._env = env

    def __call__(self, environ, start_response):

        generator = TagGenerator(self._env)

        def get_content_length(headers):
            for header in headers:
                if header[0] == 'Content-Length':
                    return header
            return None

        def new_start_response(status, response_headers, exc_info=None):

            headers = filter(_is_html, response_headers)
            if len(list(headers)) == 0:
                return start_response(status, response_headers, exc_info)

            environ['FLASK_DEV_MARK'] = True
            content_length = get_content_length(response_headers)
            if content_length is not None:
                size = int(content_length[1])
                response_headers.remove(content_length)
                response_headers.append(('Content-Length',
                                         str(size + generator.size)))
            return start_response(status, response_headers, exc_info)

        body = next(self.app(environ, new_start_response))
        if 'FLASK_DEV_MARK' in environ:
            body = generator.generate(body.decode('utf-8')).encode('utf-8')
        return [body]
