from api.api import app
from pathlib import Path
import uvicorn
import config

if __name__ == "__main__":

    uvicorn.run(
        f"{Path(__file__).stem}:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=config.DEBUG,
        log_level="debug",
        workers=2
    )