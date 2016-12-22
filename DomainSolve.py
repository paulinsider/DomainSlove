#coding=utf-8
import mechanize
import cookielib
import chardet
import threading
import sys
import Queue
import time
import urllib

q = Queue.Queue()
def work(line, br):
    error = open("qqerror.txt", 'w')
    title = ''
    url = ''
    print line
    param = line.split('\t')
    if param[1] == '1.1.1.1':
        q.put("gg")
    url = 'http://' + param[0]
    try:
        r = br.open(url, timeout = 1)
        html = r.read()
        bm = chardet.detect(html)
        print bm
        title = br.title()
        if bm['encoding'] == 'GB2312':
            title = title.decode(bm['encoding'])
            title.encode("utf-8")
    except mechanize.HTTPError as e:
        error.write(url + '\n')
    except mechanize.URLError as e:
        error.write(url + '\n')
    finally:
        pass
    if (title == '' or title is None):
        titlr = ''
        url = 'https://' + param[0]
        try:
            print url
            r = br.open(url, timeout = 1)
            html = r.read()
            bm = chardet.detect(html)
            print bm
            title = br.title()
            if bm['encoding'] == 'GB2312':
                title = title.decode(bm['encoding'])
                title.encode("utf-8")
        except mechanize.HTTPError as e:
            error.write(url + '\n')
        except mechanize.URLError as e:
            error.write(url + '\n')
        finally:
            pass
        if (title == '' or title is None):
            q.put("gg")
    outline = url + '\t' + title + '\n' 
    q.put(outline)

if __name__=='__main__':
    number = 1
    reload(sys)
    sys.setdefaultencoding( "utf-8" )
    br = mechanize.Browser()
    br.set_cookiejar(cookielib.LWPCookieJar()) # Cookie jar
    
    br.set_handle_equiv(True) # Browser Option
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')] 
    file = open("qq.txt")
    out = open("qqout.txt", 'w')
    while 1:
        print ("%d/3152"%(number))
        number += 1
        line = file.readline()
        t = threading.Thread(target=work, args=(line, br))
        start_time = time.time()
        t.start()
        while 1:
            flag = 0
            timeout = time.time() - start_time
            time.sleep(1)
            if timeout > 10:
                break
            if q.qsize() > 0:
                flag = 1
                break
        if flag == 1:
            outline = q.get()
            if outline == 'gg':
                continue
            out.write(outline)
