import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from loguru import logger
from tqdm import tqdm


MESSAGE_TEMPLATE =\
    "Добрый день\n" \
    "\n" \
    "ТЕКСТ\n" \
    "\n" \
    "Best regards,\n"\
    "EUGENE ROSLYAKOV\n"   # noqa

# setup the parameters of the message
DEFAULT_CC = "CC"
PASSWORD = "PASSWORD"
USERNAME = "USERNAME"
SMTP_SERVER = "SMTP_SERVER"
SERVER_PORT = "PORT"
DEFAILT_FROM = "FROM"
DEFAULT_SUBJECT = "SUBJECT"
USER_NAME_FILE = "./test_users.txt"


def read_users(file_name):
    ret = []

    with open(file_name, 'r') as read_file:
        for line in read_file:
            to_user = str(line).strip() + "@sigma.software"
            logger.debug("to_user '{}'".format(to_user))
            ret.append(to_user)

    return ret


def send_mail_to_recipient(server, recipient_address, pbar):
    # create message object instance
    pbar.set_description("processing '{}'".format(recipient_address))

    msg = MIMEMultipart()

    msg['From'] = DEFAILT_FROM
    msg['Subject'] = DEFAULT_SUBJECT
    msg['CC'] = DEFAULT_CC
    msg.attach(MIMEText(MESSAGE_TEMPLATE, 'plain'))

    server.sendmail(msg['From'], [recipient_address, DEFAULT_CC], msg.as_string())


def main():
    recipients_list = read_users(USER_NAME_FILE)

    server = smtplib.SMTP('{}: {}'.format(SMTP_SERVER, SERVER_PORT))
    server.starttls()
    server.login(USERNAME, PASSWORD)

    try:
        pbar = tqdm(recipients_list)
        for recipient in pbar:
            send_mail_to_recipient(server, recipient, pbar)

    except BaseException as e:
        logger.exception("error sending message: '{}'".format(e))

    finally:
        server.quit()

    return 0


if __name__ == "__main__":
    res = main()
    exit(res)
