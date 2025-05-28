import tkinter as tk
from tkinter import messagebox
import os

class BlogApp:
    def __init__(self):
        # 프로젝트 경로 출력
        self.project_path = os.path.dirname(os.path.realpath(__file__))
        print(f"프로젝트 경로: {self.project_path}")
        
        # 메인 윈도우 설정
        self.setup_main_window()
        
        # 텍스트 윈도우 설정
        self.setup_text_window()
    
    def setup_main_window(self):
        """메인 윈도우 (이미지 표시)"""
        self.root = tk.Tk()
        self.root.title("Blog - 이미지 뷰어")
        self.root.geometry("840x420")
        self.root.resizable(False, False)
        
        # 이미지 로드 및 표시
        self.load_main_image()
    
    def setup_text_window(self):
        """텍스트 윈도우"""
        self.text_window = tk.Toplevel(self.root)
        self.text_window.title("Blog - 텍스트 에디터")
        self.text_window.geometry("600x400")
        
        # 텍스트 프레임
        text_frame = tk.Frame(self.text_window)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 텍스트 위젯과 스크롤바
        self.text = tk.Text(text_frame, wrap="word", font=("Arial", 11))
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)
        
        # 패킹
        scrollbar.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        
        # 초기 텍스트 설정
        self.setup_initial_text()
        
        # 하단 이미지
        self.load_text_window_image()
    
    def load_main_image(self):
        """메인 윈도우 이미지 로드"""
        try:
            image_path = os.path.join(self.project_path, "맥치킨.jpg")
            if os.path.exists(image_path):
                self.main_image = tk.PhotoImage(file=image_path)
                label = tk.Label(self.root, image=self.main_image)
                label.pack(pady=20)
            else:
                placeholder = tk.Label(self.root, text="메인 이미지 없음\n(맥치킨.jpg)", 
                                    font=("Arial", 16), bg="lightblue")
                placeholder.pack(pady=20, fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("오류", f"메인 이미지 로드 실패: {e}")
    
    def load_text_window_image(self):
        """텍스트 윈도우 이미지 로드"""
        try:
            image_path = os.path.join(self.project_path, "맥치킨.jpg")
            if os.path.exists(image_path):
                self.text_image = tk.PhotoImage(file=image_path)
                # 이미지 크기 조정 (선택사항)
                image_label = tk.Label(self.text_window, image=self.text_image)
                image_label.pack(pady=10)
        except Exception as e:
            print(f"텍스트 윈도우 이미지 로드 실패: {e}")
    
    def setup_initial_text(self):
        """초기 텍스트 및 스타일 설정"""
        # 텍스트 삽입
        self.text.insert("1.0", "안녕하세요.\n")
        self.text.insert("2.0", "반갑습니다.")
        self.text.insert("2.1", "갑")
        
        # 태그 스타일 설정
        self.text.tag_add("강조", "1.0", "1.6")
        self.text.tag_config("강조", background="yellow", font=("Arial", 11, "bold"))
        self.text.tag_remove("강조", "1.1", "1.2")
    
    def run(self):
        """애플리케이션 실행"""
        self.root.mainloop()

if __name__ == "__main__":
    app = BlogApp()
    app.run()
