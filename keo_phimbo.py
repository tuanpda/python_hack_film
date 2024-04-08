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
from pushdatafilmseries import push_data_to_database

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
    streamsUrl,
    server,
    tongsotap,
    thoiluong,
    status,
    tapso,
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
    new_video["streamsUrl"] = streamsUrl
    new_video["server"] = server
    new_video["tongsotap"] = tongsotap
    new_video["thoiluong"] = thoiluong
    new_video["status"] = status
    new_video["tapso"] = tapso
    videos.append(new_video)


def job():
    num_of_page = 50
    page_number = 1
    link_phim = "https://phimhay.ink/danh-sach/phim-bo"

    while page_number <= num_of_page:

        link = "https://phimhay.ink/danh-sach/phim-bo"
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
        # print(article_div_videos)

        for article_div_videos in article_div_videos_series_movies:
            # thông tin ban đầu của video
            href_video = article_div_videos.find("a")["href"]
            title_video = article_div_videos.find("a")["title"]
            image_video = article_div_videos.find(name="img")["src"]
            category_video = article_div_videos.find(
                name="div", class_="typez Drama"
            ).text.strip()
            tapso_video = (
                article_div_videos.find(name="div", class_="bt")
                .find(name="span", class_="epx")
                .text.strip()
            )
            tapso_number = tapso_video.split()[-1]

            # đến link detail video
            get_detail_movie = requests.get(href_video)
            # print(get_detail_movie.status_code)
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
                # print(link_href)
                # get media tập hiện tại
                get_media_movie = requests.get(link_href)
                # print(get_media_movie.status_code)
                if get_media_movie.status_code == 200:
                    # print(get_media_movie.status_code)
                    movie_detail = get_media_movie.text
                    get_movie_detail = BeautifulSoup(movie_detail, "html.parser")
                    li_tags = get_movie_detail.find("li", class_="episode")
                    a_tags = li_tags.find_all("a")
                    # print(a_tags[1]['data-link'])

                    # get link media tập hiện tại
                    link_media = a_tags[1]["data-link"]

                    # get các tập khác của film
                    series_movie_list = soup_movie_detail.find(
                        name="div", class_="eplister"
                    )("li")
                    # số lượng phim trong series_movie_list
                    total_series_movies = len(series_movie_list)
                    # bỏ qua tập hiện tại
                    first_element_skipped = False
                    for i, ser_mov in tqdm(
                        enumerate(series_movie_list, start=1), total=total_series_movies
                    ):
                        if i == 1:
                            continue  # Bỏ qua phần tử đầu tiên và tiếp tục vòng lặp
                        link_tap = ser_mov.find("a")["href"]
                        tap_so = ser_mov.find("div", class_="epl-num").text

                        href_link_tap = requests.get(link_tap)
                        if href_link_tap.status_code == 200:
                            mv_dt = href_link_tap.text
                            get_tapkhac = BeautifulSoup(mv_dt, "html.parser")
                            li_tags = get_tapkhac.find("li", class_="episode")
                            a_tags = li_tags.find_all("a")
                            # get link media tập hiện tại
                            link_media = ''
                            for a_tag in a_tags:
                                if a_tag["data-type"] == "embed":
                                    link_media = a_tag["data-link"]
                            # print(link_media)

                            # add video các tập trong seri
                            add_videos(
                                title_video,
                                info_movie[3],
                                info_movie[1],
                                "",
                                "SeriesMovies",
                                "Phim bộ",
                                href_video,
                                image_video,
                                info_movie[7],
                                link_media,
                                "https://phimhay.ink/",
                                info_movie[5],
                                info_movie[2],
                                info_movie[0],
                                tap_so,
                            )

                add_videos(
                    title_video,
                    info_movie[3],
                    info_movie[1],
                    "Phim 18 + không dành cho trẻ chưa đến tuổi vị thành niên. App sẽ không chịu trách nhiệm quản lý vấn đề này. Kiến nghị phụ huynh tự quản !",
                    "SeriesMovies",
                    "Phim bộ",
                    href_video,
                    image_video,
                    info_movie[7],
                    link_media,
                    "https://phimhay.ink/",
                    info_movie[5],
                    info_movie[2],
                    info_movie[0],
                    tapso_number,
                )
        print(f"Xong trang: ", page_number)
        page_number += 1

        # ghi ra file json
        with open(f"phimhay_phimbo.json", "w", encoding="utf-8") as write_file:
            json.dump(videos, write_file, ensure_ascii=False)

        push_data_to_database("phimhay_phimbo.json")


# # Khởi tạo scheduler
# scheduler = BlockingScheduler()

# # Lập lịch cho công việc chạy vào mỗi ngày vào 17:45
# scheduler.add_job(job, "cron", hour=10, minute=25)

# # Lập lịch cho công việc chạy cứ mỗi 10 giờ kể từ 21:45 hàng ngày
# scheduler.add_job(job, "interval", hours=2)

# # Bắt đầu lịch trình
# try:
#     scheduler.start()
# except KeyboardInterrupt:
#     pass

job()
