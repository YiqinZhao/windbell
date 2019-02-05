import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(subject, content, attachment=(), receiver=None, config={}):
    """
    Send Email
    :param subject: email subject
    :param content: email content, string
    :param attachment: attachment, string
    :param email_receiver: optional receiver. Use env if none.
    :return:
    """
    host, port = config['smtp_server'].split(':')
    to = config['default_receiver'] if receiver is None else receiver

    smtp = smtplib.SMTP_SSL(host=host, port=port)
    smtp.login(config['sender_email'], config['sender_pwd'])

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = '%s <%s>' % (config['sender_name'], config['sender_email'])
    msg['To'] = to

    # Email body
    msg.attach(MIMEText(content, 'html', _charset='utf-8'))

    # Email Attachments
    for item in attachment:
        att = MIMEText(item['value'], _charset='utf-8')
        att['Content-Disposition'] = 'attachment; filename=' + item['name']
        msg.attach(att)

    smtp.sendmail(config['sender_email'],
                  to,
                  msg.as_string().encode('utf-8'))


if __name__ == '__main__':
    send_email('Email Test', 'Email Test')
