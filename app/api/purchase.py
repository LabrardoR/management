"""
purchase.py
购买相关接口，涉及到付款的接口先存在这里（还没完善）
"""
from datetime import datetime, timedelta

from anyio import current_time
from fastapi import APIRouter, HTTPException, Depends, Request, Response
from tortoise import Tortoise
from tortoise.backends.asyncpg.client import F

from app.models.user import User
from app.schemas.purchase import PurchaseVIPRequest, PurchasePointsRequest
from app.utils.redis import get_redis
from app.utils.user import get_current_user, get_code, check_code, redis_client

redis_client = get_redis()
# 生成路由对象
api_pay = APIRouter()

@api_pay.post("/purchase_vip", description="购买365元套餐")
async def purchase_vip(purchase_vip_request : PurchaseVIPRequest, request: Request, current_user: User = Depends(get_current_user)):
    days = purchase_vip_request.days

    if not days or not type:
        raise HTTPException(status_code=400, detail="信息错误！")


    # todo 支付
    # if 支付失败:
    #     raise HTTPException(status_code=400, detail="用户取消支付")


    # 支付成功
    # 写入 100 积分
    await User.filter(id=current_user.id).update(points = current_user.points + 1000)
    # 写入 5 场景
    result_1 = redis_client.set(str(current_user.id) + ":scene:", 5)
    # 写入 1 声音
    result_2 = redis_client.set(str(current_user.id) + ":video:", 1)

    # if not result:
    #     raise HTTPException(status_code=500, detail="服务器内部错误，支付失败")

    return {"message" : "支付成功"}


@api_pay.post("/purchase_points", description="购买积分")
async def purchase_points(purchase_point_request: PurchasePointsRequest, request: Request, current_user: User = Depends(get_current_user)):
    points = purchase_point_request.points
    if not points:
        raise HTTPException(status_code=400, detail="信息错误！")

    # 假定此处调用了其他函数，进行了支付
    # 这里的支付逻辑可以是调用第三方支付接口，然后确认支付成功。

    try:
        # 开始事务
        async with Tortoise.transaction():
            # 假设支付成功，开始更新用户积分
            new_points = points + current_user.points
            result = await User.filter(id=current_user.id).update(points=new_points)

            if not result:
                raise HTTPException(status_code=500, detail="服务器内部错误，购买失败")

        # 提交事务（在事务块结束后自动提交）
        return {"message": "支付成功"}

    except Exception as e:
        # 如果有异常发生，自动回滚事务
        raise HTTPException(status_code=500, detail=f"购买积分过程中发生错误: {str(e)}")
