import numpy as np
import time
import cv2
import tensorflow as tf


class _persondetection_:

    def __init__(self):
        self.interpreter = tf.lite.Interpreter(model_path="centernet_coco.tflite")
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.label_names = [line.rstrip('\n') for line in open("label_map.txt")]
        self.label_names = np.array(self.label_names)
        self.inputSize = 320


    def person_det_func(self,image):
        img_rgb_original = cv2.resize(image, (self.inputSize, self.inputSize), cv2.INTER_AREA)
        img_rgb = np.array(img_rgb_original.reshape([1, self.inputSize, self.inputSize, 3]) , dtype= np.float32)
        self.interpreter.set_tensor(self.input_details[0]['index'], img_rgb)
        self.interpreter.invoke()
        outputClasses = self.interpreter.get_tensor(self.output_details[1]['index'])
        outputScores = self.interpreter.get_tensor(self.output_details[2]['index'])
        numDetections = self.interpreter.get_tensor(self.output_details[3]['index'])
        numDetectionsOutput = int(np.minimum(numDetections[0],10))
        for i in range(numDetectionsOutput):
            if outputScores[0][i] > 0.35:
                try:
                    class_name = self.label_names[int(outputClasses[0][i])]
                    if class_name == '"person"':
                        return True
                except:
                    pass


