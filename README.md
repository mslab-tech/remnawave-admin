<div align="center">

<img src="remnawave-admin.webp" alt="Remnawave Admin" width="100%" />

# Remnawave Admin

**Панель управления и Telegram-бот поверх вашей панели Remnawave**

Пользователи, ноды, анти-абуз, почта и мониторинг — в одном месте

[![Stars](https://img.shields.io/github/stars/mslab-tech/remnawave-admin?style=flat-square&logo=github&logoColor=white&labelColor=1f2430&color=f5c518)](https://github.com/mslab-tech/remnawave-admin/stargazers) [![Release](https://img.shields.io/github/v/release/mslab-tech/remnawave-admin?style=flat-square&logo=github&logoColor=white&labelColor=1f2430&color=3fb950)](https://github.com/mslab-tech/remnawave-admin/releases/latest) [![License](https://img.shields.io/badge/License-AGPL_v3-blue?style=flat-square&logo=gnu&logoColor=white)](LICENSE)

### [💬 Чат](https://t.me/remnawave_admin) · [🛟 Поддержка](https://t.me/rwa_moder_bot?start=support)

</div>

---

Панель Remnawave отвечает за пользователей и конфигурацию. Remnawave Admin берёт на себя всё остальное: собирает подключения с нод, ищет разделение подписок и торренты, принимает меры, шлёт уведомления, хранит историю и показывает, что происходит.

Работает поверх вашей панели по API, данные держит в своей базе.

## Возможности

🛡 **Анти-абуз.** Анализаторы подключений ищут разделение подписок и накрутку пробных: одновременные подключения, «невозможные путешествия», сети, устройства, HWID, User-Agent. Меры — от предупреждения клиенту до ограничения скорости и отключения — можно включить автоматически, а каждое нарушение разобрать в его карточке.

🧲 **Торренты.** Тег роутинга Xray и разбор трафика на ноде: шифрованный BitTorrent тоже видно, а лаунчеры игр и синхронизацию файлов можно отметить как «не торрент».

🛰 **Агент на нодах.** Логи Xray, метрики хоста, удалённый терминал и каталог скриптов, ограничение скорости на ноде, качество канала до клиентов. Ставится одной строкой из панели.

🚨 **Атаки и сбои.** Детектор DDoS-атак на ноды, тревоги о падении нод и о проблемах с каналом.

📧 **Почтовый сервер.** Свой MX, DKIM, приём входящих, проверка SPF/DKIM/DMARC — без внешних SMTP-провайдеров.

📈 **Мониторинг и аналитика.** Метрики Prometheus и дашборды Grafana, гео-карта подключений, рейтинг хостеров, аналитика по пользователям, автоматизации.

🤖 **Telegram-бот.** Управление через Telegram: пользователи и ноды, уведомления с кнопками действий, раскладка по топикам форума.

🔌 **API и интеграции.** Свой API с ключами и правами, webhook с подписью, нарушения в кабинете Bedolaga.

А также: конструктор автоматизаций, бэкапы по расписанию, журнал действий, роли и права, 2FA, темы оформления, русский и английский интерфейс.

## Как начать

1. Клонируйте репозиторий: `git clone https://github.com/mslab-tech/remnawave-admin.git`.
2. Скопируйте `.env.example` в `.env` и заполните обязательные параметры.
3. Создайте сеть `docker network create remnawave-network` и запустите `docker compose up -d`.

Полная инструкция — в [документации по установке](docs/guide/installation.md). Вопросы — в [чат](https://t.me/remnawave_admin) или в поддержку [@rwa_moder_bot](https://t.me/rwa_moder_bot?start=support).

## История проекта

Проект начался как форк `Case211/remnawave-admin` и теперь развивается самостоятельно в [mslab-tech/remnawave-admin](https://github.com/mslab-tech/remnawave-admin). Здесь доступны [документация](docs/README.md) и [релизы](https://github.com/mslab-tech/remnawave-admin/releases).

## Лицензия

Код этого репозитория — GNU AGPL v3.0 с исключением для плагинов (§7), см. [LICENSE](LICENSE); версии до 2.15.x включительно остаются под MIT.

## Поддержать

TON `UQDDe-jyFTbQsPHqyojdFeO1_m7uPF-q1w0g_MfbSOd3l1sC`
USDT TRC20 `TGyHJj2PsYSUwkBbWdc7BFfsAxsE6SGGJP`
BTC `1J6Zz7XcrpFkchwFmuU5WTFYTxziBdSwRz`

<div align="center">
Сделано для сообщества Remnawave
</div>
