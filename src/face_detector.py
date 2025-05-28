"""
얼굴 인식 및 나이 예측 모듈
"""
import cv2
import numpy as np
from config import *
import os

class FaceDetector:
    def __init__(self):
        self.face_net = None
        self.age_net = None
        self.video = None
        self.load_models()
        
    def load_models(self):
        """모델 로드"""
        try:
            if os.path.exists(FACE_MODEL) and os.path.exists(FACE_PROTO):
                self.face_net = cv2.dnn.readNet(FACE_MODEL, FACE_PROTO)
                print("얼굴 인식 모델 로드 완료")
            else:
                print(f"얼굴 인식 모델 파일을 찾을 수 없습니다: {FACE_MODEL}, {FACE_PROTO}")
                
            if os.path.exists(AGE_MODEL) and os.path.exists(AGE_PROTO):
                self.age_net = cv2.dnn.readNet(AGE_MODEL, AGE_PROTO)
                print("나이 예측 모델 로드 완료")
            else:
                print(f"나이 예측 모델 파일을 찾을 수 없습니다: {AGE_MODEL}, {AGE_PROTO}")
                
        except Exception as e:
            print(f"모델 로드 오류: {e}")
        
    def initialize_camera(self, source=0):
        """카메라 초기화"""
        try:
            self.video = cv2.VideoCapture(source)
            if self.video.isOpened():
                # 카메라 설정
                self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                print(f"카메라 {source} 초기화 성공")
                return True
            else:
                print(f"카메라 {source} 초기화 실패")
                return False
        except Exception as e:
            print(f"카메라 초기화 오류: {e}")
            return False
        
    def detect_face(self, frame, conf_threshold=0.7):
        """얼굴 검출"""
        if self.face_net is None:
            return frame, []
            
        try:
            frame_opencv_dnn = frame.copy()
            frame_height, frame_width = frame_opencv_dnn.shape[:2]
            
            blob = cv2.dnn.blobFromImage(frame_opencv_dnn, 1.0, (300, 300), [104, 117, 123], True, False)
            self.face_net.setInput(blob)
            detections = self.face_net.forward()
            
            face_boxes = []
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > conf_threshold:
                    x1 = int(detections[0, 0, i, 3] * frame_width)
                    y1 = int(detections[0, 0, i, 4] * frame_height)
                    x2 = int(detections[0, 0, i, 5] * frame_width)
                    y2 = int(detections[0, 0, i, 6] * frame_height)
                    face_boxes.append([x1, y1, x2, y2])
                    cv2.rectangle(frame_opencv_dnn, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
            return frame_opencv_dnn, face_boxes
            
        except Exception as e:
            print(f"얼굴 검출 오류: {e}")
            return frame, []
        
    def predict_age(self, face_roi):
        """나이 예측"""
        if self.age_net is None:
            return "(25~32)"  # 기본값
            
        try:
            blob = cv2.dnn.blobFromImage(face_roi, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            self.age_net.setInput(blob)
            age_preds = self.age_net.forward()
            age = AGE_LIST[age_preds[0].argmax()]
            return age
        except Exception as e:
            print(f"나이 예측 오류: {e}")
            return "(25~32)"  # 기본값
        
    def detect_age_from_camera(self, timeout=10):
        """카메라에서 나이 검출"""
        if not self.video or not self.video.isOpened():
            print("카메라가 초기화되지 않았습니다.")
            return None
            
        frame_count = 0
        max_frames = timeout * 10  # 약 10초 (FPS 고려)
        
        try:
            while frame_count < max_frames:
                ret, frame = self.video.read()
                if not ret:
                    print("카메라에서 프레임을 읽을 수 없습니다.")
                    break
                    
                # 프레임 표시
                cv2.imshow("얼굴 인식 - 스페이스바를 누르면 촬영", frame)
                
                result_img, face_boxes = self.detect_face(frame)
                
                if face_boxes:
                    # 가장 큰 얼굴 선택
                    largest_face = max(face_boxes, key=lambda box: (box[2]-box[0]) * (box[3]-box[1]))
                    
                    padding = 20
                    y1 = max(0, largest_face[1] - padding)
                    y2 = min(largest_face[3] + padding, frame.shape[0] - 1)
                    x1 = max(0, largest_face[0] - padding)
                    x2 = min(largest_face[2] + padding, frame.shape[1] - 1)
                    
                    face = frame[y1:y2, x1:x2]
                    
                    if face.size > 0:
                        age = self.predict_age(face)
                        print(f"감지된 나이: {age}")
                        return age
                        
                # 키 입력 처리
                key = cv2.waitKey(100) & 0xFF
                if key == ord(' '):  # 스페이스바
                    if face_boxes:
                        largest_face = max(face_boxes, key=lambda box: (box[2]-box[0]) * (box[3]-box[1]))
                        padding = 20
                        y1 = max(0, largest_face[1] - padding)
                        y2 = min(largest_face[3] + padding, frame.shape[0] - 1)
                        x1 = max(0, largest_face[0] - padding)
                        x2 = min(largest_face[2] + padding, frame.shape[1] - 1)
                        face = frame[y1:y2, x1:x2]
                        if face.size > 0:
                            age = self.predict_age(face)
                            return age
                elif key == 27:  # ESC
                    break
                    
                frame_count += 1
                
            print("얼굴을 감지할 수 없습니다.")
            return None
            
        except Exception as e:
            print(f"얼굴 감지 중 오류: {e}")
            return None
        
    def release(self):
        """리소스 해제"""
        if self.video:
            self.video.release()
        cv2.destroyAllWindows()
        print("카메라 리소스가 해제되었습니다.")
