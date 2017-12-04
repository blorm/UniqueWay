# coding: utf-8

import urllib2
import re


# proxy
def setProxy():
    proxy_addr = '61.155.164.112:3128'
    proxy_handler = urllib2.ProxyHandler({'http': 'http://' + proxy_addr})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)

# search travel notes of 'keyword', return 'n' lines of url
def search(keyword, n):
    # &t=info 游记

    try:
        url = 'http://www.mafengwo.cn/search/s.php?q=' + keyword + '&t=info'
        page = urllib2.urlopen(url, timeout=3).read().decode('utf-8')
    except:
        print 'url open error'
        exit()
    pattern = re.compile(u'相关结果\d*条')
    match = re.findall(pattern, page)

    if len(match) == 0:
        print '[error]' + keyword + ' not found !!!'
        print page
        exit()

    print keyword, match[0]
    results = int(match[0][4:-1])
    if results < n:
        print '相关结果没有', n, '条', \
              '将只显示', results, '条'
        n = results
    else:
        print '相关结果共有', results, '条', \
              '将显示前', n, '条'

    p = 1
    list = [keyword.decode('utf-8')]
    sum = 0
    # 15 results per page
    while sum < n:
        url = 'http://www.mafengwo.cn/search/s.php?q=' + keyword\
              + '&t=info' + '&p=' + str(p)
        page = urllib2.urlopen(url).read().decode('utf-8')

        pattern = re.compile(u'http://www.mafengwo.cn/i/\d*.html')
        match = re.findall(pattern, page)
        # print match
        for i in match:
            if i != list[-1]:
                list.append(i)
                sum += 1
        p += 1

    return list[0: n+1]

# strip <> from html page, return travel notes words
def strip(url):
    # url = 'http://www.mafengwo.cn/i/959258.html'
    page = urllib2.urlopen(url).read().decode('utf-8')
    # print len(page)

    page = adDelete(page)

    # &nbsp; &gt;
    pattern = re.compile(r'&nbsp;|&gt;')
    page = re.sub(pattern, ' ', page)

    # html head meta script link body div a p span i li ul img strong
    html_marker = ['head', 'script', 'style']
    printFlag = 1       # 1: print   0: no print
    i = 0
    info = [url, ]
    while i < len(page):
        if page[i] == '<':
            j = i + 1
            while j < len(page) and page[j] != '>':
                j += 1
            # <>
            if j == i+1:
                pass
            # <xxxxx />
            elif page[j-1] == '/':
                pass
            # <!xxxxxx>
            elif i+1 < len(page) and page[i+1] == '!':
                # <!-- xxxx -->
                if i+3 < len(page) and page[i+1: i+4] == '!--':
                    j = i + 4
                    while j+3 < len(page) and page[j+1: j+4] != '-->':
                        j += 1
                    j += 3
            # </xxx>
            elif i+1 < len(page) and page[i+1] == '/':
                s = page[i+2: j]
                if s in html_marker:
                    printFlag = 1
            # <xxx  xxxx>
            else:
                k = i + 1
                while page[k] != ' ' and page[k] != '>':
                    k += 1
                s = page[i+1: k]
                if s in html_marker:
                    printFlag = 0
            i = j + 1
        elif page[i] == ' ' or page[i] == u'\u0009' or page[i] == u'\u000a':
            i += 1
        elif printFlag == 1:
            j = i + 1
            while j < len(page) and page[j] != '<':
                j += 1
            # print page[i: j]        #ord(page[i]),
            info.append(page[i:j])
            i = j
        else:
            i += 1
    return info

# delete heads and tails, only return <div class="main">
def adDelete(page):
    if u'>不再显示<' in page:
        start = page.index(u'>不再显示<')
    elif u'<div class="main">' in page:
        start = page.index(u'<div class="main">')
    else:
        start = 0

    if u'<div class="float-bar hide">' in page:
        end = page.index(u'<div class="float-bar hide">')
    else:
        end = len(page)-1
    # print 'start:', start
    # print 'end:',   end
    # if start == 0 or end == 0:
    #     print 'adDelete error'
    return page[start: end+1]

#
def timeSelect(slice):
    info = []
    # 时间 用时
    # 20分钟 2小时 半小时 一刻钟 几分钟
    #早上 下午 夜里
    key = [u'用时', u'时间', u'小时', u'分钟', u'刻钟'
           u'早上', u'下午', u'晚上', u'夜里']

    # x月 x日 x号 x天
    # 07:00 11:00 11：00 11点20 11点
    # 11.20-11.30
    pattern = re.compile(u'\d[月日号天]+|\d{1,2}[:：点]+|'
                         u'\d{1,2}\.\d{1,2}')

    for i in range(len(slice)):
        match = re.findall(pattern, slice[i])
        if len(match) > 0:
            info.append(i)
        else:
            for j in key:
                if j in slice[i]:
                    info.append(i)
                    break

    return info


if __name__ == '__main__':

    setProxy()

    keyword = '清水寺'
    n = 2
    urls = search(keyword, n)
    for i in urls:
        print i
    for i in range(1, n+1):
        slice = strip(urls[i])
        # page = adDelete(page)
        print
        print keyword, i, '/', n, ':', urls[i]
        time = timeSelect(slice)
        for i in time:
            print slice[i]
    # page = strip(list[1])
    # page = adDelete(page)
    # for i in page:
    #     print i