import os
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


from_addr = os.getenv("MAIL_USER")
email_list = ['']
subject = 'Allure report'
password = os.getenv("MAIL_PASSWORD")
server = smtplib.SMTP('smtp.office365.com', 587)
server.starttls()
SUMMARY_FILE = "target/allure-report/widgets/summary.json"

server.login(from_addr, password)
print("email login successfully....")



try:
    with open(SUMMARY_FILE, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("Error: summary.json not found. Ensure Allure report is generated.")
    exit(1)

passed = data["statistic"]["passed"]
failed = data["statistic"]["failed"]
broken = data["statistic"]["broken"]
skipped = data["statistic"]["skipped"]
total = data["statistic"]["total"]


email_body = f"""
Allure Test Report Summary:

📌 **Total Tests**: {total}
✅ **Passed**: {passed}
❌ **Failed**: {failed}
⚠️ **Broken**: {broken}
🚧 **Skipped**: {skipped}

📊 **Success Rate**: {round((passed / total) * 100, 2)}% 

🔗 View full report: http://autotest-develop.avis2dev.e-taxes.gov.az http://autotest-develop.avis2dev.e-taxes.gov.az/reports.html
"""


for persons in email_list:
  msg = MIMEMultipart()
  msg['From'] = from_addr
  msg['To'] = persons
  msg['Subject'] = subject
  body = MIMEText(email_body, 'plain')
  msg.attach(body)


  #attachmentPath = "allure-results.zip"

  #try:
  #      with open(attachmentPath, "rb") as attachment:
  #              p = MIMEApplication(attachment.read(),_subtype="zip")
  #              p.add_header('Content-Disposition', "attachment; filename= %s" % attachmentPath.replace(attachmentPath,"reports.zip"))
  #              msg.attach(p)
  #except Exception as e:
  #      print(str(e))

  server.send_message(msg, from_addr=from_addr, to_addrs=persons)
  print(f"email sent successfully to {persons}")
  
server.quit()
