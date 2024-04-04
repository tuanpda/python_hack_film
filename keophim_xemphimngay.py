# libraries
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import json
import codecs
import random
from tqdm import tqdm
import datetime
import time
import subprocess

# from file pushdatafilmtosqlserver
from pushdatafilmtosqlserver import push_data_to_database

# Lấy ngày hiện tại
current_datetime = datetime.datetime.now()
current_date = current_datetime.strftime("%Y-%m-%d")
current_time = current_datetime.strftime("%H:%M:%S")
current_day = current_datetime.strftime("%A")
# Tạo file
filename = f"log_xemphimngay.txt"
# define video database
videos = []
# open file
with open(filename, "a", encoding="utf-8") as file:
    file.write("# LOG KEO PHIM \n")
    file.write(f"1: DATE: {current_date} \n")
    file.write(f"2: TIME: {current_time} \n")
    file.write(f"3: DAY: {current_day} \n")
    file.write("4: Server Xemphimngay \n")
    file.write("5: Link: https://xemphimngay.com/ \n")
    file.write("# Starting ... \n")


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


# Get Films with category
def get_Film_Data_With_Cat(
    link_phim,
    code_name_cat,
    name_of_cat,
    code_cat_on_web,
    num_of_page,
    page_number,
    json_file_name,
):
    # Thời gian bắt đầu kéo
    start_time = time.time()
    
    print(f"# Time start scan: {start_time} \n")
    print(f"# start scan {name_of_cat} \n")
    print(f"# Đang đặt thông số kéo {num_of_page} trang \n")
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"# Thoi gian bat dau keo: {start_time} \n")
        file.write(f"# Bat dau keo {name_of_cat} \n")
        file.write(f"# Thong so keo {num_of_page} trang \n")

    while page_number <= num_of_page:
        # Link get phim
        get_link = f"{link_phim}/{code_cat_on_web}?page={page_number}"

        response = requests.get(get_link)
        response.encoding = response.apparent_encoding
        data_web = response.text

        # Sử dụng BeautifulSoup để phân tích HTML
        soup = BeautifulSoup(data_web, "html.parser")

        # Tìm tất cả các phần tử <div> có class là "card"
        article_div_video = soup.find(
            name="div",
            class_="grid grid-flow-row grid-cols-2 sm:grid-cols-3 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-6 gap-2",
        )
        find_movies = article_div_video.find_all("a")
        for find_movie in tqdm(find_movies, desc="Getting up to data", unit=" article"):
            # get thông tin push CSDL
            href_movie = find_movie["href"]
            title_movie = find_movie["title"]
            image_movie = find_movie.find("img")["data-src"]

            # get đến trang để lấy dữ liệu video
            get_movie = requests.get(href_movie)
            if get_movie.status_code == 200:
                data_web_movie = get_movie.text
                soup_data_movie = BeautifulSoup(data_web_movie, "html.parser")

                # lấy thông tin cơ bản về phim
                ul_info_films = soup_data_movie.find(
                    name="ul",
                    attrs={
                        "class": "grid grid-flow-row grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 mt-2 gap-2"
                    },
                )
                if ul_info_films is not None:
                    li_tags = ul_info_films.find_all(name="li")
                    # print(li_tags)
                    infos_movie = []
                    for li_tag in li_tags:
                        text = li_tag.find("span").text.strip()
                        infos_movie.append(text)

                # thời lượng
                # print(infos_movie[3])
                # # year
                # print(infos_movie[4])
                # # quốc gia
                # print(infos_movie[7])
                # # diễn viên
                # print(infos_movie[8])
                # # tác giả
                # print(infos_movie[9])

                # Nội dung phim
                try:
                    content_movie = soup_data_movie.find(
                        name="div", attrs={"class": "whitespace-pre-wrap"}
                    ).text
                except AttributeError:
                    content_movie = ""

                # tìm nút watch video mai sẽ xem xét việc nút có tồn tại hay không??
                fin_button_watch = soup_data_movie.find(
                    name="div",
                    class_="absolute bottom-4 text-center w-full bg-main-700 bg-opacity-40 py-2 m-0",
                )
                link_movie_check = fin_button_watch.find("a")
                if link_movie_check is not None:
                    link_to_watch = fin_button_watch.find("a")["href"]
                    # đi đến link để lấy link media
                    get_to_media_movie = requests.get(link_to_watch)
                    if get_to_media_movie.status_code == 200:
                        data_wb = get_to_media_movie.text
                        soup_data_wb = BeautifulSoup(data_wb, "html.parser")

                        find_link = soup_data_wb.find(name="div", class_="flex items-center")
                        a_tags = find_link.find_all("a")
                        ob_link = []
                        for a_tag in a_tags:
                            data_link = a_tag.get("data-link")
                            # print(data_link)
                            ob_link.append(data_link)
                        # print(ob_link)
                        link_movie = ob_link[1]

                        add_videos(
                            random.randint(1, 10000),
                            title_movie,
                            infos_movie[7],
                            infos_movie[4],
                            content_movie,
                            code_name_cat,
                            name_of_cat,
                            href_movie,
                            image_movie,
                            infos_movie[8],
                            link_movie,
                            'https://xemphimngay.com/'
                        )

                        # ghi ra file json
                        with open(f"{json_file_name}", "w", encoding="utf-8") as write_file:
                            json.dump(videos, write_file, ensure_ascii=False)

        print(f"# Xong trang {page_number} của {name_of_cat} ")
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"# Xong trang {page_number} cua {name_of_cat}  \n")
        page_number += 1
        
    # Thời gian kết thúc
    end_time = time.time()
    # Thời gian đã trôi qua
    elapsed_time = end_time - start_time

    print(f"# Keo xong toan bo {num_of_page} trang {name_of_cat} ")
    print(f"# Day du lieu DB")
    push_data_to_database(f"{code_name_cat}", f"{json_file_name}", 1)
    print(f"# Done")
    print(f"# Time hoan thanh: {elapsed_time} giây")

    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"# Keo xong toan bo {num_of_page} trang {name_of_cat}  \n")
        file.write(f"# Bat dau day du lieu vao DB \n")
        file.write(f"# Day xong du lieu \n")
        file.write(f"# Thoi gian hoan thanh: {elapsed_time} giây \n")
        file.write(f"# Ending # \n")
        file.write(f"#   \n")
        file.write(f"#  ----- \n")

# các thông số cơ bản
linkphim = "https://xemphimngay.com/the-loai"
num_of_page_value = 3
page_number_value = 1
server='https://xemphimngay.com'
# Khai báo các thông số cho từng loại phim
film_types = [
    ("ActionFilm", "Phim hành động", "hanh-dong", "xemphimngay_phimhanhdong.json"),
    ("MartialFilm", "Phim võ thuật", "vo-thuat", "xemphimngay_phimvothuat.json"),
    ("AnimelFilm", "Phim hoạt hình", "hoat-hinh", "xemphimngay_phimhoathinh.json"),
    ("HorrorFilm", "Phim kinh dị", "kinh-di", "xemphimngay_phimkinhdi.json"),
    ("WarFilm", "Phim chiến tranh", "chien-tranh", "xemphimngay_phimchientranh.json"),
    ("PolFilm", "Phim hình sự", "hinh-su", "xemphimngay_phimhinhsu.json"),
    ("LoveFilm", "Phim tình cảm", "tinh-cam", "xemphimngay_phimtinhcam.json"),
    ("StudentFilm", "Phim học đường", "hoc-duong", "xemphimngay_phimhocduong.json"),
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
        film_type[3], #jsonfile
    ]
    functions_to_call.append({"function": get_Film_Data_With_Cat, "args": function_args})
    
# Gọi các hàm được lưu trong danh sách
for function_info in functions_to_call:
    function = function_info["function"]
    args = function_info["args"]
    function(*args)
