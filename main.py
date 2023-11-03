import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse

from endpoints import users, auth, groups, categories, homeworks, points, chat
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "http://localhost",
]

app = FastAPI(title="Headman FastAPI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


main_router = APIRouter()

main_router.include_router(auth.router, prefix="/auth", tags=["auth"])
main_router.include_router(users.router, prefix="/users", tags=["users"])
main_router.include_router(groups.router, prefix="/groups", tags=["groups"])
main_router.include_router(categories.router, prefix="/categories", tags=["categories"])
main_router.include_router(homeworks.router, prefix="/homeworks", tags=["homeworks"])
main_router.include_router(points.router, prefix="/points", tags=["points"])
main_router.include_router(chat.router, prefix="/chat", tags=["chat"])

app.include_router(main_router, prefix="/api")

app.include_router(chat.router, prefix="/chat")
# @app.on_event("startup")
# async def startup():
#     await database.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


@app.get("/", response_class=RedirectResponse)
async def read_items():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
