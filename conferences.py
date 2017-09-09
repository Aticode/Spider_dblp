# -*- coding:utf-8 -*-
#Use requests (2.13.0), lxml (3.8.0)
#Authors: Ati
#Date: 2017/09

import os
import sys
import re
import csv
import requests
from lxml import etree


def extractor(tree, fp_name):
    fp = open(fp_name, 'wt', newline = '', encoding = 'utf-8')
    writer = csv.writer(fp)
    lis = tree.xpath("//li[@class='entry inproceedings']")
    for li in lis:
        #conf
        conf = fp_name.split('\\')[-2].strip() + '/' + (fp_name.split('\\')[-1]).split('.')[-2].strip()
        #year
        year = re.search(r'\d{4}', li.xpath("//header[@class='headline noline']/h1/text()")[0].strip()).group(0)
        #area
        area = 'None'
        if li.xpath("..//preceding-sibling::header/h2/text()"):
            area = li.xpath("..//preceding-sibling::header/h2/text()")[-1].replace('\n', '').rstrip('I').strip()
        #title
        title_spans = li.xpath(".//span[@class='title']")
        for title_span in title_spans:
            titles = title_span.xpath('string(.)').strip()
            title_string = ''
            for title in titles:
                title_string = title_string + title
            title_string = title_string.strip()
        #author
        author_string = ''
        authors = li.xpath(".//span[@itemprop='author']/a/span/text()")
        for author in authors:
            author_string = author_string + author.strip() + ';'
        #link
        link = 'None'
        if li.xpath("./nav/ul/li[1]/div[1]/a/@href"):
            link = li.xpath("./nav/ul/li[1]/div[1]/a/@href")[0].strip()
        writer.writerow((conf, year, area, title_string, author_string, link))
    fp.close()
    print('Finish: ', fp_name.encode('utf-8'))

def spider(headers, conferences_url):
    #get into each conference url
    for conference_url in conferences_url:
        html_level1 = requests.get(conference_url, headers = headers).content
        tree_level1 = etree.HTML(html_level1)
        conferences = tree_level1.xpath("//a[contains(@href, 'dblp.uni-trier.de/db/conf/') and contains(@href, 'html')]/@href")
        conferences = list(set(conferences))
        fp_dir = os.path.split(os.path.realpath(sys.argv[0]))[0] + os.sep + 'source' + \
            os.sep + 'conf' + os.sep + conference_url.split('/')[-2]
        if not os.path.exists(fp_dir):
            os.makedirs(fp_dir)

        #get into each conference page
        for conference in conferences:
            fp_name = fp_dir + os.sep + (conference.split('/')[-1]).split('.')[0] + '.csv'
            #Do not rewrite history records
            if os.path.exists(fp_name):
                print('History: ', fp_name.encode('utf-8'))
                continue
            html_level2 = requests.get(conference, headers = headers).content
            tree_level2 = etree.HTML(html_level2)
            #if it is the conference page
            if tree_level2.xpath("//li[@class='entry inproceedings']"):
                extractor(tree_level2, fp_name)
            #else there is a deeper level
            else:
                volumes = tree_level2.xpath("//*[@id='main']/ul/li/a/@href")
                for volume in volumes:
                    fp_name = fp_dir + os.sep + (volume.split('/')[-1]).split('.')[0] + '.csv'
                    #Do not rewrite history records
                    if os.path.exists(fp_name):
                        print('History: ', fp_name.encode('utf-8'))
                        continue
                    html_level3 = requests.get(volume, headers = headers).content
                    tree_level3 = etree.HTML(html_level3)
                    extractor(tree_level3, fp_name)

def main():
    headers={
        'Accept':'*/*',
        'Connection':'keep-alive',
        'Origin':'http://dblp.uni-trier.de/db/conf/',
        'Referer':'http://dblp.uni-trier.de/db/conf/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    }

    conferences_url = [\
                ### IACR conferences ###
                  'http://dblp.uni-trier.de/db/conf/crypto/',\
                  'http://dblp.uni-trier.de/db/conf/eurocrypt/',\
                  'http://dblp.uni-trier.de/db/conf/asiacrypt/',\
                  'http://dblp.uni-trier.de/db/conf/pkc/',\
                  'http://dblp.uni-trier.de/db/conf/tcc/',\
                  'http://dblp.uni-trier.de/db/conf/ches/',\
                  'http://dblp.uni-trier.de/db/conf/fse/',\
                ### Other class A, B conferences ###
                  'http://dblp.uni-trier.de/db/conf/sp/',\
                  'http://dblp.uni-trier.de/db/conf/uss/',\
                  'http://dblp.uni-trier.de/db/conf/ccs/',\
                  'http://dblp.uni-trier.de/db/conf/ndss/',\
                  'http://dblp.uni-trier.de/db/conf/acsac/',\
                  'http://dblp.uni-trier.de/db/conf/esorics/',\
                  'http://dblp.uni-trier.de/db/conf/csfw/',\
                  'http://dblp.uni-trier.de/db/conf/raid/',\
                  'http://dblp.uni-trier.de/db/conf/dsn/',\
                  'http://dblp.uni-trier.de/db/conf/srds/',\
                ### Other conferences ###
                  'http://dblp.uni-trier.de/db/conf/infocom/',\
                ### class C conferences ###
                #   'http://dblp.uni-trier.de/db/conf/wisec/',\
                #   'http://dblp.uni-trier.de/db/conf/ih/',\
                #   'http://dblp.uni-trier.de/db/conf/sacmat/',\
                #   'http://dblp.uni-trier.de/db/conf/drm/',\
                #   'http://dblp.uni-trier.de/db/conf/acns/',\
                #   'http://dblp.uni-trier.de/db/conf/acisp/',\
                #   'http://dblp.uni-trier.de/db/conf/dfrws/',\
                #   'http://dblp.uni-trier.de/db/conf/fc/',\
                #   'http://dblp.uni-trier.de/db/conf/dimva/',\
                #   'http://dblp.uni-trier.de/db/conf/sec/',\
                #   'http://dblp.uni-trier.de/db/conf/isw/',\
                #   'http://dblp.uni-trier.de/db/conf/icics/',\
                #   'http://dblp.uni-trier.de/db/conf/securecomm/',\
                #   'http://dblp.uni-trier.de/db/conf/nspw/',\
                #   'http://dblp.uni-trier.de/db/conf/ctrsa/',\
                #   'http://dblp.uni-trier.de/db/conf/soups/',\
                #   'http://dblp.uni-trier.de/db/conf/sacrypt/',\
                #   'http://dblp.uni-trier.de/db/conf/trustcom/',\
                #   'http://dblp.uni-trier.de/db/conf/pam/',\
                #   'http://dblp.uni-trier.de/db/conf/pet/',\
                #   'http://dblp.uni-trier.de/db/conf/icdf2c/',\
                ]

    spider(headers, conferences_url)

if __name__ == "__main__":  
    main()