import sys
import urllib.request
import re 
import random
import threading 
import time
from bs4 import BeautifulSoup
from Class import FanHao

def cili_parse(fanhao,proxy_headers):
    global cili_fanhaos
    cili_fanhaos = []
    try:
        fanhao_url = 'http://www.cili.tv/search/%s_ctime_1.html'%urllib.request.quote(fanhao.decode(sys.stdin.encoding).encode('utf8'))
        proxy_request = urllib.request.Request(fanhao_url,headers=proxy_headers)
        response = urllib.request.urlopen(proxy_request,timeout=5)
        fanhao_html = response.read()
    except Exception:
        return cili_fanhaos

    soup = BeautifulSoup(fanhao_html,"html.parser")
    soup_items = soup.find_all("div",attrs={"class":"item"})
    if soup_items:
        for item in soup_items:
            title = item.a.text.strip()
            info = item.find("div",attrs={"class":"info"}) 
            spans = info.find_all("span")
            file_size = str(spans[1].b.text)
            downloading_count = int(str(spans[2].b.string))
            magnet_url = str(spans[3].find("a").get('href'))
            resource = 'Cili'
            resource_url = 'http://www.cili.tv'
            fanhao = FanHao(title,file_size,downloading_count,None,magnet_url,resource,resource_url)
            cili_fanhaos.append(fanhao)
    return cili_fanhaos

def btdb_parse(fanhao,proxy_headers):
    global btdb_fanhaos
    btdb_fanhaos = []
    try:
        fanhao_url = 'http://btdb.in/q/%s/'%urllib.request.quote(fanhao.decode(sys.stdin.encoding).encode('utf8'))
        proxy_request = urllib.request.Request(fanhao_url,headers=proxy_headers)
        response = urllib.request.urlopen(proxy_request,timeout=10)
        fanhao_html = response.read()
    except Exception:
        return btdb_fanhaos

    soup = BeautifulSoup(fanhao_html,"html.parser")
    soup_items = soup.find_all("li",attrs={"class":"search-ret-item"})
    if soup_items:
        for item in soup_items:
            title = item.find("h2").find("a").get("title")
            info = item.find("div",attrs={"class":"item-meta-info"}).find_all("span",attrs={"class":"item-meta-info-value"})
            file_size = info[0].text
            downloading_count = int(info[-1].text)
            file_number = int(info[1].text)
            magnet_url = item.find("div",attrs={"class":"item-meta-info"}).find("a",attrs={"class":"magnet"}).get("href")
            resource = 'BTDB'
            resource_url = 'http://btdb.in'
            fanhao = FanHao(title,file_size,downloading_count,file_number,magnet_url,resource,resource_url)
            btdb_fanhaos.append(fanhao)
    return btdb_fanhaos



def btcherry_parse(fanhao,bt_page,proxy_headers):
    globals()['btcherry_fanhaos_%s' %str(bt_page)]=[]
   
    try:
        fanhao_url = 'http://www.btcherry.net/search?keyword='+urllib.request.quote(fanhao.decode(sys.stdin.encoding).encode('utf8'))+'&p='+str(bt_page)
        proxy_request = urllib.request.Request(fanhao_url,headers=proxy_headers)
        response = urllib.request.urlopen(proxy_request,timeout=10)
        fanhao_html = response.read()
    except Exception:
        return globals()['btcherry_fanhaos_%s' %str(bt_page)]
    
    soup = BeautifulSoup(fanhao_html,"html.parser")
    soup_items = soup.find_all("div",attrs={"class":"r"})
    if soup_items:
        for item in soup_items:
            try:
                title = item.find("h5",attrs={"class":"h"}).text
                if title.rfind('> */@')>0:
                    title=title[title.rfind("> */@")+5:]
                elif title.rfind('> */]@')>0:
                    title=title[title.rfind("> */]@")+6:]
                if title.rfind('> */')>0:
                    title=title[title.rfind("> */")+4:]        
                info = item.find("div").find_all("span")
                file_size = info[2].find("span",attrs={"class":"prop_val"}).text
                file_number = int(info[4].find("span",attrs={"class":"prop_val"}).text)
                magnet_url = item.find("div").find("a").get("href")
            except Exception:
                pass
             
            resource = 'BTCherry'
            resource_url = 'http://www.btcherry.net'
            fanhao = FanHao(title,file_size,None,file_number,magnet_url,resource,resource_url)
            globals()['btcherry_fanhaos_%s' %str(bt_page)].append(fanhao)
    return globals()['btcherry_fanhaos_%s' %str(bt_page)]

def zhongziIn_parse(fanhao,proxy_headers):
    global zhongziIn_fanhaos
    zhongziIn_fanhaos = []
   
    try:
        fanhao_url = 'http://www.zhongzi.in/s/'+urllib.request.quote(fanhao.decode(sys.stdin.encoding).encode('utf8'))
        proxy_request = urllib.request.Request(fanhao_url,headers=proxy_headers)
        response = urllib.request.urlopen(proxy_request,timeout=10)
        fanhao_html = response.read()
    except Exception:
        return zhongziIn_fanhaos
    
    soup = BeautifulSoup(fanhao_html,"html.parser")
    soup_items = soup.find("div",attrs={"class":"wx_list"}).find_all("li")
    
    if soup_items:
        for item in soup_items:
            title = item.find("a").get('title')
            info = item.find("span",attrs={"class":"j_size"})
            file_size = info.text.split(":")[1] 
            magnet_url = info.find("a").get('href') 
            resource = 'zhongzi.in'
            resource_url = 'http://www.zhongzi.in'
            fanhao = FanHao(title,file_size,None,None,magnet_url,resource,resource_url)
            zhongziIn_fanhaos.append(fanhao)
    return zhongziIn_fanhaos
    

def btku_parse(fanhao,proxy_headers):
    global btku_fanhaos
    btku_fanhaos = []
   
    try:
        fanhao_url = 'http://www.btku.me/q/%s/'%urllib.request.quote(fanhao.decode(sys.stdin.encoding).encode('utf8'))
        proxy_request = urllib.request.Request(fanhao_url,headers=proxy_headers)
        response = urllib.request.urlopen(proxy_request,timeout=10)
        fanhao_html = response.read()
    except Exception:
        return btku_fanhaos
    
    soup = BeautifulSoup(fanhao_html,"html.parser")
    soup_items = soup.find("div",attrs={"id":"search_Results"}).find_all("li",attrs={"class":"results"})
    if soup_items:
        for item in soup_items:
            title = item.find("h2").find("a").text
            info = item.find("p",attrs={"class":"resultsIntroduction"})
            file_number = int(info.find_all("label")[0].string)
            file_size = info.find_all("label")[1].string
            downloading_count = int(info.find_all("label")[2].string)
            magnet_url = info.find("span",attrs={"class":"downLink"}).find_all("a")[1].get('href')
            resource = 'BTKU'
            resource_url = 'http://www.btku.me'
            fanhao = FanHao(title,file_size,downloading_count,file_number,magnet_url,resource,resource_url)
            btku_fanhaos.append(fanhao)
    return btku_fanhaos

def Qululu_parse(fanhao,proxy_headers):
    global Qululu_fanhaos
    Qululu_fanhaos = []
   
    try:
        fanhao_url = 'http://www.qululu.cn/search1/b/%s/1/hot_d'%fanhao.decode(sys.stdin.encoding).encode('utf8').encode('hex')
        proxy_request = urllib.request.Request(fanhao_url,headers=proxy_headers)
        response = urllib.request.urlopen(proxy_request,timeout=10)
        fanhao_html = response.read()
    except Exception:
        return Qululu_fanhaos
    
    soup = BeautifulSoup(fanhao_html,"html.parser")
    soup_items = soup.find("ul",attrs={"class":"mlist"}).find_all("li")
    if soup_items:
        for item in soup_items:
            title = item.find("div",attrs={"class":"T1"}).find("a").string
            title = re.sub('<span class="mhl">','',re.sub('</span>','',title.decode('hex')))
            info = item.find("dl",attrs={"class":"BotInfo"}).find("dt").find_all("span")
            file_size = info[0].string.replace(' ','')
            file_number = int(info[1].string)
            downloading_count = int(info[3].string)
            magnet_url = item.find("div",attrs={"class":"dInfo"}).find("a").get('href')
            resource = 'Qululu'
            resource_url = 'http://www.qululu.cn'
            fanhao = FanHao(title,file_size,downloading_count,file_number,magnet_url,resource,resource_url)
            Qululu_fanhaos.append(fanhao)
    return Qululu_fanhaos

def nimasou_parse(fanhao,proxy_headers):
    global nimasou_fanhaos
    nimasou_fanhaos = []
   
    try:
        fanhao_url = 'http://www.nimasou.com/l/%s-hot-desc-1'%urllib.request.quote(fanhao.decode(sys.stdin.encoding).encode('utf8'))
        proxy_request = urllib.request.Request(fanhao_url,headers=proxy_headers)
        response = urllib.request.urlopen(proxy_request,timeout=10)
        fanhao_html = response.read()
    except Exception:
        return nimasou_fanhaos
    
    soup = BeautifulSoup(fanhao_html,"html.parser")
    try:
        soup_items = soup.find("table",attrs={"class":"table"}).find_all("tr")
    except Exception:
        return nimasou_fanhaos
    if soup_items:
        for item in soup_items:
            title = item.find("td",attrs={"class":"x-item"}).find("a",attrs={"class":"title"}).text
            info = item.find("td",attrs={"class":"x-item"}).find("div",attrs={"class":"tail"}).text.split(':')
            file_size = info[2].split(' ')[1] + info[2].split(' ')[2]
            downloading_count = int(info[3].split(' ')[1])
            magnet_url = item.find("td",attrs={"class":"x-item"}).find("div",attrs={"class":"tail"}).find("a").get('href')
            resource = 'NiMaSou'
            resource_url = 'http://www.nimasou.com'
            fanhao = FanHao(title,file_size,downloading_count,None,magnet_url,resource,resource_url)
            nimasou_fanhaos.append(fanhao)
    return nimasou_fanhaos

def print_result(fanhaos):
    if fanhaos:
        for fanhao in fanhaos:
            try:
                print(('名称:%s'%fanhao.title))
                print(('文件大小:%s'%fanhao.file_size))
                if fanhao.downloading_count:
                    print(('热度:%d'%fanhao.downloading_count))
                else:
                    print ('热度:--')
                if fanhao.file_number:
                    print(('文件数:%s'%str(fanhao.file_number)))
                else:
                    print ('文件数:--')
                print(('磁力链接:%s'%fanhao.magnet_url))
                print(('来源:%s'%fanhao.resource))
                print(('-'*40))
            except Exception:
                pass
        print(('资源数:%d个'%len(fanhaos)))
    else:
        print ('抱歉未找到相关资源！')


def set_headers():
    headers1 = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6','Accept':'text/html;q=0.9,*/*;q=0.8','Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3'}
    headers2 = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5'}
    headers3 = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'}
    headers4 = {'User-Agent:':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
    headers = [headers1,headers2,headers3,headers4]
    return random.choice(headers)
    

def create_url(fanhaos):
    fanhao_html = open("Index.html","r",encoding='utf-8').read()
    soup = BeautifulSoup(fanhao_html,"html.parser")
    fanhao_tbody_html = soup.find("tbody")
    for index,fanhao in enumerate(fanhaos):
        tr_tag = soup.new_tag('tr')
        fanhao_tbody_html.insert(0,tr_tag)
        
        fanhao_tbody_tr = fanhao_tbody_html.find('tr')
        th_tag = soup.new_tag('th')
        th_tag.string = str(len(fanhaos)-index)
        fanhao_tbody_tr.insert(0,th_tag)
        
        title_tag = soup.new_tag('td')
        title_tag.string = ''+fanhao.title+''
        fanhao_tbody_tr.insert(1,title_tag)
        
        file_size_tag = soup.new_tag('td')
        file_size_tag.string = fanhao.file_size
        fanhao_tbody_tr.insert(2,file_size_tag)
        
        downloading_count_tag = soup.new_tag('td')
        if fanhao.downloading_count is not None:
            downloading_count_tag.string = str(fanhao.downloading_count)
        else:
            downloading_count_tag.string = '--'
        fanhao_tbody_tr.insert(3,downloading_count_tag)

        file_number_tag = soup.new_tag('td')
        if fanhao.file_number is not None:
            file_number_tag.string = str(fanhao.file_number)
        else:
            file_number_tag.string = '--'
        fanhao_tbody_tr.insert(4,file_number_tag)
        
        magnet_url_tag = soup.new_tag('td')
        magnet_url_tag['class'] = 'magnet'
        fanhao_tbody_tr.insert(5,magnet_url_tag)
        fanhao_magnet_td = fanhao_tbody_tr.find('td',attrs={'class':'magnet'})
        magnet_url_a = soup.new_tag('a',href=fanhao.magnet_url)
        magnet_url_a.string = '点击下载'
        magnet_url_a['class'] = 'btn btn-success'
        fanhao_magnet_td.insert(0,magnet_url_a)

        resource_tag = soup.new_tag('td')
        resource_tag.string = fanhao.resource
        fanhao_tbody_tr.insert(6,resource_tag)

    return soup




def sel (fanhao):
        # Input title to search
        fanhao =fanhao.encode()
        # Counting time start point 
        start_time = time.time()
        
        threads = []
        
        btdb_thread = threading.Thread(target=btdb_parse,args=(fanhao,set_headers(),))
        threads.append(btdb_thread)
        
        cili_thread = threading.Thread(target=cili_parse,args=(fanhao,set_headers(),))
        threads.append(cili_thread)
        
        for bt_i in range(1,10+1):
            threads.append(threading.Thread(target=btcherry_parse,args=(fanhao,bt_i,set_headers(),)))

        zhongziIn_thread = threading.Thread(target=zhongziIn_parse,args=(fanhao,set_headers(),))
        threads.append(zhongziIn_thread)
        
        btku_thread = threading.Thread(target=btku_parse,args=(fanhao,set_headers(),))
        threads.append(btku_thread)

        Qululu_thread = threading.Thread(target=Qululu_parse,args=(fanhao,set_headers(),))
        threads.append(Qululu_thread)
        
        nimasou_thread = threading.Thread(target=nimasou_parse,args=(fanhao,set_headers(),))
        threads.append(nimasou_thread)

        for t in threads:
            t.start()
        
        for t in threads:
            t.join()
        print(threads)
        fanhaos=[]
        for bt_ii in range(1,10+1):
            fanhaos=fanhaos+globals()['btcherry_fanhaos_%s' %str(bt_ii)]
        fanhaos=fanhaos+btdb_fanhaos+cili_fanhaos+zhongziIn_fanhaos+btku_fanhaos+Qululu_fanhaos+nimasou_fanhaos 

        # Sorting bt by descending
        #fanhaos.sort(key=lambda fanhao:fanhao.downloading_count)
        
        print_result(fanhaos)
        # Counting time end point
        finish_time = time.time()
        elapsed = finish_time - start_time
        print('耗时:%s 秒'%elapsed)

        soup = create_url(fanhaos)
        return soup.prettify()
