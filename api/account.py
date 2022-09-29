# import all libraries
from deta import Deta
from botocore.exceptions import ClientError
from forms import StatusModel
import logging
from dotenv import dotenv_values

# Set up our logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
config = dotenv_values(".env")

class Account:
    def __init__(self):
        self.deta = Deta(config.DATABASE_KEY)
        self.accounts = self.deta.Base('accounts')

    def create_account(self, formData):
        """
            Add existing AWS account credentials to the app \
            Parameters:\
                - name, accessId, secretKey, region, status
        """ 
        try:
            # check whether the posted record status is active
            if formData.status is StatusModel.active:
                # collect all records whose status is active 
                active_account = self.accounts.fetch({"status": "active"})
                # loop through the active records
                for acc in active_account.items:
                    # set the record to inactive
                    self.accounts.update(updates={
                        "status": StatusModel.inactive
                    }, key=acc['key'])

            # create a new account record
            account = self.accounts.insert({
                        "name": formData.name,
                        "accessId": formData.accessId,
                        "secretKey": formData.secretKey,
                        "region": formData.region,
                        "status": formData.status
                    })

        except ClientError as error:
            if error.response['Error']['Code'] == 'LimitExceededException':
                logger.warn('API call limit exceeded; backing off and retrying...')
            else:
                raise error

        return account

    def get_accounts(self):
        """
            A method to get all registered AWS account credentials
        """
        try:
            # fetch all account records
            accounts = self.accounts.fetch()
        except ClientError as error:
            if error.response['Error']['Code'] == 'LimitExceededException':
                logger.warn('API call limit exceeded; backing off and retrying...')
            else:
                raise error

        return accounts

    def mark_account_active(self, keyId: str):
        """
            The method changes every other record without the specified to inactive and activating the queried record
            Parameter key is required
        """
        try:
            if(keyId is not None):
                # collect records whose status is active
                active_account = self.accounts.fetch({"status": "active"})
                
                # loop through the active record and set them to inactive
                for acc in active_account.items:
                    self.accounts.update(updates= {
                        "status": StatusModel.inactive
                    }, key = acc['key'])

                # set the specified record to active
                self.accounts.update(updates={
                    "status": StatusModel.active
                }, key=keyId)

        except ClientError as error:
            if error.response['Error']['Code'] == 'LimitExceededException':
                logger.warn('API call limit exceeded; backing off and retrying...')
            else:
                raise error

        return {"message": "Status Updated successfully"}