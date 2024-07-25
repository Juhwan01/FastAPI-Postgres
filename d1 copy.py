import requests

# 사용자 설정 부분
API_KEY = 'jh4odot6b7'
API_SECRET = 'Qxp7PJEk3Vjt6blpBEDc8jVUoFh35KC9sEWhGYWN'

def geocode(address):
    url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode'
    params = {'query': address}
    headers = {
        'X-NCP-APIGW-API-KEY-ID': API_KEY,
        'X-NCP-APIGW-API-KEY': API_SECRET
    }
    
    response = requests.get(url, params=params, headers=headers)
    result = response.json()
    
    if result['status'] == 'OK':
        if result['addresses']:
            x = result['addresses'][0]['x']
            y = result['addresses'][0]['y']
            return f"{x},{y}"
    return None

# 사용자로부터 주소 입력 받기
start_address = input("출발지 주소를 입력하세요: ")
goal_address = input("도착지 주소를 입력하세요: ")

# 주소를 좌표로 변환
START_COORDINATES = geocode(start_address)
GOAL_COORDINATES = geocode(goal_address)

if START_COORDINATES is None or GOAL_COORDINATES is None:
    print("주소를 좌표로 변환하는데 실패했습니다.")
else:
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
            
            # 평균 속도를 60km/h로 가정하여 예상 소요 시간 계산
            avg_speed = 60  # km/h
            estimated_duration = (distance / 1000) / (avg_speed / 3600)  # 초 단위
            
            print(f"출발지: {start_address}")
            print(f"도착지: {goal_address}")
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