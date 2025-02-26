import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from_addr = ''
email_list = ['']
subject = 'Allure report'
content = 'Allure Report Results'
password = ''
server = smtplib.SMTP('smtp', 587)
server.starttls()

server.login(from_addr, password)
print("email login successfully....")

for persons in email_list:
  msg = MIMEMultipart()
  msg['From'] = from_addr
  msg['To'] = persons
  msg['Subject'] = subject
  body = MIMEText(content, 'plain')
  msg.attach(body)
  attachmentPath = "allure-results.zip"

  try:
        with open(attachmentPath, "rb") as attachment:
                p = MIMEApplication(attachment.read(),_subtype="zip")
                p.add_header('Content-Disposition', "attachment; filename= %s" % attachmentPath.replace(attachmentPath,"reports.zip"))
                msg.attach(p)
  except Exception as e:
        print(str(e))

  server.send_message(msg, from_addr=from_addr, to_addrs=persons)
  print(f"email sent successfully to {persons}")
