# -*- coding:UTF-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import pymysql
import sys
import random 
from selenium.webdriver.common.keys import Keys

#根据民政部社会组织信息 
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


db = pymysql.connect("192.168.40.91","confluence","confluence","confluence" ,charset='utf8')

cur = db.cursor()


options = webdriver.ChromeOptions()
options.add_argument( random.choice(USER_AGENTS))

driver = webdriver.Chrome('/users/hzw/downloads/chromedriver', chrome_options=options)
url = "http://www.chinanpo.gov.cn/search/orgcx.html"

driver.get(url)
time.sleep(3)
print('org local  Info')


elem2=driver.find_element_by_xpath("//div[@id='local-tab']/a")
        #elem2.send_keys(Keys.ENTER)
elem2.click() 
time.sleep(3)


pagecur=1

while pagecur<=39934:

    print(str(pagecur))
    elem1=driver.find_elements_by_xpath("//table[@class='table-1 mar-top']/tbody/tr")
        #elem2.send_keys(Keys.ENTER)

       

    for row in elem1:
        zuzhi1=row.find_element_by_xpath("./td[2]").text 
        zuzhi2=row.find_element_by_xpath("./td[3]").text 
        zuzhi3=row.find_element_by_xpath("./td[4]").text 
        zuzhi4=row.find_element_by_xpath("./td[5]").text 
        zuzhi5=row.find_element_by_xpath("./td[6]").text 
        zuzhi6=row.find_element_by_xpath("./td[7]").text 
        
        print(zuzhi1+zuzhi2+zuzhi3+zuzhi4+zuzhi5+zuzhi6)

        inssql="INSERT INTO zuzhi(orgname,xydm,zzlx,level,fr,status) VALUES ('"+zuzhi1+"','"+zuzhi2+"','"+zuzhi3+"','"+zuzhi4+"','"+zuzhi5+"','"+zuzhi6+"' )"
        #print(inssql)
        cur.execute(inssql)
        db.commit()



    elem2=driver.find_element_by_xpath("//a[contains(text(),'下页')]")
        #elem2.send_keys(Keys.ENTER)
    elem2.click() 
    time.sleep(3)


   
    pagecur=pagecur+1

driver.quit()

    