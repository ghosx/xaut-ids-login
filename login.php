<?php
	$cookie_file = dirname(__FILE__).'\cookie.txt';
	function get_data(){
		global $cookie_file;
		$url = 'http://ids.xaut.edu.cn/authserver/login?service=http%3A%2F%2Fmy.xaut.edu.cn%2Flogin.portal';
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL,$url);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_HEADER, 1);
		curl_setopt($ch, CURLOPT_COOKIEJAR, $cookie_file);
		$output = curl_exec($ch);
		curl_close($ch);
		preg_match('<input type="hidden" name="lt" value="(\S+)" />', $output, $match);
		$lt = $match[1];
		preg_match('<input type="hidden" name="execution" value="(\S+)" />', $output ,$match);
		$execution = $match[1];
		$_eventId = 'submit';
		return array($lt,$execution,$_eventId);
	}

	function login($username,$password){
		//第一次302跳转 获取ticket
		global $cookie_file;
		$url = 'http://ids.xaut.edu.cn/authserver/login?service=http://my.xaut.edu.cn/login.portal';
		$arr = array(
				'Host:ids.xaut.edu.cn',
				'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
				'Accept-Language:zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
				'Accept-Encoding:gzip, deflate',
				'Content-Type:application/x-www-form-urlencoded',
				'Referer:http://ids.xaut.edu.cn/authserver/login?service=http://my.xaut.edu.cn/login.portal',
				'Connection:keep-alive',
				'Upgrade-Insecure-Requests:1');
		$inf = get_data();
		$post_data = "username=".$username."&password=".$password."&lt=$inf[0]&execution=$inf[1]&_eventId=$inf[2]";
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $url);
		curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 0);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_POST, 1);
		curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
		curl_setopt($ch, CURLOPT_HEADER, 1);
		curl_setopt($ch, CURLOPT_HTTPHEADER, $arr);
		curl_setopt($ch, CURLOPT_COOKIEFILE, $cookie_file);
		$data = curl_exec($ch);
		curl_close($ch);
		preg_match('/Location:([^;]*)\nC/', $data, $match);
		return $match[1];
	}



	function go($url){
		//第二次302跳转获取cookie及location
		$ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_HEADER, true);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 10);
		$data = curl_exec($ch);
		curl_close($ch);
		preg_match_all("/Set\-Cookie:([^;]*);/", $data, $match);
		$cookie = substr($match[1][0], 1);
		preg_match('/Location:([^;]*)\nC/', $data, $match);
		$Location = trim($match[1]);
		$arr = array(
            'Host: my.xaut.edu.cn',
            'Connection: keep-alive',
            'Upgrade-Insecure-Requests: 1',
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0' ,
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'DNT: 1',
            'Accept-Encoding: gzip, deflate',
            'Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.6,ko;q=0.4,ja;q=0.2,en;q=0.2,en-US;q=0.2',
            'Cookie:'.$cookie,
        );

		$ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $Location);
        curl_setopt($ch, CURLOPT_HEADER, 0);
        curl_setopt($ch, CURLOPT_NOBODY, false);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'GET' );
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $arr);
        curl_setopt($ch, CURLOPT_TIMEOUT, 10);
        $data = curl_exec($ch);
        print_r($data);
	}

$User = 'XXX';
$PassWd = 'XXX';

$ticket = login($User,$PassWd);
go(trim($ticket));

?>
