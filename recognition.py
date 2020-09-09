import face_recognition
import cv2
import numpy as np
import pickle
import mail

#projemizin bu sayfasında wabcamden görülen yüzün tanınıp tanınmadığını kontrol ediyoruz. burası yüzü ayırt ettiğimiz kısımdır.
#eğer kişi daha önceden kayıtlıysa kişinin ismi yüzü etrafında çqıkan frame'de yazılı olur.
#eğer kişi kayıtlı değilse, sistemin bilmediği bir yüzse o zaman frame kenarında 'unknown' olarak belirtilir.

f= open("ref_name.pkl","rb")
ref_dictt= pickle.load(f)
f.close()
f= open("ref_embed.pkl","rb")
embed_dictt= pickle.load(f) #bu değişkenlere pickle dosyalarımızda sakladığımız bilgileri atıyoruz.
f.close()

tanidikYuzBilgileri= []
tanidikYuzIsimleri= [] #tanıdık yüz bilgilerini kaydetmek için boş arrayler tanımlıyoruz. bilgilerimizi arrayler aracılığıyla
#karşılaştıracağız.

for id , embed_list in embed_dictt.items():
    for my_embed in embed_list:
        tanidikYuzBilgileri+= [my_embed] #pickle dosyasına kayıtlı yüzlerin bilgilerini arraylerimize ekliyoruz.
        tanidikYuzIsimleri+= [id]

video_capture= cv2.VideoCapture(0) #wabcamimiz açılıyor.
yuzLokasyonu= []
yuzBilgileri= []
yuzIsmi= [] #bu arraylerde wabcamde görünen yüzün bilgileri kaydedilecek.
process_this_frame= True

while True:
    ret, frame= video_capture.read()
    small_frame= cv2.resize(frame, (0, 0), fx= 0.25, fy= 0.25) #frame boyut bilgilerimiz.
    rgb_small_frame= small_frame[:, :, ::-1]

    if process_this_frame:
        yuzLokasyonu= face_recognition.face_locations(rgb_small_frame) #bu arrayimize wabcamdeki yüzün lokasyon bilgileri atılıyor.
        yuzBilgileri= face_recognition.face_encodings(rgb_small_frame, yuzLokasyonu) #bu arrayimize ise bu lokasyondaki yüzün
        #bilgileri atanıyor.
        yuzIsmi= []

        for bilgi in yuzBilgileri: #yüz bilgileri içindeki arrayimizdeki bilgileri sırasıyla kontrol ediyoruz.
            karsilastir= face_recognition.compare_faces(tanidikYuzBilgileri, bilgi) #elimizdeki bilgi ile tanıdık olarak
            #kaydettiğimiz kişilerin yüz bilgilerini karşılaştırıyoruz.
            yuzBenzerligi= face_recognition.face_distance(tanidikYuzBilgileri, bilgi) #yüzlerin ne kadar benzediği bilgisini atıyoruz.
            eslesim= np.argmin(yuzBenzerligi)

            if karsilastir[eslesim]:
                isim= tanidikYuzIsimleri[eslesim] #eğer eşleşim tutuyorsa tanıdık yüz isimleri arrayindeki bu eşleşimi isme atıyoruz.
                mail.mesaj(ref_dictt[isim]) #bu isim bilgisini mail olarak gönderiyoruz.

            else:
                isim= 'Unknown' #eğer eşleşim tutmuyorsa isme unknown etiketi atıyoruz.
                ref_dictt["Unknown"]= "Unknown" #sözlüğümüze unknown bilgilerini ekliyoruz.
                mail.mesaj(ref_dictt[isim]) #isim bilgisini mail olarak gönderiyoruz.

            yuzIsmi.append(isim) #ismimizi array listemize ekliyoruz.

    process_this_frame= not process_this_frame

    for (top_s, right, bottom, left), isim in zip(yuzLokasyonu, yuzIsmi): #burası ekrandaki frame ve frame'e isim bilgisini yazmak için.
        top_s*= 4
        right*= 4
        bottom*= 4
        left*= 4
        cv2.rectangle(frame, (left, top_s), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font= cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, ref_dictt[isim], (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    font= cv2.FONT_HERSHEY_DUPLEX
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF== ord('q'): #eğer kullanıcı q tuşuna basarsa sistem kapanıyor.
        break

print("Kamera kapatılıyor.")
video_capture.release()
print("Kamera kapatıldı.")
print("Program sonra erdi.")
cv2.destroyAllWindows()