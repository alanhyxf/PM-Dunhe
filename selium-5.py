# -*- coding:UTF-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import pymysql
import sys
import random 
from selenium.webdriver.common.keys import Keys

#根据慈善组织信息 
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
url = "http://cishan.chinanpo.gov.cn/biz/ma/csmh/a/csmhaindex.html/"

driver.get(url)
time.sleep(3)
print('cishan Info')

pagestr=driver.find_element_by_xpath("//div[@class='pagebar_wrap']/font[1]").text

pattern = re.compile(r'\d+')   # 查找数字
result1 = pattern.findall(pagestr)
pagecur=int(result1[0])
pages=int(result1[1])
#projects=int(result1[2])
print(str(pagecur)+" "+str(pages))
pagecur=294 

elem2=driver.find_element_by_xpath("//span[contains(text(),'末页')]")
    #elem2.send_keys(Keys.ENTER)
elem2.click() 
time.sleep(3)
while pagecur<=pages:

    #print(pagecur)

    
    #elem1=driver.find_element_by_xpath("//input[@id='pageno1']")
    #elem1.send_keys(str(pagecur))

    #JavascriptExecutor js = (JavascriptExecutor) driver;
    #js.executeScript("tz()");



    print(str(pagecur)+". ")

    elem5=driver.find_elements_by_xpath("//tbody/tr")

    for row in elem5:

        cishan1=row.find_element_by_xpath("./td[2]").text 
        cishan2=row.find_element_by_xpath("./td[3]").text 
        cishan3=row.find_element_by_xpath("./td[4]").text 
        cishan4=row.find_element_by_xpath("./td[5]").text 

        try:
            row.find_element_by_xpath("./td[3]/i").is_displayed() 
        except:
            cishan5= "非公募"
        else:
            cishan5= "公募"

        cishan=cishan1+cishan2+cishan3+cishan4+cishan5
        print(cishan)
 
        inssql="INSERT INTO CISHAN(xydm,orgname,createdate,djjg,ispublic) VALUES ('"+cishan1+"','"+cishan2+"','"+cishan3+"','"+cishan4+"','"+cishan5+"' )"
        #print(inssql)
        cur.execute(inssql)
        db.commit()

    elem2=driver.find_element_by_xpath("//span[contains(text(),'下一页')]")
    #elem2.send_keys(Keys.ENTER)
    elem2.click() 
    time.sleep(1)
    pagestr=driver.find_element_by_xpath("//div[@class='pagebar_wrap']/font[1]").text
    pattern = re.compile(r'\d+')   # 查找数字
    result1 = pattern.findall(pagestr)
    pagecur=int(result1[0])
   
    pagecur=pagecur+1

driver.quit()

    