import os
import requests

# GitHub Secrets에서 환경 변수로 가져오기
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

def check_cgv():
    # CGV 홍대(0013) 스케줄 조회 URL
    url = "https://www.cgv.co.kr/common/showtimes/iframeTheater.aspx"
    params = {
        "areacode": "01",
        "theaterCode": "0013", # 홍대
        "date": "20260919"      # 9월 19일
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        html = response.text

        # 영화명 존재 여부 확인 (극장판 치이카와: 인어섬의 비밀)
        target_movie = "치이카와"
        
        if target_movie in html:
            msg = (
                "🚨 치이카와 예매 오픈!\n\n"
                "CGV 홍대\n"
                "9/19 상영 회차가 확인되었습니다.\n\n"
                "지금 예매하세요!"
            )
            send_telegram(msg)
            print("예매 오픈 감지: 텔레그램 알림 발송 완료")
        else:
            print("아직 예매가 오픈되지 않았습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    check_cgv()