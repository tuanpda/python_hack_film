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
    title,
    country,
    year,
    content,
    category,
    category_name,
    link,
    image,
    actor,
    thoiluong,
    author,
    streamsUrl,
    server,

):
    new_video = {}
    new_video["title"] = title
    new_video["country"] = country
    new_video["year"] = year
    new_video["content"] = content
    new_video["category"] = category
    new_video["category_name"] = category_name
    new_video["link"] = link
    new_video["image"] = image
    new_video["actor"] = actor
    new_video["thoiluong"] = thoiluong
    new_video["author"] = author
    new_video["streamsUrl"] = streamsUrl
    new_video["server"] = server

    videos.append(new_video)


def job():
    num_of_page = 3
    page_number = 1
    link_phim = "https://phimhay.ink/the-loai/phim-18"
    
    
    while page_number <= num_of_page:
        # Link get phim
        link = f"{link_phim}/?page={page_number}"

        response = requests.get(link)
        response.encoding = response.apparent_encoding
        data_web = response.text

        # Sử dụng BeautifulSoup để phân tích HTML
        soup = BeautifulSoup(data_web, "html.parser")

        # Tìm tất cả các phần tử <div> có class là "bs"
        article_div_videos_series_movies = soup.find_all(
            name="article",
            class_="bs",
        )

        for article_div_videos in tqdm(article_div_videos_series_movies, desc="Processing pages", unit="articles"):  # Sử dụng tqdm
            # thông tin ban đầu của video
            href_video = article_div_videos.find("a")["href"]
            title_video = article_div_videos.find("a")["title"]
            # print(title_video)
            image_video = article_div_videos.find(name="img")["src"]

            # đến link detail video
            get_detail_movie = requests.get(href_video)
            if get_detail_movie.status_code==200:
                data_web_detail = get_detail_movie.text
                soup_movie_detail = BeautifulSoup(data_web_detail, "html.parser")

                # thông tin movie
                info_movie = []
                spans_tag = soup_movie_detail.find(name="div", class_="spe")("span")
                for span_tag in spans_tag:
                    content = span_tag.get_text(strip=True)
                    info_movie.append(content.split(":")[1].strip())
                    # print(content.split(':')[1].strip())
                # print(info_movie)

                # link media
                link_href = ""
                get_hrf = soup_movie_detail.find(name="a", class_="bookmark")
                # print(get_hrf)
                if get_hrf is not None:
                    link_href = get_hrf["href"]
                    # get media tập hiện tại
                    get_media_movie = requests.get(link_href)
                    
                    if get_media_movie.status_code == 200:
                        # print(get_media_movie.status_code)
                        movie_detail = get_media_movie.text
                        get_movie_detail = BeautifulSoup(movie_detail, "html.parser")
                        li_tags = get_movie_detail.find("li", class_="episode")
                        a_tags = li_tags.find_all("a")
                        # print(a_tags[1]['data-link'])

                        # get link media tập hiện tại
                        link_media = ''
                        for a_tag in a_tags:
                            if a_tag["data-type"] == "embed":
                                link_media = a_tag["data-link"]
                        # print(link_media)

                    add_videos(
                        title_video,
                        info_movie[3],
                        info_movie[1],
                        "Phim 18 + không dành cho trẻ chưa đến tuổi vị thành niên. App sẽ không chịu trách nhiệm quản lý vấn đề này. Kiến nghị phụ huynh tự quản !",
                        "18PlusFilm",
                        "Phim 18Plus",
                        href_video,
                        image_video,
                        info_movie[7],
                        info_movie[2], # thời lượng
                        info_movie[6], # author
                        link_media,
                        "https://phimhay.ink/",
                    )
                    
        print(f'Done page', {page_number})
        
        page_number += 1
        

        # ghi ra file json
        with open(f"phimhay_phim18plus.json", "w", encoding="utf-8") as write_file:
            json.dump(videos, write_file, ensure_ascii=False)

        push_data_to_database("phim18plus","phimhay_phim18plus.json", 1)
        

# # Khởi tạo scheduler
# scheduler = BlockingScheduler()

# # Lập lịch cho công việc chạy vào mỗi ngày vào 17:45
# scheduler.add_job(job, "cron", hour=14, minute=0)

# # Lập lịch cho công việc chạy cứ mỗi 10 giờ kể từ 21:45 hàng ngày
# scheduler.add_job(job, "interval", hours=3)

# # Bắt đầu lịch trình
# try:
#     scheduler.start()
# except KeyboardInterrupt:
#     pass

job()