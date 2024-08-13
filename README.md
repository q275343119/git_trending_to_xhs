# git_trending_to_xhs
## 项目说明
爬取Python语言每日Trending中的项目，并总结发布至小红书

## 安装
### 环境准备
Python 3.11 (其他版本没有尝试)
### 部署签名服务
使用 [ReaJason/xhs](https://github.com/ReaJason/xhs)项目中的签名服务

或者参考此项目自己搭建

本项目是自己搭建的一个sign服务，相比于原始服务，新增了一个获取a1的接口

sign服务启动
```bash
python basic_sign_server.py
```
### 安装依赖
```bash
pip install -r requirements.txt
```

### 配置env
在`.env.local`中配置参数
```dotenv
URL_GITHUB_TRENDING = "https://github.com/trending/python?since=daily"
URL_SIGN_A1 = "获取a1的四肢"
URL_SIGN_SIGN = "h签名地址"

OPENAI_APP_KEY = "your openai app key"
OPENAI_BASE_URL = "base irl"
OPENAI_MODEL = "gpt-4o-mini"

DOWNLOAD_DIR = "./projects_readme"
FONT_PATH = "./msyh.ttc"


LOG_DIR = "./log"
LOG_FILE = "app.log"
LOG_LEVEL = "INFO"
LOG_TO_CONSOLE = True

COOKIES = "创作中心 webprofile 中的 cookie"

```
配置之后修改文件名
```bash
cp .env.local .env
```

### 运行
```bash
python main.py
```
每日结果会存在 DOWNLOAD_DIR 目录下