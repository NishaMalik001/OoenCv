import cv2
import csv
import cvzone
from cvzone.HandTrackingModule import HandDetector

pTime = 0
cTime = 0

cap = cv2.VideoCapture(0)
cap.set(3, 1200)
cap.set(4, 720)
detector = HandDetector()

class MCQ:
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])
        self.userAns = None

    def update(self, cursor, bboxs):

        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)



pathCSV = "mcqs.csv"
with open(pathCSV, newline='\n') as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]
    mcqList = []
    for q in dataAll:
        mcqList.append(MCQ(q))

print(len(mcqList))
qNo = 0
qTotal = len(dataAll)
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    mcq = mcqList[1]

    img, bbox = cvzone.putTextRect(img, mcq.question, [100, 100], 2, 2, offset=5, border=2)
    img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [100, 250], 2, 2, offset=5, border=2)
    img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [400, 250], 2, 2, offset=5, border=2)
    img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [100, 400], 2, 2, offset=5, border=2)
    img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [400, 400], 2, 2, offset=5, border=2)

    if hands:
        lmList = hands[0]['lmList']
        cursor = lmList[8]
        length = detector.findDistance(lmList[8], lmList[12], img)
        info = detector.findDistance(lmList[8], lmList[12], img)
        img = detector.findDistance(lmList[0], lmList[12], img)
        if length > 60:
            mcq.update(cursor, [bbox1, bbox2, bbox3, bbox4])
            print("CLICKED")

    cv2.imshow('frame', img)
    cv2.waitKey(1)