
from flask import Flask, render_template
from flask_paginate import Pagination, get_page_args
import json
import random

# Get Data from file JSON
# Get data film lẻ
with open("z_data_hfilm_le.json", "r", encoding='utf-8') as read_file:
    data_videos_phimle = json.load(read_file)

# Get data film chiếu rạp
with open("z_data_hfilm_chieurap.json", "r", encoding='utf-8') as read_file:
    data_videos_phimchieurap = json.load(read_file)

# get top film
get_top_phimle = []
for feed in data_videos_phimle[:24]:
    get_top_phimle.append(feed)

# get top film chiếu rạp
get_top_phimchieurap = []
for feed in data_videos_phimchieurap[:24]:
    get_top_phimchieurap.append(feed)

# get some film sigle phim le page
get_some_phimle_single = []
for feed in data_videos_phimle[:12]:
    get_some_phimle_single.append(feed)

# get some film sigle phim chiếu rạp page
get_some_chieurap_single = []
for feed in data_videos_phimchieurap[:12]:
    get_some_chieurap_single.append(feed)

# view_link


app = Flask(__name__)


def get_videos_phimle(offset=0, per_page=2):
    return data_videos_phimle[offset: offset + per_page]


def get_videos_chieurap(offset=0, per_page=2):
    return data_videos_phimchieurap[offset: offset + per_page]


@app.route('/')
def home():
    sampled_list = random.sample(data_videos_phimle, 5)
    # print(sampled_list)
    return render_template('index.html', all_posts=get_top_phimle, all_posts_chieurap=get_top_phimchieurap, random_videos=sampled_list)


@app.route('/<int:index>')
def show_post_le(index):
    requested_post = None
    link_iframe = None
    for blog_post in data_videos_phimle:
        if blog_post["_id"] == index:
            requested_post = blog_post
            link_iframe = requested_post['link_play']
            # print(link_iframe)

    return render_template("single.html", post=requested_post, all_iframe=link_iframe, all_posts=get_some_phimle_single)


@app.route('/phimle-posts')
def all_phimle():
    page, per_page, offset = get_page_args(
        page_parameter="page", per_page_parameter="per_page")
    total = len(data_videos_phimle)
    pagination_data_videos_phimle = get_videos_phimle(
        offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page,
                            total=total)
    return render_template("phimle.html", all_phimle=pagination_data_videos_phimle, page=page, per_page=per_page, pagination=pagination)


@app.route('/phimchieurap-posts')
def all_phimchieurap():
    page, per_page, offset = get_page_args(
        page_parameter="page", per_page_parameter="per_page")
    total = len(data_videos_phimchieurap)
    pagination_data_videos_phimchieurap = get_videos_chieurap(
        offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page,
                            total=total, css_framework='bootstrap4')
    return render_template("phimchieurap.html", all_phimchieurap=pagination_data_videos_phimchieurap, page=page, per_page=per_page, pagination=pagination)


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=80)
