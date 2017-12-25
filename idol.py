import re  
import urllib.request 
import time
'''import pyodbc '''
import ssl
'''
def connMsSql():
    conn_info = 'DRIVER={SQL Server};DATABASE=%s;SERVER=%s;UID=%s;PWD=%s'%('idol','localhost','sa','123')
    conn = pyodbc.connect(conn_info)
    cur = conn.cursor()
    return cur
'''
def getHtml(url,head):  
    he = urllib.request.Request(url,None,head)
    page = urllib.request.urlopen(he,timeout=20)  
    html = page.read().decode('utf-8') 
    return html    
  
def getImg(html,i,head):  
    reg = r'href=\"(//is.sankakucomplex.com.+?\?'+i+')\"' 
    imgre = re.compile(reg)  
    imglist = set(imgre.findall(html)) 
    x = 0  
    for imgurl in imglist:
        if imgurl.find('sample')>-1:
            continue 
           
        he = urllib.request.Request('https:'+imgurl,None,head)
        page = urllib.request.urlopen(he,timeout=20)  
        src = page.read() 
        with open('C:\idol\%s' % imgurl[imgurl.rfind('?')+1:]+imgurl[imgurl.rfind('.'):imgurl.rfind('?')], "wb") as code:     
            code.write(src)
            print("https:"+imgurl)
        '''
        cur=connMsSql()
        cur.execute("insert into src(src) values ('https:%s')" %imgurl)
        cur.commit() 
        '''           
        with open('C:\idol\src.txt','a') as url:
            url.write("https:"+imgurl+"\n")   
        x = x + 1

ssl._create_default_https_context = ssl._create_unverified_context            
val={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
i=652841
flag=0
while i<i+30000:
    try:
        html = getHtml("https://idol.sankakucomplex.com/post/show/"+str(i),val)  
        getImg(html,str(i),val)
        i+=1
        flag=0   
    except Exception as e:
        flag+=1
        if str(e).find('please slow down')>-1:
            print("下载速度太快，暂停十分钟，当前时间：", time.strftime('%Y-%m-%d %X', time.localtime()))
            time.sleep(600)
            continue
        if flag%4==0:
            time.sleep(10*flag)
        if flag==10:
            with open('C:\idol\error.txt','a') as error:
                error.write(str(i)+" error:"+str(e)+"\n")
                i+=1
                flag=0
            print("失败："+str(i),"异常：",e)   
        print("神秘代号%s第%s次下载失败，正在重试。异常：%s" % (str(i),str(flag),str(e)))

