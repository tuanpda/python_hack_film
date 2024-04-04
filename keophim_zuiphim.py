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
# print("Date:", current_date)
# print("Time:", current_time)
# print("Day:", current_day)

# Tạo tên file
filename = f"log_zuiphim.txt"
# define video database
videos = []
# open file
with open(filename, "a", encoding="utf-8") as file:
    file.write("# LOG KEO PHIM \n")
    file.write(f"1: DATE: {current_date} \n")
    file.write(f"2: TIME: {current_time} \n")
    file.write(f"3: DAY: {current_day} \n")
    file.write("4: Server Zuiphim \n")
    file.write("5: Link: https://zuiphim.org/ \n")
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


# Get Films Mới nhất
def get_Film_Data_Newest(
    link_phim,
    code_name_cat,
    name_of_cat,
    num_of_page,
    page_number,
    json_file_name,
):
    print(f"# Bắt đầu kéo {name_of_cat} \n")
    print(f"# Đang đặt thông số kéo {num_of_page} trang \n")
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"# Bắt đầu kéo {name_of_cat} \n")
        file.write(f"# Đang đặt thông số kéo {num_of_page} trang \n")

    while page_number <= num_of_page:
        print(f"# Đang lấy trang {page_number} của {name_of_cat}")
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"# Đang lấy trang {page_number} của {name_of_cat} \n")

        # Link get phim
        get_link = f"{link_phim}"

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
                            find_div = soup_data_movie.find(name="div", class_="text-center")
                        except AttributeError:
                            find_div = " "
                        # Tìm tất cả các thẻ 'a' có class là 'btn btn-default streaming-server'
                        try:
                            a_tags = find_div.find_all(
                                "a", class_="btn btn-default streaming-server"
                            )
                        except AttributeError:
                            a_tags = " "
                        # Lấy giá trị của thuộc tính 'data-link' từ mỗi thẻ 'a'
                        try:
                            data_links = [a["data-link"] for a in a_tags]
                        except AttributeError:
                            data_links = " "

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
                            'https://zuiphim.org/'
                        )

                        # ghi ra file json
                        with open(f"{json_file_name}", "w", encoding="utf-8") as write_file:
                            json.dump(videos, write_file, ensure_ascii=False)

        print(f"# Xong trang {page_number} của {name_of_cat} ")
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"# Xong trang {page_number} của {name_of_cat}  \n")
        page_number += 1

    print(f"# Kéo xong toàn bộ {num_of_page} trang {name_of_cat} ")
    print(f"# Bắt đầu đẩy dữ liệu vào DB")
    push_data_to_database(f"{code_name_cat}", f"{json_file_name}", 0)
    print(f"# Đẩy xong dữ liệu")

    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"# Kéo xong toàn bộ {num_of_page} trang {name_of_cat}  \n")
        file.write(f"# Bắt đầu đẩy dữ liệu vào DB \n")
        file.write(f"# Đẩy xong dữ liệu \n")


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
    # Thời gian bắt đầu kéo
    start_time = time.time()

    print(f"# Thời gian bắt đầu kéo: {start_time} \n")
    print(f"# Bắt đầu kéo {name_of_cat} \n")
    print(f"# Đang đặt thông số kéo {num_of_page} trang \n")
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"# Thời gian bắt đầu kéo: {start_time} \n")
        file.write(f"# Bắt đầu kéo {name_of_cat} \n")
        file.write(f"# Đang đặt thông số kéo {num_of_page} trang \n")

    while page_number <= num_of_page:
        print(f"# Đang lấy trang {page_number} của {name_of_cat}")
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"# Đang lấy trang {page_number} của {name_of_cat} \n")

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
                            find_div = soup_data_movie.find(name="div", class_="text-center")
                        except AttributeError:
                            find_div = " "
                        # Tìm tất cả các thẻ 'a' có class là 'btn btn-default streaming-server'
                        try:
                            a_tags = find_div.find_all(
                                "a", class_="btn btn-default streaming-server"
                            )
                        except AttributeError:
                            a_tags = " "
                        # Lấy giá trị của thuộc tính 'data-link' từ mỗi thẻ 'a'
                        try:
                            data_links = [a["data-link"] for a in a_tags]
                        except AttributeError:
                            data_links = " "

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
                            'https://zuiphim.org/'
                        )

                        # ghi ra file json
                        with open(f"{json_file_name}", "w", encoding="utf-8") as write_file:
                            json.dump(videos, write_file, ensure_ascii=False)

        print(f"# Xong trang {page_number} của {name_of_cat} ")
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"# Xong trang {page_number} của {name_of_cat}  \n")
        page_number += 1

    # Thời gian kết thúc
    end_time = time.time()
    # Thời gian đã trôi qua
    elapsed_time = end_time - start_time

    print(f"# Kéo xong toàn bộ {num_of_page} trang {name_of_cat} ")
    print(f"# Bắt đầu đẩy dữ liệu vào DB")
    push_data_to_database(f"{code_name_cat}", f"{json_file_name}", 1)
    print(f"# Đẩy xong dữ liệu")
    print(f"# Thời gian hoàn thành: {elapsed_time} giây")

    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"# Kéo xong toàn bộ {num_of_page} trang {name_of_cat}  \n")
        file.write(f"# Bắt đầu đẩy dữ liệu vào DB \n")
        file.write(f"# Đẩy xong dữ liệu \n")
        file.write(f"# Thời gian hoàn thành: {elapsed_time} giây \n")
        file.write(f"# Ending # \n")
        file.write(f"#   \n")
        file.write(f"#  ----- \n")


# các thông số cơ bản
linkphimnewest = 'https://zuiphim.org'
linkphim = "https://zuiphim.org/the-loai"
num_of_page_value = 10
page_number_value = 1

# GỌI HÀM GET PHIM MỚI
get_Film_Data_Newest(
    linkphimnewest,
    "NewMovie",
    "Phim mới",
    1,
    1,
    "zuiphim_phimmoi.json",
)

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
        film_type[3], #jsonfile
    ]
    functions_to_call.append({"function": get_Film_Data_With_Cat, "args": function_args})
    
# Gọi các hàm được lưu trong danh sách
for function_info in functions_to_call:
    function = function_info["function"]
    args = function_info["args"]
    function(*args)


# GỌI HÀM TRONG FILE KÉO PHIM TẠI SERVER XEMPHIMNGAY.COM
subprocess.run(["python", "keophim_xemphimngay.py"])