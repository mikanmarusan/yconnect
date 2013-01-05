#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Yahoo! JAPAN YConnect(OAuth2.0 + OpenID Connect) for Python Sample Application

Explicit Grant Flow
http://developer.yahoo.co.jp/yconnect/
"""

from yconnect import YConnectExplicit
from wsgiref import simple_server
from pprint import pprint 
from StringIO import StringIO
import cgi

client_id     = '<your client_id>';
client_secret = '<your client_secret>';
redirect_uri  = '<your redirect_uri>';

class YConnectApplication(object):

	def __call__(self, environ, start_response):
		
		yconnect = YConnectExplicit(client_id, client_secret);
		method = environ['REQUEST_METHOD']

		if method == 'GET':

			# get 'code' query
			params = {}
			query = cgi.parse_qsl(environ.get('QUERY_STRING'))
			for q in query:
				params.update({q[0]:q[1]})
			code = params.get('code', '');

			if code == '':

				# 1) Authorization Request
				authrization_uri = yconnect.authorization(redirect_uri);

				start_response('301 Moved', [('Location', authrization_uri)])
				return ''

			else:

				# 2) Access Token Request and UserInfo Request
				access_token = yconnect.token(code, redirect_uri);
				userinfo = yconnect.userinfo(access_token)

				output = StringIO()
				pprint(userinfo, output)

				start_response('200 OK', [('ContentType', 'text/plain')])
				return output.getvalue()

		else:
			start_response('501 Not Implemented', [('Content-type', 'text/plain')])
			return 'Not Implemented'


application = YConnectApplication()

if __name__ == '__main__':
    server = simple_server.make_server('', 80, application)
    server.serve_forever()
