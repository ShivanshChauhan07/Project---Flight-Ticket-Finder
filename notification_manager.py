import smtplib
my_email = "rajput3770@yahoo.com"
password = "rolwpndovctaxjwv"

class NotificationManager:
    def send_mail(self,message):
                with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
                    connection.starttls()
                    connection.login(user=my_email,password=password)
                    connection.sendmail(from_addr=my_email,to_addrs="python3770@gmail.com",msg="Subject:Flight Ticket Alert\n\n"
                                                                                               f"{message}")
