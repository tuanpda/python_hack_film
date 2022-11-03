


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import codecs
import random

link_web = 'https://hfim.tk/series'
response = requests.get(link_web)
# encoding tiếng việt - fix lỗi font 
response.encoding = response.apparent_encoding
data_web = response.text
soup = BeautifulSoup(data_web, "html.parser")

videos = []

# add video
def add_videos(_id, video_title, video_link, video_mode, video_image, link_play):
    new_video = {}
    new_video["_id"] = _id
    new_video["title"] = video_title
    new_video["link"] = video_link
    new_video["mode"] = video_mode
    new_video["image"] = video_image  
    new_video["link_play"] = link_play
    videos.append(new_video)

# tìm tất cả video từ thẻ div
articles_div_video = soup.find_all(name="div", class_="ml-item")
for video in articles_div_video:
    a_tag = video.find('a')
    title_video = a_tag.get('oldtitle')
    # print(title_video)

    href_video = a_tag.get('href')
    link_video = urljoin(link_web, href_video)
    # print(urljoin(link_web, href_video))

    span_tag = video.find('span')
    mode_video = span_tag.text
    # print(span_tag.text)

    img_tag = video.find('img')
    link_img = img_tag.get('data-original')
    # print(img_video)

    link_combine=[]
    get_video_sgl = requests.get(link_video)
    data_web_sgl = get_video_sgl.text
    soup_sgl = BeautifulSoup(data_web_sgl, "html.parser")
    div_vd = soup_sgl.find_all(name="div", class_="movieplay")
    for div_link in div_vd:
        iframe_video= div_link.find('iframe')
        link_play = iframe_video.get('src')
        link_combine.append(link_play)
        # print(link_play)
        
    add_videos(random.randint(1, 10000), title_video, link_video, mode_video, link_img, link_combine)

    
with open("z_data_hfilm_bo.json", "w", encoding='utf-8') as write_file:
    json.dump(videos, write_file, ensure_ascii=False)