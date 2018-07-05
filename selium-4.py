# -*- coding:UTF-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import pymysql
import sys
import random 
from selenium.webdriver.common.keys import Keys

#根据基金会基本信息获取基金会负责人信息 
#
#
#!/usr/bin/python3

# 

USER_AGENTS = [
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (iPhone; U; CPU like Mac OS X) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    ]




def getProjInfo(codeno,title):

    options = webdriver.ChromeOptions()
    options.add_argument( random.choice(USER_AGENTS))



    #如果开始检索，设置log文件process为 1 ，结束设置为99  tablename控制信息类别
    updatesql="INSERT INTO foundationlog(no,tablename,proc) VALUES("+str(codeno)+",1,1)"
    #print(updatesql)
    cur.execute(updatesql)
    db.commit()
        #print("update OK")



    driver = webdriver.Chrome('/users/hzw/downloads/chromedriver', chrome_options=options)
    url1 = "http://data.foundationcenter.org.cn/About_"
    url2 = codeno 
    url3 = ".html"
    url = url1 + str(url2) + url3
        #print(url)
    driver.get(url)
    time.sleep(5)
    print('Project Info:3')

    print(driver.find_element_by_xpath("//table[@id='councilTbl']").get_attribute("style"))
    if (driver.find_element_by_xpath("//table[@id='councilTbl']").get_attribute("style")=="display: none;"):
        print("无理事会信息")
    else:

    
        councillist= driver.find_elements_by_xpath("//table[@id='councilTbl']/tbody/tr")
        del councillist[0]   
        
        if len(councillist)>10:
            elem=driver.find_element_by_xpath("//div[@id='councilBtn']")
            elem.click()
        
        for council in councillist:   
            sx =council.find_element_by_xpath(".//td[1]").text
            xm=council.find_element_by_xpath(".//td[2]").text
            zhiwu=council.find_element_by_xpath(".//td[3]").text
            xb=council.find_element_by_xpath(".//td[4]").text
            cishu=council.find_element_by_xpath(".//td[5]").text
            col=[sx,xm,zhiwu,xb,cishu ]
            print(col)
            inssql="INSERT INTO FoundationCouncil(no,xm,zhiwu,xb,cishu) VALUES ('"+str(codeno)+"','"+xm+"','"+zhiwu+"','"+xb+"','"+cishu+"' )"
            #print(inssql)
            cur.execute(inssql)
            db.commit()

           
    if (driver.find_element_by_xpath("//table[@id='supervisorTbl']").get_attribute("style")=="display: none;"):
        print("无监事会信息")
    else:
        councillist2= driver.find_elements_by_xpath("//table[@id='supervisorTbl']/tbody/tr ")
        del councillist2[0]  
        for council2 in councillist2:       
            xm=council2.find_element_by_xpath(".//td[2]").text
            zhiwu="监事"
            xb=council2.find_element_by_xpath(".//td[3]").text
            cishu=council2.find_element_by_xpath(".//td[4]").text
            col=[xm,zhiwu,xb,cishu ]
            print(col)
            inssql="INSERT INTO FoundationCouncil(no,xm,zhiwu,xb,cishu) VALUES ('"+str(codeno)+"','"+xm+"','"+zhiwu+"','"+xb+"','"+cishu+"' )"
            #print(inssql)
            cur.execute(inssql)
            db.commit()

    
    driver.quit()
    updatesql="INSERT INTO  FoundationLog(no,tablename,proc) VALUES ("+str(codeno)+",1,99)"

    cur.execute(updatesql)
    db.commit()
    return 
 





#if len(sys.argv)< 3:
#    print('参数不够')
#    exit 

#start=int(sys.argv[1])
#end=int(sys.argv[2])

#tablename 1 info 2 cw 3 proj
start=33
end=72946


#conn = psycopg2.connect(database="dunhe", user="postgres", password="yxfhalan", host="192.168.40.91", port="5432")
db = pymysql.connect("192.168.40.91","confluence","confluence","confluence" ,charset='utf8')

cur = db.cursor()


if __name__ == '__main__':

    cur.execute("SELECT no,title  from  FoundationInfo where  no >=%s and no<%s order by no ",(start,end))
    rows = cur.fetchall()
    for row in rows:
        print("no = ", row[0])
        print( "Title = ", row[1], "\n")

        #查日志表，是否有处理过 
        selsql="SELECT no,tablename  from FoundationLog where tablename=1 and no="+str(row[0])

        #selsql="SELECT no,title  from space_ds.FoundationLog where tablename=3 and no=33“
        cur.execute(selsql)
        
        rows2 = cur.fetchall()
        if len(rows2)==0:       
            
            #爬前状态更新为1


            getProjInfo(row[0],row[1])
            time.sleep(3)
            #爬完后状态更新为99



    print ("查询结束")
    db.close()  

    