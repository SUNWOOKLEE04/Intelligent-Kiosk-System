# 🏆 ICT Convergence Hackathon - Intelligent Kiosk System

**6th ICT Convergence Hackathon - Design Excellence Award (2021)**  
*High School Project - Team Leader & UX Strategy Director*

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logobadge/opencv-%23white.svg?style=for-the-badge&logo=opencvbadge/tkinter-FF6B35?style=for-the-badge&logo 개요

이 프로젝트는 **2021년 제6회 ICT융합 해커톤**에서 **디자인 우수상**을 수상한 시각장애인을 위한 지능형 키오스크 시스템입니다. 고등학교 재학 중 팀 리더로 참여하여 개발한 프로젝트로, 접근성과 사용자 경험에 중점을 둔 혁신적인 솔루션입니다.

### 🎯 프로젝트 목적
- **디지털 접근성 향상**: 시각장애인도 쉽게 사용할 수 있는 키오스크
- **사회적 가치 창출**: 디지털 소외계층의 편의성 증대
- **기술적 혁신**: AI 기반 음성인식과 얼굴인식 기술 융합

## ⭐ 주요 성과

- **🏆 제6회 ICT융합 해커톤 디자인 우수상 수상**
- **👥 팀 리더 & UX 전략 디렉터** 역할 수행
- **🤝 디자인-개발-기획 팀 통합 관리** 경험
- **♿ 접근성 중심의 UI/UX 설계** 완성

## 🚀 주요 기능

### 🎤 **음성 인식 시스템**
```python
# 음성 주문 처리
def listen_for_order(self):
    """미리 녹음된 안내음성과 실시간 음성인식으로 주문 처리"""
    self.play_voice_prompt()  # "주문을 말해주세요" 음성 재생
    # Google Speech Recognition API 활용
```

### 👁️ **얼굴 인식 & 나이 예측**
```python
# OpenCV DNN 모델을 활용한 연령대별 맞춤 추천
AGE_RECOMMENDATIONS = {
    "(0~2)": "맥모닝",
    "(15~20)": "상하이버거세트", 
    "(25~32)": "빅맥세트",
    # ... 연령대별 개인화된 메뉴 추천
}
```

### ♿ **시각장애인 접근성 지원**
- **TTS(Text-to-Speech)**: 모든 메뉴와 가격 정보 음성 안내
- **대형 폰트 지원**: 저시력자를 위한 가변 폰트 크기
- **고대비 UI**: 명확한 색상 대비로 가독성 향상
- **키보드 네비게이션**: 마우스 없이도 전체 기능 이용 가능

### 🛒 **스마트 주문 관리**
- Excel 기반 주문내역 자동 저장
- 실시간 주문 집계 및 가격 계산
- 주문 수정/취소 기능

## 🛠️ 기술 스택

| 분야 | 기술 |
|------|------|
| **AI/ML** | OpenCV DNN, Google Speech Recognition |
| **GUI** | Python Tkinter, PIL/Pillow |
| **음성처리** | pyttsx3, pygame, speech_recognition |
| **데이터** | pandas, openpyxl |
| **언어** | Python 3.x |

## 📁 프로젝트 구조

```
PYTHONPROJECT/
├── src/
│   ├── config.py              # 메뉴 데이터 및 설정
│   ├── main_app.py           # 메인 GUI 애플리케이션
│   ├── face_detector.py      # 얼굴인식 & 나이예측 모듈
│   ├── voice_recognition.py  # 음성인식 & TTS 모듈
│   └── order_manager.py      # 주문관리 시스템
├── models/                   # OpenCV DNN 모델 파일
├── images/                   # 메뉴 이미지 리소스
├── voice.mp3                # 음성 안내 파일
├── requirements.txt
└── README.md
```

## ⚡ 빠른 시작

### 1. 환경 설정
```bash
git clone https://github.com/your-username/ict-hackathon-kiosk.git
cd ict-hackathon-kiosk
pip install -r requirements.txt
```

### 2. 모델 파일 준비
OpenCV DNN 모델 파일들을 `models/` 폴더에 배치:
- `opencv_face_detector.pbtxt`
- `opencv_face_detector_uint8.pb`  
- `age_deploy.prototxt`
- `age_net.caffemodel`

### 3. 실행
```bash
python src/main_app.py
```

## 🎮 사용법

1. **얼굴 인식 시작**: 카메라로 연령대 감지 후 맞춤 메뉴 추천
2. **음성 주문**: "빅맥세트 주세요" 같은 자연스러운 음성으로 주문
3. **접근성 모드**: 키보드만으로 모든 기능 이용 가능
4. **주문 완료**: Excel 파일로 주문내역 자동 저장

## ⚠️ 프로젝트 상태 및 고려사항

### 🎓 **고등학교 프로젝트 배경**
이 프로젝트는 **2021년 고등학교 재학 중** 개발한 것으로, 다음과 같은 특징이 있습니다:

- **교육적 목적**: 학습 과정에서 개발된 프로토타입
- **시간 제약**: 해커톤 대회 기간 내 완성된 MVP
- **코드 구조**: 상용 수준 대비 개선 여지 존재

### 🔧 **현재 코드 상태**
```python
# ⚠️ 일부 코드는 고등학교 시절 작성으로 개선이 필요할 수 있습니다
# ✅ 핵심 기능은 정상 동작하며, 접근성 요구사항을 충족합니다
# 🔄 필요시 리팩토링하여 사용하시기 바랍니다
```

### 📈 **개선 권장사항**
- [ ] 모듈 구조 최적화
- [ ] 예외 처리 강화  
- [ ] 코드 문서화 개선
- [ ] 테스트 코드 추가
- [ ] 성능 최적화

## 🤝 기여 및 활용

### 💡 **자유로운 활용**
```
이 프로젝트는 학습 및 연구 목적으로 자유롭게 사용하실 수 있습니다.
개선사항이나 버그 발견 시 이슈 등록 및 PR을 환영합니다!
```

### 🎯 **활용 가능 분야**
- 접근성 연구 프로젝트
- 음성인식 시스템 학습
- OpenCV 얼굴인식 예제
- 키오스크 UI/UX 참고자료

## 📞 연락처

- **GitHub**: [@your-username](https://github.com/your-username)
- **Email**: your.email@example.com


---

*"2021년 고등학생의 도전정신과 혁신이 담긴 프로젝트입니다. 완벽하지 않을 수 있지만, 접근성에 대한 진정한 고민이 녹아있습니다. 필요하시면 가져가서 더 발전시켜 주세요!"* 🚀

**⭐ Star를 눌러주시면 큰 힘이 됩니다!**

---
