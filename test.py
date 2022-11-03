
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import codecs
import random

get_video_sgl = requests.get('https://hfim.tk/truyen-thuyet-thuc-son-van-kiem-quy-tong.html')
data_web_sgl = get_video_sgl.text
soup_sgl = BeautifulSoup(data_web_sgl, "html.parser")

p_tag = soup_sgl.find(name="p", class_="f-desc")
des_video = p_tag.text
print(des_video)
