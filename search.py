import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import smtplib
import db
import send_mail


def get_emails(link):
    req = requests.get(link)
    soup = BeautifulSoup(req.text , 'html.parser')
    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.\w{2,3}",soup.text, re.I))
    links = soup.find_all('a')
    page_links = set()
    for link in links :
        if 'href' in link.attrs:
            page_links.add(link.attrs['href'])
    return new_emails , page_links

url = input('please enter your url : ' )
# url = 'http://37.152.180.106/'

# with open('text.html' , '+w' ) as f :
#     f.write(str(soup.prettify()))
# regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

do_scrape = deque([url])
all_mails = set()
while(len(do_scrape)):
    url = do_scrape.popleft()
    emails  , links = get_emails(url)
    all_mails = all_mails | emails
    for link in links :
        do_scrape.append(link)
# Now we will add the emails to the database
link = 'http://www.google.com'
db.main(all_mails)
send_mail.send_mail(link)





