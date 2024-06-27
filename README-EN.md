# SpinnerCoin Clicker

[![Static Badge](https://img.shields.io/badge/Telegram-Bot%20Link-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/spinnercoin_bot/app?startapp=r_3830128)

#### Join my [Telegram channel](https://t.me/scriptron). I will be posting news about new bots and scripts there.
## Important Notes

> 🇷🇺 README на русском доступен [здесь](README.md)

## Functionality
| Functional                                            | Supported |
|-------------------------------------------------------|:---------:|
| Multithreading                                        |     ✅     |
| Binding a proxy to a session                          |     ✅     |
| Auto-spinning                                         |     ✅     |
| Auto-upgrade of the spinner                           |   ✅    |
| Support tdata / pyrogram .session / telethon .session |     ✅     |

## [Settings](https://github.com/Re-Diss/SpinnerCoin/blob/main/.env-example)
| Settings                | Description                                                                                                                                                                                                                     |
|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **API_ID / API_HASH**   | Platform data from which to launch a Telegram session (stock - Android)                                                                                                                                                         |
| **ADD_TAPS_ON_TURBO**    | How many taps will be added when turbo is activated (default. [10,15])                                                                                                                                                          |
| **AUTO_UPGRADE**     | Should I improve the spinner (True / False)                                                                                                                                                                                     |
| **MAX_UPGRADE_LEVEL**     | Max upgrade level                                                                                                                                                                                                               |
| **APPLY_DAILY_ENERGY**   | Whether to use the daily free energy boost (True / False)                                                                                                                                                                       |
| **APPLY_DAILY_TURBO**    | Whether to use the daily free turbo boost (True / False)                                                                                                                                                                        |
| **TAPS_COUNT**  | Number of taps. If the spinner level is below 12, a value from 5 to 7 is applied. If the spinner level is 12 or higher and it is minted as an NFT, the value specified by you is applied, if 12 and not minted then from 5 to 7 |
| **USE_PROXY_FROM_FILE** | Whether to use proxy from the `bot/config/proxies.txt` file (True / False)                                                                                                                                                      |

## Installation
You can download [**Repository**](https://github.com/Re-Diss/SpinnerCoin) by cloning it to your system and installing the necessary dependencies:
```shell
~ >>> git clone https://github.com/Re-Diss/SpinnerCoin.git
~ >>> cd SpinnerCoin

#Linux
~/SpinnerCoin >>> python3 -m venv venv
~/SpinnerCoin >>> source venv/bin/activate
~/SpinnerCoin >>> pip3 install -r requirements.txt
~/SpinnerCoin >>> cp .env-example .env
~/SpinnerCoin >>> nano .env # Here you must specify your API_ID and API_HASH , the rest is taken by default
~/SpinnerCoin >>> python3 main.py

#Windows
~/SpinnerCoin >>> python -m venv venv
~/SpinnerCoin >>> venv\Scripts\activate
~/SpinnerCoin >>> pip install -r requirements.txt
~/SpinnerCoin >>> copy .env-example .env
~/SpinnerCoin >>> # Specify your API_ID and API_HASH, the rest is taken by default
~/SpinnerCoin >>> python main.py
```

Also for quick launch you can use arguments, for example:
```shell
~/SpinnerCoin >>> python3 main.py --action (1/2)
# Or
~/SpinnerCoin >>> python3 main.py -a (1/2)

#1 - Create session
#2 - Run spinner
```
