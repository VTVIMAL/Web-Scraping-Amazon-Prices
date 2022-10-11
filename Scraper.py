from bs4 import BeautifulSoup
import requests
import smtplib
import os
from email.message import EmailMessage

# Amazon url
URL = 'https://www.amazon.in/Amazfit-AMOLED-Display-Monitor-Bluetooth-Storage/dp/B08XWRSKVK/ref=sr_1_8?keywords' \
      '=amazfit+smart+watch&qid=1665469364&qu=eyJxc2MiOiI1LjUzIiwicXNhIjoiNS40MSIsInFzcCI6IjQuNzYifQ%3D%3D&sprefix' \
      '=%2Caps%2C274&sr=8-8 '

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/105.0.0.0 Safari/537.36",
           "Accept-Encoding": "gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}


source = requests.get(URL, headers=headers)

content = BeautifulSoup(source.content, 'html.parser')

soup = BeautifulSoup(content.prettify(), 'html.parser')

# user email and password
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')


# check the price of product
def check_price():

    title = soup.find(id='productTitle').get_text() # view the name of product(optional: for later use )

    price = soup.find('span', class_='a-offscreen').get_text()
    price = price.strip()[1:].replace(",", "")  # reformatting the price

    float_price = float(price) # converting price from str -> float

    acceptable_price = 7000

    if float_price <= acceptable_price:
        send_mail()  # send mail if price acceptable


def send_mail():

    msg = EmailMessage()
    msg['Subject'] = 'Price Drop for Product'
    msg['Form'] = EMAIL_ADDRESS
    msg['To'] = 'vimalprasad0000001@gmail.com'
    msg.set_content('Check the link to view the product '
                       'https://www.amazon.in/Amazfit-AMOLED-Display-Monitor-Bluetooth-Storage/dp/B08XWRSKVK/ref'
                       '=sr_1_8?keywords'
                       '=amazfit+smart+watch&qid=1665469364&qu=eyJxc2MiOiI1LjUzIiwicXNhIjoiNS40MSIsInFzcCI6IjQuNzYifQ'
                       '%3D%3D&sprefix'
                       '=%2Caps%2C274&sr=8-8')

    server = smtplib.SMTP('smtp.gmail.com', 587)
    # identify to gmail smtp client
    server.ehlo()
    # secure email using  tls encryption
    server.starttls()
    # re-identify ourself after encryption
    server.ehlo()

    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    server.send_message(msg)


check_price()