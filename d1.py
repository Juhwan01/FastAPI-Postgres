import requests

# 사용자 설정 부분
API_KEY = 'jh4odot6b7'
API_SECRET = 'Qxp7PJEk3Vjt6blpBEDc8jVUoFh35KC9sEWhGYWN'

START_COORDINATES = '129.0756,35.1798'  # 부산 시청의 좌표 (경도, 위도)
GOAL_COORDINATES = '129.0588,35.2325'  # 금정 구청의 좌표 (경도, 위도)

# 요청 URL 설정
url = f'https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving?start={START_COORDINATES}&goal={GOAL_COORDINATES}'

headers = {
    'X-NCP-APIGW-API-KEY-ID': API_KEY,
    'X-NCP-APIGW-API-KEY': API_SECRET
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    
    if data['code'] == 0:
        route = data['route']['traoptimal'][0]
        summary = route['summary']
        
        distance = summary['distance']  # 거리 (미터 단위)
        api_duration = summary['duration']  # API에서 제공하는 시간 (초 단위)
        
        # 평균 속도를 40km/h로 가정하여 예상 소요 시간 계산
        avg_speed = 60  # km/h
        estimated_duration = (distance / 1000) / (avg_speed / 3600)  # 초 단위
        
        print(f"출발지: {START_COORDINATES}")
        print(f"도착지: {GOAL_COORDINATES}")
        print(f"총 거리: {distance} 미터")
        print(f"API 제공 시간: {api_duration} 초")
        
        # 예상 소요 시간 (계산된 값)
        hours, remainder = divmod(int(estimated_duration), 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"예상 소요 시간 (평균 속도 60km/h 기준): {hours}시간 {minutes}분 {seconds}초")
    else:
        print(f"API 오류: {data['message']}")
else:
    print(f"HTTP 요청 오류: {response.status_code}")
    print("오류 응답:", response.text)