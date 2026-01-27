import structlog
from fastapi import FastAPI

from housing_prices.api.routers import router
from housing_prices.logs import configure_structlog
from housing_prices.settings import IS_LOCAL

# Setup app
is_debug = IS_LOCAL
configure_structlog(is_debug=is_debug)
logger = structlog.get_logger("app")
app = FastAPI(
    title="House prices predictor",
    description="API for predicting house prices",
    version="0.1.0",
    debug=is_debug,
)
logger.info("FastAPI app created")

# Add API routes
app.include_router(router)
logger.info("FastAPI routers added")

# For local debugging
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
