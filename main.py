import uvicorn
from tg_bot.bot import main

if __name__ == "__main__":
    uvicorn.run(
        app="rnd_fastapi_server.server:app",
        host="localhost",   
        port=8080,
        reload=True,
    )
#main()