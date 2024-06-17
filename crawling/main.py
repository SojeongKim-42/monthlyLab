#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

result = ''
result += '공익법인명,사업연도,대표자,설립근거법,설립연월일,설립유형,소재지,공익사업유형,전화번호/팩스,설립주체,홈페이지 주소 /전자우편 주소,이사수,기부금(단체) 유형,자원봉사자 연인원 수,주무관청,고용직원 수,'
result += '총 자산가액,부채,순자산,'
result += '총 자산가액,토지,건물주식 및 출자지분,금융자산,기타자산,'
result += '사업수익_소계_공익목적사업,사업수익_소계_기타사업,사업수익_기부금품_공익목적사업,사업수익_기부금품_기타사업,사업수익_보조금_공익목적사업,사업수익_보조금_기타사업,사업수익_회비수익_공익목적사업,사업수익_회비수익_기타사업,사업수익_기타_공익목적사업,사업수익_기타_기타사업,사업외 수익_공익목적사업,사업외 수익_기타사업,고유목적사업 준비금 환입액_공익목적사업,고유목적사업 준비금 환입액_기타사업,총계수익_공익목적사업,총계수익_기타사업,'
result += '기부금품_개인기부금품,기부금품_영리법인기부금품,모금단체 재단 등 다른 공익법인 등의 지원금품,기부금품_기타기부금품,'
result += '사업비용_소계_공익목적사업,사업비용_소계_기타사업,사업비용_사업수행비용_공익목적사업,사업비용_사업수행비용_기타사업,사업비용_일반관리비용_공익목적사업,사업비용_일반관리비용_기타사업,사업비용_모금비용_공익목적사업,사업비용_모금비용_기타사업,사업비용_기타_공익목적사업,사업비용_기타_기타사업,사업외 비용_공익목적사업,사업외 비용_기타사업,고유목적사업 준비금 전입액_공익목적사업,고유목적사업 준비금 전입액_기타사업,총계비용_공익목적사업,총계비용_기타사업,'
result += '사업비용_분배비용(국내),사업비용_분배비용(국외),사업비용_분배비용(국외),사업비용_인력비용,사업비용_시설비용,사업비용_기타비용,'
result += '복식부기,적용회계기준,세무확인,외부회계감사 여부,'
result += '\n'


driver = webdriver.Chrome("C:/A_Projects/crowling/chromedriver")
#for page in range(1,1275):
for page in range(1,1275):

    url = 'https://www.nanumkorea.go.kr/nts/cptList.do?pbcbizTy=&ctbmGrpTy=&cprNm=&pageIndex={}&_=1683380358416'.format(page)
    driver.get(url)
    html = driver.page_source  
    soup = BeautifulSoup(html, 'html.parser')


    t_title = soup.find_all('td', {'class': 't_title'})
    t_no = soup.find_all('td', {'class': 't_no'})
    t_type1 = soup.find_all('td', {'class': 't_type1'})
    t_type2 = soup.find_all('td', {'class': 't_type2'})
    t_btn = soup.find_all('td', {'class': 't_btn'})

    for _t_btn in t_btn:
        dat_bsnmno = _t_btn.find('a',{'class': 'btn_white hometaxLink'}).get('data-bsnmno')

        url2 = 'https://www.nanumkorea.go.kr/nts/ntsSumryReport.do?bsnmNo='+ dat_bsnmno+'&cratQu=2020'
        driver.get(url2)
        html2 = driver.page_source  
        soup2 = BeautifulSoup(html2, 'html.parser')

        #단체정보
        danche_info = soup2.find('div', {'class': 'danche_info'})
        for dd in danche_info.find_all('div', {'class': 'dd'}):
        #for li in danche_info.find_all('div', {'class': 'dt'}):
            result += dd.text.replace(',','') + ','


        #재무현황
        tbl_infos = soup2.find_all('table', {'class': 'tbl_info'})
        tbl_info1 = tbl_infos[0]
        for td in tbl_info1.find_all('td'):
            result += td.text.replace(',','') + ','
        
        
        #자산현황
        tbl_info2 = tbl_infos[1]
        for td in tbl_info2.find_all('td'):
            result += td.text.replace(',','').replace('-','0') + ','


        #수익 현황
        tbl_info3 = tbl_infos[2]
        for td in tbl_info3.find_all('td'):
            result += td.text.replace(',','').replace('-','0') + ','


        #공익목적사업의 수익세부현황
        tbl_info4 = tbl_infos[3]
        for td in tbl_info4.find_all('td')[1:5]:
            result += td.text.replace(',','').replace('-','0') + ','


        #비용 현황
        tbl_info5 = tbl_infos[4]
        for td in tbl_info5.find_all('td'):
            result += td.text.replace(',','').replace('-','0') + ','

        
        #공익목적사업의 비용세부현황
        tbl_info6 = tbl_infos[5]
        for td in tbl_info6.find_all('td')[1:6]:
            result += td.text.replace(',','') + ','

        
        #세무확인과 회계감사(여:Y, 부:N)
        tbl_info7 = tbl_infos[6]
        for td in tbl_info7.find_all('td'):
            if (len(td.text.split('N'))>=2):
                result +='N'+ ','
            elif (len(td.text.split('Y'))>=2):
                result +='Y'+ ','
            else :
                result +=','
        result += '\n'
        
       
f3 = open("./result.csv", 'wt', encoding='UTF8')
f3.write(result)
f3.close()      
