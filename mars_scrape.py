from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import time

def scrape():
    browser = Browser('chrome',executable_path='chromedriver', headless=True)
    news_title,news_p = mars_news(browser)
    
    mars_data = {
        'mars_title':  news_title,
        'mars_p': news_p,
        'featured_img': featured_image(browser),
        'mars_weather': mars_weather(browser),
        'hemispheres': hemi(browser),
        'mars_facts': mars_facts()
    }

    return mars_data




def mars_news(browser):
    # # Visit the NASA Mars News Site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    browser.is_element_present_by_css('ul.item_list li.slide', wait_time=1)
    html = browser.html
    news_soup = bs(html,'html.parser')
    slide_elem = news_soup.select_one('ul.item_list li.slide')
    try:
        news_title=slide_elem.find('div', class_='content_title').get_text()
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_p

# JPL Space Images Featured Image
def featured_image(browser):
    
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    browser.is_element_not_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()
    html=browser.html
    img_soup = bs(html,"html.parser")
    try:
        img_url_rel = img_soup.select("figure.lede a img")[0].get('src')
        img_url = f"https://www.jpl.nasa.gov{img_url_rel}"
    except AttributeError:
        return None  
        
    return img_url


# Mars Weather
def mars_weather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    weather_soup = bs(html,'html.parser')
    mars_weather_tweet = weather_soup.find('div', attrs={'class': 'tweet', 'data-name':'Mars Weather'})
    try:
        mars_weather = mars_weather_tweet.find('p','tweet-text').get_text()
    except AttributeError:
        pattern = re.compile(r'sol')
        mars_weather = weather_soup.find('span', text=pattern).text

    return mars_weather


# Mars Hemispheres
def hemi(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemisphere_image_urls = []
    links = browser.find_by_css('a.product-item.itemLink h3')
    len(links)
    for i in range(len(links)):
        hemisphere = {}
        
        browser.find_by_css('a.product-item h3')[i].click()
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        hemisphere['title'] = browser.find_by_css('h2.title').text
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    browser.quit()

    return hemisphere_image_urls

# Mars Facts
def mars_facts():
    df = pd.read_html('https://space-facts.com/mars/')[0]
    df.columns=['description','value']
    df.set_index('description')
    return df.to_html()


