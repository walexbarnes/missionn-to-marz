from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def scrape_all():
   # Initiate headless driver for deployment
    executable_path = {"chromedriver.exe"}
    browser = Browser('chrome', executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres":hemis(browser)
    }
    return data
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first <a> tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    try:
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[1]

    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def hemis(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemis = soup.find_all('img', class_='thumb')
    hemidata = []
    for hemi in range(len(hemis)):
        img_click = browser.find_by_css('.thumb')[hemi]
        img_click.click()
        imgel = browser.find_by_text('Sample')
        imghref = imgel['href']
        imgtitle= browser.find_by_css('.title').text
        hemidata.append({"title":imgtitle,"url":imghref})
        #put this page into HTML, find the href for the hemi
        #store into dic, grab title, have a list of dictionaries for each hemi
        #each dic will have title and URl for hemi
        #once in list, on HTML page, need to loop through and render hemi on page 
        browser.back()
    return hemidata


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())





