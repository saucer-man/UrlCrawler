# author: saucer_man
# date:2018-04-24
# python3.6


import re
import requests

# 获取并检验要爬取的网站
def url_get():
    url=input("please input the url:")
    try:
        kv={'user_agent':'Mozilla/5.0'}
        requests.get(url,headers=kv)
        return url
    except:
        print("your url is incorrect!!")
    return url_get()

'''
找出url中的域名
比如从https://www.xiaogeng.top/article/page/id=3筛选出www.xiaogeng.top
'''
def url_same(url):
    
    #判断输入的网站使用的是https还是http
    urlprotocol=re.findall(r'.*(?=://)',url)[0]
    print('该站使用的协议是：' + urlprotocol)
    
    if len(re.findall(r'/',url)) >2:
        if urlprotocol=='https':
            sameurl = re.findall(r'(?<=https://).*?(?=/)', url)[0]
        else:
            sameurl = re.findall(r'(?<=http://).*?(?=/)', url)[0]
    else:
        url = url + '/'
        if urlprotocol=='https':
            sameurl = re.findall(r'(?<=https://).*?(?=/)',url)[0]
        else:
            sameurl = re.findall(r'(?<=http://).*?(?=/)',url)[0]
        
    print('域名地址：' + sameurl)
    return sameurl


# 爬取url页面中的所有链接
def spiderpage(url):
    kv={'user_agent':'Mozilla/5.0'}
    r=requests.get(url,headers=kv)
    r.encoding=r.apparent_encoding
    pagetext=r.text
    pagelinks = re.findall(r'(?<=href=\").*?(?=\")|(?<=href=\').*?(?=\')',pagetext)
    return pagelinks

#筛选pagelinks中的url
def url_filtrate(pagelinks):
    '''
    print("我现在在筛选")
    '''
    #去除不是该站点的url
    same_target_url = []
    for l in pagelinks:
        if re.findall(sameurl,l):
            same_target_url.append(l)
    #去除重复url
    unrepect_url = []
    for l in same_target_url:
        if l not in unrepect_url:
            unrepect_url.append(l)
    return unrepect_url
#将一个列表写入文件
def writetofile(list):
    file=open('urls.txt','w')
    for url in list:
        file.write(url)
        file.write('\n')
    file.close()  

# url集合，循环遍历会用到
class linkQuence:
     def __init__(self):
         #已访问的url集合
         self.visited=[]
         #待访问的url集合
         self.unvisited=[]
     #获取访问过的url队列
     def getvisitedurl(self):
         return self.visited
     #获取未访问的url队列
     def getunvisitedurl(self):
         return self.unvisited
     #添加url到访问过得队列中
     def addvisitedurl(self,url):
         return self.visited.append(url)
     #移除访问过得url
     def removevisitedurl(self,url):
         return self.visited.remove(url)
     #从未访问队列中取一个url
     def unvisitedurldequence(self):
         try:
             return self.unvisited.pop()
         except:
             return None
     #添加url到未访问的队列中
     def addunvisitedurl(self,url):
         if url!="" and url not in self.visited and url not in self.unvisited:
             return self.unvisited.insert(0,url)
     #获得已访问的url数目
     def getvisitedurlount(self):
         return len(self.visited)
     #获得未访问的url数目
     def getunvistedurlcount(self):
         return len(self.unvisited)
     #判断未访问的url队列是否为空
     def unvisitedurlsempty(self):
         return len(self.unvisited)==0

        
# 真正的爬取函数
class Spider():
    def __init__(self,url):
        self.linkQuence = linkQuence()   #引入linkQuence类
        self.linkQuence.addunvisitedurl(url)   #并将需要爬取的url添加进linkQuence对列中

    def crawler(self):
        while not self.linkQuence.unvisitedurlsempty():# 若未访问队列非空
            print("嘀嘀嘀我又爬到一个")
            visitedurl = self.linkQuence.unvisitedurldequence()# 取一个url
            if visitedurl is None or visitedurl == '':
                continue
            initial_links=spiderpage(visitedurl) # 爬出该url页面中所有的链接
            right_links = url_filtrate(initial_links) # 筛选出合格的链接
            self.linkQuence.addvisitedurl(visitedurl) # 将该url放到访问过的url队列中
            for link in right_links: # 将筛选出的链接放到未访问队列中
                self.linkQuence.addunvisitedurl(link)
        # print(self.linkQuence.visited)
        print("哥我爬完了")
        return self.linkQuence.visited

if __name__ == '__main__':
    url=url_get()
    sameurl=url_same(url)
    spider=Spider(url)
    urllist=spider.crawler()
    writetofile(urllist)
    
