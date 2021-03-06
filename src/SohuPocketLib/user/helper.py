# -*- coding: utf-8 -*-

from django.conf import settings
from lxml import etree, etree
from models import Access, User
import anyjson
import hashlib
import logging
import time
import urllib2


class KanUser(object):
    """
    wrapper around User
    """
    
    def __init__(self, sohupassport_uuid = '', access_token_input = ''):
        self._sohupassport_uuid = sohupassport_uuid
        self._access_token_input = access_token_input
        self._access_token = ''
        self._user = None
        self._is_logged_in = False
        
        return None
        
    def verify_and_login(self):
        """
        if successfully log in, returns true, self._is_logged_in self.access_token self._user will be updated
        if not, returns false
        """
        if self._sohupassport_uuid and not self._access_token_input:
            self._user = self._retrieve_or_create_user_from_uuid()
            self._access_token = self._create_access_token()
            self._is_logged_in = True
        elif self._access_token_input:
            self._user = self._retrieve_user_from_access_token_input()
            if self._user:
                self._is_logged_in = True
                self._access_token = self._access_token_input
                
        return self._is_logged_in
                
    def is_logged_in(self):
        
        return self._is_logged_in
    
    def get_user(self):
        if self.is_logged_in():
            return self._user
        else:
            return None
    
    def get_access_token(self):
        if self.is_logged_in():
            return self._access_token
        else:
            return None
        
    def get_user_id(self):
        if self.is_logged_in():
            return self._user.id
        else:
            return None
    
    def get_sohupassport_uuid(self):
        if self.is_logged_in():
            return self._user.sohupassport_uuid
        else:
            return None
        
    def get_kan_username(self):
        if self.is_logged_in():
            return self._user.kan_username
        else:
            return None
        
    def set_kan_username(self, kan_username):
        if self.is_logged_in():
            self._user.kan_username = kan_username
            self._user.save()
            return True
        else:
            return False
        
    def get_kan_self_description(self):
        if self.is_logged_in():
            return self._user.kan_self_description
        else:
            return None
        
    def set_kan_self_description(self, kan_self_description):
        if self.is_logged_in():
            self._user.kan_self_description = kan_self_description
            self._user.save()
            return True
        else:
            return False
            
    def _create_access_token(self):
        hash_source = self._sohupassport_uuid + str(time.time())
        access_token_string = hashlib.new('sha1', hash_source).hexdigest()
        Access.objects.create(
                              access_token = access_token_string,
                              user = self._user,
                              )
        
        return access_token_string
    
    def _retrieve_or_create_user_from_uuid(self):
        try:
            user = User.objects.get(sohupassport_uuid = self._sohupassport_uuid)
        except User.DoesNotExist:
            user = User.objects.create(
                                       sohupassport_uuid = self._sohupassport_uuid,
                                       kan_username = '',
                                       kan_self_description = '',
                                       )
            
        return user
        
    def _retrieve_user_from_access_token_input(self):
        try:
            user = Access.objects.get(access_token = self._access_token_input).user
        except Access.DoesNotExist:
            return None
        else:
            return user

        
def serialize(python_obj):
    try:
        result = anyjson.dumps(python_obj)
    except TypeError:
        result = None
        
    return result

    
def get_user_info_for_web(request):
    sohupassport_uuid = str(request.META.get('HTTP_X_SOHUPASSPORT_UUID', ''))
    access_token_input = request.COOKIES.get('access_token', '')
    
    return sohupassport_uuid, access_token_input


def set_user_info_for_web(response, sohupassport_uuid = '', access_token = ''):
    try:
        response.set_cookie('access_token', access_token)
    except Exception:
        return False
    else:
        return True


def get_GET_dict(request):
    if request.method == 'GET':
        return request.GET
    else:
        return None

    
def get_POST_dict(request):
    if request.method == 'POST':
        return request.POST
    else:
        return None    


def input_for_verify_func(request):
    sohupassport_uuid = str(request.META.get('HTTP_X_SOHUPASSPORT_UUID', ''))
    access_token_input = get_POST_dict(request).get('access_token', '')
    
    return sohupassport_uuid, access_token_input


def input_for_show_func(request):
    access_token_input = get_GET_dict(request).get('access_token', '')
    
    return access_token_input


def input_for_update_func(request):
    access_token_input = get_POST_dict(request).get('access_token', '')
    user_info_dict = dict()
    keys = ('kan_username', 'kan_self_description')
    for key in keys:
        user_info_dict[key] = get_POST_dict(request).get(key, '')
        
    return access_token_input, user_info_dict

    
def extract_class_instance_to_dict(ins):
    """
    extract class instance to dict
    dispose keys starts with _
    dispose key *id*
    """
    ins_dict = ins.__dict__.copy()
    for key in ins_dict.copy():
        if key.startswith('_'):
            del ins_dict[key]
    try:
        del ins_dict['id']
    except Exception:
        pass
    
    return ins_dict


def api2_input_for_access_token_func(request):
#    sohupassport_uuid = request.META.get('HTTP_X_SOHUPASSPORT_UUID', '')
#    if settings.IS_PRODUCTION_SERVER:
#        sohupassport_uuid = '81215bb13f2f497u'
    if request.method == 'POST':
        passport_userid = request.POST.get('userid', None)
        passport_token = request.POST.get('token', None)
        passport_gid = request.POST.get('gid', None)
    else:
        passport_userid = None
        passport_token = None
        passport_gid = None
    
#    passport_userid = 'edison_0951@yahoo.com.cn'
#    passport_token = '4813f05988a1000b1b5b8e428d0b9498'
#    passport_gid = '7bcd0c8866e5fa8b7af624732ec6d6dc60d3daee'
    
    return passport_userid, passport_token, passport_gid


def api2_input_for_verify_credentials_func(request):
    if request.method == 'POST':
        access_token_input = request.COOKIES.get('access_token', '')
    else:
        access_token_input = ''
    
    return access_token_input


def api2_input_for_update_func(request):
    if request.method == 'POST':
        access_token_input = request.COOKIES.get('access_token', '')
        valid_modify_attrs = ('username', 'description')
        modify_info = dict()
        
        for attr in valid_modify_attrs:
            if request.POST.has_key(attr):
                modify_info[attr] = request.POST[attr]
    else:
        access_token_input = ''
        modify_info = dict()
            
    return access_token_input, modify_info


def api2_convert_kan_user_to_xml_etree(kan_user):
    if kan_user:
        user = etree.Element('user')
    
        user_id = etree.SubElement(user, 'user_id')
        user_id.text = str(kan_user.get_user_id())
    
        username = etree.SubElement(user, 'username')
        username.text = kan_user.get_kan_username()
    
        description = etree.SubElement(user, 'description')
        description.text = kan_user.get_kan_self_description()
    else:
        user = None
        
    return user


def api2_modify_kan_user_common(kan_user, modify_info):
    if modify_info.has_key('username'):
        kan_user.set_kan_username(modify_info['username'])
    if modify_info.has_key('description'):
        kan_user.set_kan_self_description(modify_info['description'])
        
    return None


def api2_input_for_access_token_common(request):
    access_token_input = request.COOKIES.get('access_token', '')
    
    return access_token_input
    

def api2_convert_token_to_info(passport_userid, passport_token, passport_gid):
    info_node = etree.Element('info')
    
    userid_node = etree.SubElement(info_node, 'userid')
    userid_node.text = passport_userid
    
    token_node = etree.SubElement(info_node, 'token')
    token_node.text = passport_token
    
    appid_node = etree.SubElement(info_node, 'appid')
    appid_node.text = settings.APP_ID
    
    gid_node = etree.SubElement(info_node, 'gid')
    gid_node.text = passport_gid
    
    sig_node = etree.SubElement(info_node, 'sig')
    hash_source = (passport_userid or '') \
                + (passport_token or '') \
                + (settings.APP_ID or '') \
                + (passport_gid or '') \
                + (settings.APP_KEY or '')
    logging.warning(hash_source)
    try:
        sig_node.text = hashlib.new('md5', hash_source).hexdigest()
    except TypeError:
        sig_node.text = ''
    
    return info_node


def api2_auth_token(passport_userid, passport_token, passport_gid):
    info_etree = api2_convert_token_to_info(passport_userid, passport_token, passport_gid)
    auth_token_port = 'http://internal.passport.sohu.com/interface/mobile/mobile_authtoken.jsp'
    data = etree.tostring(info_etree, xml_declaration=True, encoding='gbk')
    logging.warning(data)
    resp = urllib2.urlopen(auth_token_port, data).read()
    logging.warning(resp)
    if resp == '0':
        sohupassport_uuid = passport_userid
    else:
        sohupassport_uuid = None
    
    return sohupassport_uuid