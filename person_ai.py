from person_classes.face_mesh_class import _facemesh_
from person_classes.distraction_class import _distraction_
from person_classes.person_detection_class import _persondetection_
import time
import cv2
from datetime import datetime, date
import numpy as np
import json
from func_timeout import func_timeout, FunctionTimedOut

class PersonAI:
    def __init__(self) -> None:
        self.person_found_time = 0
        self.distraction_time = 0
        self.distraction = True
        self.person=False
        self.time_not=0
        self.distraction_val=False
        self.distraction_not=0
        self.distraction_status = ""
        self.val_person=False
        
        self.continuous_distraction = False
        self.no_person = False
        
        self._face_mesh = _facemesh_()
        self._distraction_det = _distraction_()
        self._person_det = _persondetection_()
        
        self.start_event=time.time()
        self.end_event=time.time()
        self.start_overwrite=time.time()
        self.end_overwrite=time.time()
        self.start_time=time.time()
        self.end_time=time.time()
        
    def load_json_file(self):
        try:
            with open('config_parameters.json') as json_file:
                return json.load(json_file)
        except:
            print("Config file not fount")
            return ''
    
    def detection(self):
        cap = cv2.VideoCapture(0)
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        
        while True:
            ret, frame = cap.read()
            
            #### CHECKING FOR OTHER CAMERAS ####
            if ret==False:
                cap = cv2.VideoCapture(0)
                try:
                    frame_width = int(cap.get(3))
                    frame_height = int(cap.get(4))  
                except:
                    pass
                ret,frame=cap.read()
            if ret==False:
                cap = cv2.VideoCapture(1)
                try:
                    frame_width = int(cap.get(3))
                    frame_height = int(cap.get(4))
                except:
                    pass
                ret,frame=cap.read()
            if ret==False:
                cap = cv2.VideoCapture(-1)
                try:
                    frame_width = int(cap.get(3))
                    frame_height = int(cap.get(4))
                except:
                    pass
                ret,frame=cap.read()
            if ret==False:
                cap = cv2.VideoCapture(2)
                try:
                    frame_width = int(cap.get(3))
                    frame_height = int(cap.get(4))
                except:
                    pass
                ret,frame=cap.read()
            if ret==False:
                print("No Camera can be accessed!")
                continue

            orig_frame=frame.copy()
            image_empt = np.zeros((frame_height, frame_width, 3), np.uint8)
            image_empt.fill(255)
            # file_name=_database_events.get_date_time()
            

            #### READING PARAMETERS FROM CONFIGURATION FILE ####
            self.data = self.load_json_file()

            #### PERSON DETECTION MODEL CALLED ####

            if self.data['Durations']['PersonDetection']:
                self.val_person= self._person_det.person_det_func(frame)  
                #### IF PERSON FOUND ####     
                if self.val_person == True:
                    #### DATASET COLLECTION VIDEO ####
                    if self.data['Durations']['DataSetCollection']:
                        # out_dataset.write(orig_frame)
                        end_time=time.time()
                        if int(end_time-start_time) > (int(self.data['Durations']['DataSetVideoDuration'])+40):
                            start_time = time.time()
                            
                    self.person_found_time=0
                    self.person=False

                    #### DISTRACTION MODEL CALLED ####
                    if self.data['Durations']['Distraction']:
                        val_mesh, mesh_val, image = self._face_mesh.face_mesh_func(frame)
                        if val_mesh == True:
                            frame, self.distraction = self._distraction_det.distraction_det_func(mesh_val, image)
                            if self.distraction == True:
                                if self.distraction_val==False:
                                    self.distraction_not=time.perf_counter()
                                    self.distraction_val=True
                                self.distraction_time=time.perf_counter()
                                self.distraction_status = "Distracted"
                            elif self.distraction == False:
                                self.distraction_time = 0
                                self.distraction_val=False
                                self.distraction_status = "Not Distracted"   
                    else:
                        self.distraction=True
                        self.distraction_status="Distraction Model Stopped"

                #### IF PERSON NOT FOUND ####
                else:
                    if self.person == False:
                        self.time_not = time.perf_counter()
                        self.person = True
                    self.person_found_time = time.perf_counter()
                    self.distraction_status="Not Distracted"
                    self.distraction=False

            if self.distraction_time-self.distraction_not >= round(self.data['Durations']['CheckDistractionInterval']):
                # print("Five Secend Distraction ----------------------------")
                self.continuous_distraction = True

            if self.person_found_time-self.time_not >= round(self.data['Durations']['CheckPersonInterval']):
                # print("No Person @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2")
                self.no_person = True
            
            cv2.putText(image_empt, "Person Found: {}.".format(
                str(self.val_person)), (10, 80), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0), 1)
            cv2.putText(image_empt, "Distraction: {}.".format(
                str(self.distraction)), (10, 120), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0), 1)
            cv2.putText(image_empt, "D Status: {}.".format(
                str(self.distraction_status)), (10, 160), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0), 1)
          
            image = np.hstack((frame, image_empt))
            
            cv2.imshow('image', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
            
# personai = PersonAI()
# personai.detection()  