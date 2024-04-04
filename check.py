
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


link = "https://xemphimngay.com/the-loai/hanh-dong"

response = requests.get(link)
response.encoding = response.apparent_encoding
data_web = response.text

# Sử dụng BeautifulSoup để phân tích HTML
soup = BeautifulSoup(data_web, "html.parser")

# Tìm tất cả các phần tử <div> có class là "card"
article_div_video = soup.find(
    name="div",
    class_="grid grid-flow-row grid-cols-2 sm:grid-cols-3 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-6 gap-2",
)

find_movie  =  article_div_video.find('a')
# get thông tin push CSDL
href_movie = find_movie['href']
title_movie = find_movie['title']
image_movie = article_div_video.find('img')['data-src']

# get đến trang để lấy dữ liệu video
get_movie = requests.get(href_movie)
data_web_movie = get_movie.text
soup_data_movie = BeautifulSoup(data_web_movie, "html.parser")


# lấy thông tin cơ bản về phim
ul_info_films = soup_data_movie.find(name='ul', attrs={'class': 'grid grid-flow-row grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 mt-2 gap-2'})
if ul_info_films is not None:
    li_tags = ul_info_films.find_all(name='li')
    # print(li_tags)
    infos_movie = []
    for li_tag in li_tags:
        text = li_tag.find('span').text.strip()
        infos_movie.append(text)

# thời lượng
print(infos_movie[3])
# year
print(infos_movie[4])
# quốc gia
print(infos_movie[7]) 
# diễn viên
print(infos_movie[8])
# tác giả
print(infos_movie[9])


# Nội dung phim
try:
    content_movie = soup_data_movie.find(name='div', attrs={'class': 'whitespace-pre-wrap'}).text
except AttributeError:
    content_movie = ''

# tìm nút watch video mai sẽ xem xét việc nút có tồn tại hay không??
fin_button_watch = soup_data_movie.find(name='div', class_='absolute bottom-4 text-center w-full bg-main-700 bg-opacity-40 py-2 m-0')
link_movie_check = fin_button_watch.find("a")
if link_movie_check is not None:
    link_to_watch = fin_button_watch.find('a')['href']
    # đi đến link để lấy link media
    get_to_media_movie = requests.get(link_to_watch)
    data_wb = get_to_media_movie.text
    soup_data_wb = BeautifulSoup(data_wb, "html.parser")

    find_link = soup_data_wb.find(name='div', class_='flex items-center')
    a_tags = find_link.find_all('a')
    ob_link = []
    for a_tag in a_tags:
        data_link = a_tag.get('data-link')
        # print(data_link)
        ob_link.append(data_link)

    link_movie = ob_link[1]

print('link-media: ', link_movie)
print('href_movie: ', href_movie)
print('title_movie: ', title_movie)
print('image_movie: ', image_movie)
print('content_movie: ', content_movie)
print('thời lượng: ', infos_movie[3])
print('year: ', infos_movie[4])
print('country: ', infos_movie[7])
print('diễn viên: ', infos_movie[8])
print('author: ', infos_movie[9])

