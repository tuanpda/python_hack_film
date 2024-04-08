from bs4 import BeautifulSoup

html_content = """
<div class="text-center text-primary">
    <a data-id="115143" data-link="https://hls1.streamc.xyz/9cbc0b930b197bb333f03aa55dd24e90/hls.m3u8" data-type="m3u8" onclick="chooseStreamingServer(this)" class="btn btn-default streaming-server active">
        <i class="icon-play"></i>
        <span class="title">VIP #2</span>
    </a>
</div>
"""

soup = BeautifulSoup(html_content, "html.parser")
a_tags = soup.find_all("a")

data_links = ''
for a_tag in soup.find_all("a"):
    if a_tag["data-type"] == "embed":
        data_links = a_tag["data-link"]

print(data_links)
