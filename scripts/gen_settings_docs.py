"""Генератор русской страницы «Настройки панели» в формате GitHub Markdown.

Настроек около двухсот, и держать их описания вручную синхронными с кодом
невозможно: любая новая настройка через месяц окажется недокументированной,
а удалённая останется в тексте навсегда. Поэтому справочник собирается из
того же каталога, по которому панель строит интерфейс, и переводов, которыми
подписаны те же настройки во фронте.

Запуск (из корня репозитория):

    python scripts/gen_settings_docs.py

Пишет docs/reference/settings.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from shared.config_service import DEFAULT_CONFIG_DEFINITIONS  # noqa: E402

LOCALES = ROOT / "web" / "frontend" / "src" / "locales"

# Порядок разделов на странице: сначала то, что настраивают в первый день,
# потом редкое. Порядок в самом каталоге настроек другой — он про интерфейс.
CATEGORY_ORDER = [
    "general",
    "notifications",
    "violations",
    "security",
    "mailserver",
    "backup",
    "reports",
    "finance",
    "performance",
    "sync",
]

INTRO = {
    "general": "Базовые вещи: язык, логи, доступ к панели Remnawave, ключи внешних сервисов. Часть значений здесь — секреты, они правятся на своих страницах, а в списке настроек показываются только для справки.",
    "notifications": "Куда и о чём писать в Telegram. Топики раскладывают события по темам форума, типы уведомлений включают и выключают отдельные события.",
    "violations": "Самый большой раздел: анализаторы, пороги срабатывания, автоматические действия и сроки хранения. Что означают анализаторы и как разбирать инциденты — в разделе [Анти-абуз](../guide/anti-abuse.md).",
    "security": "Защита самой панели и детект атак на ноды: методы входа, ограничение перебора, чёрный список пользователей.",
    "mailserver": "Встроенный почтовый сервер: TLS, приём входящих, спам-оценка, сроки хранения. Как поднять — в разделе [Почтовый сервер](../guide/mail.md).",
    "backup": "Расписание, сроки хранения и «мёртвая рука» — алерт о том, что бэкапов давно не было. Подробнее в разделе [Бэкапы](../guide/backups.md).",
    "reports": "Периодические сводки: что присылать, когда и кому.",
    "finance": "Учёт расходов на инфраструктуре и доходов: валюта отчётов, курсы, напоминания о списаниях, синхронизация с API хостеров.",
    "performance": "Пулы соединений, кэш и интервалы фоновых задач. Трогать стоит, когда упёрлись в потолок, а не заранее.",
    "sync": "Синхронизация с панелью Remnawave.",
}

PAGE_HEADER = """# Настройки панели

Почти всё в панели настраивается из интерфейса, без правки файлов и перезапуска: **Настройки**. Изменение применяется сразу.

Значение берётся по цепочке **база данных → `.env` → значение по умолчанию**. Пока настройку не трогали в интерфейсе, работает то, что задано в `.env` или зашито в код; после первого изменения она живёт в базе, и `.env` на неё больше не влияет.

В списке настройки помечены: `В БД` — значение переопределено и хранится в базе, `.env` — взято из окружения, `По умолч.` — из кода. Отдельные значения только для чтения: они управляются со своих страниц, а здесь показаны для полноты.

> [!TIP]
> **Эта страница собрана из кода**
> Названия, описания и значения по умолчанию берутся прямо из каталога настроек панели, поэтому не расходятся с тем, что вы видите в интерфейсе. Обновляется командой `python scripts/gen_settings_docs.py`.
"""

TABLE_HEAD = "| Настройка | Ключ | По умолчанию | Что делает |\n|---|---|---|---|"
READONLY_NOTE = "только чтение"
EMPTY_DEFAULT = "пусто"
NO_SUBCATEGORY = "Основное"
FOOTER = "\n## Настройки агента\n\nПеременные агента задаются на самой ноде и в этот список не попадают — см. [Node Agent](../guide/node-agent.md#переменные-агента).\n"


def load_translations() -> Dict[str, Any]:
    data = json.loads((LOCALES / "ru" / "translation.json").read_text(encoding="utf-8"))
    return data.get("settings", {})


def cell(text: str) -> str:
    """Экранирование содержимого для Markdown-таблицы и HTML."""
    text = text.replace("|", "\\|").replace("\n", " ").strip()
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    return text.replace("{{", "&#123;&#123;").replace("}}", "&#125;&#125;")


def describe(item: Dict[str, Any], strings: Dict[str, Any]) -> tuple[str, str]:
    """Подпись и описание настройки: сначала перевод, иначе то, что в каталоге."""
    entry = strings.get("configItems", {}).get(item["key"], {})
    label = entry.get("label") or item.get("display_name") or item["key"]
    description = entry.get("description") or item.get("description") or ""

    notes = []
    if item.get("is_readonly"):
        notes.append(READONLY_NOTE)
    if item.get("env_var_name"):
        notes.append(f"`{item['env_var_name']}`")
    if notes:
        description = f"{description} ({', '.join(notes)})" if description else f"({', '.join(notes)})"

    return label, description


def render() -> str:
    strings = load_translations()
    categories = strings.get("categories", {})
    subcategories = strings.get("subcategories", {})

    by_category: Dict[str, List[Dict[str, Any]]] = {}
    for item in DEFAULT_CONFIG_DEFINITIONS:
        by_category.setdefault(item.get("category", "general"), []).append(item)

    # Категория, забытая в CATEGORY_ORDER, не должна исчезнуть со страницы.
    order = CATEGORY_ORDER + [c for c in by_category if c not in CATEGORY_ORDER]

    out = [PAGE_HEADER]
    for category in order:
        items = by_category.get(category)
        if not items:
            continue

        title = categories.get(category, category)
        out.append(f"\n## {title}\n")
        intro = INTRO.get(category)
        if intro:
            out.append(f"{intro}\n")

        groups: Dict[str, List[Dict[str, Any]]] = {}
        for item in items:
            groups.setdefault(item.get("subcategory") or "", []).append(item)

        multiple = len(groups) > 1
        for subcategory, group in groups.items():
            if multiple:
                name = subcategories.get(subcategory, subcategory) if subcategory else NO_SUBCATEGORY
                out.append(f"\n### {name}\n")

            out.append(TABLE_HEAD)
            for item in sorted(group, key=lambda i: i.get("sort_order", 0)):
                label, description = describe(item, strings)
                default = item.get("default_value")
                default = f"`{default}`" if default not in (None, "") else EMPTY_DEFAULT
                out.append(
                    f"| **{cell(label)}** | `{item['key']}` | {default} | {cell(description)} |"
                )
            out.append("")

    out.append(FOOTER)
    return "\n".join(out)


def main() -> None:
    path = ROOT / "docs" / "reference" / "settings.md"
    path.write_text(render(), encoding="utf-8")
    print(f"{path.relative_to(ROOT)}: {len(DEFAULT_CONFIG_DEFINITIONS)} настроек")


if __name__ == "__main__":
    main()
