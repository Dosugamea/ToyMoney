from fastapi import FastAPI
from routers import airdrops, machines, products, transactions, users

app = FastAPI(
    title='ToyMoneyServer',
    description='Build and use toy money easily.',
    version='0.1'
)


@app.get('/')
async def hello():
    return {"status": 200, "message": "API is running."}


app.include_router(
    airdrops.router,
    prefix="/airdrops",
    responses={404: {"description": "Not found"}},
)

app.include_router(
    machines.router,
    prefix="/machines",
    responses={404: {"description": "Not found"}},
)

app.include_router(
    products.router,
    prefix="/products",
    responses={404: {"description": "Not found"}},
)

app.include_router(
    transactions.router,
    prefix="/transactions",
    responses={404: {"description": "Not found"}},
)

app.include_router(
    users.router,
    prefix="/users",
    responses={404: {"description": "Not found"}},
)
