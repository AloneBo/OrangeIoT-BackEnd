# Flask-Verification-code

Usage:
```python
...
from captcha import get_captcha_img
...
@app.route('/')
def index():
    image_data, text = get_captcha_img()
    resp = make_response(image_data)
    resp.headers['Content-Type'] = "image/png"
    return resp
```

![](https://raw.githubusercontent.com/AloneBo/Flask-Verification-code/master/demo.png)

