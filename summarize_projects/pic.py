from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

from config import config_settings
from utils.logging_util import logger
"""
Generate image
"""


def generate_image():
    """
    生成图片
    :return:
    """
    logger.info(f"输出概览图片")
    today = datetime.now()
    # 设置图像大小，和原图保持一致
    img_width = 1440
    img_height = 1920
    img = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # 加载支持中文的字体
    try:
        font_path = config_settings.font_path # 请将此路径替换为你的实际字体文件路径
        font_title = ImageFont.truetype(font_path, 28)
        font_header = ImageFont.truetype(font_path, 22)
        font_text = ImageFont.truetype(font_path, 18)
    except IOError:
        font_title = ImageFont.load_default()
        font_header = ImageFont.load_default()
        font_text = ImageFont.load_default()

    # 添加标题和日期
    draw.text((img_width // 2 - 100, 20), "GitHub Daily Trending", fill=(0, 112, 192), font=font_title)  # 蓝色标题
    draw.text((img_width // 2 - 50, 70), today.strftime("%Y-%m-%d"), fill=(112, 112, 112), font=font_header)  # 灰色日期

    # 描绘表格内容
    y_position = 130
    padding = 20

    file_name = f"{config_settings.download_dir}/{today.strftime('%Y%m%d')}/Summary.csv"

    with open(file_name, "r", encoding="utf-8") as f:
        _ = f.readline()
        row = f.readline()
        while row:
            project_name, project_description, project_url, total_starts, today_start = row.strip().split("\t")
            draw.text((padding, y_position), f"{project_name}", fill=(33, 114, 184), font=font_text)  # 深蓝色项目名称

            # Stars 和 Today's Stars 右对齐
            stars_text = f"""★ {total_starts}  {today_start}"""
            text_bbox = draw.textbbox((0, 0), stars_text, font=font_text)
            text_width = text_bbox[2] - text_bbox[0]

            # 根据原图调整 Stars 和 Today's Stars 的颜色
            star_color = (255, 170, 0)  # 橙色的星星
            today_star_color = (0, 128, 0)  # 绿色的Today's Stars

            draw.text((img_width - padding - text_width, y_position), f"★ {total_starts}", fill=star_color,
                      font=font_text)  # 橙色stars

            draw.text(
                (img_width - padding - text_width + draw.textbbox((0, 0), f"★ {total_starts}", font=font_text)[2],
                 y_position),
                f"""  Today's stars: {today_start.replace(" stars today", "")}""", fill=today_star_color,
                font=font_text)  # 绿色Today's Stars

            # Description 自动换行
            desc = project_description
            max_width = img_width - 2 * padding
            current_line = ""
            lines = []
            for word in desc:
                line_with_word = current_line + word
                line_bbox = draw.textbbox((0, 0), line_with_word, font=font_text)
                line_width = line_bbox[2] - line_bbox[0]
                if line_width <= max_width:
                    current_line = line_with_word
                else:
                    lines.append(current_line)
                    current_line = word
            lines.append(current_line)

            for line in lines:
                y_position += 25
                draw.text((padding, y_position), line, fill=(0, 0, 0), font=font_text)  # 黑色描述

            # 绘制分隔线
            y_position += 35
            draw.line((padding, y_position, img_width - padding, y_position), fill=(200, 200, 200), width=2)  # 灰色分隔线

            y_position += 10

            row = f.readline()

            # 保存图像
        img.save(f"{config_settings.download_dir}/{today.strftime('%Y%m%d')}/TrendingProjects.png")



