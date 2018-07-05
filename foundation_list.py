# -*- coding:UTF-8 -*-
# 根据基金会的页面，写入金融、项目 
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time


if __name__ == '__main__':

    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"')
    driver = webdriver.Chrome('/users/hzw/downloads/chromedriver', chrome_options=options)

    url1 = "http://data.foundationcenter.org.cn/foundation.html"
    #url2 = 51
    #url3 = ".html"

    #f=open('/users/hzw/desktop/results2.csv','w',newline='',encoding='gbk')
    #w = csv.writer(f)

    while url2 < 500:
        print(url2)
        url = url1 + str(url2) + url3
        #print(url)
        driver.get(url)
        time.sleep(3)
        html = driver.page_source
        bf1 = BeautifulSoup(html, 'html.parser')

        title = driver.find_element_by_xpath("//div[@class='name_l']//a").get_attribute("title")
        xydm = driver.find_element_by_xpath("//span[@id='RegisterNO']").text
        President = driver.find_element_by_xpath("//span[@id='President']").text
        # President=driver.find_element_by_xpath("//span[@id='President']").text

        FoundationType = driver.find_element_by_xpath("//span[@id='FoundationType']").text
        Secretary = driver.find_element_by_xpath("//span[@id='Secretary']").text
        CreateDate = driver.find_element_by_xpath("//span[@id='CreateDate']").text
        LinkerTel = driver.find_element_by_xpath("//span[@id='LinkerTel']").text
        OriginalFoundNum = driver.find_element_by_xpath("//span[@id='OriginalFoundNum']").text
        LinkerFax = driver.find_element_by_xpath("//span[@id='LinkerFax']").text
        DepartMentTypeName = driver.find_element_by_xpath("//span[@id='DepartMentTypeName']").text
        LinkerEmail = driver.find_element_by_xpath("//span[@id='LinkerEmail']").text
        OrganMasterAddress = driver.find_element_by_xpath("//span[@id='OrganMasterAddress']").text
        FoundationAddress = driver.find_element_by_xpath("//span[@id='FoundationAdress']").text
        Purpose = driver.find_element_by_xpath("//span[@id='Purpose']").text
        row=[title,xydm,President,FoundationType,Secretary,CreateDate,LinkerTel,\
                OriginalFoundNum,LinkerFax,DepartMentTypeName,LinkerEmail,OrganMasterAddress,FoundationAddress,Purpose]
        #print(row)
        inssql="INSERT INTO space_ds.FoundationInfo(No,title,xydm,President,FoundationType,Secretary,CreateDate,LinkerTel,OriginalFoundNum,LinkerFax,DepartMentTypeName,LinkerEmail,OrganMasterAddress,FoundationAddress,Purpose) VALUES ('"+str(url2)+"','"+title+"','"+xydm+"','"+President+"','"+FoundationType+"','"+Secretary+"','"+CreateDate+"','"+LinkerTel+"','"+OriginalFoundNum+"','"+LinkerFax+"','"+DepartMentTypeName+"','"+LinkerEmail+"','"+OrganMasterAddress+"','"+FoundationAddress+"','"+Purpose+"' )"


        #print(inssql)
        print(xydm)
        if xydm == "--":
        	print("Null record")
        else:	
          cur.execute(inssql)
          print(inssql)


        #w.writerow(row)

        url2 = url2 + 1

conn.commit()
print("Records created successfully")
conn.close()
