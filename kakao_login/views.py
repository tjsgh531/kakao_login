from django.shortcuts import render, redirect

from django.conf import settings
import requests
from django.http import HttpResponse

kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"
kakao_token_uri = "https://kauth.kakao.com/oauth/token"
kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"

def home(request):
    return render(request, 'home.html')

def kakaoLogin(request):
    client_id = settings.KAKAO_CONFIG["REST_API_KEY"]
    redirect_uri = settings.KAKAO_CONFIG["CALLBACK"]

    #카카오톡 측에서 지정한 경로
    #code값을 request에 담아서 redirect uri 설정 경로로 줌
    uri = f"{kakao_login_uri}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    return redirect(uri) 

def kakaoCallback(request):
    code = request.GET["code"]

    if not code:
        return HttpResponse("코드가 제대로 안왔어요")

    # 아래 데이터를 kakao_token_url 로 POST해서 토큰을 얻을 거에요
    request_data = {
        'grant_type' : 'authorization_code',
        'client_id': settings.KAKAO_CONFIG["REST_API_KEY"],
        'redirect_uri' : settings.KAKAO_CONFIG["CALLBACK"],
        'client_secret' : settings.KAKAO_CONFIG["CLIENT_KEY"],
        'code': code
    }
    token_heders = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }

    #아래 token_res가 온전하게 받아 오면 kakao loin 성공
    token_res = requests.post(kakao_token_uri, data=request_data, headers=token_heders)

    token_json = token_res.json()

    #카카오톡 계정 정보를 얻기 위한 권한 token
    access_token = token_json.get('access_token')

    if not access_token:
        return HttpResponse("access_token이 없어 kakao 계정 데이터 받아 올 수가 없어")
    
    # 'Bearer ' 마지막 띄어쓰기 필수(카카오톡 측에서 지정한 형식)
    access_token = f"Bearer {access_token}"
    auth_headers = {
        "Authorization": access_token,
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    
    user_info_res = requests.get(kakao_profile_uri, headers=auth_headers)
    user_info_json = user_info_res.json()

    # 이메일 수신 동의가 안되어 있으면 아래 정보들을 들고 올 수 없음.
    # 카카오 계정에서 받아온 유저 정보
    user_info_json_id = user_info_json.get('id')
    social_type = 'kakao'
    social_id = f"{social_type}_{user_info_json_id}"
    
    kakao_account = user_info_json.get('kakao_account')
    
    if not kakao_account:
        return ("없엉")
    
    
    user_email = kakao_account.get('email')

    kakao_info = {
        'social_id' : social_id,
        'kakao_account' : kakao_account,     
    }
    
    return render(request, 'result.html', kakao_info)