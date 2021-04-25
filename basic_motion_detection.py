# kütüphaneleri tanımlanıyor
import  cv2
import numpy as np

cap = cv2.VideoCapture('vtest.avi')#'0'

# videoda 2 kare alınıyor
ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    diff = cv2.absdiff(frame1,frame2) # 2 karenin farkı alınıyor
    gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY) # alınan kareyi gri formata dönüştürülür
    blur = cv2.GaussianBlur(gray,(5,5),0) # kare bulanıklaştırılarak pc nin algılama kolaylaştırılır
    _,thresh = cv2.threshold(blur,20,255,cv2.THRESH_BINARY) # eşik değerine göre siyah ya da beyaz olarak güncelle
    dilated = cv2.dilate(thresh,None,iterations=3) # pikseller genişletilir
    contours,_  = cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # dış çerçeve algılanır

    # cv2.drawContours(frame1,contours,-1,(255,255,0),2)
    # çerçeveler arasında gezerek algılanan şekiller çerçeveye alınır.
    for contour in contours:
        (x,y,w,h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 900:
            continue
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2,)
        cv2.putText(frame1,'status: {}'.format('Movement'),(10,20),cv2.FONT_HERSHEY_SIMPLEX,
                    1,(0,0,255),3)
    cv2.imshow('feed',frame1)
    frame1 = frame2
    ret,frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()