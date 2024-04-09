# check đơn của https://xemphimngay.com/

import requests
from bs4 import BeautifulSoup
import re


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
    videos.append(new_video)


get_link = "https://zuiphim.org/the-loai/vien-tuong"


response = requests.get(get_link)
response.encoding = response.apparent_encoding
data_web = response.text
# Sử dụng BeautifulSoup để phân tích HTML
soup = BeautifulSoup(data_web, "html.parser")

# Tìm tất cả các phần tử <div> có class là "popup"
all_articles_div_video = soup.find(name="div", class_="popup")

# Lấy giá trị của thuộc tính style chứa URL của hình ảnh
style_attribute = all_articles_div_video.find("a", class_='ico-play ico-play-sm')
link_href = style_attribute['href']
if link_href is not None:
    # đến link detail video
    get_detail_movie = requests.get(link_href)
    if get_detail_movie.status_code==200:
        print(get_detail_movie)