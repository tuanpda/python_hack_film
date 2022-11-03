# import codecs
# import json

# data = [{
#     'title': 'Chị vợ quyến rũ em rể ngay tại nhà bố mẹ',
#     'link': 'https://vlxx.sex/video/chi-vo-quyen-ru-em-re-ngay-tai-nha-bo-me/1640/',
#     'image': 'https://vlxx.sex/img2/1640.jpg',
#     'image_alt': 'ĐỖI VỢ - 2020'
# }

# ]

# with codecs.open('your_file.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False)


import json

sampleDict= {
    "string1": "明彦",
    "string2": u"\u00f8"
}
with open("unicodeFile.json", "w", encoding='utf-8') as write_file:
    json.dump(sampleDict, write_file, ensure_ascii=False)
print("Done writing JSON serialized Unicode Data as-is into file")

with open("unicodeFile.json", "r", encoding='utf-8') as read_file:
    print("Reading JSON serialized Unicode data from file")
    sampleData = json.load(read_file)
print("Decoded JSON serialized Unicode data")
print(sampleData["string1"], sampleData["string1"])