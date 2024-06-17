import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import json
import codecs
import random

# define video database
videos = []

# add video
def add_videos(_id, title, country, year, content, category, category_name, link, image, actor, streamsUrl):
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

link1 = 'https://zuiphim.org/'
link2 = 'https://zuiphim.org/danh-sach/phim-le'

response = requests.get(link1)
response.encoding = response.apparent_encoding
data_web = response.text

# Sử dụng BeautifulSoup để phân tích HTML
soup = BeautifulSoup(data_web, "html.parser")

# Tìm tất cả các phần tử <div> có class là "popup"
all_articles_div_video = soup.find_all(name="div", class_="popup")

for article_div_video in all_articles_div_video:
    # Lấy giá trị của thuộc tính style chứa URL của hình ảnh
    style_attribute = article_div_video.find("div", class_="latest-movie-img-container").get("style")
    image_url = re.search(r"url\('([^']+)'\)", style_attribute).group(1) if style_attribute else None

    # Lấy giá trị của thuộc tính href từ thẻ <a>
    href_value = article_div_video.find("a", class_="ico-play").get("href")

    # Lấy giá trị của thuộc tính title từ thẻ <div>
    title_value = article_div_video.get("title")

    # get đến trang chứa video phim để tìm nút bấm vào watch lấy phim
    get_detail_movie = requests.get(href_value)
    data_web_detail = get_detail_movie.text
    soup_movie_detail = BeautifulSoup(data_web_detail, "html.parser")
    
    # Get content nội dung phim có trong class addthis_inline_share_toolbox_yl99
    info_movie = soup_movie_detail.find(name='div', class_='addthis_inline_share_toolbox_yl99').text.strip()

    # Get Country - nước sản xuất
    p_tags_with_country = soup_movie_detail.find_all(lambda tag: tag.name == 'p' and 'Quốc gia:' in tag.text)[0]
    country = p_tags_with_country.find('a').get('title')

    # Get Năm phát hành - Year
    p_tags_with_year = soup_movie_detail.find_all(lambda tag: tag.name == 'p' and 'Năm phát hành:' in tag.text)[0]
    year = p_tags_with_year.text.replace('Năm phát hành: ', '').strip()

    # Get diễn viên
    p_tags_with_actor = soup_movie_detail.find_all(lambda tag: tag.name == 'p' and 'Diễn Viên:' in tag.text)[0]
    try: 
        actor = p_tags_with_actor.find('a').get('tite', ' ').replace('Diễn viên', '').strip()
    except AttributeError:
        actor = ' '
    
    # Tìm tất cả các thẻ div có class là 'btn_watch'
    find_link = soup_movie_detail.find(name='div', class_='block_watch').find('a')
    href_movie= find_link['href']
    
    # get đến trang để lấy dữ liệu video
    get_movie = requests.get(href_movie)
    data_web_movie = get_movie.text
    soup_data_movie = BeautifulSoup(data_web_movie, "html.parser")
    
    # tìm tất cả các thẻ div có class là text-center
    find_div = soup_data_movie.find(name='div', class_='text-center')
    # Tìm tất cả các thẻ 'a' có class là 'btn btn-default streaming-server'
    a_tags = find_div.find_all('a', class_='btn btn-default streaming-server')
    # Lấy giá trị của thuộc tính 'data-link' từ mỗi thẻ 'a'
    data_links = [a['data-link'] for a in a_tags]
    
    # print data
    print(info_movie)
    # print(image_url)
    # print(href_value)
    # print(title_value)
    # print(info_movie)
    # print(country)
    # print(year)
    # print(actor)
    # print(data_links)
    
    # def add_videos(_id, title, country, year, content, category, category_name, link, image, actor, streamsUrl):
    
#     add_videos(random.randint(1, 10000), title_value, country,
#                    year, info_movie, 'NewMovie', 'Phim mới', href_value, image_url, actor, data_links)
    

# with open("zuiphim_phimmoi.json", "w", encoding='utf-8') as write_file:
#         json.dump(videos, write_file, ensure_ascii=False)
    
