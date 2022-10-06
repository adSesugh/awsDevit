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
        self.ec2 = self.session.client('ec2')

    def list_instances(self):
        """
            Get list of ec2 instances
        """
        try:
            instances = self.ec2.describe_instances()
        except ClientError as error:
            if error.response['Error']['Code'] == 'LimitExceededException':
                logger.warn('API call limit exceeded; backing off and retrying...')
            else:
                raise error

        return instances

    def create_instance(self):
        """
            Method to create an instance using a predefined paramenters
        """
        try:
            image_id = self.get_ami_id()
            instance = self.ec2.run_instances(ImageId=image_id,MinCount=1,MaxCount=1,\
                    InstanceType="t3.micro"
                )

            print(instance)
        except ClientError as error:
            raise error

        return instance

    def get_single_instance(self, instanceId):
        """
            Method to pull a single instance details
            Parameters: instanceId - required
        """
        try:
            instance = self.ec2.describe_instances(InstanceIds=[instanceId])
        except ClientError as error:
            raise error

        return instance

    def mark_instance_as(self, instanceIds, action):
        """
            Method to perform start, stop, terminate instance
        """
        try:
            # loop through the instance ids
            for instance in instanceIds:
                # check the action state and issue appropriate command to be executed on the specified instance
                if action is ActionModel.Start:
                    self.ec2.start_instances(InstanceIds=[instance])
                elif action is ActionModel.Stop:
                    self.ec2.stop_instances(InstanceIds=[instance])
                elif action is ActionModel.Terminate:
                    self.ec2.terminate_instance(InstanceIds=[instance])
            
        except ClientError as error:
            if error.response['Error']['Code'] == 'LimitExceededException':
                logger.warn('API call limit exceeded; backing off and retrying...')
            else:
                raise error

        return {"message": "Command sent successfully"}

    def create_image(self):
        image = self.ec2.create_image(InstanceId='i-1234567890abcdef0', Name='AWSDevit')
        return image

    def get_ami_id(self):
        """
            Method to retrieve an AMI ID
        """
        response = self.ec2.describe_images(Owners=["amazon"], Filters=[{'Name': 'name', 'Values': ['amzn-ami-hvm-*']}])
        return response['Images'][0]['ImageId'] 