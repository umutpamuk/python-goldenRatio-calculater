import numpy as np
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

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

mouth_cascade = cv2.CascadeClassifier('haarcascade_mouth.xml')


for l in range(1, 140):

    print('%d. resim:' % (l))
    img = cv2.imread('%d.jpeg' % (l))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Yüz hesaplanması ,çizimi ve değerlerin tutulması
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
        facesxw = x + w - 50
        facesyh = y + h
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray)
        mouths = mouth_cascade.detectMultiScale(roi_gray, 3.4, 5)

        # gözbebegi = gözbebegi_cascade.detectMultiScale(roi_gray,1.3,5)

        eyessayac = 0
        mounthssayac = 0
        x1 = 0
        x2 = 0
        xw1 = 0
        xw2 = 0
        x2arası = 0
        x1arası = 0
        mounthxw = 0
        eyesxw = 0
        firstratio = 0
        toplamoran = 0
        toplamaltınoran = 0

        # Göz çizimi ve degerlerin tutulması
        for (ex, ey, ew, eh) in eyes:
            ex = ex + 5
            ey = ey + 5
            ew = ew - 5
            eh = eh - 5
            if int(eyessayac) == 0:
                x1 = ex
                y1 = ey
                xw1 = ex + ew
                x1arası = ex + (ew / 2)
            if int(eyessayac) == 1:
                x2 = ex + ew
                xw2 = ex + ew
                w2 = ew
                xa2 = ex
                x2arası = (w2 / 2) + xa2

            cv2.rectangle(roi_color, (ex, ey), (ex + (ew), ey + (eh)), (0, 255, 255), 1)
            eyessayac = eyessayac + 1

        # Agız çizimi ve degerlerinin tutulması
        for (nx, ny, nw, nh) in mouths:
            if int(mounthssayac) < 1:
                mounthxw = (nx + nw) - nx
                cv2.rectangle(roi_color, (nx, ny), (nx + nw, ny + nh), (255, 0, 255), 1)
                mounthssayac = mounthssayac + 1
                facesandmounty = ny + 100
                mounthyh = ny + nh
                jawandmount = facesyh - ny

        # kulanılan hesaplamalar
        eyesxw = x2 - x1
        twoeyesbetween = x2arası - x1arası
        twobrowsebetween = xa2 - xw1

        # oran hesaplamaları
        print(eyesxw,mounthxw,x2,x1)
        firstratio = eyesxw / mounthxw
        secondratio = facesyh / facesxw
        thirdratio = facesandmounty / jawandmount
        fourthratio = facesyh / (facesyh - y1)
        fifthratio = twoeyesbetween / twobrowsebetween

        # oranların birbirine orananı ve ortalaması
        toplamoran = firstratio + secondratio + thirdratio + fourthratio + fifthratio
        toplamaltınoran = toplamoran / 5

        # oranları ekrana basma
        print('1. oran:' + str(firstratio))  # göz genişliği / agiz genişliğiyle
        print('2. oran:' + str(secondratio))  # yüzün yüksekliği / yüzün genişliği
        print('3. oran:' + str(thirdratio))  # dudakucu alınucu / dudak ucu cane ucu
        print('4. oran:' + str(fourthratio))  # yüz boyu / cene ucundan kaş birleşim yeri arası
        print('5. oran:' + str(fifthratio))  # göz bebekleri arası / kaşlar arası
        print('toplam altın oran:' + str(toplamaltınoran))  # tüm oranların ortalaması

        # Mysql kaydedilen deger dönüştürme
        class NumpyMySQLConverter(mysql.connector.conversion.MySQLConverter):
            """ A mysql.connector Converter that handles Numpy types """

            def _float32_to_mysql(self, value):
                return float(value)

            def _float64_to_mysql(self, value):
                return float(value)

            def _int32_to_mysql(self, value):
                return int(value)

            def _int64_to_mysql(self, value):
                return int(value)

    # Sql baglantı kontrolu
    try:
        conn = mysql.connector.connect(**config)
        conn.set_converter_class(NumpyMySQLConverter)
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

        # Sql Gelen verileri İnsertleme(Oluşturma)
        cursor.execute("INSERT INTO haar (A1, A2, A3, A4, A5, Total) VALUES (%s, %s,%s, %s, %s, %s);",
                       (firstratio, secondratio, thirdratio, fourthratio, fifthratio, toplamaltınoran))
    conn.commit()
    cursor.close()
    conn.close()

cv2.namedWindow("output", cv2.WINDOW_NORMAL)
imS = cv2.resize(img, (1000, 1000))
cv2.imshow("output", imS)
cv2.waitKey(0)
