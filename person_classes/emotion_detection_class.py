from keras.models import load_model
import numpy as np
import dlib
import cv2


class _emotiondetection_:

    def __init__(self):
        self.emotions = {
        0: {
            "emotion": "Angry",
            "color": (193, 69, 42)
        },
        1: {
            "emotion": "Angry",
            "color": (164, 175, 49)
        },
        2: {
            "emotion": "Angry",
            "color": (40, 52, 155)
        },
        3: {
            "emotion": "Happy",
            "color": (23, 164, 28)
        },
        4: {
            "emotion": "Angry",
            "color": (164, 93, 23)
        },
        5: {
            "emotion": "Angry",
            "color": (218, 229, 97)
        },
        6: {
            "emotion": "Neutral",
            "color": (108, 72, 200)
        }}
    
        self.faceLandmarks = "shape_predictor_68_face_landmarks.dat"
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.faceLandmarks)
        self.emotionModelPath = 'emotionModel.hdf5'  # fer2013_mini_XCEPTION.110-0.65
        self.emotionClassifier = load_model(self.emotionModelPath, compile=False)
        self.emotionTargetSize = self.emotionClassifier.input_shape[1:3]


    def shapePoints(self,shape):
        self.coords = np.zeros((68, 2), dtype="int")
        for i in range(0, 68):
            self.coords[i] = (shape.part(i).x, shape.part(i).y)
        return self.coords


    def rectPoints(self,rect):
        self.x = rect.left()
        self.y = rect.top()
        self.w = rect.right() - self.x
        self.h = rect.bottom() - self.y
        return (self.x, self.y, self.w, self.h)

    def emotion_det_function(self,image):
        emotion_val=""
        grayFrame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = self.detector(grayFrame, 0)
        for rect in rects:
            shape = self.predictor(grayFrame, rect)
            points = self.shapePoints(shape)
            (x, y, w, h) = self.rectPoints(rect)
            grayFace = grayFrame[y:y + h, x:x + w]
            try:
                grayFace = cv2.resize(grayFace, (self.emotionTargetSize))
            except:
                continue

            grayFace = grayFace.astype('float32')
            grayFace = grayFace / 255.0
            grayFace = (grayFace - 0.5) * 2.0
            grayFace = np.expand_dims(grayFace, 0)
            grayFace = np.expand_dims(grayFace, -1)
            emotion_prediction = self.emotionClassifier.predict(grayFace)
            emotion_probability = np.max(emotion_prediction)
            if (emotion_probability > 0.2):
                emotion_label_arg = np.argmax(emotion_prediction)
                if (str(self.emotions[emotion_label_arg]['emotion']) == 'Angry' and emotion_probability>0.55):
                    emotion_val="Neutral"
                if (str(self.emotions[emotion_label_arg]['emotion']) == 'Angry' and emotion_probability<0.55):
                    emotion_val="Angry"
                if (str(self.emotions[emotion_label_arg]['emotion']) != 'Angry'):
                    emotion_val=str(self.emotions[emotion_label_arg]['emotion'])
                return emotion_val
            else:
                return "Neutral"