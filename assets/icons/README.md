# Иконки бота

Набор **Churn & Gold** — 41 иконка в едином стиле «пласт масла».

- `svg/` — исходники (вектор, 512×512, viewBox 0 0 120 120). Источник правды.
- `png/` — растр 512×512 для Telegram (бот шлёт именно их через `send_photo`).

## Состав

| Группа | Файлы |
|---|---|
| Экранные действия | `action_start`, `action_profile`, `action_next_task`, `action_return_task`, `action_rest_start`, `action_rest_end`, `action_done`, `action_failed` |
| Статусы прогресса | `status_0_raw_cream`, `status_7_whipped_butter`, `status_14_smooth_texture`, `status_21_premium_block`, `status_28_solid_gold` |
| Дни марафона | `day_01` … `day_28` |

## Пересборка после правок

Правим `.svg` (или описание в `tools/build_icons.py`) и запускаем:

```bash
python tools/build_icons.py
```

Скрипт перезаписывает `svg/` и растеризует всё в `png/` через headless Edge/Chrome.
Для обычной работы бота скрипт не нужен — PNG лежат в репозитории.

## Подключение в коде

`bot/media.py` — хелперы `answer_with_icon` / `send_with_icon`. Если PNG-файла
нет, они молча откатываются на обычный текст, бот не падает.
