import cv2
import face_recognition
import pickle

#projemizin bu sayfasında yüzü tanıma yapacağız. sisteme tanıtmak istediğimiz bir yüz olduğu zaman
#bu sayfayı çalıştıracağız.

isim= input("Tanıtacağınız ismi giriniz: ")
id= input("ID bilgisini giriniz: ") #burada kişinin isim ve id bilgilerini sisteme kaydedeceğiz. id bilgileri 001'den başlayarak
#sırayla verilebilir.

try:
    f= open("ref_name.pkl","rb") #pickle dosyalarına isim bilgilerini kaydediyoruz.
    ref_dictt= pickle.load(f)
    f.close()

except:
    ref_dictt= {}

ref_dictt[id]= isim
f= open("ref_name.pkl","wb")
pickle.dump(ref_dictt,f)
f.close()

try:
    f= open("ref_embed.pkl","rb") #pickle dosyalarına yüz bilgilerini kaydediyoruz.
    embed_dictt= pickle.load(f)
    f.close()

except:
    embed_dictt= {}

for i in range(5): #burada yüzün 5 kez resmi çekiliyor. daha doğru bir kullanım için yüzün 5 farklı açıdan resmini çekeceğiz.
    key= cv2.waitKey(1)
    webcam= cv2.VideoCapture(0) #kameraya erişiyoruz.

    while True:
        check, frame= webcam.read()
        cv2.imshow("Capturing", frame)
        small_frame= cv2.resize(frame, (0, 0), fx= 0.25, fy= 0.25)
        rgb_small_frame= small_frame[:, :, ::-1]
        key= cv2.waitKey(1)

        if key== ord('s'): #s harfine basıldığı zaman resim çekiliyor.
            face_locations= face_recognition.face_locations(rgb_small_frame)

            if face_locations!= []:
                face_encoding= face_recognition.face_encodings(frame)[0]

                if id in embed_dictt:
                    embed_dictt[id]+= [face_encoding]

                else:
                    embed_dictt[id]= [face_encoding]
                webcam.release()
                cv2.waitKey(1)
                cv2.destroyAllWindows()
                break

        elif key== ord('q'): #q harfine basıldığı zaman program sonlandırılıyor.
            webcam.release()
            cv2.destroyAllWindows()
            break

    if key == ord('q'):  # q harfine basıldığı zaman program sonlandırılıyor.
        print("Kamera kapatılıyor.")
        webcam.release()
        print("Kamera kapatıldı.")
        print("Program sonra erdi.")
        cv2.destroyAllWindows()
        break

f= open("ref_embed.pkl","wb")
pickle.dump(embed_dictt,f)
f.close()