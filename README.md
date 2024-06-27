# SpinnerCoin Clicker

[![Static Badge](https://img.shields.io/badge/Telegram-Bot%20Link-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/spinnercoin_bot/app?startapp=r_3830128)

#### Подписывайтесь на наш [телеграм канал](https://t.me/scriptron). Там будут новости о новый ботах
## Важно

- **Python Version:** Программное обеспечение работает на Python 3.10 - 3.11. Использование другой версии может привести к ошибкам.
- НЕ ИСПОЛЬЗУЙТЕ ОСНОВНОЙ АККАУНТ, ПОТОМУ ЧТО ВСЕГДА ЕСТЬ ШАНС ПОЛУЧИТЬ БАН В TELEGRAM



> 🇪🇳 README in english available [here](README-EN.md)

## Функционал  
| Функционал                                              | Поддерживается |
|---------------------------------------------------------|:--------------:|
| Многопоточность                                         |       ✅        |
| Привязка прокси к сессии                                |       ✅        |
| Авто-спиннер                                            |       ✅        |
| Авто-апгрейд спиннера                                   | ✅          |
| Поддержка tdata / pyrogram .session / telethon .session |       ✅        |

## Предварительные условия
Прежде чем начать, убедитесь, что у вас установлено следующее:
- [Python](https://www.python.org/downloads/) **version 3.10**

## Получение API ключей
1. Перейдите на сайт [my.telegram.org](https://my.telegram.org) и войдите в систему, используя свой номер телефона.
2. Выберите **"API development tools"** и заполните форму для регистрации нового приложения.
3. Запишите `API_ID` и `API_HASH` в файле `data/config.py`, предоставленные после регистрации вашего приложения.

## [Настройки](https://github.com/Re-Diss/SpinnerCoin/blob/main/.env-example)
| Настройка               | Описание                                                                                                                                                                                                   |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **API_ID / API_HASH**   | Данные платформы, с которой запускать сессию Telegram _(сток - Android)_                                                                                                                                   |
| **ADD_TAPS_ON_TURBO**    | Сколько тапов будет добавлено при активации турбо (по дефолту. [10,15])                                                                                                                                    |
| **AUTO_UPGRADE**     | Улучшать ли спиннер (True / False)                                                                                                                                                                         |
| **MAX_UPGRADE_LEVEL**     | Максимальный уровень улучшения                                                                                                                                                                             |
| **APPLY_DAILY_ENERGY**   | Использовать ли ежедневный бесплатный буст энергии (True / False)                                                                                                                                          |
| **APPLY_DAILY_TURBO**    | Использовать ли ежедневный бесплатный буст турбо (True / False)                                                                                                                                            |
| **TAPS_COUNT**  | Количество тапов. Если уровень спинера ниже 12, применяется значение от 5 до 7. Если уровень спинера 12 и выше и он смайнен как NFT, применяется значение указаное вами, если 12 и не смайнен то от 5 до 7 |
| **USE_PROXY_FROM_FILE** | Использовать-ли прокси из файла `bot/config/proxies.txt` _(True / False)_                                                                                                                                  |


## Установка
Вы можете скачать [**Репозиторий**](https://github.com/Re-Diss/SpinnerCoin) клонированием на вашу систему и установкой необходимых зависимостей:
```shell
~ >>> git clone https://github.com/Re-Diss/SpinnerCoin.git
~ >>> cd SpinnerCoin

# Linux
~/SpinnerCoin >>> python3 -m venv venv
~/SpinnerCoin >>> source venv/bin/activate
~/SpinnerCoin >>> pip3 install -r requirements.txt
~/SpinnerCoin >>> cp .env-example .env
~/SpinnerCoin >>> nano .env  # Здесь вы обязательно должны указать ваши API_ID и API_HASH , остальное берется по умолчанию
~/SpinnerCoin >>> python3 main.py

# Windows
~/SpinnerCoin >>> python -m venv venv
~/SpinnerCoin >>> venv\Scripts\activate
~/SpinnerCoin >>> pip install -r requirements.txt
~/SpinnerCoin >>> copy .env-example .env
~/SpinnerCoin >>> # Указываете ваши API_ID и API_HASH, остальное берется по умолчанию
~/SpinnerCoin >>> python main.py
```

Также для быстрого запуска вы можете использовать аргументы, например:
```shell
~/SpinnerCoin >>> python3 main.py --action (1/2)
# Или
~/SpinnerCoin >>> python3 main.py -a (1/2)

# 1 - Создает сессию
# 2 - Запускает спиннер
```
