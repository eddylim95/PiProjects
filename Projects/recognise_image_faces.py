import face_recognition
import pickle
import cv2
import sys
from config_reader import getJsonConfig

recognitionModel = getJsonConfig("image_recognition", "model")
encodingPickleLocation = getJsonConfig("encoding", "encodingPickleLocation")
encodingDataList = getJsonConfig("encoding", "data")

# load encodings
print("Loading encodings...")
data = pickle.loads(open(encodingPickleLocation , "rb").read())

# load input image
inputImage = cv2.imread(sys.argv[1])
print("Analysing {}...".format(sys.argv[1]))
# convert to RGB
rgb = cv2.cvtColor(inputImage, cv2.COLOR_BGR2RGB)

# set bounding boxes for faces
print("recognising faces...")
boxes = face_recognition.face_locations(rgb, model= recognitionModel)
encodings = face_recognition.face_encodings(rgb, boxes)

names = []

for encoding in encodings:
    # attempt to match known faces
    matches = face_recognition.compare_faces(data[encodingDataList[0]], encoding)
    name = "unknown"
    # check if there is a match
    if True in matches:
        # find all indexes of matched encodings and store
        matchedIds = [i for (i,b) in enumerate(matches) if b]
        counts = {}

        # loop over matched indexs and keep a count for each matched face
        for i in matchedIds:
            name = data[encodingDataList[1]][i]
            counts[name] = counts.get(name, 0) + 1

        # select name with largest number of matches
        name = max(counts, key=counts.get)

    # update list of names
    names.append(name)

# loop over recognised faces
for((top, right, bottom, left), name)in zip(boxes, names):
    # draw recognised names on the image
    cv2.rectangle(inputImage, (left, top), (right, bottom), (0, 255, 0), 2)
    y = top -15 if top -15 > 15 else top + 15
    cv2.putText(inputImage, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 225, 0), 2)

# show image
cv2.imshow("Image", inputImage)
cv2.waitKey(0)