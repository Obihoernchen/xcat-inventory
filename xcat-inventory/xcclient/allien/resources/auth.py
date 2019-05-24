###############################################################################
# IBM(c) 2019 EPL license http://www.eclipse.org/legal/epl-v10.html
###############################################################################

# -*- coding: utf-8 -*-

import uuid

from flask import request, current_app, jsonify, g
from flask_restplus import Resource, Namespace, fields

from ..authmanager import *
from . import token_parser

ns = Namespace('auth', description='The Authorization section for APIs')

auth_post_resource = ns.model('auth_post_Resource', {
    'username': fields.String(description="User account name", required=True),
    'password': fields.String(description="User account password", required=True)
})


def check_request_user(request):
    try:
        if request.headers['Content-Type'] == 'application/json':
            post_data = request.get_json()
        elif 'form' in request.headers['Content-Type']:
            post_data = request.form.to_dict()
        else:
            return 400, 'Unsupported Content-Type'
        usr = post_data['username']
        pwd = post_data['password']
        g.username = usr
        g.password = pwd
        if check_user_account(usr, pwd):
            return 200, None
        else:
            return 401, None
    except Exception:
        return 401, None


def check_request_token(request):
    try:
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split(" ")[1] 
    except Exception:
        return 401
    g.auth_token = auth_token
    flag, user = check_user_token(auth_token)
    if flag == 1:
        r, m = check_request_user(request)
        if not r == 200 or check_user_token(auth_token, username=g.username, check_expire=False)[0] != 0:
            return 401
    elif flag == 2:
        return 401
    g.username = user
    return 200


def check_request_token_without_account(request):
    try:
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split(" ")[1] 
    except Exception:
        return 401
    g.auth_token = auth_token
    flag, user = check_user_token(auth_token)
    if flag == 2:
        return 401
    return 200


@ns.route('/login')
class ToLogin(Resource):

    @ns.expect(auth_post_resource)
    @ns.response(200, '{ "token": { \
    "expire: "xxx", \
    "id": "tokenid" \
     }}')
    def post(self):
        r, m = check_request_user(request)
        if r == 200: 
            token = uuid.uuid1()
            t = time.time()
            expire = time.time() + 86400
            insert_user_token(g.username, str(token), str(expire))
            return jsonify({'token':{'id': str(token), 'expire': time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(expire))}}) 
        elif m is not None:
            ns.abort(r, m)
        else:
            ns.abort(r)


@ns.route('/refresh')
@ns.doc(security='apikey')
class ToRefresh(Resource):

    @ns.response(200, "Token refreshed")
    def post(self):
        r = check_request_token(request)
        if r == 200:
            update_user_token(g.auth_token, str(time.time() + 86400))
            return "Token refreshed"
        else:
            ns.abort(r)


@ns.route('/logout')
@ns.doc(security='apikey')
class ToLogout(Resource):

    @ns.response(200, "Logged out")
    def post(self):
        r = check_request_token_without_account(request)
        if r == 200:
            remove_user_token(g.auth_token)
            return 'Logged out'
        else:
            ns.abort(r)
