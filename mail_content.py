from imapclient import IMAPClient
import datetime
from email import message_from_bytes
from email.header import decode_header
import re
# 解码主题
def decode_subject(subject):
    decoded_str = decode_header(subject)
    subject_str = ''
    for text, charset in decoded_str:
        if charset:
            subject_str += text.decode(charset)
        else:
            subject_str += text if isinstance(text, str) else text.decode('utf-8')
    return subject_str

# 提取邮件正文
def extract_body_from_email(email_message):
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == 'text/plain':
                charset = part.get_content_charset()
                if charset is None:
                    charset = 'utf-8'
                return part.get_payload(decode=True).decode(charset)
    else:
        return email_message.get_payload()


def clean_email_body(email_body):
    # 删除 "=20" 这种无用字符
    cleaned_body = email_body.replace("=20", "")
    
    # 删除网址
    cleaned_body = re.sub(r'http\S+', '', cleaned_body)
    cleaned_body = re.sub(r'https\S+', '', cleaned_body)
    # 删除换行符和回车符
    cleaned_body = cleaned_body.replace("\n", "").replace("\r", "")
    
    return cleaned_body

   

# 定义时间范围
start_time = datetime.time(hour=18, minute=0) 
end_time = datetime.time(hour=19, minute=0)
current_date = datetime.datetime.now().date()  
start_datetime = datetime.datetime.combine(current_date, start_time)  
end_datetime = datetime.datetime.combine(current_date, end_time)
username  = "pdwjzyjy9408@163.com"
password  = "PCGNNEEMDDISRWUI"
# 当前日期
current_date = datetime.date(2023, 9, 2)

with IMAPClient(host='imap.163.com') as client:
    client.login(username, password)
    client.id_({"name": "IMAPClient", "version": "2.1.0"})
    client.select_folder('INBOX')

    # 搜索今天的邮件
    messages = client.search(['ON', current_date])

    # 获取邮件的内部日期和正文
    response = client.fetch(messages, ['INTERNALDATE', 'BODY[]'])

    for msgid, data in response.items():
        internal_date = data[b'INTERNALDATE']
        email_message = message_from_bytes(data[b'BODY[]'])
        # print(internal_date,type(internal_date))
        # 解析邮件的内部日期来获取时间
        # email_time = internal_date.datetime().time()

        # 检查时间是否在指定的范围内
        if start_datetime <= internal_date <= end_datetime:
            subject = email_message['Subject']
            body = email_message.get_payload()
            # print('正文')
            # print(f"ID: {msgid}, Subject: {decode_subject(subject)}, Body: {body}")
            # 将所有正文内容放到一个字符串中，
            mail_content = extract_body_from_email(body[0])
            mail_content = clean_email_body(mail_content)
            print(mail_content)