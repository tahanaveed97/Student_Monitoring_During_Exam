import cv2
from scipy.spatial import distance as dist
import numpy as np
import math

class _distraction_:
    
    def __init__(self):
        self.val = 0.22
        self.valU = 0.10
        self.valD = -0.13
        self.ear = 0.3
        self.maxYawnScore=10
        self.maxSleepScore=10
        self.sleepingScore=0
        self.yawningScore=0
        self.distraction=True



    def eye_aspect_ratio(self,eye):
        A = dist.euclidean(eye[2], eye[3])
        B = dist.euclidean(eye[4], eye[5])
        D = dist.euclidean(eye[6], eye[7])
        E = dist.euclidean(eye[8], eye[9])
        C = dist.euclidean(eye[0], eye[1])
        ear_ = (A + B + D + E) / (5.0 * C)
        return ear_


    def distraction_det_func(self,land_marks,image):
        h, w = image.shape[:2]
        for face_landmarks in land_marks:
            a = [data_point for data_point in face_landmarks.landmark]
        right_eye = [263, 362, 249, 390, 373, 374, 380,
                    381, 382, 466, 388, 387, 386, 385, 384, 398]
        req_re = [263, 362, 384, 381, 385, 380, 387, 373, 388, 390]
        req_le = [133, 33, 161, 163, 160, 144, 157, 154, 158, 153]
        up_lips = [12]
        bot_lips = [14]
        left = []
        right = []
        left_eye = [133, 33, 155, 154, 153, 145, 144,
                    163, 7, 173, 157, 158, 159, 160, 161, 246]

        for i in range(len(a)):
            if i in right_eye or i in left_eye or i in up_lips or i in bot_lips:
                if i in req_le:
                    left.append((a[i].x, a[i].y))
                if i in req_re:
                    right.append((a[i].x, a[i].y))
                size = np.array([w, h])
                box = [a[i].x, a[i].y] * size
                (X, Y) = box.astype(int)
                cv2.circle(image, (X, Y), 1, (0, 255, 0), -1)

        distanceLeft = a[33].x-a[34].x
        distanceRight = a[264].x-a[359].x

        distanceUP = a[10].z - a[152].z
        distanceLIPS = a[14].y - a[12].y
        # cv2.putText(image, str(distanceLIPS) + str(), (550, 100),
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        try:
            slope=(a[10].y-a[152].y)/(a[10].x-a[152].x)
            angle=math.degrees(math.atan(1/slope))
        except:
            angle=0

        # if angle>15:
        #     cv2.putText(image, "head tilted Right", (50, 110),
        #                     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # elif angle<-15:
        #     cv2.putText(image, "head tilted Left", (50, 110),
        #                     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # if distanceLIPS > 0.01:
        #     cv2.putText(image, " Mouth Open" + str(), (50, 120),
        #                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        #     self.yawningScore+=1
        # else:
        #     self.yawningScore=0

        if distanceLeft < 0.01:
            self.distraction=True
            cv2.putText(image, " watching left", (300, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif distanceRight < 0.00:
            self.distraction=True
            cv2.putText(image, " watching right", (300, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif distanceUP >= self.valU:
            self.distraction=True
            cv2.putText(image, " watching up", (300, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif distanceUP <= self.valD:
            self.distraction=True
            cv2.putText(image, " watching down", (300, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            leftEAR = self.eye_aspect_ratio(left)
            rightEAR = self.eye_aspect_ratio(right)
            ear = (leftEAR + rightEAR) / 2.0
            if ear < self.val:
                self.distraction=True
                cv2.putText(image, "BLINKED", (300, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                self.sleepingScore+=1
            else:
                self.sleepingScore=0
                self.distraction=False

        # if self.sleepingScore>self.maxSleepScore:
        #     cv2.putText(image, "SLEEPING", (300, 30),
        #                     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        # if self.yawningScore>self.maxYawnScore:
        #   cv2.putText(image, "Yawning", (300, 65),
        #                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        return image,self.distraction
                    



