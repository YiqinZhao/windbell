import json
import pystache

from windbell.utils import config
from windbell.mail import send_email


def send(subject, template, data,
         attachment=(), receiver=None, smtp_server=None,
         sender_email=None, sender_pwd=None, sender_name=None):
    """send email

    Parameters
    ----------
    subject : str
        email subject
    template : str
        template text
    data : dict
        JSON data
    attachment : tuple, optional
        attachments (the default is ())
    receiver : str, optional
        specific email receiver to override default (the default is None)
    smtp_server : str, optional
        SMTP server (the default is None)
    sender_email : str, optional
        smtp server [server:port] (the default is None)
    sender_pwd : str, optional
        sender password (the default is None)
    sender_name : str, optional
        sender name (the default is None)
    """

    conf = {v: config[v]['value'] for v in config}
    content = pystache.render(template, data)

    conf['default_receiver'] = receiver if receiver else conf['default_receiver']
    conf['smtp_server'] = smtp_server if smtp_server else conf['smtp_server']
    conf['sender_email'] = sender_email if sender_email else conf['sender_email']
    conf['sender_pwd'] = sender_pwd if sender_pwd else conf['sender_pwd']
    conf['sender_name'] = sender_name if sender_name else conf['sender_name']

    send_email(subject, content,
               attachment=attachment,
               receiver=receiver,
               config=conf)
