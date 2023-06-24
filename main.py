import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse

from endpoints import users, auth, groups, categories, homeworks, points


app = FastAPI(title="Headman FastAPI")
main_router = APIRouter()

main_router.include_router(auth.router, prefix="/auth", tags=["auth"])
main_router.include_router(users.router, prefix="/users", tags=["users"])
main_router.include_router(groups.router, prefix="/groups", tags=["groups"])
main_router.include_router(categories.router, prefix="/categories", tags=["categories"])
main_router.include_router(homeworks.router, prefix="/homeworks", tags=["homeworks"])
main_router.include_router(points.router, prefix="/services", tags=["points"])

app.include_router(main_router, prefix="/api")


# @app.on_event("startup")
# async def startup():
#     await database.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


@app.get("/", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <body bgcolor="#1c1c1c">
            <p color="white"><a href="http://127.0.0.1:8000/docs">FastAPI DOCS</a></p>
        </body>
    </html>
    """


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
