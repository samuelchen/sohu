# -*- coding: utf-8 -*-

from article.helper import generate_single_xml_etree
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from helper import KanUser, serialize
from lxml import etree
from user.helper import get_kan_user_to_xml_etree, \
    input_for_api2_access_token_func, input_for_verify_func, input_for_show_func, \
    extract_class_instance_to_dict, input_for_update_func, \
    input_for_api2_verify_credentials_func, input_for_api2_update_func, \
    update_kan_user_instance
import logging
import datetime


def verify(request):
    """
    verify user infomation, return access_token
    """
    sohupassport_uuid, access_token_input = input_for_verify_func(request)
    kan_user = KanUser(sohupassport_uuid, access_token_input)
    kan_user.verify_and_login()
    if kan_user.is_logged_in():
        response_dict = dict()
        response_dict['access_token'] = kan_user.get_access_token()
        response = HttpResponse(serialize(response_dict))
    else:
        response = HttpResponse(serialize(None))
        
    return response


def verify_test(request):
    
    return render_to_response('user_verify_test.html',
                              context_instance = RequestContext(request))

    
def show(request):
    """
    show user infomation
    """
    access_token_input = input_for_show_func(request)
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    if kan_user.is_logged_in():
        response_dict = extract_class_instance_to_dict(kan_user.get_user())
        response = HttpResponse(serialize(response_dict))
    else:
        response = HttpResponse(serialize(None))
        
    return response


def show_test(request):
    
    return render_to_response('user_show_test.html',
                              context_instance = RequestContext(request))

    
def update(request):
    """
    update user infomation
    """
    access_token_input, user_info_dict = input_for_update_func(request)
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    if kan_user.is_logged_in():
        kan_user.set_kan_username(user_info_dict.get('kan_username', ''))
        kan_user.set_kan_self_description(user_info_dict.get('kan_self_description', ''))
        response_dict = extract_class_instance_to_dict(kan_user.get_user())
        response = HttpResponse(serialize(response_dict))
    else:
        response = HttpResponse(serialize(None))
        
    return response


def update_test(request):
    
    return render_to_response('user_update_test.html',
                              context_instance = RequestContext(request))


def api2_access_token(request):
    
    sohupassport_uuid = input_for_api2_access_token_func(request)
    kan_user = KanUser(sohupassport_uuid, '')
    kan_user.verify_and_login()
    response = None
    mimetype = 'text/xml'
    if kan_user.is_logged_in():
        kan_user_etree = get_kan_user_to_xml_etree(kan_user)
        if kan_user_etree is not None:
            response = etree.tostring(kan_user_etree, xml_declaration=True, encoding='utf-8')
        http_response = HttpResponse(response, mimetype=mimetype)
        http_response.set_cookie('access_token',
                                 kan_user.get_access_token(),
                                 expires=datetime.datetime.now() + datetime.timedelta(days=1),
                                 httponly=False)
    else:
        response_etree = generate_single_xml_etree('status', request.GET.get('status', ''))
        response = etree.tostring(response_etree, xml_declaration=True, encoding='utf-8')
        http_response = HttpResponse(response, mimetype=mimetype)
        
    return http_response


def api2_verify_credentials(request):
    
    access_token_input = input_for_api2_verify_credentials_func(request)
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    response = None
    mimetype = 'text/xml'
    if kan_user.is_logged_in():
        kan_user_etree = get_kan_user_to_xml_etree(kan_user)
        if kan_user_etree is not None:
            response = etree.tostring(kan_user_etree, xml_declaration=True, encoding='utf-8')
        http_response = HttpResponse(response, mimetype=mimetype)
        http_response.set_cookie('access_token', kan_user.get_access_token(), httponly=False)
    else:
        response_etree = generate_single_xml_etree('status', 'verify failed')
        response = etree.tostring(response_etree, xml_declaration=True, encoding='utf-8')
        http_response = HttpResponse(response, mimetype=mimetype)
        
    return http_response


def api2_update(request):
    
    access_token_input, modify_info = input_for_api2_update_func(request)
    kan_user = KanUser('', access_token_input)
    kan_user.verify_and_login()
    response = None
    mimetype = 'text/xml'
    if kan_user.is_logged_in():
        update_kan_user_instance(kan_user, modify_info)
        kan_user_etree = get_kan_user_to_xml_etree(kan_user)
        if kan_user_etree is not None:
            response = etree.tostring(kan_user_etree, xml_declaration=True, encoding='utf-8')
        http_response = HttpResponse(response, mimetype=mimetype)
        http_response.set_cookie('access_token', kan_user.get_access_token())
    else:
        response_etree = generate_single_xml_etree('status', 'verify failed')
        response = etree.tostring(response_etree, xml_declaration=True, encoding='utf-8')
        http_response = HttpResponse(response, mimetype=mimetype)
        
    return http_response


def api2_update_test(request):
    
    return render_to_response('api2_account_update_test.html',
                              context_instance = RequestContext(request))
