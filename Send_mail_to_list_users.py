from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from loguru import logger
from tqdm import tqdm



MESSAGE_TEMPLATE =\
    "Добрый день\n" \
    "\n" \
    "В короткий промежуток времени истекает срок действия сертификатов подписи кода ESET SHA1 и SHA256.\n" \
    "Чтобы продолжить получать обновления, пользователям более старых продуктов ESET необходимо выполнить обновление\n" \
    "до версии, которая поддерживает плавное переключение сертификатов." \
    "\n"\
    "https://support.eset.com/ca7304/?locale=en_US&viewlocale=en_US\n"\
    "\n" \
    "SC планирует обновить антивирус на вашем компьютере \n" \
    "Процесс обновления происходит автоматически и в фоновом режиме, от вас нужна только перезагрузка\n " \
    "компьютера после оповещения антивируса, либо в удобное время. В процессе обновления компьютер может немного тормозить (+- 10 минут)\n"\
    "\n"\
    "Когда это будет удобно?\n" \
    "\n"\
    "Спасибо\n" \
    "\n" \
    "Best regards,\n"\
    "EUGENE ROSLYAKOV\n"   # noqa

# setup the parameters of the message
DEFAULT_CC = "soc@sigma.software"
PASSWORD = "PASSWORD"
USERNAME = "eugene.roslyakov"
DEFAILT_FROM = "eugene.roslyakov@sigma.software"
DEFAULT_SUBJECT = "ESET NOD32 Antivirus on your device is outdated"
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

    server = smtplib.SMTP('smtp.i.sigmaukraine.com: 2528')
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
