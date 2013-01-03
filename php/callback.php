<?php
	include_once 'YConnect.php';

	$client_id     = '<your client_id>';
	$client_secret = '<your client_sercret>';

	$redirect_uri  = '<your redirect_uri>';

	$yconnect = new YConnect($client_id, $client_secret);

	if (!array_key_exists('code', $_GET) || empty($_GET['code'])) {
		// 1) Authorization Request
		$yconnect->authorization($redirect_uri);
		exit;
	
	}
	else {
		// 2) Access Token Request and UserInfo Request 
		$code = $_GET['code'];

		$response = $yconnect->token($code, $redirect_uri);
		$access_token =  $response['access_token'];

		$response = $yconnect->userinfo($access_token);

		echo '<html><meta charset="UTF-8"><body><pre>';
		var_dump($response);
		echo '</pre></body></html>';
	}
