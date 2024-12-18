"""
schemas/purchase.py
购买相关的数据模型
"""
from pydantic import BaseModel, EmailStr, UUID4, field_validator
from typing import Optional


class PurchaseVIPRequest(BaseModel):
    days: Optional[int] # 周卡、月卡、季卡、年卡
    type: Optional[str] # 购买的VIP类型


class PurchasePointsRequest(BaseModel):
    points: Optional[int] # 购买的积分数量

class CAKEYRequest(BaseModel):
    password: Optional[str]

