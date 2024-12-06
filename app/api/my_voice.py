"""
我的数字人接口
"""
import datetime

from fastapi import APIRouter, HTTPException, Depends, Request, Response
from tortoise.exceptions import IntegrityError

from app.models.user import User
from app.schemas.user import UserRegister, UserCodeLogin, UserPasswordLogin, UserReset, UserResponse, UserUpdate

import hashlib
import random
import re