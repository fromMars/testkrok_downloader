# coding: utf-8

import urllib2
import re
import socket
import cookielib
import urllib
import datetime
import threading
import os


def get(req,retries=3):
    try:
        response = urllib2.urlopen(req)
        data = response.read()
    except Exception , what:
        print what,req
        if retries>0:
            return get(req,retries-1)
        else:
            print 'GET Failed',req
            return ''
    return data

def get_qw(url, data_list=[], cnt=0, year=0, number=0, folder_name='0'):
    # Enable cookie support for urllib2
    #cookiejar = cookielib.CookieJar()
    #urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
    #urllib2.install_opener(urlOpener)

    headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'testkrok.org.ua',
            'Origin':'https://testkrok.org.ua',
            'Referer':'https://testkrok.org.ua/?test='+str(number),
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
        }
    f_data = {}
    print url
    referer_num = re.compile('\d+$')
    referer_number = referer_num.findall(url)[0]

    if cnt==0:
        pass
    elif cnt==1:
        f_data = {
            'testtype': 'mixed',
            'start': '1'
        }
    else:
        question_id = data_list[0]
        question_an = data_list[1]
        bbk = data_list[2]
        mix_value = data_list[3]
        f_data = {
            'question_id': question_id,
            'question_an': question_an,
            'answer': bbk,
            'mix': mix_value,
        }

    if cnt==0:
        request = urllib2.Request(url)
    else:
        request = urllib2.Request(url, urllib.urlencode(f_data), headers)

    #response = 0
    html = get(request)

    '''
    with open("C:\Users\ZMB\Documents\My WangWang\\b{0}.html".format(str(count)), "wb") as f1:
        f1.write(html)
    '''

    if cnt==0:
        url_f = re.compile('(?<=form action=").*?(?=")')
        url_dir = url_f.findall(html)[0]
        url = "https://testkrok.org.ua" + url_dir

        qw = 0
        bbk = 0
        question_an = 0
        question_id = 0
        mix_value = 0
    else:
        try:
            qw_f = re.compile('(?<=p class="qw">).*(?=</p>)')
            bbk_f = re.compile('(?<=var bbk=").*?(?=";)')
            an_q = re.compile('(?<=question_an" value=").*?(?=")')
            id_q = re.compile('(?<=question_id" value=").*?(?=")')
            mix_v = re.compile('(?<=name="mix" value=").*?(?=")')
            qw = qw_f.findall(html)[0]
            bbk = bbk_f.findall(html)[0]
            question_an = an_q.findall(html)[0]
            question_id = id_q.findall(html)[0]
            mix_value = mix_v.findall(html)[0]

            bbk_txt = 'name="answer" value="{0}" onclick="g();u()" /><label for="{0}1" onclick="">'.format(bbk)
            answer_text = re.compile('(?<=%s).*?(?=</label>)'%re.escape(bbk_txt))
            answer_t = answer_text.findall(html)[0]

            print "\n_____________@test={0}____________s".format(number)
            with open(r"/root/all/{0}/{1}.txt".format(folder_name, year), "a") as f:
                f.writelines('\r\n')
                f.write("\tQ({0}): ".format(cnt) + qw)
                f.write("\t\tA: ({0}){1}".format(bbk, answer_t))
                f.writelines('\r\n')
        except Exception as err2:
            print err2, "no question found, exit"
            return -1
    print cnt
    return [question_id, question_an, bbk, mix_value, url, referer_number]


def get_year(year, number, folder_name):
    # Enable cookie support for urllib2
    cookiejar = cookielib.CookieJar()
    urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
    urllib2.install_opener(urlOpener)

    url = "https://testkrok.org.ua"

    req = urllib2.Request(url)
    get(req)
    print "\n_____________@Homepage____________"

    url = "https://testkrok.org.ua/?test=" + number
    count = 0
    data_list = []

    with open(r"/root/all/{0}/{1}.txt".format(folder_name, year), "wb") as f:
        f.write("Created at: " + str(datetime.datetime.now()))
        f.write('\r\n')
    while 1:
        print data_list
        if data_list:
            url = data_list[4]
            number = data_list[5]
        data_list = get_qw(url, data_list, count, year, number, folder_name)
        if data_list==-1:
            return "{0}:{1} FINISHED.".format(number, year)
        count += 1


a1 = {
    "2241":"2005",
    "2242":"2006",
    "2243":"2007",
    "2598":"2008",
    "2244":"2009",
    "2245":"2010",
    "2394":"2011",
    "2757":"2012, Иностранцы",
    "2756":"2012",
    "2757":"2012, Иностранцы",
    "21106":"2013, Иностранцы",
    "21103":"2013",
    "21362":"2014"
}
a2011 = {
    "2097":"Акушерство и гинекология",
     "2098":"Гигиена",
     "2099":"Педиатрия, 1",
     "2100":"Педиатрия, 2 ",
     "2101":"Терапия, 1 ",
     "2102":"Терапия, 2 ",
     "2103":"Хирургия, 1 ",
     "2104":"Хирургия, 2 "
}
a2012 = {
    "2654":"Акушерство и гинекология, 1",
    "2655":"Акушерство и гинекология, 2",
    "2656":"Акушерство и гинекология, 3",
    "2660":"Педиатрия, 1",
    "2661":"Педиатрия, 2",
    "2662":"Педиатрия, 3",
    "2663":"Педиатрия, 4",
    "2657":"О1бщая врачебная подготовка, 1",
    "2658":"О2бщая врачебная подготовка, 2",
    "2659":"О3бщая врачебная подготовка, 3",
    "2664":"Терапия, 1",
    "2665":"Терапия, 2",
    "2666":"Терапия, 3",
    "2667":"Терапия, 4",
    "2668":"Терапия, 5",
    "2669":"Терапия, 6",
    "2670":"Хирургия, 1",
    "2671":"Хирургия, 2",
    "2672":"Хирургия, 3",
    "2673":"Хирургия, 4"
}
a2013 = {
    "21008":"Акушерство и гинекология",
    "21010":"Педиатрия, 1",
    "21011":"Педиатрия, 2",
    "21009":"Гигиена",
    "21012":"Терапия, 1",
    "21013":"Терапия, 2",
    "21014":"Терапия, 3",
    "21015":"Терапия, 4",
    "21016":"Хирургия, 1",
    "21017":"Хирургия, 2"
}
a2014 = {
    "21236":"Акушерство и гинекология",
    "21239":"Педиатрия, 1",
    "21240":"Педиатрия, 2",
    "21237":"Гигиена",
    "21238":"Организация здравохранения",
    "21241":"Терапия, 1",
    "21242":"Терапия, 2",
    "21243":"Терапия, 3",
    "21244":"Терапия, 4",
    "21245":"Хирургия, 1",
    "21246":"Хирургия, 2"
}

all_in_one = [a2012]

name_cnt = 2
for i in all_in_one:
    name_cnt += 1
    folder_name = str(name_cnt)
    for j in i:
        get_year(i[j], j, name_cnt)



#get_year("2013", "21362")


'''
for i in a1:
    threading.Thread(target=get_year, args=(i,a1[i]),
                                 name='thread-'+i).start()
    #t.start()
'''
