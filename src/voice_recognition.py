"""
음성 인식 모듈 - 음성 주문 처리 및 TTS
"""
import speech_recognition as sr
import pyttsx3
import pygame
import os
from config import MENU_DATA, VOICE_PROMPT_FILE

class VoiceRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = None
        self.init_tts()
        self.init_pygame()
        
        # 음성 명령 매핑
        self.create_voice_commands()
        
    def init_tts(self):
        """TTS 엔진 초기화"""
        try:
            self.tts_engine = pyttsx3.init()
            # TTS 설정
            voices = self.tts_engine.getProperty('voices')
            if voices:
                self.tts_engine.setProperty('voice', voices[0].id)
            self.tts_engine.setProperty('rate', 180)  # 말하기 속도
            self.tts_engine.setProperty('volume', 0.8)  # 음량
            print("TTS 엔진 초기화 완료")
        except Exception as e:
            print(f"TTS 초기화 오류: {e}")
            
    def init_pygame(self):
        """pygame 초기화 (mp3 재생용)"""
        try:
            pygame.mixer.init()
            print("pygame mixer 초기화 완료")
        except Exception as e:
            print(f"pygame 초기화 오류: {e}")
            
    def create_voice_commands(self):
        """음성 명령 매핑 생성"""
        self.voice_commands = {}
        
        # 각 메뉴에 대해 단품/세트 명령어 생성
        for menu_id, menu_info in MENU_DATA.items():
            menu_name = menu_info["name"]
            
            # 단품
            self.voice_commands[menu_name] = (menu_id, "single")
            self.voice_commands[menu_name + "단품"] = (menu_id, "single")
            
            # 세트
            self.voice_commands[menu_name + "세트"] = (menu_id, "set")
            self.voice_commands[menu_name + "셋트"] = (menu_id, "set")  # 발음 변형
            
        print(f"음성 명령어 {len(self.voice_commands)}개 생성 완료")
        
    def speak(self, text):
        """텍스트 음성 출력"""
        if not self.tts_engine:
            print(f"TTS: {text}")
            return
            
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS 오류: {e}")
            
    def play_voice_prompt(self):
        """미리 녹음된 음성 파일 재생"""
        try:
            if os.path.exists(VOICE_PROMPT_FILE):
                pygame.mixer.music.load(VOICE_PROMPT_FILE)
                pygame.mixer.music.play()
                
                # 재생 완료까지 대기
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                print("음성 프롬프트 재생 완료")
            else:
                print("음성 파일이 없어 TTS로 대체")
                self.speak("주문을 말해주세요")
        except Exception as e:
            print(f"음성 파일 재생 오류: {e}")
            self.speak("주문을 말해주세요")
    
    def process_voice_command(self, order_text):
        """음성 명령어 처리"""
        # 공백 제거 및 정규화
        order_text_clean = order_text.replace(" ", "").replace(".", "").replace(",", "")
        
        print(f"정규화된 음성: {order_text_clean}")
        
        # 직접 매칭 시도
        if order_text_clean in self.voice_commands:
            return self.voice_commands[order_text_clean]
            
        # 부분 매칭 시도
        for command, (menu_id, item_type) in self.voice_commands.items():
            if command in order_text_clean or order_text_clean in command:
                print(f"부분 매칭 성공: {command}")
                return menu_id, item_type
                
        print("매칭되는 메뉴를 찾을 수 없습니다.")
        return None, None
    
    def listen_for_order(self):
        """음성 주문 인식"""
        # 미리 녹음된 음성 재생
        self.play_voice_prompt()
        
        try:
            with sr.Microphone() as source:
                print("마이크 노이즈 조정 중...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("주문할 메뉴를 말해주세요!")
                
                # 음성 입력 대기
                audio = self.recognizer.listen(source, timeout=15, phrase_time_limit=10)
                
            print("음성을 분석하고 있습니다...")
            order_text = self.recognizer.recognize_google(audio, language='ko-KR')
            print(f"인식된 음성: {order_text}")
            
            return self.process_voice_command(order_text)
            
        except sr.WaitTimeoutError:
            self.speak("시간이 초과되었습니다. 다시 시도해주세요.")
            return None, None
        except sr.UnknownValueError:
            self.speak("음성을 인식할 수 없습니다. 다시 시도해주세요.")
            return None, None
        except sr.RequestError as e:
            print(f"음성 인식 서비스 오류: {e}")
            self.speak("음성 인식 서비스에 문제가 있습니다.")
            return None, None
        except Exception as e:
            print(f"음성 인식 오류: {e}")
            return None, None
            
    def test_microphone(self):
        """마이크 테스트"""
        try:
            with sr.Microphone() as source:
                print("마이크 테스트 중...")
                self.recognizer.adjust_for_ambient_noise(source)
                print("3초 동안 말해보세요:")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                
            text = self.recognizer.recognize_google(audio, language='ko-KR')
            print(f"테스트 결과: {text}")
            self.speak(f"다음과 같이 인식되었습니다: {text}")
            return True
            
        except Exception as e:
            print(f"마이크 테스트 실패: {e}")
            return False
