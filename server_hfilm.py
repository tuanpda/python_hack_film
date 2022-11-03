

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import codecs
import random

# define video database
videos = []
# add video


def add_videos(_id, video_title, video_link, video_mode, video_image, link_play, video_descript):
    new_video = {}
    new_video["_id"] = _id
    new_video["title"] = video_title
    new_video["link"] = video_link
    new_video["mode"] = video_mode
    new_video["image"] = video_image
    new_video["link_play"] = link_play
    new_video["descript"] = video_descript
    videos.append(new_video)

# get page 1 phim lẻ


def get_page_one():
    link_web = 'https://hfim.tk/the-loai/phim-le'
    response = requests.get(link_web)
    # encoding tiếng việt - fix lỗi font
    response.encoding = response.apparent_encoding
    data_web = response.text
    soup = BeautifulSoup(data_web, "html.parser")
    # tìm tất cả video từ thẻ div
    articles_div_video = soup.find_all(name="div", class_="ml-item")
    for video in articles_div_video:
        a_tag = video.find('a')
        title_video = a_tag.get('oldtitle')
        # print(title_video)

        href_video = a_tag.get('href')
        # print(href_video)
        link_video = urljoin(link_web, href_video)
        # print(link_video)

        span_tag = video.find('span')
        mode_video = span_tag.text
        # print(span_tag.text)

        img_tag = video.find('img')
        link_img = img_tag.get('data-original')
        # print(img_video)

        link_combine = []
        descript_video = []

        get_video_sgl = requests.get(link_video)
        data_web_sgl = get_video_sgl.text
        soup_sgl = BeautifulSoup(data_web_sgl, "html.parser")
        div_vd = soup_sgl.find_all(name="div", class_="movieplay")
        for div_link in div_vd:
            iframe_video = div_link.find('iframe')
            link_play = iframe_video.get('src')
            link_combine.append(link_play)
            # print(link_play)

        p_tag = soup_sgl.find(name="p", class_="f-desc")
        if (p_tag):
            des_video = p_tag.text
        else:
            des_video = ""

        add_videos(random.randint(1, 10000), title_video, link_video,
                   mode_video, link_img, link_combine, des_video)

# get page x


def get_page_another():
    get_num_page = 10
    page = 2
    link_web = 'https://hfim.tk/the-loai/phim-le'
    link_web_page = 'https://hfim.tk/the-loai/phim-le/page/'
    while (page <= get_num_page):
        get_page = str(page)
        link_full = urljoin(link_web_page, get_page)
        # print(link_full)
        response = requests.get(link_full)
        # encoding tiếng việt - fix lỗi font
        response.encoding = response.apparent_encoding
        data_web = response.text
        soup = BeautifulSoup(data_web, "html.parser")

        # tìm tất cả video từ thẻ div
        articles_div_video = soup.find_all(name="div", class_="ml-item")
        for video in articles_div_video:
            a_tag = video.find('a')
            title_video = a_tag.get('oldtitle')
            # print(title_video)

            href_video = a_tag.get('href')
            # print(href_video)
            link_video = urljoin(link_web, href_video)
            # print(link_video)

            span_tag = video.find('span')
            mode_video = span_tag.text
            # print(span_tag.text)

            img_tag = video.find('img')
            link_img = img_tag.get('data-original')
            # print(img_video)

            link_combine = []
            descript_video = []

            get_video_sgl = requests.get(link_video)
            data_web_sgl = get_video_sgl.text
            soup_sgl = BeautifulSoup(data_web_sgl, "html.parser")
            div_vd = soup_sgl.find_all(name="div", class_="movieplay")
            for div_link in div_vd:
                iframe_video = div_link.find('iframe')
                link_play = iframe_video.get('src')
                link_combine.append(link_play)
                # print(link_play)

            p_tag = soup_sgl.find(name="p", class_="f-desc")
            if (p_tag):
                des_video = p_tag.text
            else:
                des_video = ""

            add_videos(random.randint(1, 10000), title_video, link_video,
                       mode_video, link_img, link_combine, des_video)

        page += 1


def server_phimle():
    get_page_one()
    get_page_another()

    with open("z_data_hfilm_le.json", "w", encoding='utf-8') as write_file:
        json.dump(videos, write_file, ensure_ascii=False)

# get page 1 phim chiếu rạp


def get_page_one_chieu_rap():
    link_web = 'https://hfim.tk/the-loai/phim-chieu-rap'
    response = requests.get(link_web)
    # encoding tiếng việt - fix lỗi font
    response.encoding = response.apparent_encoding
    data_web = response.text
    soup = BeautifulSoup(data_web, "html.parser")
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

        link_combine = []
        # descript_video=[]

        get_video_sgl = requests.get(link_video)
        data_web_sgl = get_video_sgl.text
        soup_sgl = BeautifulSoup(data_web_sgl, "html.parser")
        div_vd = soup_sgl.find_all(name="div", class_="movieplay")
        for div_link in div_vd:
            iframe_video = div_link.find('iframe')
            link_play = iframe_video.get('src')
            link_combine.append(link_play)
            # print(link_play)

        p_tag = soup_sgl.find(name="p", class_="f-desc")
        des_video = p_tag.text

        add_videos(random.randint(1, 10000), title_video, link_video,
                   mode_video, link_img, link_combine, des_video)

# get page x


def get_page_another_chieurap():
    get_num_page = 40
    page = 2
    link_web = 'https://hfim.tk/the-loai/phim-chieu-rap'
    link_web_page = 'https://hfim.tk/the-loai/phim-chieu-rap/page/'
    while (page <= get_num_page):
        get_page = str(page)
        link_full = urljoin(link_web_page, get_page)
        # print(link_full)
        response = requests.get(link_full)
        # encoding tiếng việt - fix lỗi font
        response.encoding = response.apparent_encoding
        data_web = response.text
        soup = BeautifulSoup(data_web, "html.parser")

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

            link_combine = []
            descript_video = []

            get_video_sgl = requests.get(link_video)
            data_web_sgl = get_video_sgl.text
            soup_sgl = BeautifulSoup(data_web_sgl, "html.parser")
            div_vd = soup_sgl.find_all(name="div", class_="movieplay")
            for div_link in div_vd:
                iframe_video = div_link.find('iframe')
                link_play = iframe_video.get('src')
                link_combine.append(link_play)
                # print(link_play)

            p_tag = soup_sgl.find_all(name="p", class_="f-desc")
            for des in p_tag:
                des_video = des.text
                descript_video.append(des_video)

            add_videos(random.randint(1, 10000), title_video, link_video,
                       mode_video, link_img, link_combine, descript_video)

        page += 1


def server_phimchieurap():
    get_page_one_chieu_rap()
    # get_page_another_chieurap()

    with open("z_data_hfilm_chieurap.json", "w", encoding='utf-8') as write_file:
        json.dump(videos, write_file, ensure_ascii=False)


# running
server_phimle()
# server_phimchieurap()
