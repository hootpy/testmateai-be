from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.utils.dashboard import convert_dashboard_to_response
from app.core.depends.get_current_user import get_current_user
from app.core.depends.get_session import get_session
from app.crud.dashboard import DashboardCrud
from app.model.model import User

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
)


@router.get("")
async def get_dashboard(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Get comprehensive dashboard data
    """
    # Get dashboard data
    dashboard_data = await DashboardCrud.get_dashboard_data(db, current_user.id)

    # Convert to response format
    dashboard_response = convert_dashboard_to_response(dashboard_data)

    return {"success": True, "data": dashboard_response}
