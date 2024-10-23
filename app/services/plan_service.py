from app.services import *
from app.models import SubscriptionPlan


subscription_plans_filter_dict = {

}


async def get_subscription_plan_by_id(id):
    obj = await SubscriptionPlan.objects.filter(id=id).afirst()
    return obj
