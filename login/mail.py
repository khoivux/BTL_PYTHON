import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    # Cấu hình tài khoản gửi
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "kuboyhello1@gmail.com"
    app_password = "ljhs yvln wtdu szwt"

    # Tạo nội dung email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject

    # Thêm nội dung email
    msg.attach(MIMEText(body, "plain"))

    try:
        # Kết nối đến server SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Bật chế độ bảo mật TLS
        server.login(sender_email, app_password)
        
        # Gửi email
        server.send_message(msg)
        print("Email đã được gửi thành công!")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi gửi email: {e}")
    finally:
        server.quit()
        