# _*_ coding:utf-8 _*_

"""
    notes send email
    11003@sangfor.com
"""
import pythoncom
from win32com.client import makepy, DispatchEx

from conf import config
from logger_util import logger


def send_mail(server, db_file, reciver_list, subject, body=None):
    pythoncom.CoInitialize()
    makepy.GenerateFromTypeLibSpec('Lotus Domino Objects')
    logger.info('init mail client')
    session = DispatchEx('Notes.NotesSession')
    db = session.GetDatabase(server, db_file)
    if not db.IsOpen:
        logger.info('open mail db')
        try:
            db.OPENMAIL
        except Exception as e:
            logger.info('could not open database')

    logger.info("Send email ing")
    doc = db.CREATEDOCUMENT
    doc.sendto = reciver_list
    doc.Subject = subject
    if body:
        doc.Body = body
    doc.SEND(0, reciver_list)
    logger.info('send success')


def send_message(recivers, title, body):
    """
    note发送邮件
    :param recivers:
    :param title:
    :param body:
    :return:
    """
    try:
        server = config.mail_server
        db_file = config.mail_user
        send_mail(server, db_file, recivers, title, body)
    except Exception as e:
        logger.exception(e)
