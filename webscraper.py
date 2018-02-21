import requests
from bs4 import BeautifulSoup
import json

def geturls():
    urls = []
    #link1
    #for i in range(1,12):
        #url = 'https://www.pinoyexchange.com/forums/showthread.php?t=437167&page='+str(i)
    #link2
    for i in range(1,136):
        url = 'https://www.pinoyexchange.com/forums/showthread.php?t=257479&page='+str(i)
        urls.append(url)

    return urls

def getusernames(username_elements): 
    post_usernames = []
    for name in username_elements:
            ext_name = name.text.strip()
            #extract username if username is email protected
            if(ext_name.find('[email') != -1):
                ext_name = name['title'].strip(" is offline").strip(" is online").strip()
            post_usernames.append(ext_name)
    return post_usernames

def getpostdates(post_date_elements):
    post_dates = []
    for date in post_date_elements:
            post_dates.append(date.text.strip())
    return post_dates        

def getpostsinfo(post_elements,post_usernames,post_dates):
    posts_info = []
    counter = 0
    for content in post_elements:
        post = {}
        post['replied_to'] = ''
        post['replied_to_message'] = ''
        post['username'] = post_usernames[counter]
        post['date_posted'] = post_dates[counter]
        
        replied_to = content.select('.bbcode_postedby')
        #check if post is a reply
        if(len(replied_to) > 0):
            replied_to_name = replied_to[0].strong.text.strip()
            message = content.select('.message')
            quoted_message = message[0].text.strip()
            post['replied_to'] = replied_to_name
            post['replied_to_message'] = quoted_message
            content.find(class_='bbcode_container').decompose()
            
        text = content.text.strip()
        post['content'] = text
        posts_info.append(post)
        counter = counter + 1
    return posts_info

def scrape(urls):
    for url in urls:
        
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        post_elements = soup.select("blockquote.postcontent.restore")
        username_elements = soup.find_all(class_='username')
        post_date_elements = soup.find_all(class_='postdate')
        #extract all usernames
        post_usernames = getusernames(username_elements)

        #extract postdates
        post_dates = getpostdates(post_date_elements)
        
        #extract post contents
        posts_info = getpostsinfo(post_elements,post_usernames,post_dates)

        return posts_info


urls = geturls()
posts_info = scrape(urls)
print(json.dumps(posts_info))