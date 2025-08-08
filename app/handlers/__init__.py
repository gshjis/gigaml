from .auth import router as auth_router
from .tasks import router as task_router

routers = [task_router, auth_router]
__all__ = ["task_router", "auth_router"]
