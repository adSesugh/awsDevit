from pydantic import BaseModel, Field
from typing import List, Union
from enum import Enum

class StatusModel(str, Enum):
    inactive = 'inactive'
    active = 'active'

class AccountModel(BaseModel):
    name: str
    accessId: str
    secretKey: str
    region: str
    status: StatusModel

class ActionModel(str, Enum):
    Start = 'Start',
    Stop = 'Stop',
    Terminate = 'Terminate'
