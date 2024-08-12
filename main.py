# daily job
from github_trending.get_trending import trending
from summarize_projects.pic import generate_image
from summarize_projects.summarize import get_summarize_for_all
from upload_note.upload import upload_note
from utils.logging_util import logger


def main():
    """
    主任务
    :return:
    """
    logger.info("启动")

    # 1.获取今日趋势
    trending()
    # 2.总结今日趋势
    get_summarize_for_all()
    # 3.导出今日趋势图片
    generate_image()
    # 4.上传笔记
    upload_note()

    logger.info("结束")


if __name__ == '__main__':
    main()
