"""
설정 파일 - 메뉴 데이터, 모델 경로, 상수 정의
"""
import os

# 햄버거 메뉴 데이터
MENU_DATA = {
    1: {"name": "새우버거", "single_price": 5, "set_price": 6, "image": "새우버거 (Small) (Custom).png"},
    2: {"name": "치즈버거", "single_price": 5, "set_price": 6, "image": "치즈버거 (Small) (Custom).png"},
    3: {"name": "치킨버거", "single_price": 5, "set_price": 6, "image": "맥치킨 (Small) (Custom).png"},
    4: {"name": "빅맥", "single_price": 5, "set_price": 6, "image": "빅맥-removebg-preview (Small) (Custom).png"},
    5: {"name": "불고기버거", "single_price": 4, "set_price": 5, "image": "불고기버거-removebg-preview (Small) (Custom).png"},
    6: {"name": "햄버거", "single_price": 4, "set_price": 5, "image": None},
    7: {"name": "상하이버거", "single_price": 6, "set_price": 7, "image": "맥스파이시_상하이 (Small) (Custom).png"},
    8: {"name": "쿼터파운더치즈", "single_price": 7, "set_price": 8, "image": "쿼터파운더_치즈 (Small) (Custom).png"},
    9: {"name": "맥모닝", "single_price": 4, "set_price": 5, "image": "맥모닝-removebg-preview (Small) (Custom).png"},
    10: {"name": "치킨치즈버거", "single_price": 6, "set_price": 7, "image": "맥치킨_치즈 (Small) (Custom).png"},
    11: {"name": "더블불고기버거", "single_price": 6, "set_price": 7, "image": None},
    12: {"name": "더블쿼터파운더치즈", "single_price": 8, "set_price": 9, "image": None},
}

# 연령대별 추천 메뉴
AGE_RECOMMENDATIONS = {
    "(0~2)": "맥모닝",
    "(4~6)": "맥모닝", 
    "(8~12)": "불고기버거",
    "(15~20)": "상하이버거세트",
    "(25~32)": "빅맥세트",
    "(38~43)": "빅맥세트",
    "(48~53)": "쿼터파운더치즈",
    "(60~100)": "불고기버거세트"
}

# OpenCV 모델 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
IMAGES_DIR = os.path.join(BASE_DIR, "images")

FACE_PROTO = os.path.join(MODELS_DIR, "opencv_face_detector.pbtxt")
FACE_MODEL = os.path.join(MODELS_DIR, "opencv_face_detector_uint8.pb")
AGE_PROTO = os.path.join(MODELS_DIR, "age_deploy.prototxt")
AGE_MODEL = os.path.join(MODELS_DIR, "age_net.caffemodel")

# 모델 설정
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
AGE_LIST = ['(0~2)', '(4~6)', '(8~12)', '(15~20)', '(25~32)', '(38~43)', '(48~53)', '(60~100)']

# 음성 파일 경로
VOICE_PROMPT_FILE = os.path.join(BASE_DIR, "voice.mp3")
