import whois
import requests
import datetime
from urllib.parse import urlparse

def load_urls4check(path):
    with open(path, 'r') as file:
        for line in file:
            yield line.strip()

def is_server_respond_with_200(url):
    response = requests.get(url)
    return response.status_code == requests.codes.ok

def get_domain_expiration_date(domain_name):
    domain_info = whois.whois(domain_name)
    if isinstance(domain_info.expiration_date,list):
        return domain_info.expiration_date[0]
    return domain_info.expiration_date

def extract_domain_name(url):
    parsed_uri = urlparse(url)
    return parsed_uri.netloc

if __name__ == '__main__':
    for url in load_urls4check('../checking_urls.txt'):
        print(url)
        if is_server_respond_with_200(url):
            print(' - response OK')
        else:
            print(' - response Error')
        domain_name = extract_domain_name(url)
        expiration = get_domain_expiration_date(domain_name)
        td_month = datetime.timedelta(days=30)
        future_day = datetime.date.today() + td_month
        if future_day <= expiration.date():
            print(' - domain paid at least 30 days ({0})'.format(
                expiration.strftime('%Y-%m-%d')
            ))
        else:
            print(' - must be paid before {0}'.format(
                expiration.strftime('%Y-%m-%d')
            ))
        print()
