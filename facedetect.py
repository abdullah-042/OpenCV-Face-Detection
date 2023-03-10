import cv2
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

#Builder.load_file('facedetect.kv')

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

class MainLayout(BoxLayout):
    pass

class MyCamera(Image):
    def __init__(self, **kwargs):
        super(MyCamera, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        fps = 60
        Clock.schedule_interval(self.update, 1.0/fps)

    def get_texture(self, frame):
        buffer = cv2.flip(frame, 0).tobytes()
        image_texture = Texture.create(
            size=(frame.shape[1],
                  frame.shape[0]),
            colorfmt='bgr')
        image_texture.blit_buffer(
            buffer,
            colorfmt='bgr',
            bufferfmt='ubyte')

        return image_texture

    def detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            center = x + w // 2, y + h // 2
            radius = w // 2
            cv2.circle(frame, center, radius, (0, 255, 0), 2)
            cv2.putText(frame,
                        "Face detected",
                        (x + 50, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)

        return frame

    def update(self, dt):
        ret, frame = self.capture.read()
        fliped = cv2.flip(frame, 1)
        if not ret:
            return
        if self.detect:
            self.detect_faces(fliped)
        self.texture = self.get_texture(fliped)

class FaceDetectApp(App):
    def build(self):
        self.layout = MainLayout()
        return self.layout

if __name__ == '__main__':
    FaceDetectApp().run()