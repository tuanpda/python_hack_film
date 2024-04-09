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


def get_Film_Data_With_Cat(
    link_phim,
    code_name_cat,
    name_of_cat,
    code_cat_on_web,
    num_of_page,
    page_number,
    json_file_name,
):
    while page_number <= num_of_page:
        # Link get phim
        link = f"{link_phim}/{code_cat_on_web}?page={page_number}"
        print('Kéo thể loại: ' + link)
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

        for article_div_videos in tqdm(article_div_videos_series_movies, desc="Processing pages", unit="articles"):
            cat_video = article_div_videos.find(name="div", class_="typez Movie")
            if cat_video is not None:
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
                            info_movie[3], # country
                            info_movie[1], # year
                            "Chúc bạn xem phim vui vẻ tại App Phimhay. Hi vọng mang đến cho bạn trải nghiệm tốt nhất. Phim chưa có nội dung giới thiêu. Cảm ơn tất cả các bạn",
                            code_name_cat,
                            name_of_cat,
                            href_video,
                            image_video,
                            info_movie[7], # actors
                            info_movie[2], # thời lượng
                            info_movie[6], # author
                            link_media,
                            "https://phimhay.ink/",
                        )
        # Xong toàn bộ trang thì tiến hành ghi vào file json
        if not os.path.exists(json_file_name):
            # Nếu tệp không tồn tại, mở một tệp mới
            with open(json_file_name, "w", encoding="utf-8") as write_file:
                json.dump({}, write_file)  # Ghi một đối tượng JSON trống vào tệp mới
        # ghi data
        with open(f"{json_file_name}", "w", encoding="utf-8") as write_file: 
            json.dump(videos, write_file, ensure_ascii=False)
        
        print(f'Done page', page_number)
        # đối trang khác
        page_number += 1           

    # Ghi vào DB. xong toàn bộ trang của 1 thể loại thì đẩy vào 1 lần
    push_data_to_database(f"{code_name_cat}", f"{json_file_name}", 1)

def job():
    # các thông số cơ bản
    linkphim = "https://phimhay.ink/the-loai"
    num_of_page_value = 50
    page_number_value = 1
    server = "https://phimhay.ink"

    # GỌI HÀM GET PHIM THEO THỂ LOẠI
    # Khai báo các thông số cho từng loại phim
    film_types = [
        ("ActionFilm", "Phim hành động", "hanh-dong", "phimhay.json"),
        ("MartialFilm", "Phim võ thuật", "vo-thuat", "phimhay.json"),
        ("AnimelFilm", "Phim hoạt hình", "hoat-hinh", "phimhay.json"),
        ("HorrorFilm", "Phim kinh dị", "kinh-di", "phimhay.json"),
        ("WarFilm", "Phim chiến tranh", "chien-tranh", "phimhay.json"),
        ("PolFilm", "Phim hình sự", "hinh-su", "phimhay.json"),
        ("LoveFilm", "Phim tình cảm", "tinh-cam", "phimhay.json"),
        ("StudentFilm", "Phim học đường", "hoc-duong", "phimhay.json"),        
        ("SportFilm", "Phim thể thao", "the-thao", "phimhay.json"),
        ("FictionlFilm", "Phim viễn tưởng", "vien-tuong", "phimhay.json"),
        ("ClassicFilm", "Phim kinh điển", "kinh-dien", "phimhay_kinhdien.json"),
        ("SoulFilm", "Phim tâm lý", "tam-ly", "phimhay_tamly.json"),
        ("MusicFilm", "Phim âm nhạc", "am-nhac", "phimhay_amnhac.json"),
        ("SecretFilm", "Phim bí ẩn", "bi-an", "phimhay_bian.json"),
        ("CotrangFilm", "Phim cổ trang", "co-trang", "phimhay_cotrang.json"),
        ("FunnyFilm", "Phim hài hước", "hai-huoc", "phimhay_haihuoc.json"),
        ("ChinhkichFilm", "Phim chính kịch", "chinh-kich", "phimhay_chinhkich.json"),
        ("ThanthoaiFilm", "Phim thần thoại", "than-thoai", "phimhay_thanthoai.json"),
        ("FamilyFilm", "Phim gia đình", "gia-dinh", "phimhay_giadinh.json"),
    ]

    functions_to_call = []

    # Lặp qua danh sách các loại phim và thêm các hàm gọi vào danh sách functions_to_call
    for film_type in film_types:
        function_args = [
            linkphim,
            film_type[0],  # code_name_cat
            film_type[1],  # name_of_cat
            film_type[2],  # code_cat_on_web
            num_of_page_value,
            page_number_value,
            film_type[3],  # jsonfile
        ]
        functions_to_call.append(
            {"function": get_Film_Data_With_Cat, "args": function_args}
        )
        
    # Gọi các hàm được lưu trong danh sách
    for function_info in functions_to_call:
        function = function_info["function"]
        args = function_info["args"]
        function(*args)


       
job()
