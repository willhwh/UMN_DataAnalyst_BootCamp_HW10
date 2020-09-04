from bs4 import BeautifulSoup
import pandas as pd
import requests
from splinter import Browser
import time

executable_path = {"executable_path": "/usr/local/bin/chromedriver"}


def scrape():
    browser=Browser("chrome", **executable_path, headless=False)

    #NASA Mars News
    url='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    news=soup.find('ul',class_='item_list').find_all('li',class_='slide')
    for i in news[:1]:
        news_title=i.find('h3').text
        news_p=i.find('div',class_='article_teaser_body').text
        print(news_title,'\n',news_p)

    #JPL Mars Space Images - Featured Image
    url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    photos=soup.find('ul',class_='articles').find_all('li',class_='slide')
    for i in photos[:1]:
        partial_link=i.find('div',class_='img').find('img')['src']
        featured_image_url='https://www.jpl.nasa.gov/'+partial_link
        print(featured_image_url)
    
    #Mars Facts
    url='https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(1)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    tables=pd.read_html(html)
    table0=tables[0]
    table0.columns=['Feature','Value']
    table0['Feature']=table0['Feature'].apply(lambda x:x.replace(":",''))
    print(table0)
    table0.set_index('Feature',inplace=True)
    table0.to_html('Mars_Facts.html')
    table_data=table0.reset_index().values.tolist()

    #Mars Hemispheres
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(1)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')
    results=soup.find('div',id='product-section').find_all('div',class_='item')

    names_list=[]
    img_link_list=[]

    for result in results:
        result_link='https://astrogeology.usgs.gov/'+result.find('a')['href']
        name=result.find('h3').text
        names_list.append(name)
        browser.visit(result_link)
        time.sleep(1)
    
        html=browser.html
        soup=BeautifulSoup(html,'html.parser')
        browser.click_link_by_text('Open') 
        time.sleep(1)
    
        html=browser.html
        soup=BeautifulSoup(html,'html.parser')
        img_link=soup.find('div',class_='downloads').find('a')['href']
        img_link_list.append(img_link)
    
    hemisphere_image_urls = []
    for name,link in zip(names_list,img_link_list):
        hemisphere_image_urls.append({'title':name,'img_url':link})

    browser.quit()

    mars_dict={'News_Title':news_title,'News_Summary':news_p,"Mars_img":featured_image_url,\
                "Mars_Facts":table_data,"Mars_Hemispheres":hemisphere_image_urls}

    
    return mars_dict

