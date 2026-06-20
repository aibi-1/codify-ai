import os
import json
from http.server import BaseHTTPRequestHandler
import urllib.request

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
MODEL = "gpt-4o-mini"

SCHOOL_DATA = """
Название: Codify

Стоимость:
50 000 сом за 4 месяца обучения.

Телефон:
+996500431430

Сайт:
codify.lab

Instagram:
codify.kids

Основатель:
Динара Руслан

Выпускники:
Более 10 000 выпускников.

Методология:
Harvard & MIT

Филиалы:
- Бишкек, 7 микрорайон 26/2
- Бишкек, Ибраимова 115
- Джал, Тыналиева 2/7

Расписание:
09:30 - 11:30 Scratch
12:00 - 14:00 Roblox
14:30 - 16:30 HTML/CSS
17:00 - 19:00 Python/JS

Преподаватели:
Максат Каныбеков — HTML/CSS
Азамат — Python
Азамат — Startup Studio

Особенности:
- Онлайн обучение
- Запись уроков
- Рассрочка
- Бесплатная ИИ диагностика
- BootCamp
- Хакатоны
"""

SYSTEM_PROMPT = f"""Ты помощник школы Codify.

Отвечай только используя информацию ниже.

{SCHOOL_DATA}

Правила:

1. Не выдумывай информацию.
2. Если ответа нет в базе знаний, отвечай:

"Извините, я не знаю ответ на этот вопрос.
Свяжитесь с менеджером:
+996500431430"

3. Отвечай кратко и вежливо.
"""


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body)
        user_message = data.get('message', '').strip()

        if not OPENAI_API_KEY:
            self._respond(500, {'error': 'API ключ не настроен. Установите OPENAI_API_KEY.'})
            return

        if not user_message:
            self._respond(400, {'error': 'Пустое сообщение'})
            return

        try:
            payload = json.dumps({
                'model': MODEL,
                'messages': [
                    {'role': 'system', 'content': SYSTEM_PROMPT},
                    {'role': 'user', 'content': user_message},
                ],
                'temperature': 0,
            }).encode('utf-8')

            req = urllib.request.Request(
                'https://api.openai.com/v1/chat/completions',
                data=payload,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {OPENAI_API_KEY}',
                },
            )

            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read())
                answer = result['choices'][0]['message']['content']
                self._respond(200, {'answer': answer})

        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            try:
                error_msg = json.loads(error_body).get('error', {}).get('message', str(e))
            except Exception:
                error_msg = str(e)
            self._respond(502, {'error': error_msg})

        except Exception as e:
            self._respond(500, {'error': str(e)})

    def _respond(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
