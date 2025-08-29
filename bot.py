from aiogram import Bot, Dispatcher, types
from fastapi import FastAPI, Request
import os
import uvicorn

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 8000))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

app = FastAPI()

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"You said: {message.text}")

@app.post(WEBHOOK_PATH)
async def webhook(req: Request):
    data = await req.json()
    update = types.Update(**data)
    await dp.process_update(update)
    return {"ok": True}

async def on_startup():
    await bot.set_webhook(f"https://my-telegram-bot-a86x.onrender.com{WEBHOOK_PATH}")

@app.on_event("startup")
async def startup():
    await on_startup()

if __name__ == "__main__":
    uvicorn.run(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
