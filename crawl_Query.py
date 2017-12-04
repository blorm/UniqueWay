# coding: utf-8

import re
import urllib2
import time

# proxy
def setProxy():
    proxy_addr = '122.72.18.34:80'
    proxy_handler = urllib2.ProxyHandler({'http': 'http://' + proxy_addr})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)

def search(keyword):
    url = 'http://www.mafengwo.cn/search/s.php?q=' + keyword
    try:
        page = urllib2.urlopen(url).read().decode('utf-8')
        # print page
    except Exception:
        print 'url open error'
        exit()

    pattern = re.compile(u'<a href="http:.*html".*>景点 - <.*>')
    match = re.findall(pattern, page)

    if len(match) == 0:
        print 'No Results.'
    else:
        name = []
        urls = []
        pattern = re.compile(u'http://www.mafengwo.cn/poi/\d*.html')
        for i in range(len(match)):
            # print match[i]
            name.append( strip(match[i]) )
            urls.append( re.findall(pattern, match[i])[0] )
        return name, urls

def strip(s):
    ret = ''
    i = 0
    while i < len(s):
        if s[i] == '<':
            while i < len(s) and s[i] != '>':
                i += 1
        elif s[i] != u'\u000a' and s[i] != u'\u0020':
            ret += s[i]
        i += 1
    # print 'ret:', ret
    return ret

def findTime(urls):
    results = []
    for i in range(len(urls)):
        results.append('')
        # print urls[i]
        page = urllib2.urlopen(urls[i]).read().decode('utf-8')

        # too many visits in a sec will be banned !
        time.sleep(0.5)

        pattern = re.compile(u'用时参考</div>[\d\D]*<div class="content">.*</div>')
        match = re.findall(pattern, page)
        # print match
        for line in match:
            results[i] += strip(line)
    return results

if __name__ == '__main__':
    # setProxy()

    print '请输入目的地：',
    # dest = raw_input()
    dest = '清水寺'
    print dest

    name, urls = search(dest)
    if name != None:
        # print 'urls', urls
        time = findTime(urls)

    for i in range(len(time)):
        print name[i]
        if time[i] == '':
            print '  用时参考 x'
        else:
            print ' ', time[i]
