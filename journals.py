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
    lis = tree.xpath("//li[@class='entry article']")
    for li in lis:
        #jour
        jour = fp_name.split('\\')[-2].strip() + '/' + (fp_name.split('\\')[-1]).split('.')[-2].strip()
        #year
        year = li.xpath("..//preceding-sibling::header/h2/text()")[-1].split(',')[-1].strip()
        #number
        number = li.xpath("..//preceding-sibling::header/h2/text()")[-1].split(',')[1].strip()
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
        writer.writerow((jour, year, number, title_string, author_string, link))
    fp.close()
    print('Finish: ', fp_name.encode('utf-8'))

def spider(headers, journals_url):
    #get into each journal url
    for journal_url in journals_url:
        html_level1 = requests.get(journal_url, headers = headers).content
        tree_level1 = etree.HTML(html_level1)
        journals = tree_level1.xpath("//div[@id='main']/ul/li/a/@href")
        fp_dir = os.path.split(os.path.realpath(sys.argv[0]))[0] + os.sep + 'source' + os.sep + journals[0].split('/')[-3] + os.sep + journals[0].split('/')[-2]
        if not os.path.exists(fp_dir):
            os.makedirs(fp_dir)

        #get into each journal page
        for journal in journals:
            fp_name = fp_dir + os.sep + (journal.split('/')[-1]).split('.')[0] + '.csv'
            #Do not rewrite history records
            if os.path.exists(fp_name):
                print('History: ', fp_name.encode('utf-8'))
                continue
            html_level2 = requests.get(journal, headers = headers).content
            tree_level2 = etree.HTML(html_level2)
            extractor(tree_level2, fp_name)

def main():
    headers={
        'Accept':'*/*',
        'Connection':'keep-alive',
        'Origin':'http://dblp.uni-trier.de/db/conf/',
        'Referer':'http://dblp.uni-trier.de/db/conf/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    }

    journals_url = [\
                ### IACR journals ###
                  'http://dblp.uni-trier.de/db/journals/joc/',\
                  'http://dblp.uni-trier.de/db/journals/tosc/',\
                ### Other class A, B journals ###
                  'http://dblp.uni-trier.de/db/journals/tdsc/',\
                  'http://dblp.uni-trier.de/db/journals/tifs/',\
                  'http://dblp.uni-trier.de/db/journals/tissec/',\
                  'http://dblp.uni-trier.de/db/journals/compsec/',\
                  'http://dblp.uni-trier.de/db/journals/dcc/',\
                  'http://dblp.uni-trier.de/db/journals/jcs/',\
                ### Class C jounals ###
                #   'http://dblp.uni-trier.de/db/journals/ejisec/',\
                #   'http://dblp.uni-trier.de/db/journals/iet-ifs/',\
                #   'http://dblp.uni-trier.de/db/journals/imcs/',\
                #   'http://dblp.uni-trier.de/db/journals/istr/',\
                #   'http://dblp.uni-trier.de/db/journals/ijisp',\
                #   'http://dblp.uni-trier.de/db/journals/ijics/',\
                #   'http://dblp.uni-trier.de/db/journals/scn/',\
                ]
    
    spider(headers, journals_url)

if __name__ == "__main__":
    main()