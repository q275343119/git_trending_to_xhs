from openai import OpenAI
from datetime import datetime, timedelta

from config import config_settings
from utils.logging_util import logger

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=config_settings.openai_app_key,
    base_url=config_settings.openai_base_url
)


def gpt_35_api(messages: list):
    """为提供的对话消息创建新的回答

    Args:
        messages (list): 完整的对话消息
    """
    completion = client.chat.completions.create(model=config_settings.openai_model, messages=messages)
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


def load_project_list(now: datetime):
    """
    获取项目清单
    :param now:
    :return:
    """
    file_path = f"{config_settings.download_dir}/{now.strftime('%Y%m%d')}/Summary.csv"
    with open(file_path, 'r',encoding='utf-8') as f:
        csv = f.read()
    return csv


def get_summarize_for_all():
    """
    总结所有的项目
    :return:
    """
    logger.info("基于chatGPT总结今日trending")
    now = datetime.now()
    messages = [
        {"role": "system",
         "content": f"""你作为一个资深的程序员，每天都有逛github的习惯，并且非常善于总结，且乐于分享，稍后我会将今日({now.strftime('%Y-%m-%d')})python语言的trending项目发给你。
         你需要输出一段小红书笔记，用于概括和总结今天的趋势。要求：尽可能多的使用emoji，字数限定在300字以内
         """},
    ]
    now = datetime.now()
    csv = load_project_list(now)

    messages.append({"role": "user", "content": csv})

    content = gpt_35_api(messages)

    with open(f"{config_settings.download_dir}/{now.strftime('%Y%m%d')}/xhs_note.txt","w",encoding='utf-8') as f:
        f.write(content)






if __name__ == '__main__':
    get_summarize_for_all()
    # print(load_project_list(datetime.now()))
