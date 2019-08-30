# -*- Encoding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import codecs


def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'  # noqa
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


def parse_one_page(html):

    soup = BeautifulSoup(html, 'lxml')
    i = 0
    for item in soup.select('tr')[2:-1]:

        yield{
            'time': item.select('td')[i].text,
            'issue': item.select('td')[i+1].text,
            'digits': item.select('td em')[0].text,
            'ten_digits': item.select('td em')[1].text,
            'hundred_digits': item.select('td em')[2].text,
            'single_selection': item.select('td')[i+3].text,
            'group_selection_3': item.select('td')[i+4].text,
            'group_selection_6': item.select('td')[i+5].text,
            'sales': item.select('td')[i+6].text,
            'return_rates': item.select('td')[i+7].text
        }


def write_to_excel(f):
    header = [u'开奖日期', u'期号', u'个位数', u'十位数', u'百位数', u'单数', u'组选3', u'组选6', u'销售额', u'返奖比例']  # noqa
    f.write(u','.join(header))
    f.write('\n')

    for k in range(1, 250):
        url = 'http://kaijiang.zhcw.com/zhcw/html/3d/list_%s.html' % (str(k))
        html = get_one_page(url)
        if not html:
            print('skip page: %s' % k)
            continue

        for item in parse_one_page(html):
            f.write(u'"%s"' % u'","'.join(map(lambda x: x.strip(), [
                item['time'],
                item['issue'],
                item['digits'],
                item['ten_digits'],
                item['hundred_digits'],
                item['single_selection'],
                item['group_selection_3'],
                item['group_selection_6'],
                item['sales'],
                item['return_rates'],
                ])))
            f.write('\n')


def main():

    with codecs.open('3d.csv', 'w', encoding='utf8') as f:
        write_to_excel(f)


if __name__ == '__main__':
    main()
