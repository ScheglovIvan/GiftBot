import requests
from bs4 import BeautifulSoup
import json
    

def parser(url, price):
    try:
        headers = {
            'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
            }

        course_url = 'https://blockchain.info/ru/ticker'
        course_session = requests.Session()
        course_request = course_session.get(course_url, headers=headers)
        course_soup = BeautifulSoup(course_request.content, 'html.parser')

        course = json.loads(str(course_soup))['USD']['last']

        headers = {
            'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
            }

        base_url = url
        session = requests.Session()
        request = session.get(base_url, headers=headers)
        soup = BeautifulSoup(request.content, 'html.parser')

        recipient_wallet = soup.find('div', attrs={'class': 'sc-1myx216-0 QtNr'}).find('div', attrs={'class': 'sc-19pxzmk-0 iWKmuA'}).find('a').text
        transfer_amount = course * float(soup.find('div', attrs={'class': 'sc-1myx216-0 QtNr'}).find('div', attrs={'class': 'kad8ah-0 hEUgGr'}).text[:-4])
        
        my_wallet = "bc1qt6y69dvkwfu9crqvmmf2wx3y24p68ptkep82d9"
        
        
        if my_wallet == recipient_wallet:
            if transfer_amount >= price:
                return ["(1/3) Link ✅", "(2/3) Btc wallet ✅", "(3/3) Payment ✅", True]
            else:
                return ["(1/3) Link ✅", "(2/3) Btc wallet ✅", "(3/3) Payment ❌\n\nYou paid less than you need. Please transfer the part of the amount that is missing and try again."]
        else:
            return ["(1/3) Link ✅", "(2/3) Btc wallet ❌\n\nThe recipient's bitcoin wallet does not match with our bitcoin wallet. Please submit a new correct link and try again."]
    except:
        return ["(1/3) Link ❌\n\nThe link you provided was not found, or someone has already sent it. Send a new link and try again"]
