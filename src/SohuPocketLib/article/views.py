# -*- coding: utf-8 -*-

import os

from django.shortcuts import render_to_response
from django.http import HttpResponse

from readable import ReadableArticle
from fetch import PageFetcher

def post(request, url):
    '''
    post a url to db
    '''
    fetcher = PageFetcher()
    originalPage = fetcher.single_page(url)
    ra = ReadableArticle()
    ra.feed(originalPage)
    readableArticle = ra.get_readable_article()
    readableTitle = ra.get_readable_title()
    with open(os.path.join(os.path.dirname(__file__), 'temp').replace('\\','/') + '/' + readableTitle, 'w') as tempFile:
        tempFile.write(readableArticle)
    return HttpResponse(readableArticle)