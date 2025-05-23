import uvicorn
from tg_bot.bot import main
from model.char_constructor import CharConstructor


if __name__ == "__main__":
    uvicorn.run(
        app="rnd_fastapi_server.server:app",
        host="localhost",   
        port=8000,
        reload=True,
    )
main()