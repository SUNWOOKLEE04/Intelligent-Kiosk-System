import tkinter as tk
from tkinter import messagebox
import os

class ImageViewerApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Image Viewer")
        self.window.geometry("840x420")
        
        # 프로젝트 경로 출력
        self.project_path = os.path.dirname(os.path.realpath(__file__))
        print(f"프로젝트 경로: {self.project_path}")
        
        # UI 구성
        self.setup_ui()
        
    def setup_ui(self):
        """UI 구성"""
        # 메인 프레임
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 이미지 로드 및 표시
        self.load_and_display_image(main_frame)
        
    def load_and_display_image(self, parent):
        """이미지 로드 및 표시"""
        try:
            image_path = os.path.join(self.project_path, "맥치킨.jpg")
            
            if os.path.exists(image_path):
                self.image = tk.PhotoImage(file=image_path)
                label = tk.Label(parent, image=self.image, relief="ridge", bd=2)
                label.pack(pady=10)
            else:
                # 이미지가 없을 경우
                placeholder = tk.Label(parent, text="이미지 파일을 찾을 수 없습니다\n(맥치킨.jpg)", 
                                    font=("Arial", 14), bg="lightgray", 
                                    relief="ridge", bd=2)
                placeholder.pack(pady=10, padx=10, fill="both", expand=True)
                
        except Exception as e:
            messagebox.showerror("오류", f"이미지 로드 중 오류 발생: {e}")
    
    def run(self):
        """애플리케이션 실행"""
        self.window.mainloop()

if __name__ == "__main__":
    app = ImageViewerApp()
    app.run()
