import asyncio
import aiohttp
import logging
import random
import os
from tasksio import TaskPool

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] -> %(message)s",
    datefmt="%I:%M:%S",
)

if os.name == "posix":
    os.system("clear")
else:
    os.system("cls")

class Checker(object):

    def __init__(self):

        self.tasks = int(input("Tasks: "))

        self.tokens = []

        for f in open("data/tokens.txt"):
            self.tokens.append(f.replace("\n", ""))

        with open("data/proxies.txt", encoding="utf-8") as f:
            self.proxies = [i.strip() for i in f]

    async def check_tokens(self, token: str):
        try:
            async with aiohttp.ClientSession(headers={"Authorization": token}) as session:
                proxy_format = "http://{}".format(random.choice(self.proxies))
                async with session.get("https://discordapp.com/api/v9/users/@me/library", proxy=proxy_format) as response:
                    if "You need to verify your account in order to perform this action." in await response.text():
                        logging.info("Phone Locked -> {}".format(token))
                        f = open("data/tokens [LOCKED].txt", "a+")
                        f.write("{}\n".format(token))
                        f.close()
                    else:
                        async with session.get("https://discord.com/api/v9/users/@me", proxy=proxy_format) as response:
                            if response.status == 200:
                                logging.info("Working -> {}".format(token))
                                f = open("data/tokens [WORKING].txt", "a+")
                                f.write("{}\n".format(token))
                                f.close()
                            else:
                                logging.info("Invalid -> {}".format(token))
                                f = open("data/tokens [INVALID].txt", "a+")
                                f.write("{}\n".format(token))
                                f.close()
        except Exception:
            pass
    
    async def start(self):
        async with TaskPool(self.tasks) as pool:
            for token in self.tokens:
                await pool.put(self.check_tokens(token))

if __name__ == "__main__":
    client = Checker()
    asyncio.run(client.start())
