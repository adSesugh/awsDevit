import boto3
from deta import Deta
from dotenv import dotenv_values

config = dotenv_values(".env")

def check_access():
    """
        Grab active credentials to start
    """
    project = Deta(config['DATABASE_KEY'])
    creds = project.Base('accounts')
    credentials = creds.fetch({"status": 'active'})

    for credential in credentials.items:
        pass

    session = boto3.Session(
        #aws_access_key_id=credential['accessId'],
        #aws_secret_access_key=credential['secretKey'],
        aws_access_key_id=config['Access_Key_ID'],
        aws_secret_access_key=config['Secret_Access_Key'],
    )

    return session 