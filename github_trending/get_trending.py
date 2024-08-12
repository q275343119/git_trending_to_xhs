"""
Collect the README.md files from trending GitHub projects
"""
import datetime
import os.path
from lxml import etree

import requests
from bs4 import BeautifulSoup

from config import config_settings
from utils.logging_util import logger


def get_projects() -> list[dict]:
    """
    Retrieve the project name
    :return:
    """
    url = config_settings.url_github_trending
    logger.info(f"打开trending网页-{url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    repos = soup.find_all('article', class_='Box-row')

    trending_repos = []
    for repo in repos:
        repo_name = repo.h2.a['href'][1:]  # 获取仓库名

        logger.info(f"解析项目信息-{repo_name}")

        project_description = repo.p.text.strip() if repo.p else ""
        repo_url = f"https://github.com/{repo_name}"

        total_stars = repo.find_all("div")[2].a.text.strip()
        today_starts = repo.find_all("div")[2].find_all("span")[-1].text.strip()
        project_info_dict = {
            "name": repo_name,
            "project_description":project_description,
            "url": repo_url,
            "total_starts": total_stars,
            "today_start": today_starts
        }
        trending_repos.append(project_info_dict)
    logger.info(f"trending信息获取完毕")
    return trending_repos


def save_readme(file_name: str, context: bytes):
    """
    save readme
    :param file_name:
    :param context:
    :return:
    """
    md_dir = config_settings.download_dir
    now = datetime.datetime.now().strftime("%Y%m%d")
    save_dir_path = os.path.join(md_dir, now)
    if not os.path.exists(save_dir_path):
        os.mkdir(save_dir_path)
    with open(os.path.join(save_dir_path, file_name), 'wb') as f:
        f.write(context)


def get_default_branch(project_url):
    """
    get default branch of project
    :param project_url:
    :return:
    """
    response = requests.get(project_url)
    soup = BeautifulSoup(response.content, "html.parser")
    dom = etree.HTML(str(soup))
    default_branch = str(
        dom.xpath('//*[@id="branch-picker-repos-header-ref-selector"]/span/span[1]/div/div[2]/span/text()[2]')[0])
    return default_branch

def get_project_readme(projects: list[dict]):
    """
    download project's readme
    :param projects:
    :return:
    """
    csv = "project_name\tproject_description\tproject_url\ttotal_starts\ttoday_start"
    for d in projects:
        project_url = d["url"]
        project_name = d["name"]
        project_description = d["project_description"]
        total_starts = d["total_starts"]
        today_start = d["today_start"]

        logger.info(f"获取README.md-{project_name}")

        default_branch = get_default_branch(project_url)

        file_name = f"{project_name.split('/')[-1]}.md"
        md_url = f"https://raw.githubusercontent.com/{project_name}/{default_branch}/README.md"
        response = requests.get(md_url)
        if response.status_code == 200:
            save_readme(file_name, response.content)

        csv += f'\n{project_name}\t{project_description}\t{project_url}\t{total_starts}\t{today_start}'
    # Summary for today
    logger.info(f"保存今日trending")
    save_readme("Summary.csv", csv.encode("utf-8"))


def trending():
    projects = get_projects()
    get_project_readme(projects)



