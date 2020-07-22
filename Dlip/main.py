import dlib
import cv2
import mysql.connector
from mysql.connector import errorcode

# Obtain connection string information from the portal
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'umut1810',
    'database': 'goldenRatio'
}

for xx in range(1, 140):
    # GoldenRatioCalculate
    cap = cv2.imread('%d.jpeg' % (xx))
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    gray = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        # cv2.rectangle(cap, (x1, y1), (x2, y2), (0, 255, 0), 1)
        # print(x1,x2,y1,y2)

        landmarks = predictor(gray, face)

        for n in (8, 33, 36, 45, 48, 54, 62, 66):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(cap, (x, y), 1, (0, 0, 255), -1)
            for n in range(0, 68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                cv2.circle(cap, (x, y), 2, (0, 0, 255), -1)

        cv2.line(cap, (landmarks.part(33).x, landmarks.part(33).y), (landmarks.part(8).x, landmarks.part(8).y),
                 (0, 0, 255),
                 1)
        cv2.line(cap, (landmarks.part(66).x, landmarks.part(66).y), (landmarks.part(8).x, landmarks.part(8).y),
                 (255, 255, 255),
                 1)

        cv2.line(cap, (landmarks.part(66).x, landmarks.part(66).y), (landmarks.part(8).x, landmarks.part(8).y),
                 (255, 255, 255),
                 1)
        cv2.line(cap, (landmarks.part(33).x, landmarks.part(33).y), (landmarks.part(62).x, landmarks.part(62).y),
                 (0, 0, 255),
                 1)

        cv2.line(cap, (landmarks.part(36).x, landmarks.part(36).y), (landmarks.part(45).x, landmarks.part(45).y),
                 (0, 255, 0), 1)
        cv2.line(cap, (landmarks.part(48).x, landmarks.part(48).y), (landmarks.part(54).x, landmarks.part(54).y),
                 (0, 255, 0), 1)

        cv2.line(cap, (landmarks.part(36).x, landmarks.part(36).y), (landmarks.part(48).x, landmarks.part(48).y),
                 (0, 255, 0), 1)
        cv2.line(cap, (landmarks.part(48).x, landmarks.part(48).y), (landmarks.part(8).x, landmarks.part(8).y),
                 (0, 255, 0), 1)

        cv2.line(cap, (landmarks.part(27).x, landmarks.part(27).y), (landmarks.part(62).x, landmarks.part(62).y),
                 (0, 0, 0), 1)
        cv2.line(cap, (landmarks.part(62).x, landmarks.part(62).y), (landmarks.part(8).x, landmarks.part(8).y),
                 (255, 255, 255), 1)

        # cv2.imshow("Frame", cap)
        # cv2.namedWindow("output", cv2.WINDOW_NORMAL)  # Create window with freedom of dimensions
        # imS = cv2.resize(cap, (1000, 1000))  # Resize image
        # cv2.imshow("output", imS)

        x = landmarks.part(36).x
        y = landmarks.part(45).x
        B1 = y - x
        x1 = landmarks.part(48).x
        y1 = landmarks.part(54).x
        A1 = y1 - x1
        Sonuc1 = B1 / A1
        print("A1 => ", Sonuc1, " Goz/Agiz", B1, A1)

        x2 = landmarks.part(66).y
        y2 = landmarks.part(8).y
        B2 = x2 - y2
        x3 = landmarks.part(33).y
        y3 = landmarks.part(62).y
        A2 = x3 - y3
        Sonuc2 = B2 / A2
        print("A2 => ", Sonuc2, " Burun-UstDudak/AltDudak-Cene ")

        x4 = landmarks.part(33).y
        y4 = landmarks.part(8).y
        B3 = x4 - y4
        x5 = landmarks.part(66).y
        y5 = landmarks.part(8).y
        A3 = x5 - y5
        Sonuc3 = B3 / A3
        print("A3 => ", Sonuc3, "  Burun-Cene/Altdudak-Cene")

        x6 = landmarks.part(36).y
        y6 = landmarks.part(48).y
        B4 = x6 - y6
        x7 = landmarks.part(48).y
        y7 = landmarks.part(8).y
        A4 = x7 - y7
        Sonuc4 = B4 / A4
        print("A4 => ", Sonuc4, "  SolGoz-Agız/Agız-Cene")

        x8 = landmarks.part(27).y
        y8 = landmarks.part(62).y
        B5 = x8 - y8
        x9 = landmarks.part(62).y
        y9 = landmarks.part(8).y
        A5 = x9 - y9
        Sonuc5 = B5 / A5
        print("A5 => ", Sonuc5, "  BurunBaşlangıç-UstDudak/UstDudak-Cene")

        Total = (Sonuc1 + Sonuc2 + Sonuc3 + Sonuc4 + Sonuc5) / 5
        print("Total => ", Total)

        print(xx,"*********************************************************")
    # Construct connection string
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()

        # Insert some data into table
        cursor.execute("INSERT INTO Ratio (A1, A2, A3, A4, A5, Total) VALUES (%s, %s,%s, %s, %s, %s);",
                       (Sonuc1, Sonuc2, Sonuc3, Sonuc4, Sonuc5, Total))

    # Cleanup
    conn.commit()
    cursor.close()
    conn.close()
    print("Done.")
    # cv2.waitKey(0)
