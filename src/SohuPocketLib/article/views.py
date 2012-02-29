# -*- coding: utf-8 -*-

from article.helper import get_myarticle_list_to_xml_etree, input_for_list_func, \
    get_myarticle_instance_to_xml_etree, input_for_show_func, input_for_update_func, \
    generate_single_xml_etree, input_for_destroy_func, input_for_modify_func, \
    modify_or_destroy_myarticle_instance, UpdateArticleInfo, api2_input_for_count, \
    get_myarticle_list_count, api2_convert_count_to_etree, api2_input_for_list, \
    api2_input_for_update_read_progress, api2_input_for_add, api2_input_for_delete, \
    api2_input_for_update, api2_input_for_star, api2_input_for_unstar, \
    api2_input_for_archive, api2_input_for_unarchive, api2_input_for_move, \
    api2_input_for_get_text
from common.helper import KanError
from constants import TRUE_REPR
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from lxml import etree
from page.tasks import PageFetchHandler
from user.helper import KanUser
import logging


def list(request, response_format):
    access_token_input, offset, limit = input_for_list_func(request)
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    response = None
    mimetype = 'text/plain'
    logging.warning(str(request.GET))
    if kan_user.is_logged_in():
        if response_format == 'xml':
            myarticle_list_etree = get_myarticle_list_to_xml_etree(kan_user.get_user_id(),
                                                                   offset,
                                                                   limit)
            response = etree.tostring(myarticle_list_etree,
                                      xml_declaration=True,
                                      encoding='utf-8')
            mimetype ='text/xml'
            
    return HttpResponse(response, mimetype=mimetype)


def list_test(request, *args, **kwargs):
    
    return render_to_response('article_list_test.html',
                              context_instance = RequestContext(request))


def show(request, key, response_format):
    access_token_input = input_for_show_func(request)
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    response = None
    mimetype = 'text/plain'
    logging.warning(str(request.GET))
    if kan_user.is_logged_in():
        if response_format == 'xml':
            myarticle_instance_etree = get_myarticle_instance_to_xml_etree(kan_user.get_user_id(),
                                                                           key)
            if myarticle_instance_etree is not None:
                response = etree.tostring(myarticle_instance_etree,
                                          xml_declaration=True,
                                          encoding='utf-8')
                mimetype = 'text/xml'
            
    return HttpResponse(response, mimetype=mimetype)
    

def show_test(request, *args, **kwargs):
    
    return render_to_response('article_show_test.html',
                              context_instance = RequestContext(request))

    
def update(request, response_format):
    access_token_input, url = input_for_update_func(request)
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    response = None
    logging.warning(str(request.POST))
    mimetype = 'text/plain'
    if kan_user.is_logged_in():
        update_article_info = UpdateArticleInfo(kan_user.get_user_id())
        try:
            PageFetchHandler.delay(url, update_article_info)
        except Exception:
            pass
        else:
            if response_format == 'xml':
                response_etree = generate_single_xml_etree('status', 'success')
                response = etree.tostring(response_etree, xml_declaration=True, encoding='utf-8')
                mimetype = 'text/xml'
                
    return HttpResponse(response, mimetype=mimetype)


def update_test(request, *args, **kwargs):
    
    return render_to_response('article_update_test.html',
                              context_instance = RequestContext(request))


def destroy(request, key, response_format):
    access_token_input = input_for_destroy_func(request)
    logging.warning(str(request.POST))
    modify_info = dict()
    modify_info['is_delete'] = TRUE_REPR
    
    return modify_or_destroy_base(access_token_input, modify_info, key, response_format)

        
def destroy_test(request, *args, **kwargs):
    
    return render_to_response('article_destroy_test.html',
                              context_instance = RequestContext(request))

        
def modify(request, key, response_format):
    access_token_input, modify_info = input_for_modify_func(request)
    logging.warning(str(request.POST))
    
    return modify_or_destroy_base(access_token_input, modify_info, key, response_format)


def modify_test(request, *args, **kwargs):
    
    return render_to_response('article_modify_test.html',
                              context_instance = RequestContext(request))


def modify_or_destroy_base(access_token_input, modify_info, key, response_format):
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    response = None
    is_successful = False
    mimetype = 'text/plain'
    if kan_user.is_logged_in():
        user_id = kan_user.get_user_id()
        is_successful = modify_or_destroy_myarticle_instance(user_id, key, modify_info)
    if response_format == 'xml':
        response_etree = generate_single_xml_etree('status', 'success' if is_successful else 'fail')
        response = etree.tostring(response_etree, xml_declaration=True, encoding='utf-8')
        mimetype = 'text/xml'
        
    return HttpResponse(response, mimetype=mimetype)


##############################
# views for api2
##############################


def api2_list(request):
    access_token_input, offset, limit, folder_name, order_by = api2_input_for_list(request)
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    response = None
    mimetype = 'text/xml'
    if kan_user.is_logged_in():
        article_list = select_article_list(kan_user.get_user_id(), folder_name, order_by, offset, limit)
        article_list_etree = convert_article_list_to_etree(article_list)
        response = etree.tostring(article_list_etree, xml_declaration=True, encoding='utf-8')
    else:
        error_etree = KanError('1000').get_error_etree()
        response = etree.tostring(error_etree, xml_declaration=True, encoding='utf-8')
    return HttpResponse(response, mimetype=mimetype)


def api2_count(request):
    access_token_input, folder_id = api2_input_for_count(request)
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    response = None
    mimetype = 'text/xml'
    if kan_user.is_logged_in():
        count = get_myarticle_list_count(kan_user.get_user_id(), folder_id)
        count_etree = api2_convert_count_to_etree(count)
        response = etree.tostring(count_etree, xml_declaration=True, encoding='utf-8')
    else:
        error_etree = KanError('1000').get_error_etree()
        response = etree.tostring(error_etree, xml_declaration=True, encoding='utf-8')
    
    return HttpResponse(response, mimetype=mimetype)
    


def api2_count_test(request, *args, **kwargs):
    
    return render_to_response('api2_bookmarks_count_test.html',
                              context_instance = RequestContext(request))


def api2_update_read_progress(request):
    access_token_input, bookmark_id, progress, progress_timestamp = api2_input_for_update_read_progress(request)
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    response = None
    mimetype = 'text/xml'
    if kan_user.is_logged_in():
        pass
    else:
        error_etree = KanError('1000').get_error_etree()
        response = etree.tostring(error_etree, xml_declaration=True, encoding='utf-8')
    return HttpResponse(response, mimetype=mimetype)


def api2_add(request):
    access_token_input, url, title, description, folder_name, content = api2_input_for_add(request)
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    response = None
    mimetype = 'text/xml'
    if kan_user.is_logged_in():
        pass
    else:
        error_etree = KanError('1000').get_error_etree()
        response = etree.tostring(error_etree, xml_declaration=True, encoding='utf-8')
    return HttpResponse(response, mimetype=mimetype)


def api2_delete(request):
    access_token_input, bookmark_id = api2_input_for_delete(request)
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    response = None
    mimetype = 'text/xml'
    if kan_user.is_logged_in():
        pass
    else:
        error_etree = KanError('1000').get_error_etree()
        response = etree.tostring(error_etree, xml_declaration=True, encoding='utf-8')
    return HttpResponse(response, mimetype=mimetype)


def api2_update(request):
    access_token_input, bookmark_id, title, description = api2_input_for_update(request)
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    response = None
    mimetype = 'text/xml'
    if kan_user.is_logged_in():
        pass
    else:
        error_etree = KanError('1000').get_error_etree()
        response = etree.tostring(error_etree, xml_declaration=True, encoding='utf-8')
    return HttpResponse(response, mimetype=mimetype)


def api2_view(request):
    access_token_input, bookmark_id = api2_input_for_update(request)
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    response = None
    mimetype = 'text/xml'
    if kan_user.is_logged_in():
        pass
    else:
        error_etree = KanError('1000').get_error_etree()
        response = etree.tostring(error_etree, xml_declaration=True, encoding='utf-8')
    return HttpResponse(response, mimetype=mimetype)


def api2_star(request):
    access_token_input, bookmark_id = api2_input_for_star(request)
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    response = None
    mimetype = 'text/xml'
    if kan_user.is_logged_in():
        pass
    else:
        error_etree = KanError('1000').get_error_etree()
        response = etree.tostring(error_etree, xml_declaration=True, encoding='utf-8')
    return HttpResponse(response, mimetype=mimetype)


def api2_unstar(request):
    access_token_input, bookmark_id = api2_input_for_unstar(request)
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    response = None
    mimetype = 'text/xml'
    if kan_user.is_logged_in():
        pass
    else:
        error_etree = KanError('1000').get_error_etree()
        response = etree.tostring(error_etree, xml_declaration=True, encoding='utf-8')
    return HttpResponse(response, mimetype=mimetype)


def api2_archive(request):
    access_token_input, bookmark_id = api2_input_for_archive(request)
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    response = None
    mimetype = 'text/xml'
    if kan_user.is_logged_in():
        pass
    else:
        error_etree = KanError('1000').get_error_etree()
        response = etree.tostring(error_etree, xml_declaration=True, encoding='utf-8')
    return HttpResponse(response, mimetype=mimetype)


def api2_unarchive(request):
    access_token_input, bookmark_id = api2_input_for_unarchive(request)
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    response = None
    mimetype = 'text/xml'
    if kan_user.is_logged_in():
        pass
    else:
        error_etree = KanError('1000').get_error_etree()
        response = etree.tostring(error_etree, xml_declaration=True, encoding='utf-8')
    return HttpResponse(response, mimetype=mimetype)


def api2_move(request):
    access_token_input, bookmark_id, folder_name = api2_input_for_move(request)
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    response = None
    mimetype = 'text/xml'
    if kan_user.is_logged_in():
        pass
    else:
        error_etree = KanError('1000').get_error_etree()
        response = etree.tostring(error_etree, xml_declaration=True, encoding='utf-8')
    return HttpResponse(response, mimetype=mimetype)


def api2_get_text(request):
    access_token_input, bookmark_id = api2_input_for_get_text(request)
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    response = None
    mimetype = 'text/xml'
    if kan_user.is_logged_in():
        pass
    else:
        error_etree = KanError('1000').get_error_etree()
        response = etree.tostring(error_etree, xml_declaration=True, encoding='utf-8')
    return HttpResponse(response, mimetype=mimetype)
