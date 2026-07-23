"""
Main entry point for running the application
"""

import os
import uvicorn
from backend.app.config import settings


if __name__ == "__main__":
    use_reload = settings.debug_enabled and os.name != "nt"
    uvicorn.run(
        "backend.app.main:app",
        host=settings.host,
        port=settings.port,
        workers=settings.workers,
        reload=use_reload,
        log_level=settings.log_level.lower(),
    )
