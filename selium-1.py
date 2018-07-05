# -*- coding:UTF-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import psycopg2
import sys

#根据基金会基本信息获取财务信息


#!/usr/bin/python3

# 
def getCWInfo(codeno,title):
    options = webdriver.ChromeOptions()
    options.add_argument(
    'user-agent="Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"')
    driver = webdriver.Chrome('/users/hzw/downloads/chromedriver', chrome_options=options)

    url1 = "http://data.foundationcenter.org.cn/financeInfo_"
    url2 = codeno 
    url3 = ".html"
    url = url1 + str(url2) + url3
    #print(url)
    driver.get(url)
    time.sleep(3)
    #html = driver.page_source
    #bf1 = BeautifulSoup(html, 'html.parser')
    #print('Container info:')
    #print(driver.find_element_by_xpath("//div[@id='container2']").text)
    if (driver.find_element_by_xpath("//div[@id='container2']").text=="暂无财务信息"):
        print("无财务信息")
        driver.quit()
        return
    print('Financial Year:')
    selects=driver.find_elements_by_xpath("//div[@id='financeInfo']/a")

    for select in selects: 
        #print(select.text)
        select.click()
        time.sleep(3)
        financeAnnual = select.text
        finance1 = driver.find_element_by_xpath("//table[@class='tab_list']/tbody/tr[1]/td[1]").text
        finance2 = driver.find_element_by_xpath("//table[@class='tab_list']/tbody/tr[2]/td[1]").text
        finance21 = driver.find_element_by_xpath("//table[@class='tab_list']/tbody/tr[3]/td[1]").text
        finance22 = driver.find_element_by_xpath("//table[@class='tab_list']/tbody/tr[4]/td[1]").text
        finance23 = driver.find_element_by_xpath("//table[@class='tab_list']/tbody/tr[5]/td[1]").text
        finance24 = driver.find_element_by_xpath("//table[@class='tab_list']/tbody/tr[6]/td[1]").text
        finance25 = driver.find_element_by_xpath("//table[@class='tab_list']/tbody/tr[7]/td[1]").text
        finance3 = driver.find_element_by_xpath("//table[@class='tab_list']/tbody/tr[8]/td[1]").text
        finance31 = driver.find_element_by_xpath("//table[@class='tab_list']/tbody/tr[9]/td[1]").text
        finance32= driver.find_element_by_xpath("//table[@class='tab_list']/tbody/tr[10]/td[1]").text
        finance33 = driver.find_element_by_xpath("//table[@class='tab_list']/tbody/tr[11]/td[1]").text
        finance34 = driver.find_element_by_xpath("//table[@class='tab_list']/tbody/tr[12]/td[1]").text

        Fyear=financeAnnual
        F1=re.sub(",", "", finance1[finance1.find('：') + 1:])  
        F2=re.sub(",", "", finance2[finance2.find('：') + 1:])  
        F21=re.sub(",", "", finance21[finance21.find('：') + 1:])  
        F22=re.sub(",", "", finance22[finance22.find('：') + 1:])  
        F23=re.sub(",", "", finance23[finance23.find('：') + 1:])  
        F24=re.sub(",", "", finance24[finance24.find('：') + 1:])  
        F25=re.sub(",", "", finance25[finance25.find('：') + 1:])  
        F3=re.sub(",", "", finance3[finance3.find('：') + 1:]) 
        F31=re.sub(",", "", finance31[finance31.find('：') + 1:])  
        F32=re.sub(",", "", finance32[finance32.find('：') + 1:])  
        F33=re.sub(",", "", finance33[finance33.find('：') + 1:])  
        F34=re.sub(",", "", finance34[finance34.find('：') + 1:])  

        col=[codeno,Fyear,F1,F2,F21,F22,F23,F24,F25,F3,F31,F32,F33,F34]
        #print(col)
        inssql="INSERT INTO space_ds.FoundationCW(no,title,year,F1,F2,F21,F22,F23,F24,F25,F3,F31,F32,F33,F34) VALUES ('"+str(codeno)+"','"+title+"','"+Fyear+"','"+F1+"','"+F2+"','"+F21+"','"+F22+"','"+F23+"','"+F24+"','"+F25+"','"+F3+"','"+F31+"','"+F32+"','"+F33+"','"+F34+"' )"
        #print(inssql)
        cur.execute(inssql)
        conn.commit()
    
    driver.quit()

    return 
 





if len(sys.argv)< 3:
    print('参数不够')
    exit 

start=int(sys.argv[1])
end=int(sys.argv[2])

conn = psycopg2.connect(database="dunhe", user="postgres", password="yxfhalan", host="192.168.40.91", port="5432")
cur = conn.cursor()

if __name__ == '__main__':

    cur.execute("SELECT no,title  from space_ds.FoundationInfo where id>=%s and id<%s order by id",(start,end))
    rows = cur.fetchall()
    for row in rows:
        print("ID = ", row[0])
        print( "Title = ", row[1], "\n")
        getCWInfo(row[0],row[1])
    print ("查询结束")
    conn.close()  

    