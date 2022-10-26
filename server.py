


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

link_web = 'https://vlxx.sex/'
response = requests.get(link_web)
data_web = response.text
soup = BeautifulSoup(data_web, "html.parser")

# head_tag = soup.find("head")
# # print(head_tag)
# title_page = head_tag.find("title").get("title")
# # print(title_page.get_text())
# link_page = head_tag.find("link").get("href")
# # print(link_page)

videos = []

# add video
def add_videos(video_title, video_link, video_image, image_alt):
    new_video = {}
    new_video["title"] = video_title
    new_video["link"] = video_link
    new_video["image"] = video_image
    new_video["image_alt"] = image_alt
    videos.append(new_video)

# tìm tất cả video từ thẻ div
articles_div_video = soup.find_all(name="div", class_="video-item")
# print(articles_div_video)
for artic_tag in articles_div_video:
    # lấy thẻ a từ thẻ div cha
    articles_tag_a = artic_tag.find("a")
    # get title video từ thẻ a
    title_video = articles_tag_a.get("title")

    # get link video từ thẻ a
    link_tag = articles_tag_a.get("href")
    link_video = urljoin(link_web, link_tag)

    # get image từ thẻ a
    img_tag = articles_tag_a.find("img")
    img_alt = img_tag.get("alt")
    img_link = img_tag.get("data-original")
    
    add_videos(title_video, link_video, img_link, img_alt)
    
# print(videos)
# lấy 10 trang tiếp theo
url_next = 2
link_part = "https://vlxx.sex/new/"

while (url_next <= 20):
    url_next_link = str(url_next)
    link_web = urljoin(link_part, url_next_link)
    response = requests.get(link_web)
    data_web = response.text
    soup = BeautifulSoup(data_web, "html.parser")
    
    articles_div_video = soup.find_all(name="div", class_="video-item")
    for artic_tag in articles_div_video:
        articles_tag_a = artic_tag.find("a")
        title_video = articles_tag_a.get("title")
        link_tag = articles_tag_a.get("href")
        link_video = urljoin(link_web, link_tag)
        img_tag = articles_tag_a.find("img")
        img_alt = img_tag.get("alt")
        img_link = img_tag.get("data-original")       
        add_videos(title_video, link_video, img_link, img_alt)
        
    url_next += 1
    
print(videos[0])