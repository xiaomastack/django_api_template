# Django RestFramework API 项目模板
- 支持签名认证
- token(过期)认证
- 支持跨域
- 命令行操作使用ipython风格

# 使用方法
- 安装`cookiecutter`

``` shell
$ pip install cookiecutter
```

- 使用模板生成项目

``` shell
$ cookiecutter https://github.com/xiaomastack/django_api_template
# 或者
$ cookiecutter gh:xiaomastack/django_api_template
# 或者
$ cookiecutter git@github.com:xiaomastack/django_api_template.git
```

- 安装环境

``` shell
$ pip install -r requirements.txt
```

- 初始化数据库

``` shell
$ python manage.py makemigrations account
$ python manage.py migrate
```

- 创建管理员用户

``` shell
$ python manage.py createsuperuser
```

- 为用户`root`生成签名密钥对

``` shell
$ python manage.py genapikey root
api_key: root
api_secret: ATLV5DdHH9ZSsfAtyn6emz2YvqIb9KL4
```

接口认证使用`httpsig.requests_auth.HTTPSignatureAuth`包

``` python
class BasicAuthHttp(object):
    def __init__(self, key=KEY, secret=SECRET):
        self.auth = HTTPSignatureAuth(key_id=key, secret=secret)
        self.headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': key,
            'Date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def httpGet(self, url):
        return requests.get(url, auth=self.auth, headers=self.headers)
```

- 通过接口获取`token`

``` shell
$ curl -H "Content-Type: application/json" -X POST -d '{"username":"root","password":"123787Gemini"}' http://127.0.0.1:2000/token/
{"token":"51448e1f2265898a6ee63271a1019003a36710e8"}
```

接口认证头信息带上`Authorization`

```
Authorization -> Token a9992aa866ce447c80e1e3b00f3729e2 
```