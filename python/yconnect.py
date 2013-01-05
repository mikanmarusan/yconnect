#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Yahoo! JAPAN YConnect(OAuth2.0 + OpenID Connect) for Python Sample Class

Explicit Grant Flow
http://developer.yahoo.co.jp/yconnect/
"""

import urllib
import urllib2
import base64
import json

class YConnectExplicit:
	
	_AUTHORIZATION_URI = 'https://auth.login.yahoo.co.jp/yconnect/v1/authorization';
	_TOKEN_URI         = 'https://auth.login.yahoo.co.jp/yconnect/v1/token';
	_USERINFO_URI      = 'https://userinfo.yahooapis.jp/yconnect/v1/attribute';

	def __init__(self, client_id, client_secret):
		self.client_id = client_id
		self.client_secret = client_secret
	
	def authorization(self,
	                  redirect_uri,
	                  response_type = 'code',
	                  scope = 'openid profile email address'):
		params = {
		    'response_type': response_type,
		    'client_id':  self.client_id,
		    'redirect_uri': redirect_uri,
		    'scope': scope,
		}

		return YConnectExplicit._AUTHORIZATION_URI + '?' + urllib.urlencode(params)
	
	def token(self, code, redirect_uri):
		params = {
		    'grant_type': 'authorization_code',
		    'code': code,
		    'redirect_uri': redirect_uri,
		}

		headers = {
		    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8', 
		    'Authorization': 'Basic ' + base64.b64encode(self.client_id + ':' + self.client_secret)
		}

		response = YConnectExplicit.http_request(YConnectExplicit._TOKEN_URI,
		                                         'POST',
		                                         params,
		                                         headers)
		response = json.loads(response);

		# obtain access token
		access_token = str(response['access_token'])
		return access_token
	
	def userinfo(self, access_token):
		params = {
		    'schema': 'openid',
		}

		headers = {
		    'Authorization': 'Bearer ' + access_token
		}
		
		response = YConnectExplicit.http_request(YConnectExplicit._USERINFO_URI,
		                                         'GET',
		                                         params,
		                                         headers)
		return json.loads(response)

	@staticmethod
	def http_request(uri, scheme, params, headers):

		query = urllib.urlencode(params)
		
		if scheme == 'GET':
			uri = uri + '?' + query
			req = urllib2.Request(uri, None, headers)
		else:
			req = urllib2.Request(uri, query, headers)

		response = urllib2.urlopen(req)
		response = response.read()

		return response
