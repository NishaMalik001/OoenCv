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
        # here you have three values corresponding to the x, y and z  
        # The required values(location are x, and y) so we are getting those location(values) here.       
        cursor = lmList[8][:2]
        
        # print(type(cursor[0]))
        
        # print(type(cursor))
        # 
        point1 =tuple(lmList[8][:2] )
        # print(type(point1))
        point2 =tuple(lmList[12][:2]) 
        
        # The findDistance function returns there values, 1 length, 2. info, 3. image(mat)
        length, info, img = detector.findDistance(point1, point2, img)
        length1, info, img = detector.findDistance(point1, point2, img)
        length2, info, img = detector.findDistance(tuple(lmList[0][:2]), point2, img)
        if length > 60:
            mcq.update(cursor, [bbox1, bbox2, bbox3, bbox4])
            print("CLICKED")

    cv2.imshow('frame', img)
    key =cv2.waitKey(1)
    if key ==ord('q'):
        break

cv2.destroyAllWindows()