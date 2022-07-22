import hashlib
from datetime import datetime

def crypt(password):
    """
    Fonction qui crypte un mot de passe
    :param password: (str) mot de passe
    :return: (str) le hash du mot de passe
    """
    hash_pwd = hashlib.new('sha256')
    hash_pwd.update(password.encode())
    hash_pwd = hash_pwd.hexdigest()
    return hash_pwd

def date_in_str():
    now = datetime.now()
    date_format_str = "%d/%m/%Y à %H:%M:%S.%f"
    date_now = now.strftime(date_format_str)
    return date_now

def str_in_date(date):
    date_format_str = "%d/%m/%Yà%H:%M:%S.%f"
    return  datetime.strptime(date, date_format_str)