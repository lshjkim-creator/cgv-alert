import os
import time
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"텔레그램 발송 실패: {e}")

def check_cgv():
    url = "https://www.cgv.co.kr/common/showtimes/iframeTheater.aspx"
    params = {
        "areacode": "01",
        "theaterCode": "0013", # 용산아이파크몰
        "date": "20260919"      # 9월 19일
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        html = response.text

        target_movie = "치이카와"
        
        if target_movie in html:
            msg = (
                "🚨 치이카와 예매 오픈!\n\n"
                "CGV 용산아이파크몰\n"
                "9/19 상영 회차가 확인되었습니다.\n\n"
                "지금 예매하세요!"
            )
            send_telegram(msg)
            print("예매 오픈 감지: 텔레그램 알림 발송 완료")
            return True
        else:
            print("아직 예매 미오픈...")
            return False

    except Exception as e:
        print(f"오류 발생: {e}")
        return False

if __name__ == "__main__":
    # GitHub Actions 한 번 실행 시 최대 30분 동안 1분마다 반복
    for i in range(30):
        print(f"[{i+1}/30] CGV 예매 여부 확인 중...")
        is_open = check_cgv()
        if is_open:
            break
        time.sleep(60) # 60초(1분) 대기

if __name__ == "__main__":
    check_cgv()
