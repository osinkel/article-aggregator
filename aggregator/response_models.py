from enum import Enum
from pydantic import BaseModel

class Status(Enum):
    OK = 'OK'
    ERROR  = 'ERROR'
    ALREADY_EXIST = 'ALREADY_EXIST'
    USER_NOT_AUTHENTICATED = 'USER_NOT_AUTHENTICATED'
    BAD_PARSER_NAME = 'BAD_PARSER_NAME'

class ResponseMessage(BaseModel):
    status: Status
    message: str