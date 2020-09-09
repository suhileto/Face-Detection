import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#projemizin bu sayfasında gerekli kullanıcıya mail gönderiyoruz.
#mail göndermek için yüz tanıma sistemi isimli bir mail adresi oluşturduk.
#smtp serverını kullanarak pythondaki smtp kütüphaneleri yardımıyla mailimizi gönderiyoruz.

def mesaj(isim):
    message= MIMEMultipart()
    message["From"]= "yuztanimasistemii@gmail.com" #gönderici mail adresimiz.
    message["To"]= "selinlb37@gmail.com" #alıcı mail adresimiz.
    message["Subject"]= "Yüz Tanıma Sistemi" #mail konusu.

    body= """
    {} kişisi algılandı.
    """.format(isim) #mail içeriğimiz.

    body_text= MIMEText(body,"plain")
    message.attach(body_text)

    mail= smtplib.SMTP("smtp.gmail.com",587) #server bilgilerimiz.
    mail.ehlo()
    mail.starttls()
    mail.login("yuztanimasistemii@gmail.com","123Pro456je") #gönderici mail adresimize bu fonksiyon üzerinden giriş yapıyoruz.
    mail.sendmail(message["From"], message["To"], message.as_string()) #mailimizi gönderiyoruz.

    print("{} kisisi algılandı.".format(isim))

    mail.close()