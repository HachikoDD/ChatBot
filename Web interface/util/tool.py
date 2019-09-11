from hashlib import md5
from random import Random
import time
import base64
import hmac
import smtplib
from email.mime.text import MIMEText
from util.timeUtil import local_time

def create_salt(length=4):
    salt = ''
    char_list = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    count = len(char_list) - 1
    random = Random()
    for i in range(length):
        salt += char_list[random.randint(0, count)]
    return salt


def create_md5(pwd, salt):
    md = md5()
    md.update((pwd + salt).encode('utf-8'))
    return md.hexdigest()


def generate_token(k, expire=3600):
    s = str(time.time() + expire)
    byte = s.encode("utf-8")
    sha1_tshexstr = hmac.new(k.encode("utf-8"), byte, 'sha1').hexdigest()
    token = s + ':' + sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")


def certify_token(k, token):
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return False
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        return False
    known_sha1_tsstr = token_list[1]
    sha1 = hmac.new(k.encode("utf-8"), ts_str.encode('utf-8'), 'sha1')
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != known_sha1_tsstr:
        return False
    return True

def send_email(email, message):
    smtpserver = "smtp.gmail.com"
    smtpport = 465
    from_mail = "chalkrobot9900@gmail.com"
    to_mail = [email]
    password = "clxaaqshduagnyap"  # 16位授权码
    #hml
    msg = MIMEText(message, "html")
    msg['Subject'] = "[Auto Reply]Answer from Chalk Robot"
    msg['From'] = "Chalk Robot"
    msg['To'] = email
    try:
        smtp = smtplib.SMTP_SSL(smtpserver, smtpport)
        smtp.login(from_mail, password)
        smtp.sendmail(from_mail, to_mail, msg.as_string())
    except(smtplib.SMTPException) as e:
        print(e.message)
    finally:
        smtp.quit()

if __name__ == "__main__":
    question = "1"
    answer = "2"
    content = "Dear student, you have a new response for your question from Chalk Robot.\n\nQuestion: " \
              + question + "\nAnswer: " + answer + "\n\nDelivered by Chalk Robot " + local_time()
    send_email("chalkrobot9900@gmail.com", content)
