#!/usr/bin/env python
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import time


# In[3]:

def scrape():
    browser = Browser('chrome',executable_path='chromedriver', headless=True)






def mars_news(browser):
    # # Visit the NASA Mars News Site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    browser.is_element_present_by_css('ul.item_list li.slide', wait_time=1)


# In[7]:


html = browser.html
news_soup = bs(html,'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[8]:


news_title=slide_elem.find('div', class_='content_title').get_text()
news_title


# In[9]:


news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# # JPL Space Images Featured Image

# In[10]:


url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[11]:


full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[12]:


browser.is_element_not_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[13]:


html=browser.html
img_soup = bs(html,"html.parser")


# In[14]:


img_url_rel = img_soup.select("figure.lede a img")[0].get('src')
img_url_rel


# In[15]:


img_url = f"https://www.jpl.nasa.gov{img_url_rel}"
img_url


# # Mars Weather

# In[16]:


url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)

time.sleep(5)


# In[17]:


html = browser.html
weather_soup = bs(html,'html.parser')


# In[18]:


mars_weather_tweet = weather_soup.find('div', attrs={'class': 'tweet', 'data-name':'Mars Weather'})


# In[19]:


try:
    mars_weather = mars_weather_tweet.find('p','tweet-text').get_text()
    mars_weather
    
except AttributeError:
    pattern = re.compile(r'sol')
    mars_weather = weather_soup.find('span', text=pattern).text
    mars_weather
    
mars_weather


# # Mars Hemispheres

# In[41]:


url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[42]:


hemisphere_image_urls = []


# In[43]:


links = browser.find_by_css('a.product-item.itemLink h3')


# In[44]:


len(links)


# In[45]:


for i in range(len(links)):
    hemisphere = {}
    
    browser.find_by_css('a.product-item h3')[i].click()
    sample_elem = browser.links.find_by_text('Sample').first
    hemisphere['img_url'] = sample_elem['href']
    hemisphere['title'] = browser.find_by_css('h2.title').text
    hemisphere_image_urls.append(hemisphere)
    browser.back()


# In[46]:


hemisphere_image_urls


# # Mars Facts

# In[47]:


df = pd.read_html('https://space-facts.com/mars/')[0]
df.columns=['description','value']
df.set_index('description')


# In[48]:


df.to_html('Mars_Facts.html')


# In[49]:


browser.quit()

