<이론>

기본적을 kakao login을 하고 인증 되었음을 증명하는 토큰을 얻는 것이 목표이다.

토큰에을 얻기 위해서는 
① REST_API_KEY
② redirect_uri
③ CLIENT_KEY
④ code
가 필요하다

1~3은 앱을 등록 하는 과정에서 얻을 수 있고
4번 같은 경우 특정경로로 redirect를 요청하면
redirect_uri 에 설정 경로에 request에 값을 담아서 redirect한다

즉, token을 얻으면 kakao login에 성공 한 것이고 그 token을 이용하여 kakao 계정에 저장된 데이터를 사용 할 수 있다.

------------------------------------------------------------------------------------------------------------------------
<실습 과정>

1. 기본 장고 환경 설정
    1-1 가상환경
    1-2 장고 설치
    1-3 project 생성
    1-4 app생성
    1-5 settings.py 등록
    1-6 migrate

2. kakao develop에 앱등록
    https://developers.kakao.com
    
    2-1 앱 생성
        내 애플리케이션 > 애플리케이션 추가하기
        앱 이름과 사업자 명(+ 앱 이미지) 입력 공간이 나오는데 로그인 시 client에게 보여주는 것들 (앱 설정과는 무관)
    
    2-2 플랫폼 설정하기
        - 내 애플리케이션 > 앱 설정 > 요약 정보 에서 <플랫폼> 구간에서 '플랫폼 설정하기' 클릭!
        - <Web> 구간에서 "Web 플랫폼 등록" 클릭!
        - http://localhost:8000 으로 등록 ("사이트의 특정 도메인 있어도 걍 이걸로 등록 해요 ")
    
    2-3 Redirect URI 등록하기 (내 애플리케이션 > 제품 설정 > 카카오 로그인)
        - 플랫폼 설정을 완료하면 그 아랫 부분에 
          '카카오 로그인 사용 시 Redirect URI를 등록해야 합니다. 등록하러 가기'
          클릭!!!
        - 활성화 설정 상태 ON(활성화)으로 변경
        - <Redirect URI> 구간에서 "Redirect URI 등록" 클릭!!!
        - urls.py 설정 + 장고 앱 생성시 앱 이름에 따라 다르게 설정해야해요.
            로그인 확인 토큰을 주는 url이라고 생각하시면 좋아요
            ex) http://localhost:8000/kakao_login/callback/
                http://localhost:8000/앱 이름/callback/ => 형식으로 적어주면 될 듯요.

    2-4 Client code 생성
        - 내 애플리케이션 > 제품 설정 > 카카오 로그인 > 보안
        - "코드 생성" 클릭!!!
        ps) 활성화 상태 '사용 안함' 해도 무관(오히려 추천)

    2-5 email 수신 동의(선택)
        - 이거 안하면 kakao_id, email, kakao_acount등의 정보는 들고 올 수 없음
        - "내 애플리케이션 > 제품 설정 > 카카오 로그인 > 동의 항목"에 들어가면 여러가지 동의 항목 설정 가능
        - <카카오 계정(이메일)> 부분 만큼은 선택동의로 바꾸기
        - 이거 안하고 token만 확인도 가능하니 안 하실 분들은 views.py에서 카카오 계정 데이터 들고오는 부분 빼주셔야 해요. 

3. 필요 데이터 settings.py에 저장
    > settings.py에 다음과 같은 형식으로 입력
    
    KAKAO_CONFIG ={
        "REST_API_KEY" : 'abc4cp627e112205636a195cc84925e1',
        "CALLBACK" : 'http://localhost:8000/kakao_login/callback/',
        "CLIENT_KEY" : "8TzkUJovtVRcAucSmn5XRUhBg5XauZET"
    }
    (나름 보안을 위해 형식만 맞추고 이상한 값을 넣었습니다)

    "REST_API_KEY" 는 "내 애플리케이션 > 앱 설정 > 앱 키" 에 가면 REST API 키 가 있어요. 그 값을 넣어 주세요.
    "CALLBACK"은 "내 애플리케이션 > 제품 설정 > 카카오 로그인"에서 Redirect URI 설정한 값을 넣어주세요.
    "CLIENT_KEY"는 "내 애플리케이션 > 제품 설정 > 카카오 로그인 > 보안"에서 생성한 코드 값을 넣어주세요.

4. urls.py 설정
    - project urls.py 에는 앱으로 연결 했습니다.
        urlpatterns = [
            path('admin/', admin.site.urls),
            path('kakao_login/', include('kakao_login.urls')) 
        ]

    - 앱(여기서는 kakao_login)에서 urls.py
        urlpatterns = [
            path('home/', views.home, name="home"),
            path('login/', views.kakaoLogin, name="kakaoLogin"),
            path('callback/', views.kakaoCallback, name="kakaoCallback"),
        ]
        
        - home : 카카오 로그인 버튼이 있는 페이지
        - login : 카카오톡 아이디 비번 입력하는 페이지
        - callback : token 주는 페이지

5. views.py 설정
    + pip install requests 
    : kakao uri에 데이터를 요청하기(get, post 등의 가능)위한 툴

    복잡스 하니깐 파일 보세요

