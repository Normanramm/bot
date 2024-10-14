
# config.py
TOKEN = "<telegram-bot-token>"  # obtained from @BotFather
OPENAI_TOKEN = "<openai-api-key>"  # obtained from https://platform.openai.com/account/api-keys


# main.py
# Телеграм бот ChatGPT
import config
import logging
import openai
import asyncio
from gpytranslate import Translator

from aiogram import Bot, Dispatcher, executor, types

# log
logging.basicConfig(level=logging.INFO)

# init translator
t = Translator()

# init openai
openai.api_key = config.OPENAI_TOKEN

# init aiogram
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def gpt_answer(message: types.Message):
    # await message.answer(message.text)

    model_engine = "text-davinci-003"
    max_tokens = 128  # default 1024
    prompt = await t.translate(message.text, targetlang="en")
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt.text,
        max_tokens=max_tokens,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    await message.answer("ChatGPT: Генерирую ответ ...")
    translated_result = await t.translate(completion.choices[0].text, targetlang="ru")
    await message.answer(translated_result.text)

# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
