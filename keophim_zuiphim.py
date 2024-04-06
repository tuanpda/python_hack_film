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

# Đường dẫn file log
filename = r"log_keophim.txt"

# Định nghĩa video database
videos = []

# Mở file mới ở thư mục C:\
with open(filename, "a", encoding="utf-8") as file:
    file.write("# ----------------------------- \n")
    file.write(f"1: DATE: {current_date} \n")
    file.write(f"2: DAY: {current_day} \n")
    file.write("3: Server Zuiphim.org \n")
    file.write("4: Link: https://zuiphim.org/ \n")
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


# Get Films
def get_Film_Data_With_Cat(
    link_phim,
    code_name_cat,
    name_of_cat,
    code_cat_on_web,
    num_of_page,
    page_number,
    json_file_name,
):
    start_time = datetime.now()
    print("Job started at:", start_time)

    print(f"# Start scan {name_of_cat} \n")
    print(f"# Scan {num_of_page} page \n")
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"Job started at: {start_time} \n")
        file.write(f"# Start scan {name_of_cat} \n")
        file.write(f"# Scan {num_of_page} page \n")

    while page_number <= num_of_page:
        print(f"# Scan page {page_number} of {name_of_cat}")
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"# Scan page {page_number} of {name_of_cat} \n")

        # Link get phim
        get_link = f"{link_phim}/{code_cat_on_web}?page={page_number}"

        response = requests.get(get_link)
        response.encoding = response.apparent_encoding
        data_web = response.text

        # Sử dụng BeautifulSoup để phân tích HTML
        soup = BeautifulSoup(data_web, "html.parser")

        # Tìm tất cả các phần tử <div> có class là "popup"
        all_articles_div_video = soup.find_all(name="div", class_="popup")

        for article_div_video in tqdm(
            all_articles_div_video, desc="Getting up to data", unit=" article"
        ):
            # Lấy giá trị của thuộc tính style chứa URL của hình ảnh
            style_attribute = article_div_video.find(
                "div", class_="latest-movie-img-container"
            ).get("style")
            image_url = (
                re.search(r"url\('([^']+)'\)", style_attribute).group(1)
                if style_attribute
                else None
            )

            # Lấy giá trị của thuộc tính href từ thẻ <a>
            try:
                href_value = article_div_video.find("a", class_="ico-play").get("href")
            except AttributeError:
                href_value = ""

            # Lấy giá trị của thuộc tính title từ thẻ <div>
            try:
                title_value = article_div_video.get("title")
            except AttributeError:
                title_value = ""

            # get đến trang chứa video phim để tìm nút bấm vào watch lấy phim
            get_detail_movie = requests.get(href_value)
            if get_detail_movie.status_code == 200:
                data_web_detail = get_detail_movie.text
                soup_movie_detail = BeautifulSoup(data_web_detail, "html.parser")

                # Get content nội dung phim có trong class addthis_inline_share_toolbox_yl99
                try:
                    info_movie = soup_movie_detail.find(
                        name="div", class_="addthis_inline_share_toolbox_yl99"
                    ).text.strip()
                except AttributeError:
                    country = "None"

                # Get Country - nước sản xuất
                p_tags_with_country = soup_movie_detail.find_all(
                    lambda tag: tag.name == "p" and "Quốc gia:" in tag.text
                )
                try:
                    country = p_tags_with_country[0].find("a").get("title", None)
                except AttributeError:
                    country = "None"

                # Get Năm phát hành - Year
                p_tags_with_year = soup_movie_detail.find_all(
                    lambda tag: tag.name == "p" and "Năm phát hành:" in tag.text
                )[0]
                try:
                    year = p_tags_with_year.text.replace("Năm phát hành: ", "").strip()
                except AttributeError:
                    year = " "

                # Get diễn viên
                p_tags_with_actor = soup_movie_detail.find_all(
                    lambda tag: tag.name == "p" and "Diễn Viên:" in tag.text
                )[0]
                try:
                    actor = (
                        p_tags_with_actor.find("a")
                        .get("tite", " ")
                        .replace("Diễn viên", "")
                        .strip()
                    )
                except AttributeError:
                    actor = " "

                # Tìm tất cả các thẻ div có class là 'btn_watch'
                find_link = soup_movie_detail.find(name="div", class_="block_watch")
                href_movie_check = find_link.find("a")
                if href_movie_check is not None:
                    href_movie = find_link.find("a")["href"]

                    # get đến trang để lấy dữ liệu video
                    get_movie = requests.get(href_movie)
                    if get_movie.status_code == 200:
                        data_web_movie = get_movie.text
                        soup_data_movie = BeautifulSoup(data_web_movie, "html.parser")

                        # tìm tất cả các thẻ div có class là text-center
                        try:
                            find_div = soup_data_movie.find(
                                name="div", class_="text-center"
                            )
                        except AttributeError:
                            find_div = " "
                        # Tìm tất cả các thẻ 'a' có class là 'btn btn-default streaming-server'
                        try:
                            a_tags = find_div.find_all(
                                "a", class_="btn btn-default streaming-server"
                            )
                        except AttributeError:
                            a_tags = []
                            
                        data_links = ''
                        if len(a_tags) > 1: 
                            # print(a_tags[1])
                            data_links = a_tags[1]['data-link']
                        else:
                            data_links = a_tags[0]['data-link']
                            
                            # for a_tag in a_tags[1:]:
                            #     # print(a_tag['data-link'])
                            #     data_links = a_tag['data-link']
                        # Lấy giá trị của thuộc tính 'data-link' từ mỗi thẻ 'a'
                        # try:
                        #     data_links = [a["data-link"] for a in a_tags]
                        #     # data_links = a_tags[1]["data-link"]
                        # except AttributeError:
                        #     data_links = " "
                        # if len(a_tags) == 1:
                        #     data_links = a_tags[0]  # Lấy phần tử đầu tiên
                        # elif len(a_tags) >= 2:
                        #     data_links = a_tags[1]  # Lấy phần tử thứ hai
                        # else:
                        #     data_links = ""
                        # print(data_links)
                        add_videos(
                            random.randint(1, 10000),
                            title_value,
                            country,
                            year,
                            info_movie,
                            code_name_cat,
                            name_of_cat,
                            href_value,
                            image_url,
                            actor,
                            data_links,
                            "https://zuiphim.org/",
                        )

                        # ghi ra file json
                        with open(
                            f"{json_file_name}", "w", encoding="utf-8"
                        ) as write_file:
                            json.dump(videos, write_file, ensure_ascii=False)

        print(f"# Done page {page_number} of {name_of_cat} ")
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"# Done page {page_number} of {name_of_cat}  \n")
        page_number += 1

    end_time = datetime.now()
    print("Job finished at:", end_time)

    elapsed_time = end_time - start_time
    print("Elapsed time:", elapsed_time)

    print(f"# Done all {num_of_page} page {name_of_cat} ")
    push_data_to_database(f"{code_name_cat}", f"{json_file_name}", 1)

    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"# Scan all page {num_of_page} of page {name_of_cat}  \n")
        file.write(f"# Start push into DB \n")
        file.write(f"# Done at {end_time} \n")
        file.write(f"# Elapsed time about {elapsed_time} \n")


def job():
    # các thông số cơ bản
    linkphim = "https://zuiphim.org/the-loai"
    num_of_page_value = 50
    page_number_value = 1
    server = "https://zuiphim.org"

    # GỌI HÀM GET PHIM THEO THỂ LOẠI
    # Khai báo các thông số cho từng loại phim
    film_types = [
        ("ActionFilm", "Phim hành động", "hanh-dong", "zuiphim_phimhanhdong.json"),
        ("MartialFilm", "Phim võ thuật", "vo-thuat", "zuiphim_phimvothuat.json"),
        ("AnimelFilm", "Phim hoạt hình", "hoat-hinh", "zuiphim_phimhoathinh.json"),
        ("HorrorFilm", "Phim kinh dị", "kinh-di", "zuiphim_phimkinhdi.json"),
        ("WarFilm", "Phim chiến tranh", "chien-tranh", "zuiphim_phimchientranh.json"),
        ("PolFilm", "Phim hình sự", "hinh-su", "zuiphim_phimhinhsu.json"),
        ("LoveFilm", "Phim tình cảm", "tinh-cam", "zuiphim_phimtinhcam.json"),
        ("StudentFilm", "Phim học đường", "hoc-duong", "zuiphim_phimhocduong.json"),
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

    # GỌI HÀM TRONG FILE KÉO PHIM TẠI SERVER XEMPHIMNGAY.COM
    subprocess.run(["python", "keophim_xemphimngay.py"])


# # Khởi tạo scheduler
# scheduler = BlockingScheduler()

# # Lập lịch cho công việc chạy vào mỗi ngày vào 17:45
# scheduler.add_job(job, "cron", hour=14, minute=15)

# # Lập lịch cho công việc chạy cứ mỗi 10 giờ kể từ 21:45 hàng ngày
# scheduler.add_job(job, "interval", hours=4)

# # Bắt đầu lịch trình
# try:
#     scheduler.start()
# except KeyboardInterrupt:
#     pass

job()
