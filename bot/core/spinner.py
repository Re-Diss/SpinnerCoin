import asyncio
from random import randint
from datetime import datetime
from urllib.parse import unquote
import base64

import aiohttp
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from pyrogram import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered
from pyrogram.raw.functions.messages import RequestWebView

from bot.config import settings
from bot.core.headers import headers
from bot.utils import logger
from bot.exceptions import InvalidSession
from bot.utils.message_sender import msgcod


class Claimer:
    def __init__(self, tg_client: Client):
        self.session_name = tg_client.name
        self.tg_client = tg_client

    async def get_tg_web_data(self, proxy: str | None) -> str:
        if proxy:
            proxy = Proxy.from_str(proxy)
            proxy_dict = dict(
                scheme=proxy.protocol,
                hostname=proxy.host,
                port=proxy.port,
                username=proxy.login,
                password=proxy.password
            )
        else:
            proxy_dict = None

        self.tg_client.proxy = proxy_dict

        try:
            if not self.tg_client.is_connected:
                try:
                    await self.tg_client.connect()
                    rrs = False
                    msg = '/startapp r_3830128'
                    async for message in self.tg_client.get_chat_history('SpinnerCoin_bot'):
                        if message.text == msg:
                            rrs = True
                            break

                    if not rrs:
                        await self.tg_client.send_message('SpinnerCoin_bot', msg,
                                                          disable_notification=True)


                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise InvalidSession(self.session_name)

            web_view = await self.tg_client.invoke(RequestWebView(
                peer=await self.tg_client.resolve_peer('SpinnerCoin_bot'),
                bot=await self.tg_client.resolve_peer('SpinnerCoin_bot'),
                platform='android',
                from_bot_menu=False,
                url='https://spinner.timboo.pro'
            ))

            auth_url = web_view.url
            tg_web_data = unquote(
                string=auth_url.split('tgWebAppData=', maxsplit=1)[1].split('&tgWebAppVersion', maxsplit=1)[0])

            if self.tg_client.is_connected:
                await self.tg_client.disconnect()

            return tg_web_data

        except InvalidSession as error:
            raise error

        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error during Authorization: {error}")
            await asyncio.sleep(delay=randint(60, 120))

    async def get_data(self, http_client: aiohttp.ClientSession, tg_web_data: str):
        try:
            response = await http_client.post('https://api.timboo.pro/get_data', json={"initData": tg_web_data})
            response.raise_for_status()
            response_json = await response.json()

            return response_json
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when get user data: {error}")
            await asyncio.sleep(delay=randint(60, 120))

            return False

    async def init_data(self, http_client: aiohttp.ClientSession, tg_web_data: str):
        try:
            response = await http_client.post('https://back.timboo.pro/api/init-data', json={"initData": tg_web_data})
            response.raise_for_status()
            response_json = await response.json()

            return response_json
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when get user data: {error}")
            await asyncio.sleep(delay=randint(60, 120))

            return False

    async def open_box(self, http_client: aiohttp.ClientSession, tg_web_data: str):
        try:
            logger.info(f"{self.session_name} | Wait 5s before opening the box")
            await asyncio.sleep(delay=5)
            response = await http_client.post('https://api.timboo.pro/open_box',
                                              json={"initData": tg_web_data, "boxId": 8})
            response.raise_for_status()

            response_json = await response.json()
            logger.success(f"{self.session_name} | {response_json['reward_text'].replace('<br/>', '')}")

            return True
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when open the box: {error}")
            await asyncio.sleep(delay=randint(60, 120))

            return False

    async def start_spinning(self, http_client: aiohttp.ClientSession, tg_web_data: str, clicks: int) -> bool:
        try:
            response = await http_client.post('https://back.timboo.pro/api/upd-data',
                                              json={"initData": tg_web_data, "data": {
                                                  "clicks": clicks,
                                                  "isClose": 'null'
                                              }})
            response.raise_for_status()
            logger.success(
                f"{self.session_name} |  Successfully spun")

            return True
        except Exception as error:
            logger.info(f"{self.session_name} | No more spins available")
            await asyncio.sleep(delay=randint(5, 10))

            return False

    async def repair_spinner(self, http_client: aiohttp.ClientSession, tg_web_data: str) -> bool:
        try:
            response = await http_client.post('https://back.timboo.pro/api/repair-spinner',
                                              json={"initData": tg_web_data})
            response.raise_for_status()
            logger.info(f"{self.session_name} | Repair is activated")

            return True
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when repair spinner: {error}")
            await asyncio.sleep(delay=randint(60, 120))

            return False

    async def full_hp_activate(self, http_client: aiohttp.ClientSession, tg_web_data: str, spinner_id: int) -> bool:
        try:
            response = await http_client.post('https://back.timboo.pro/api/fullhp-activate',
                                              json={"initData": tg_web_data, "spinnerId": spinner_id})
            response.raise_for_status()
            await asyncio.sleep(delay=5)
            logger.success(
                f"{self.session_name} |  Full HP activated, sleep 5s")

            return True
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when activating full hp: {error}")
            await asyncio.sleep(delay=randint(60, 120))

            return False

    async def rocket_activate(self, http_client: aiohttp.ClientSession, tg_web_data: str, spinner_id: int) -> bool:
        try:
            logger.info(
                f"{self.session_name} |  Sleep 5s before rocket turbo activation")
            await asyncio.sleep(delay=5)
            response = await http_client.post('https://back.timboo.pro/api/rocket-activate',
                                              json={"initData": tg_web_data, "spinnerId": spinner_id})
            response.raise_for_status()
            logger.success(
                f"{self.session_name} |  Rocket turbo activated, wait 5s before spin")
            await asyncio.sleep(delay=5)

            return True
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when activating Rocket turbo: {error}")
            await asyncio.sleep(delay=randint(60, 120))

            return False

    async def select_spinner(self, http_client: aiohttp.ClientSession, tg_web_data: str, spinner_id: int) -> bool:
        try:
            logger.info(
                f"{self.session_name} |  Sleep 5s before switching the spinner")
            await asyncio.sleep(delay=5)
            response = await http_client.post('https://back.timboo.pro/api/select-spinner',
                                              json={"initData": tg_web_data, "spinnerId": spinner_id})
            response.raise_for_status()
            logger.success(
                f"{self.session_name} |  Switched to spinner {spinner_id}")
            await asyncio.sleep(delay=5)

            return True
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when selecting the spinner: {error}")
            await asyncio.sleep(delay=randint(60, 120))

            return False

    async def upgrade_spinner(self, http_client: aiohttp.ClientSession, tg_web_data: str, spinner_id: int,
                              current_level: int) -> bool:
        try:
            logger.info(
                f"{self.session_name} |  Sleep 5s before upgrade the spinner")
            await asyncio.sleep(delay=5)
            response = await http_client.post('https://back.timboo.pro/api/upgrade-spinner',
                                              json={"initData": tg_web_data, "spinnerId": spinner_id})
            response.raise_for_status()
            logger.success(
                f"{self.session_name} |  The spinner {spinner_id} is upgraded to {current_level + 1} level")
            await asyncio.sleep(delay=5)

            return True
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when selecting the spinner: {error}")
            await asyncio.sleep(delay=randint(60, 120))

            return False

    async def register(self, http_client: aiohttp.ClientSession, tg_web_data: str) -> bool:
        try:
            response = await http_client.post('https://api.timboo.pro/register', json={"initData": tg_web_data})
            response.raise_for_status()

            return True
        except Exception as error:
            sleep = randint(60, 120)
            await asyncio.sleep(delay=sleep)
            logger.error(f"{self.session_name} | Unknown error when register: {error} retry after {sleep}s")

            return False

    async def check_proxy(self, http_client: aiohttp.ClientSession, proxy: Proxy) -> None:
        try:
            response = await http_client.get(url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(5))
            ip = (await response.json()).get('origin')
            logger.info(f"{self.session_name} | Proxy IP: {ip}")
        except Exception as error:
            logger.error(f"{self.session_name} | Proxy: {proxy} | Error: {error}")

    async def run(self, proxy: str | None) -> None:
        rand_session_start=randint(1, 31)
        logger.info(f"{self.session_name} | Wait {rand_session_start}s before session start")
        await asyncio.sleep(delay=rand_session_start)
        is_registered = False
        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None

        async with aiohttp.ClientSession(headers=headers, connector=proxy_conn) as http_client:
            if proxy:
                await self.check_proxy(http_client=http_client, proxy=proxy)

            while True:
                try:
                    if not is_registered:
                        tg_web_data = await self.get_tg_web_data(proxy=proxy)
                        await self.register(http_client=http_client, tg_web_data=tg_web_data)
                        is_registered = True

                    box_data = await self.get_data(http_client=http_client, tg_web_data=tg_web_data)
                    init_data = await self.init_data(http_client=http_client, tg_web_data=tg_web_data)

                    current_time = int(datetime.utcnow().timestamp())
                    box_open_time = None
                    if box_data["boxes"][0]["open_time"]:
                        box_open_time = int(datetime.strptime(box_data["boxes"][0]["open_time"],
                                                              "%a, %d %b %Y %H:%M:%S %Z").timestamp())

                    main_spinner_id = init_data["initData"]["user"]["mainSpinnerId"]
                    rockets_amount = init_data["initData"]["user"]["rocketsAmount"]
                    spinners = init_data["initData"]["spinners"]
                    levels = init_data["initData"]["levels"]

                    for i, spinner in enumerate(spinners):
                        if spinner["id"] == main_spinner_id:
                            spinners.pop(i)
                            spinners.insert(0, spinner)
                            break

                    spinners_len = len(spinners)

                    if box_open_time is None or current_time > box_open_time + 57800:
                        await self.open_box(http_client=http_client, tg_web_data=tg_web_data)

                    for i in range(spinners_len):
                        spinner = spinners[i]
                        spinner_data = spinner
                        spinner_id = spinner_data["id"]

                        if i > 0:
                            await self.select_spinner(http_client=http_client,
                                                      tg_web_data=tg_web_data,
                                                      spinner_id=spinner_id)
                            logger.info(
                                f"{self.session_name} | Current spinner is: {spinner_id}")
                        else:
                            logger.info(
                                f"{self.session_name} | Current spinner is: {spinner_id}")


                        while True:
                            try:
                                is_spinner_broken = spinner_data["isBroken"]
                                end_repair_time = spinner_data["endRepairTime"]
                                spinner_level = spinner_data["level"]
                                number_of_clicks = randint(settings.TAPS_COUNT[0], settings.TAPS_COUNT[1])

                                if rockets_amount > 0:
                                    await self.rocket_activate(http_client=http_client,
                                                               tg_web_data=tg_web_data,
                                                               spinner_id=spinner_id)
                                    number_of_clicks = randint(settings.ADD_TAPS_ON_TURBO[0],
                                                               settings.ADD_TAPS_ON_TURBO[1])
                                    rockets_amount -= 1

                                if is_spinner_broken:
                                    is_registered = False
                                    current_time = int(datetime.utcnow().timestamp())

                                    if end_repair_time is None:
                                        await self.repair_spinner(http_client=http_client, tg_web_data=tg_web_data)
                                        logger.info(
                                            f"{self.session_name} |  Repair is in progress for spinner {spinner_id}")
                                        await asyncio.sleep(delay=5)
                                        break

                                    end_repair_time = datetime.strptime(end_repair_time, "%Y-%m-%dT%H:%M:%S.%fZ")
                                    end_repair_time = int(end_repair_time.timestamp())
                                    if current_time < end_repair_time:
                                        logger.info(
                                            f"{self.session_name} |  Repair is in progress for spinner {spinner_id}")
                                        await asyncio.sleep(delay=5)
                                        break
                                else:
                                    status = await self.start_spinning(http_client=http_client, tg_web_data=tg_web_data,
                                                                       clicks=number_of_clicks)

                                    if status:
                                        logger.info(
                                            f"{self.session_name} |  Sleep 5s before next spin")
                                        await asyncio.sleep(randint(5, 6))
                                    else:
                                        init_data = await self.init_data(http_client=http_client,
                                                                         tg_web_data=tg_web_data)
                                        balance = init_data["initData"]["user"]["balance"]
                                        full_hp_mount = init_data["initData"]["user"]["fullhpAmount"]

                                        if full_hp_mount > 0:
                                            await self.full_hp_activate(http_client=http_client,
                                                                        tg_web_data=tg_web_data,
                                                                        spinner_id=spinner_id)
                                            continue

                                        await self.repair_spinner(http_client=http_client, tg_web_data=tg_web_data)
                                        await asyncio.sleep(randint(5, 6))

                                        logger.info(
                                            f"{self.session_name} |  Check for updates")

                                        while settings.AUTO_UPGRADE and balance > levels[spinner_level][
                                            "price"] and spinner_level < settings.MAX_UPGRADE_LEVEL:
                                            await self.upgrade_spinner(http_client=http_client, tg_web_data=tg_web_data,
                                                                       spinner_id=spinner_id,
                                                                       current_level=spinner_level)
                                            spinner_level += 1
                                            balance -= levels[spinner_level]["price"]
                                        break


                            except Exception as error:
                                logger.error(f"{self.session_name} | Unknown error: {error}")
                                await asyncio.sleep(delay=3)

                except InvalidSession as error:
                    logger.error(f"{self.session_name} | ! ️InvalidSession: {error}")
                    await asyncio.sleep(delay=randint(60, 120))
                    raise error

                except Exception as error:
                    logger.error(f"{self.session_name} | Unknown error: {error}")
                    await asyncio.sleep(delay=randint(60, 120))

                rand_sleep = randint(7200, 8600)
                logger.info(
                    f"{self.session_name} |  Sleep {rand_sleep}s before next spinners check")
                await asyncio.sleep(rand_sleep)


async def run_spinner(tg_client: Client, proxy: str | None):
    try:
        await Claimer(tg_client=tg_client).run(proxy=proxy)
    except InvalidSession:
        logger.error(f"{tg_client.name} | Invalid Session")
        await asyncio.sleep(delay=randint(60, 120))
