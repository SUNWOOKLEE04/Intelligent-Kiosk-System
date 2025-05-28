"""
메인 애플리케이션 - GUI 및 전체 시스템 통합
"""
import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Button, Frame
import tkinter.font as font
from PIL import Image, ImageTk
import os
import threading

from order_manager import OrderManager
from face_detector import FaceDetector
from voice_recognition import VoiceRecognizer
from config import MENU_DATA, AGE_RECOMMENDATIONS, IMAGES_DIR

class FastFoodOrderApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KFE - 스마트 주문 키오스크")
        self.root.geometry("1536x864")
        self.root.configure(bg='white')
        
        # 시스템 구성요소 초기화
        self.order_manager = OrderManager()
        self.face_detector = FaceDetector()
        self.voice_recognizer = VoiceRecognizer()
        
        # UI 관련 변수
        self.font_size = 18
        self.current_menu_window = None
        self.current_order_window = None
        self.order_labels = {}  # 주문 개수 표시 라벨들
        
        # 키오스크 모드 설정
        self.kiosk_mode = False
        self.auto_reset_timer = None
        
        self.setup_main_screen()
        
    def setup_main_screen(self):
        """메인 화면 설정"""
        # 기존 위젯 제거
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # 타이틀
        title_label = Label(self.root, text="🍔 KFE 스마트 주문 키오스크", 
                           bg="white", fg="#FF6B35", font=('Arial', 40, 'bold'))
        title_label.place(x=400, y=100)
        
        # 서브 타이틀
        subtitle_label = Label(self.root, text="얼굴 인식으로 맞춤 메뉴를 추천받으세요!", 
                             bg="white", fg="#333", font=('Arial', 18))
        subtitle_label.place(x=500, y=180)
        
        # 얼굴 인식 시작 버튼
        face_button = Button(self.root, text="🎯 얼굴 인식으로 시작", 
                           command=self.start_face_detection,
                           bg="#FF6B35", fg="white", font=('Arial', 20, 'bold'),
                           width=20, height=2, relief="raised", bd=3)
        face_button.place(x=600, y=300)
        
        # 직접 주문 버튼
        direct_button = Button(self.root, text="📱 직접 주문하기", 
                             command=self.show_menu,
                             bg="#4A90E2", fg="white", font=('Arial', 20, 'bold'),
                             width=20, height=2, relief="raised", bd=3)
        direct_button.place(x=600, y=400)
        
        # 음성 테스트 버튼
        voice_test_button = Button(self.root, text="🎤 음성 테스트", 
                                 command=self.test_voice,
                                 bg="#7ED321", fg="white", font=('Arial', 16),
                                 width=15, height=1)
        voice_test_button.place(x=650, y=500)
        
        # 관리자 메뉴 (숨겨진 버튼)
        admin_button = Button(self.root, text="관리자", 
                            command=self.admin_menu,
                            bg="gray", fg="white", font=('Arial', 10),
                            width=8, height=1)
        admin_button.place(x=10, y=10)
        
        # 종료 버튼
        quit_button = Button(self.root, text="❌ 프로그램 종료", 
                           command=self.quit_app,
                           bg="#FF4757", fg="white", font=('Arial', 15),
                           width=15, height=1)
        quit_button.place(x=1350, y=800)
        
        # 자동 초기화 타이머 시작 (키오스크 모드)
        if self.kiosk_mode:
            self.start_auto_reset_timer()
            
    def start_face_detection(self):
        """얼굴 인식 시작"""
        def face_detection_thread():
            try:
                # 여러 카메라 소스 시도
                camera_sources = [0, 1, 2]
                camera_initialized = False
                
                for source in camera_sources:
                    if self.face_detector.initialize_camera(source):
                        print(f"카메라 {source} 초기화 성공")
                        camera_initialized = True
                        break
                        
                if not camera_initialized:
                    self.root.after(0, lambda: messagebox.showerror("오류", "사용 가능한 카메라를 찾을 수 없습니다."))
                    return
                    
                age = self.face_detector.detect_age_from_camera()
                self.face_detector.release()
                
                if age:
                    self.root.after(0, lambda: self.show_age_recommendation(age))
                else:
                    self.root.after(0, lambda: messagebox.showinfo("알림", "얼굴을 감지할 수 없습니다.\n직접 주문해주세요."))
                    
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("오류", f"얼굴 인식 중 오류 발생: {e}"))
        
        # 별도 스레드에서 실행
        thread = threading.Thread(target=face_detection_thread)
        thread.daemon = True
        thread.start()
        
    def show_age_recommendation(self, age):
        """연령대별 추천 메뉴 표시"""
        if age in AGE_RECOMMENDATIONS:
            recommendation = AGE_RECOMMENDATIONS[age]
            
            # 연령대에 따른 폰트 크기 조정
            font_size = 25 if age in ["(48~53)", "(60~100)", "(38~43)"] else 18
            self.font_size = font_size
            
            # 추천 창 생성
            recommend_window = Toplevel(self.root)
            recommend_window.title("🎯 개인 맞춤 메뉴 추천")
            recommend_window.geometry("700x400")
            recommend_window.configure(bg='#F8F9FA')
            recommend_window.transient(self.root)
            recommend_window.grab_set()
            
            # 추천 텍스트
            recommend_text = f"{age}세 고객님의\n추천 메뉴는 '{recommendation}' 입니다!"
            
            # 아이콘과 텍스트
            icon_label = Label(recommend_window, text="🎯", font=('Arial', 50), bg='#F8F9FA')
            icon_label.pack(pady=20)
            
            text_label = Label(recommend_window, text=recommend_text, 
                             font=('Arial', font_size, 'bold'), wraplength=600,
                             bg='#F8F9FA', fg='#2C3E50')
            text_label.pack(pady=20)
            
            # 음성 안내
            def speak_recommendation():
                self.voice_recognizer.speak(recommend_text)
                self.voice_recognizer.speak("메뉴 보기 버튼을 눌러서 주문하세요.")
                
            speak_thread = threading.Thread(target=speak_recommendation)
            speak_thread.daemon = True
            speak_thread.start()
            
            # 버튼 프레임
            button_frame = Frame(recommend_window, bg='#F8F9FA')
            button_frame.pack(pady=30)
            
            # 메뉴로 이동 버튼
            menu_button = Button(button_frame, text="📱 메뉴 보기", 
                               command=lambda: [recommend_window.destroy(), self.show_menu()],
                               bg="#4A90E2", fg="white", font=('Arial', 18, 'bold'),
                               width=15, height=2, relief="raised", bd=3)
            menu_button.pack(side=tk.LEFT, padx=10)
            
            # 다시 추천 받기 버튼
            retry_button = Button(button_frame, text="🔄 다시 추천", 
                                command=lambda: [recommend_window.destroy(), self.start_face_detection()],
                                bg="#FF6B35", fg="white", font=('Arial', 18, 'bold'),
                                width=15, height=2, relief="raised", bd=3)
            retry_button.pack(side=tk.LEFT, padx=10)
            
    def show_menu(self):
        """메뉴 화면 표시"""
        if self.current_menu_window:
            self.current_menu_window.destroy()
            
        self.current_menu_window = Toplevel(self.root)
        self.current_menu_window.title("🍔 메뉴 선택")
        self.current_menu_window.geometry("1536x864")
        self.current_menu_window.configure(bg='white')
        self.current_menu_window.transient(self.root)
        
        # 헤더
        header_frame = Frame(self.current_menu_window, bg='#FF6B35', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = Label(header_frame, text="🍔 메뉴를 선택해주세요", 
                          bg='#FF6B35', fg='white', font=('Arial', 28, 'bold'))
        title_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # 메뉴 컨테이너
        menu_frame = Frame(self.current_menu_window, bg='white')
        menu_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # 메뉴 그리드 생성
        row = 0
        col = 0
        for menu_id, menu_info in MENU_DATA.items():
            if col >= 4:  # 한 줄에 4개
                row += 1
                col = 0
                
            # 메뉴 아이템 프레임
            item_frame = Frame(menu_frame, bg='white', relief='ridge', bd=2)
            item_frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
            
            # 이미지 로드
            self.load_menu_image(item_frame, menu_info, menu_id)
            
            # 메뉴 이름
            name_label = Label(item_frame, text=menu_info["name"],
                             bg="white", fg="#2C3E50", font=('Arial', self.font_size, 'bold'))
            name_label.pack(pady=(5, 0))
            
            # 가격 정보
            price_text = f"단품: {menu_info['single_price']}$ | 세트: {menu_info['set_price']}$"
            price_label = Label(item_frame, text=price_text,
                              bg="white", fg="#27AE60", font=('Arial', 12, 'bold'))
            price_label.pack()
            
            # 주문 버튼
            order_button = Button(item_frame, text="주문하기",
                                command=lambda mid=menu_id: self.show_order_detail(mid),
                                bg="#4A90E2", fg="white", font=('Arial', 14, 'bold'),
                                width=12, height=1, relief="raised", bd=2)
            order_button.pack(pady=5)
            
            col += 1
            
        # 그리드 가중치 설정
        for i in range(4):
            menu_frame.grid_columnconfigure(i, weight=1)
        for i in range(3):
            menu_frame.grid_rowconfigure(i, weight=1)
            
        # 하단 버튼 프레임
        bottom_frame = Frame(self.current_menu_window, bg='#F8F9FA', height=100)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)
        bottom_frame.pack_propagate(False)
        
        # 음성 주문 버튼
        voice_button = Button(bottom_frame, text="🎤 음성으로 주문하기", 
                            command=self.voice_order,
                            bg="#7ED321", fg="white", font=('Arial', self.font_size),
                            width=20, height=2, relief="raised", bd=3)
        voice_button.place(x=100, y=25)
        
        # 주문 완료 버튼
        if not self.order_manager.is_empty():
            order_complete_button = Button(bottom_frame, text=f"🛒 주문 완료 (총 {self.order_manager.total_price}$)", 
                                         command=self.finalize_order,
                                         bg="#E74C3C", fg="white", font=('Arial', self.font_size, 'bold'),
                                         width=25, height=2, relief="raised", bd=3)
            order_complete_button.place(x=600, y=25)
            
        # 뒤로 가기 버튼
        back_button = Button(bottom_frame, text="⬅️ 처음으로", 
                           command=lambda: [self.current_menu_window.destroy(), self.setup_main_screen()],
                           bg="#95A5A6", fg="white", font=('Arial', 16),
                           width=15, height=2)
        back_button.place(x=1200, y=25)
        
    def load_menu_image(self, parent, menu_info, menu_id):
        """메뉴 이미지 로드"""
        image_path = None
        
        if menu_info["image"]:
            # config에서 지정된 이미지 파일
            image_path = os.path.join(IMAGES_DIR, menu_info["image"])
            if not os.path.exists(image_path):
                # 현재 디렉토리에서 찾기
                image_path = menu_info["image"]
                if not os.path.exists(image_path):
                    image_path = None
        
        try:
            if image_path and os.path.exists(image_path):
                image = Image.open(image_path)
                image = image.resize((150, 120), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                img_label = Label(parent, image=photo, bg="white", relief='sunken', bd=1)
                img_label.image = photo  # 참조 유지
                img_label.pack(pady=10)
            else:
                # 이미지가 없을 경우 텍스트 대체
                placeholder = Label(parent, text="🍔", font=('Arial', 40), 
                                  bg="lightgray", width=8, height=3, relief='sunken', bd=1)
                placeholder.pack(pady=10)
                
        except Exception as e:
            print(f"이미지 로드 오류 ({menu_info.get('image', 'None')}): {e}")
            # 오류 시 기본 아이콘 표시
            placeholder = Label(parent, text="🍔", font=('Arial', 40), 
                              bg="lightgray", width=8, height=3, relief='sunken', bd=1)
            placeholder.pack(pady=10)
            
    def show_order_detail(self, menu_id):
        """주문 상세 창 표시"""
        if self.current_order_window:
            self.current_order_window.destroy()
            
        menu_info = MENU_DATA[menu_id]
        
        self.current_order_window = Toplevel(self.current_menu_window)
        self.current_order_window.title(f"🍔 {menu_info['name']} 주문")
        self.current_order_window.geometry("600x500")
        self.current_order_window.configure(bg='#F8F9FA')
        self.current_order_window.transient(self.current_menu_window)
        self.current_order_window.grab_set()
        
        # 헤더
        header_frame = Frame(self.current_order_window, bg='#4A90E2', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = Label(header_frame, text=f"🍔 {menu_info['name']}", 
                          bg='#4A90E2', fg='white', font=('Arial', 24, 'bold'))
        title_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # 메인 컨텐츠
        content_frame = Frame(self.current_order_window, bg='#F8F9FA')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # 단품 섹션
        self.create_order_section(content_frame, menu_id, "single", 
                                "🍔 단품", menu_info['single_price'], 0)
        
        # 구분선
        separator = Frame(content_frame, height=2, bg="#BDC3C7")
        separator.pack(fill=tk.X, pady=20)
        
        # 세트 섹션
        self.create_order_section(content_frame, menu_id, "set", 
                                "🍟 세트", menu_info['set_price'], 1)
        
        # 현재 총 주문 금액
        self.total_label = Label(content_frame, 
                               text=f"💰 총 주문 금액: {self.order_manager.total_price}$",
                               font=('Arial', 18, 'bold'), fg="#E74C3C", bg='#F8F9FA')
        self.total_label.pack(pady=20)
        
        # 버튼 프레임
        button_frame = Frame(content_frame, bg='#F8F9FA')
        button_frame.pack(pady=20)
        
        # 계속 쇼핑 버튼
        continue_button = Button(button_frame, text="🛍️ 계속 쇼핑", 
                               command=self.current_order_window.destroy,
                               bg="#95A5A6", fg="white", font=('Arial', 14),
                               width=12, height=2)
        continue_button.pack(side=tk.LEFT, padx=10)
        
        # 주문 완료 버튼 (주문이 있을 때만)
        if not self.order_manager.is_empty():
            complete_button = Button(button_frame, text="✅ 주문 완료", 
                                   command=self.finalize_order,
                                   bg="#27AE60", fg="white", font=('Arial', 14, 'bold'),
                                   width=12, height=2)
            complete_button.pack(side=tk.LEFT, padx=10)
        
    def create_order_section(self, parent, menu_id, item_type, type_name, price, row):
        """주문 섹션 생성"""
        section_frame = Frame(parent, bg='white', relief='ridge', bd=1, padx=20, pady=15)
        section_frame.pack(fill=tk.X, pady=10)
        
        # 타입과 가격
        info_frame = Frame(section_frame, bg='white')
        info_frame.pack(fill=tk.X)
        
        type_label = Label(info_frame, text=type_name, 
                         font=('Arial', 18, 'bold'), bg='white', fg='#2C3E50')
        type_label.pack(side=tk.LEFT)
        
        price_label = Label(info_frame, text=f"{price}$", 
                          font=('Arial', 18, 'bold'), bg='white', fg='#27AE60')
        price_label.pack(side=tk.RIGHT)
        
        # 주문 조작 프레임
        order_frame = Frame(section_frame, bg='white')
        order_frame.pack(fill=tk.X, pady=10)
        
        # 빼기 버튼
        minus_button = Button(order_frame, text="➖", 
                            command=lambda: self.remove_from_order(menu_id, item_type),
                            bg="#E74C3C", fg="white", font=('Arial', 16, 'bold'),
                            width=3, height=1)
        minus_button.pack(side=tk.LEFT)
        
        # 수량 표시
        count_key = f"{menu_id}_{item_type}"
        current_count = self.order_manager.get_order_count(menu_id, item_type)
        self.order_labels[count_key] = Label(order_frame, text=str(current_count),
                                            font=('Arial', 20, 'bold'), bg='white', 
                                            fg='#2C3E50', width=3)
        self.order_labels[count_key].pack(side=tk.LEFT, padx=20)
        
        # 더하기 버튼
        plus_button = Button(order_frame, text="➕", 
                           command=lambda: self.add_to_order(menu_id, item_type),
                           bg="#27AE60", fg="white", font=('Arial', 16, 'bold'),
                           width=3, height=1)
        plus_button.pack(side=tk.LEFT)
        
    def add_to_order(self, menu_id, item_type):
        """주문에 아이템 추가"""
        if self.order_manager.add_item(menu_id, item_type):
            self.update_order_display(menu_id, item_type)
            
            # 성공 사운드나 시각적 피드백 (선택사항)
            menu_name = MENU_DATA[menu_id]["name"]
            type_name = "세트" if item_type == "set" else "단품"
            print(f"{menu_name} {type_name} 추가됨")
        
    def remove_from_order(self, menu_id, item_type):
        """주문에서 아이템 제거"""
        if self.order_manager.remove_from_order(menu_id, item_type):
            self.update_order_display(menu_id, item_type)
            
    def update_order_display(self, menu_id, item_type):
        """주문 현황 업데이트"""
        # 수량 라벨 업데이트
        count_key = f"{menu_id}_{item_type}"
        if count_key in self.order_labels:
            current_count = self.order_manager.get_order_count(menu_id, item_type)
            self.order_labels[count_key].config(text=str(current_count))
            
        # 총액 업데이트
        if hasattr(self, 'total_label'):
            self.total_label.config(text=f"💰 총 주문 금액: {self.order_manager.total_price}$")
            
    def voice_order(self):
        """음성 주문 처리"""
        def voice_order_thread():
            try:
                menu_id, item_type = self.voice_recognizer.listen_for_order()
                
                if menu_id and item_type:
                    self.order_manager.add_item(menu_id, item_type)
                    menu_name = MENU_DATA[menu_id]["name"]
                    type_name = "세트" if item_type == "set" else "단품"
                    
                    message = f"{menu_name} {type_name}가 주문에 추가되었습니다."
                    
                    # UI 업데이트는 메인 스레드에서
                    self.root.after(0, lambda: self.voice_recognizer.speak(message))
                    self.root.after(0, lambda: messagebox.showinfo("주문 추가", message))
                    
                    # 주문 창이 열려있으면 업데이트
                    if self.current_order_window:
                        self.root.after(0, lambda: self.update_order_display(menu_id, item_type))
                        
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("음성 주문 오류", str(e)))
                
        thread = threading.Thread(target=voice_order_thread)
        thread.daemon = True
        thread.start()
        
    def finalize_order(self):
        """주문 완료"""
        if self.order_manager.is_empty():
            messagebox.showwarning("알림", "주문할 메뉴가 없습니다.")
            return
            
        # 주문 요약 생성
        summary = self.order_manager.get_order_summary()
        order_text = "📋 주문 내역:\n\n"
        
        for item in summary:
            if item["single_count"] > 0:
                order_text += f"🍔 {item['menu']} 단품 × {item['single_count']}개 = {item['single_count'] * item['single_price']}$\n"
            if item["set_count"] > 0:
                order_text += f"🍟 {item['menu']} 세트 × {item['set_count']}개 = {item['set_count'] * item['set_price']}$\n"
                
        order_text += f"\n💰 총 금액: {self.order_manager.total_price}$"
        
        # 주문 확인 창
        result = messagebox.askyesno("주문 확인", 
                                   f"{order_text}\n\n주문하시겠습니까?",
                                   icon='question')
        
        if result:
            # 결제 처리 (Excel 저장)
            if self.order_manager.save_to_excel():
                # 성공 메시지
                success_msg = "✅ 주문이 완료되었습니다!\n\n📄 영수증이 저장되었습니다.\n🕐 약 10-15분 후 준비 완료됩니다."
                messagebox.showinfo("주문 완료", success_msg)
                
                # 음성 안내
                def speak_completion():
                    self.voice_recognizer.speak("주문이 완료되었습니다. 영수증을 확인해주세요.")
                    
                speak_thread = threading.Thread(target=speak_completion)
                speak_thread.daemon = True
                speak_thread.start()
                
                # 주문 초기화
                self.order_manager.clear_orders()
                
                # 창들 닫기
                if self.current_order_window:
                    self.current_order_window.destroy()
                if self.current_menu_window:
                    self.current_menu_window.destroy()
                    
                # 메인 화면으로 돌아가기
                self.setup_main_screen()
                
            else:
                messagebox.showerror("오류", "주문 저장 중 오류가 발생했습니다.")
                
    def test_voice(self):
        """음성 테스트"""
        def test_thread():
            self.voice_recognizer.test_microphone()
            
        thread = threading.Thread(target=test_thread)
        thread.daemon = True
        thread.start()
        
    def admin_menu(self):
        """관리자 메뉴"""
        admin_window = Toplevel(self.root)
        admin_window.title("관리자 메뉴")
        admin_window.geometry("400x300")
        admin_window.configure(bg='#F8F9FA')
        
        title_label = Label(admin_window, text="🔧 관리자 메뉴", 
                          font=('Arial', 20, 'bold'), bg='#F8F9FA')
        title_label.pack(pady=20)
        
        # 키오스크 모드 토글
        kiosk_button = Button(admin_window, 
                            text="키오스크 모드 ON" if not self.kiosk_mode else "키오스크 모드 OFF",
                            command=self.toggle_kiosk_mode,
                            bg="#4A90E2", fg="white", font=('Arial', 14),
                            width=20, height=2)
        kiosk_button.pack(pady=10)
        
        # 주문 초기화
        reset_button = Button(admin_window, text="주문 초기화",
                            command=self.reset_orders,
                            bg="#FF6B35", fg="white", font=('Arial', 14),
                            width=20, height=2)
        reset_button.pack(pady=10)
        
        # 시스템 정보
        info_button = Button(admin_window, text="시스템 정보",
                           command=self.show_system_info,
                           bg="#7ED321", fg="white", font=('Arial', 14),
                           width=20, height=2)
        info_button.pack(pady=10)
        
    def toggle_kiosk_mode(self):
        """키오스크 모드 토글"""
        self.kiosk_mode = not self.kiosk_mode
        
        if self.kiosk_mode:
            # 전체화면 모드
            self.root.attributes('-fullscreen', True)
            self.root.protocol("WM_DELETE_WINDOW", lambda: None)  # 닫기 방지
            messagebox.showinfo("키오스크 모드", "키오스크 모드가 활성화되었습니다.\nESC 키를 눌러 해제할 수 있습니다.")
            self.root.bind('<Escape>', self.exit_kiosk_mode)
        else:
            # 일반 모드
            self.root.attributes('-fullscreen', False)
            self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
            self.root.unbind('<Escape>')
            
    def exit_kiosk_mode(self, event):
        """키오스크 모드 해제"""
        self.kiosk_mode = False
        self.root.attributes('-fullscreen', False)
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        self.root.unbind('<Escape>')
        
    def reset_orders(self):
        """주문 초기화"""
        if messagebox.askyesno("주문 초기화", "모든 주문을 초기화하시겠습니까?"):
            self.order_manager.clear_orders()
            self.order_labels.clear()
            
            # 열려있는 창들 닫기
            if self.current_order_window:
                self.current_order_window.destroy()
            if self.current_menu_window:
                self.current_menu_window.destroy()
                
            self.setup_main_screen()
            messagebox.showinfo("완료", "주문이 초기화되었습니다.")
            
    def show_system_info(self):
        """시스템 정보 표시"""
        import platform
        import sys
        
        info = f"""
🖥️ 시스템 정보

운영체제: {platform.system()} {platform.release()}
Python 버전: {sys.version.split()[0]}
현재 주문 수: {len(self.order_manager.orders)}
총 주문 금액: {self.order_manager.total_price}$
키오스크 모드: {'ON' if self.kiosk_mode else 'OFF'}
"""
        
        messagebox.showinfo("시스템 정보", info)
        
    def start_auto_reset_timer(self):
        """자동 초기화 타이머 시작 (키오스크 모드)"""
        if self.auto_reset_timer:
            self.root.after_cancel(self.auto_reset_timer)
            
        # 5분 후 자동 초기화
        self.auto_reset_timer = self.root.after(300000, self.auto_reset)
        
    def auto_reset(self):
        """자동 초기화 실행"""
        if self.kiosk_mode and self.order_manager.is_empty():
            self.setup_main_screen()
            self.start_auto_reset_timer()
            
    def quit_app(self):
        """애플리케이션 종료"""
        if messagebox.askyesno("종료 확인", "프로그램을 종료하시겠습니까?"):
            try:
                self.face_detector.release()
                if self.auto_reset_timer:
                    self.root.after_cancel(self.auto_reset_timer)
                self.root.quit()
            except:
                pass
                
    def run(self):
        """애플리케이션 실행"""
        self.root.mainloop()

if __name__ == "__main__":
    print("🍔 KFE 스마트 주문 키오스크 시작")
    print("=" * 50)
    
    try:
        app = FastFoodOrderApp()
        app.run()
    except Exception as e:
        print(f"애플리케이션 실행 오류: {e}")
    finally:
        print("애플리케이션 종료")
