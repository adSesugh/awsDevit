from setup import check_access
from botocore.exceptions import ClientError
from forms import ActionModel
import logging

# Set up our logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class EC2:
    def __init__(self):
        self.session = check_access()

    def list_instances(self):
        """
            Get list of ec2 instances
        """
        try:
            ec2 = self.session.client('ec2')
            instances = ec2.describe_instances()
        except ClientError as error:
            if error.response['Error']['Code'] == 'LimitExceededException':
                logger.warn('API call limit exceeded; backing off and retrying...')
            else:
                raise error

        return instances

    def mark_instance_as(self, instanceIds, action):
        """
            Method to perform start, stop, terminate instance
        """
        try:
            ec2 = self.session.client('ec2')
            # loop through the instance ids
            for instance in instanceIds:
                # check the action state and issue appropriate command to be executed on the specified instance
                if action is ActionModel.Start:
                    ec2.start_instances(instance)
                elif action is ActionModel.Stop:
                    ec2.stop_instances(instance)
                elif action is ActionModel.Terminate:
                    ec2.terminate_instance(instance)
            
        except ClientError as error:
            if error.response['Error']['Code'] == 'LimitExceededException':
                logger.warn('API call limit exceeded; backing off and retrying...')
            else:
                raise error

        return {"message": "Command sent successfully"}