from fastapi import Body, Form, FastAPI

from setup import check_access
from forms import AccountModel, ActionModel
from ec2 import EC2
from account import Account

app = FastAPI()
session = check_access() # root

@app.get('/')
async def root():
    response = {'message': 'Hello AWSDevit'}
    return response

@app.get('/accounts/')
async def get_accounts():
    accInstance = Account()
    accounts = accInstance.get_accounts()
    return accounts

@app.post('/accounts/')
async def add_account(account: AccountModel = Body(embed=True)):
    accInstance = Account()
    response = accInstance.create_account(account)
    return response

@app.get('/accounts/{key}')
async def mark_as_active(key: str):
    accInstance = Account()
    response = accInstance.mark_account_active(key)
    return response

@app.get('/dashboard/')
async def cost_explorer():
    billing = session.client('ce')
    response = billing.get_cost_and_usage(
        TimePeriod={
            'Start': '2022-09-01',
            'End': '2022-09-30'
        },
        Granularity='MONTHLY',
        Metrics=['NormalizedUsageAmount'],
    )
    return response

@app.get('/list-instances/')
async def get_all_ec2():
    ec2Instance = EC2()
    return ec2Instance.list_instances()

@app.get('/create-ec2-instance')
async def create_ec2_instance():
    ec2Instance = EC2()
    return ec2Instance.create_instance()

@app.get('/get_ec2-instance/{instanceId}/')
async def get_single_instance(instanceId: str):
    ec2Instance = EC2()

    return ec2Instance.get_single_instance(instanceId)

@app.put('/ec2-operation/{action}/')
async def ec2_actions(instanceIds: str, action: ActionModel):
    ids = instanceIds.split(',')
    ec2Instance = EC2()
    return ec2Instance.mark_instance_as(ids, action)

