from flask import Flask, request, jsonify, send_from_directory
import os
import requests

app = Flask(__name__, static_folder='.', static_url_path='')

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


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    if not OPENAI_API_KEY:
        return jsonify({'error': 'API ключ не настроен. Установите OPENAI_API_KEY.'}), 500

    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'error': 'Пустое сообщение'}), 400

    try:
        resp = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {OPENAI_API_KEY}',
            },
            json={
                'model': MODEL,
                'messages': [
                    {'role': 'system', 'content': SYSTEM_PROMPT},
                    {'role': 'user', 'content': user_message},
                ],
                'temperature': 0,
            },
            timeout=30,
        )

        if resp.status_code != 200:
            error_data = resp.json().get('error', {})
            error_msg = error_data.get('message', f'OpenAI вернул {resp.status_code}')
            return jsonify({'error': error_msg}), 502

        result = resp.json()
        answer = result['choices'][0]['message']['content']
        return jsonify({'answer': answer})

    except requests.Timeout:
        return jsonify({'error': 'Таймаут запроса к OpenAI'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
