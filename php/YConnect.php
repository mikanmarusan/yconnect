<?php
class YConnect {

	protected $client_id;
	protected $client_sercret;

	const AUTHORIZATION_URI   = 'https://auth.login.yahoo.co.jp/yconnect/v1/authorization';
	const TOKEN_URI           = 'https://auth.login.yahoo.co.jp/yconnect/v1/token';
	const USERINFO_URI        = 'https://userinfo.yahooapis.jp/yconnect/v1/attribute';


	public function __construct($client_id, $client_secret) {
		$this->client_id     = $client_id;
		$this->client_secret = $client_secret;
	}

	public function authorization($redirect_uri,
	                              $response_type = 'code',
	                              $scope = 'openid profile email address') {
		$params = array(
			'response_type' => $response_type,
			'client_id'     => $this->client_id,
			'redirect_uri'  => $redirect_uri,
			'scope'         => $scope
		);

		$uri = self::AUTHORIZATION_URI . '?' . http_build_query($params, '', '&');
		header("Location: $uri");
	}

	public function token($code, $redirect_uri) {
		$params = array( 
			'grant_type'   => 'authorization_code',
			'code'         => $code,
			'redirect_uri' => $redirect_uri
		);

		$headers = array(
			'Content-type: application/x-www-form-urlencoded',
			'Authorization: Basic ' . base64_encode($this->client_id . ':' . $this->client_secret),
		);

		$response =  self::http_request(self::TOKEN_URI,
		                                'POST',
		                                $params,
		                                $headers);
		return json_decode($response, true);
	}

	public function userinfo($access_token) {
		$params = array(
			'schema' => 'openid'
		);

		$headers = array(
			'Authorization: Bearer ' . $access_token,
		);

		$response = self::http_request(self::USERINFO_URI,
		                               'GET',
		                               $params,
		                               $headers);
		return json_decode($response, true);
	}

	public static function http_request($uri,
	                                    $scheme,
	                                    $params,
	                                    $headers) {

		$query = http_build_query($params, '', '&');

		$ch = curl_init();

		if($scheme === 'GET') {
			curl_setopt($ch, CURLOPT_URL, $uri . '?' . $query);
		}
		else {
			curl_setopt($ch, CURLOPT_URL, $uri);
			curl_setopt($ch, CURLOPT_POST, true);
			curl_setopt($ch, CURLOPT_POSTFIELDS, $query);
		}
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

		$response = curl_exec($ch);
		curl_close ($ch);

		return $response;
	}
}
