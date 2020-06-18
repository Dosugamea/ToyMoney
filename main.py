from fastapi import FastAPI
from routers import airdrops, machines, products, transactions, wallets

app = FastAPI()


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
    wallets.router,
    prefix="/wallets",
    responses={404: {"description": "Not found"}},
)
