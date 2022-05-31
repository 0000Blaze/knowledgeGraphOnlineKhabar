import requests
from bs4 import BeautifulSoup
import pandas as pd

#returns all links in onlinekhabar
def get_links(url="https://english.onlinekhabar.com/"):
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')

    #extracting all links
    tags = soup.find_all('h2')
    links_href =[]
    links = []
    #links with the href tag
    for i in tags:
        links_href.append(i.find('a',href=True))
    #extracting the links
    for j in range(len(links_href)):
        if "category" in links_href[j]['href']: #skip the catagory links
            continue
        links.append(links_href[j]['href']) 
    return set(links)

#return header and content for the url provided
def get_data(url):
    page = requests.get(url)
    page_soup = BeautifulSoup(page.content, 'html.parser') 
    #heading
    news_title = page_soup.find_all('h1')
    #content
    article_text=''
    news_content = page_soup.find('div', class_="post-content-wrap").findAll('p') 
    for element in news_content:
        article_text += ''.join(element.findAll(text = True))

    return news_title[0].get_text(),article_text

title=[]
text=[]

#get all links
links = list(get_links())    

#get header and content in links
print("Total recodes: 20")
for k in range(20):         
    print(k+1," in progress")
    header,content = get_data(links[k])
    title.append(header)
    text.append(content)

#pandas dataframe
records = pd.DataFrame({
    'Header': title,
    'Content': text,
})

#convert pandas dataframe to csv file
records.to_csv('data.csv',index=False)
print("Records retrived and save as data.csv")

