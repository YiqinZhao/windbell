import os
import smtplib
import pystache
from datetime import datetime

from premailer import transform
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def submit(windfile):
    config = windfile.config.value

    if 'attachement' in config:
        attachment = [open(v, 'r').read() for v in config['attachement']]
    else:
        attachment = []

    t = config['to']
    receiver_list = t if type(t) == list else [t]

    for receiver in receiver_list:
        content, cfg = windfile.render(
            data_injected={
                'meta': {
                    'to': receiver,
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        )

        content = transform(
            content,
            cssutils_logging_level=None
        )

        send_email(cfg['author'],
                   receiver,
                   cfg['subject'],
                   content,
                   attachment=attachment)


def send_email(author, to, subject, content, attachment=()):
    """
    Send Email
    :param subject: email subject
    :param content: email content, string
    :param attachment: attachment, string
    :param email_receiver: optional receiver. Use env if none.
    :return:
    """
    host, port = author['smtp_server'].split(':')

    smtp = smtplib.SMTP_SSL(host=host, port=port)
    smtp.login(author['address'], author['password'])

    from_str = ''
    if author['address'] == author['name']:
        from_str = author['address']
    else:
        from_str = '%s <%s>' % (author['name'], author['address'])

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_str
    msg['To'] = to

    # Email body
    msg.attach(MIMEText(content, 'html', _charset='utf-8'))

    # Email Attachments
    for item in attachment:
        att = MIMEText(item['value'], _charset='utf-8')
        att['Content-Disposition'] = 'attachment; filename=' + item['name']
        msg.attach(att)

    # Send email
    smtp.sendmail(author['address'],
                  to,
                  msg.as_string().encode('utf-8'))
