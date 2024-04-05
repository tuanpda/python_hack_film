import os
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import json
import codecs
import random
from tqdm import tqdm
from datetime import datetime
import time
import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler

# from file pushdatafilmtosqlserver
from pushdatafilmtosqlserver import push_data_to_database

# get time
current_datetime = datetime.now()
current_date = current_datetime.strftime("%Y-%m-%d")
# current_time = current_datetime.strftime("%H:%M:%S")
current_day = current_datetime.strftime("%A")

# Định nghĩa video database
videos = []

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


link = "https://phimhay.ink/"

response = requests.get(link)
response.encoding = response.apparent_encoding
data_web = response.text

# Sử dụng BeautifulSoup để phân tích HTML
soup = BeautifulSoup(data_web, "html.parser")
print(soup)

# # Tìm tất cả các phần tử <div> có class là "card"
# article_div_videos = soup.find(
#     name="div",
#     class_="rocopa",
# )

# videos = article_div_videos.find_all(name="div", class_="swiper-slide slider__item")

# for video in videos:
#     href_video = video.find('a')['href']
#     title_video = video.find('a')['title']
#     image_video = video.find('img')['src']
#     content_video = video.find('p').text    
#     # print(href_video)
#     # print(title_video)
#     # print(image_video)
#     # print(content_video)
    
#     # access page video detail
#     get_detail_movie = requests.get(href_video)
#     print(get_detail_movie.status_code)
