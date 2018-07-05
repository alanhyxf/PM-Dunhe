# -*- coding:UTF-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import pymysql
import sys
import random 
from selenium.webdriver.common.keys import Keys

#根据基金会基本信息获取项目信息
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

    #IPproxy=random.choice(IP_AGENTS)
    #IPproxy='167.114.211.122:3128'

    #print("IPproxy"+IPproxy)

    #options.add_argument('--proxy-server=http://'+IPproxy)
    try:
        driver = webdriver.Chrome('/users/hzw/downloads/chromedriver', chrome_options=options)

        url1 = "http://data.foundationcenter.org.cn/projectInfo_"
        url2 = codeno 
        url3 = ".html"
        url = url1 + str(url2) + url3
        #print(url)
        driver.get(url)
    
        #html = driver.page_source
        #bf1 = BeautifulSoup(html, 'html.parser')
        #print('Container info:')

        elem1=driver.find_element_by_xpath("//input[@id='TxtName']")
        elem1.send_keys("18607918415")
        elem2=driver.find_element_by_xpath("//input[@id='TxtPassword']")
        elem2.send_keys("432584")
        elem2.send_keys(Keys.RETURN)
        time.sleep(5)
    
        #print(driver.find_element_by_xpath("//table[@id='projectInfo']/tbody/tr[2]/td"))

        #如果开始检索，设置log文件process为 1 ，结束设置为99 
        updatesql="INSERT INTO foundationlog(no,tablename,proc) VALUES("+str(codeno)+",3,1)"
        #print(updatesql)
        cur.execute(updatesql)
        db.commit()
        #print("update OK")
    except:
        print("error:"+str(codeno))
        driver.quit()
        return     


    if (driver.find_element_by_xpath("//table[@id='projectInfo']/tbody/tr[2]/td").text=="没有项目！"):
        print("无项目信息")
        driver.quit()
        return
    print('Project Info:')
    pagestr=driver.find_elements_by_xpath("//div[@id='div_page']/span/font[1]")

    #print(pagestr[0].text)
    pattern = re.compile(r'\d+')   # 查找数字
    result1 = pattern.findall(pagestr[0].text)
    pages=int(result1[0])
    projects=int(result1[1])

    page=1 
    while page<=pages:
        print(page)
        elem5=driver.find_elements_by_xpath("//table[@id='projectInfo']/tbody/tr")
        del elem5[1]
        del elem5[0]

        rowindex=0

        proj_1=codeno
        proj_2=title
        for row in elem5:
            #print(row.text)
            if rowindex==0:
                #proj_3 项目id
                proj_21=row.find_element_by_xpath(".//td[1]").get_attribute("oid")
                #proj_31 项目名称
                proj_22=row.find_element_by_xpath(".//td[2]").get_attribute("title")
                proj_23=row.find_element_by_xpath(".//td[3]").text
                proj_24=row.find_element_by_xpath(".//td[4]").text
                proj_25=row.find_element_by_xpath(".//td[5]").text
                proj_26=row.find_element_by_xpath(".//td[6]").text
                
                
                
            else:
                #print('begin')
                #proj_5 机构 

                proj_31=row.find_element_by_xpath("./td/div/div[1]/div[1]/span[@class='tc_span01']").get_attribute('innerHTML')
                proj_32=row.find_element_by_xpath("./td/div/div[1]/div[2]/span[@class='tc_span01']").get_attribute('innerHTML')
                proj_33=row.find_element_by_xpath("./td/div/div[2]/div[1]/span[@class='tc_span01']").get_attribute('innerHTML')
                proj_34=row.find_element_by_xpath("./td/div/div[2]/div[2]/span[@class='tc_span01']").get_attribute('innerHTML')

                #proj_6 项目概要 
                proj_35=row.find_element_by_xpath("./td/div/div[3]/div[2]").get_attribute('innerHTML').replace('\'','').replace('\"','')
                #.//td/div/div[3]/div[2]


            if rowindex==0:
                rowindex=1
            else:
                rowindex=0
                col=[proj_1,proj_2,proj_21,proj_22,proj_23,proj_24,proj_25,proj_26,proj_31,proj_32,proj_33,proj_34,proj_35]
                #print(col)

                inssql="INSERT INTO FoundationProj(no,title,oid,year,proj22,proj23,proj24,proj25,proj26,proj33,proj34,proj35) VALUES ('"+str(proj_1)+"','"+proj_2+"','"+proj_21+"','"+proj_32+"','"+proj_22+"','"+proj_23+"','"+proj_24+"','"+proj_25+"','"+proj_26+"','"+proj_33+"','"+proj_34+"','"+proj_35+"' )"
                #print(inssql)
                cur.execute(inssql)
                db.commit()


        
        

        page=page+1
        elem4=driver.find_element_by_xpath("//a[@class='page_t']")
        elem4.click()
        time.sleep(5)



    
    driver.quit()
    updatesql="INSERT INTO  FoundationLog(no,tablename,proc) VALUES ("+str(codeno)+",3,99)"

    cur.execute(updatesql)
    db.commit()
    return 
 





#if len(sys.argv)< 3:
#    print('参数不够')
#    exit 

#start=int(sys.argv[1])
#end=int(sys.argv[2])

#tablename 1 info 2 cw 3 proj
start=1000
end=729436


#conn = psycopg2.connect(database="dunhe", user="postgres", password="yxfhalan", host="192.168.40.91", port="5432")
db = pymysql.connect("192.168.40.91","confluence","confluence","confluence" ,charset='utf8')

cur = db.cursor()




if __name__ == '__main__':

    cur.execute("SELECT no,title  from  FoundationInfo where no >=%s and no<%s order by id",(start,end))
    rows = cur.fetchall()
    for row in rows:
        
        #查日志表，是否有处理过 
        selsql="SELECT no,tablename  from FoundationLog where tablename=3 and no="+str(row[0])

        #selsql="SELECT no,title  from space_ds.FoundationLog where tablename=3 and no=33“
        cur.execute(selsql)
        
        rows2 = cur.fetchall()
        if len(rows2)==0:       
            
            #爬前状态更新为1
            print("ID = ", row[0])
            print( "Title = ", row[1], "\n")



            getProjInfo(row[0],row[1])
            time.sleep(5)
            #爬完后状态更新为99



    print ("查询结束")
    conn.close()  

    