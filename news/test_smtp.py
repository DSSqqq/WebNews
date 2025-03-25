import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Данные отправителя и получателя
sender_email = "danilka780@gmail.com"
receiver_email = "danilka780@gmail.com"
password = "fsyn yumu hilq jpzj"

# Создаём письмо
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = "Тестовое письмо"
# Тело письма
body = "Привет! Это тестовое письмо."
msg.attach(MIMEText(body, "plain", "utf-8"))

try:
    # Подключаемся к серверу Gmail
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)

    # Отправляем письмо
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

    print("Письмо успешно отправлено!")

except Exception as e:
    print(f"Ошибка: {e}")