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

# lấy tên phim
title_movie = ""
get_title = all_articles_div_video.find("div", class_="movie-title")
if get_title is not None:
    title_movie = get_title.find("a").text.strip()

# Lấy href video
style_attribute = all_articles_div_video.find("a", class_="ico-play ico-play-sm")
link_href = style_attribute["href"]
if link_href is not None:
    # đến link detail video
    get_detail_movie = requests.get(link_href)
    if get_detail_movie.status_code == 200:
        data_web_detail = get_detail_movie.text
        soup_movie_detail = BeautifulSoup(data_web_detail, "html.parser")
        find_info_video = soup_movie_detail.find(
            name="div", class_="row movies-list-wrap"
        )

        # lấy đường dẫn ảnh
        image_movie = ""
        img_tag = find_info_video.find("img")
        if img_tag is not None:
            image_movie = img_tag["src"]

        # Get content nội dung phim có trong class addthis_inline_share_toolbox_yl99
        content_movie = ""
        get_ifmv = soup_movie_detail.find(
            name="div", class_="addthis_inline_share_toolbox_yl99"
        )
        if get_ifmv is not None:
            content_movie = get_ifmv.text.strip()

        # lấy country
        country = ''
        p_tags_with_country = soup_movie_detail.find_all(
            lambda tag: tag.name == "p" and "Quốc gia:" in tag.text
        )
        if p_tags_with_country is not None:
            country = p_tags_with_country[0].find("a").get("title", None)
            
        # Get Năm phát hành - Year
        year = ''
        p_tags_with_year = soup_movie_detail.find_all(
            lambda tag: tag.name == "p" and "Năm phát hành:" in tag.text
        )[0]
        if p_tags_with_year is not None:
            year = p_tags_with_year.text.replace("Năm phát hành: ", "").strip()

        # Get diễn viên
        p_tags_with_actor = soup_movie_detail.find_all(
            lambda tag: tag.name == "p" and "Diễn Viên:" in tag.text
        )

        print(p_tags_with_actor)
