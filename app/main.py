import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.routes import router

def create_app() -> FastAPI:
    """Creates and configures the FastAPI application.
    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    app = FastAPI(
        title="University Degree Recommendation API",
        description="API for recommending university degrees based on user preferences and scraping data from various sources."
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    return app

app = create_app()

if __name__ == "__main__":
    """
    Entry point for running the FastAPI application.
    Starts the application on host
    """
    uvicorn.run(app, host="0.0.0.0", port=8003)
