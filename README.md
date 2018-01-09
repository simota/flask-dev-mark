# Flask Dev Mark

## install

```
pip install flask-dev-mark-middleware
```

## How to use

```
from flask import Flask
from flask_dev_mark import DevMark

app = Flask(__name__)
app.wsgi_app = DevMark(app.wsgi_app, 'env')
```