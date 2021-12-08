import requests
from bs4 import BeautifulSoup
from lxml import etree
import csv

try:
    outputdata = open("output_data.csv", mode='w',newline='',encoding="utf-8")
except IOError:
    print("io error")
    
Item_name = []
Item_price = []
Item_rating = []
Item_link = []
Seller_name = []
Seller_rating = []


def crawler():
    url = 'https://www.flipkart.com/search?q=redmi+mobile'
    source_code = requests.get(url)
    plain_text = (source_code.text).encode('utf8')
    soup = BeautifulSoup(plain_text, features="html.parser")
    
    for link in soup.findAll('a',{'class':'_1fQZEK'}):
        href = 'https://www.flipkart.com'+link.get('href')
        Item_link.append(href)
        get_seller_name(href)
        
    for name in soup.findAll('div',{'class':'_4rR01T'}):
        item_name = name.text
        Item_name.append(str(item_name))
        
    for price in soup.findAll('div',{'class':'_30jeq3 _1_WHN1'}):
        item_price = str(price.text)
        Item_price.append(item_price[1:])
    for rating in soup.findAll('div',{'class':'_3LWZlK'}):
        item_rating = rating.text
        Item_rating.append(str(item_rating))
    

def get_seller_name(item_url):
    source_code = requests.get(item_url)
    plain_text = (source_code.text).encode('utf8')
    soup = BeautifulSoup(plain_text, features="html.parser")
    dom = etree.HTML(str(soup))
    #print(dom.xpath('//*[@id="sellerName"]/span/span')[0].text)
    Seller_name.append(str(dom.xpath('//*[@id="sellerName"]/span/span')[0].text))
    Seller_rating.append(str(dom.xpath('//*[@id="sellerName"]/span/div')[0].text))


crawler()
writer = csv.writer(outputdata)
writer.writerow(['SN','Item Name','Item Price(Rs.)','Item Rating(out of 5)','Seller Name','Seller Rating(out of 5)','Item Link'])

for i in range(len(Item_name)):
    #print(i+1,Item_name[i],Item_price[i],Item_rating[i],Seller_name[i],Seller_rating[i])
    writer.writerow([i+1,Item_name[i],Item_price[i],Item_rating[i],Seller_name[i],Seller_rating[i],Item_link[i]])
outputdata.close()

