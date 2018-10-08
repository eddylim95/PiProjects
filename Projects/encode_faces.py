from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
from config_reader import getJsonConfig

recognitionModel = getJsonConfig("image_recognition", "model")
dataPath = getJsonConfig("image_recognition", "dataPath")
encodingPickleLocation = getJsonConfig("encoding", "encodingPickleLocation")
encodingDataList = getJsonConfig("encoding", "data")

knownEncodings = []
knownNames = []

imagePaths = list(paths.list_images(dataPath))
print("{} images found in {}".format(len(imagePaths), dataPath))

for (i, imagePath) in enumerate(imagePaths):
    print("Processing image {}/{}, {}".format(i + 1, len(imagePath), imagePath))
    name = imagePath.split(os.path.sep)[-2]

    # Read image
    image = cv2.imread(imagePath)
    # Convert to RGB format for face_recognition module
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Identify facial bounding boxes
    boxes = face_recognition.face_locations(rgb, model= recognitionModel)
    # Get encodings for the faces
    encodings = face_recognition.face_encodings(rgb, boxes)
    # Save encodings and person name of the encoding
    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(name)

# pickle the encodings
print("Serializing encodings...")
data = {encodingDataList[0]: knownEncodings, encodingDataList[1]: knownNames}
f = open(encodingPickleLocation, "wb")
f.write(pickle.dumps(data))
f.close
