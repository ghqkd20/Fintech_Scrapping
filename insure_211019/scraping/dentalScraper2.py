# AIA 생명 치과보험사이트에 정보 입력(내정보) 보험료 / 보장 내역 출력하기;
# https://direct.lina.co.kr/product/ess/dtc01/easy
from selenium import webdriver
import re


def rePlaceData(value):
    numbers = re.findall("\d+", value)
    result = ""
    for i in numbers:
        decodedNumber = i
        result += decodedNumber
    return result


def getLinaData(name, birth, gender):
    driver = webdriver.Chrome('./chromedriver')
    scrapingResult = {
        'company': "라이나",
        'price': 0,
        'contents': []
    }
    driver.get('https://direct.lina.co.kr/product/ess/dtc01/easy')
    textBox = driver.find_element_by_xpath('//*[@id="birthday"]')
    textBox.send_keys(birth)
    if gender == 1:
        femaleBtn = driver.find_element_by_xpath('//*[@id="main_btn_female"]')
        femaleBtn.click()
    else:
        maleBtn = driver.find_element_by_xpath('//*[@id="main_btn_male"]')
        maleBtn.click()
    resultBtn = driver.find_element_by_xpath(
        '//*[@id="btn_direct_dental_cal"]')
    resultBtn.click()
    driver.implicitly_wait(3)

    htmlResult = driver.find_element_by_xpath(
        '//*[@id="contents"]/div[2]/div[2]/div[2]/div/table/tbody[1]/tr[1]/td[2]/strong').text
    resultValue = rePlaceData(htmlResult)
    scrapingResult['price'] = resultValue
    driver.implicitly_wait(2)
    detailBtn = driver.find_element_by_xpath('//*[@id="openLayerplanPonA2"]')
    detailBtn.click()
    driver.implicitly_wait(2)

    tableBody = driver.find_element_by_xpath(
        '//*[@id="planPonA2"]/div/div[2]/div/div/table[1]').find_element_by_tag_name('tbody')
    rows = tableBody.find_elements_by_tag_name("tr")
    contentsList = []
    for index, value in enumerate(rows):
        if index != 0:
            print(value.find_elements_by_tag_name('th')[0].text)
            contentsList.append(value.find_elements_by_tag_name('th')[0].text)
    scrapingResult['contents'] = contentsList
    return scrapingResult


print(getLinaData("유관우", "890119", 0))
