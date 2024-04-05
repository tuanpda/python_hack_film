# libraries
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import json
import codecs
import random
from tqdm import tqdm
from datetime import datetime
import os
import time
import subprocess


from apscheduler.schedulers.blocking import BlockingScheduler

# from file pushdatafilmtosqlserver
from pushdatafilmtosqlserver import push_data_to_database

# Lấy ngày hiện tại
current_datetime = datetime.now()
current_date = current_datetime.strftime("%Y-%m-%d")
current_time = current_datetime.strftime("%H:%M:%S")
current_day = current_datetime.strftime("%A")

# # Đường dẫn file log
# filename = r"log_keophim.txt"

# # Định nghĩa video database
# videos = []

# # Mở file mới ở thư mục C:\
# with open(filename, "a", encoding="utf-8") as file:
#     file.write("# ----------------------------- \n")
#     file.write(f"1: DATE: {current_date} \n")
#     file.write(f"2: DAY: {current_day} \n")
#     file.write("3: Server Zuiphim.org \n")
#     file.write("4: Link: https://zuiphim.org/ \n")
#     file.write("# Starting ... \n")


# add video
def add_videos(
    _id,
    title,
    country,
    year,
    content,
    category,
    category_name,
    link,
    image,
    actor,
    streamsUrl,
    server,
):
    new_video = {}
    new_video["_id"] = _id
    new_video["title"] = title
    new_video["country"] = country
    new_video["year"] = year
    new_video["content"] = content
    new_video["category"] = category
    new_video["category_name"] = category_name
    new_video["link"] = link
    new_video["image"] = image
    new_video["actor"] = actor
    new_video["streamsUrl"] = streamsUrl
    new_video["server"] = server
    videos.append(new_video)

