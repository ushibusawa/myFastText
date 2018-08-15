from lxml import html
import requests
import os
import sys

baseurl = 'http://lumely.org/qma/'

genre = ['anime_game', 'sport', 'entertainment', 'lifestyle',
         'society', 'literature', 'science']

rule = ['true_or_false', 'four', 'associate', 'sort', 'panel',
        'slot', 'type', 'effect', 'cube', 'order',
        'line', 'multi', 'group']

# 縦が形式、横がジャンル（７つ）
page_id_list = [805, 896, 922, 923, 924, 925, 926,
                842, 898, 946, 948, 950, 952, 954,
                845, 900, 971, 974, 975, 976, 977,
                847, 902, 1004, 1005, 1006, 1007, 1008,
                849, 904, 1019, 1020, 1021, 1022, 1023,
                851, 906, 1033, 1034, 1035, 1036, 1037,
                855, 908, 1047, 1048, 1049, 1050, 1051,
                857, 910, 1061, 1062, 1063, 1064, 1065,
                859, 912, 1080, 1076, 1077, 1078, 1079,
                861, 914, 1088, 1089, 1090, 1091, 1092,
                863, 916, 1101, 1102, 1103, 1104, 1105,
                865, 918, 1116, 1117, 1118, 1119, 1120,
                871, 920, 1123, 1124, 1125, 1126, 1127]

files = []
for r in rule:
    for g in genre:
         files.append(g + '-' + r + '.html')

download_urls = []
for page_id in page_id_list:
    url = 'http://lumely.org/qma/?page_id=' + str(page_id)
    download_urls.append(url)

for (file, url) in zip(files, download_urls):
    page = requests.get(url, timeout=5)
    with open(file, 'wb') as fout:
        fout.write(page.content)
        print (file + ' is saved.')
