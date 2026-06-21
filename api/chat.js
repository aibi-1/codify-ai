const OPENAI_API_KEY = process.env.OPENAI_API_KEY || '';
const MODEL = 'gpt-4o-mini';

const SCHOOL_DATA = `
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
`;

const SYSTEM_PROMPT = `Ты помощник школы Codify.

Отвечай только используя информацию ниже.

${SCHOOL_DATA}

Правила:

1. Не выдумывай информацию.
2. Если ответа нет в базе знаний, отвечай:

"Извините, я не знаю ответ на этот вопрос.
Свяжитесь с менеджером:
+996500431430"

3. Отвечай кратко и вежливо.
`;

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  if (!OPENAI_API_KEY) {
    return res.status(500).json({ error: 'API ключ не настроен. Установите OPENAI_API_KEY в Vercel.' });
  }

  const { message } = req.body || {};

  if (!message || !message.trim()) {
    return res.status(400).json({ error: 'Пустое сообщение' });
  }

  try {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${OPENAI_API_KEY}`,
      },
      body: JSON.stringify({
        model: MODEL,
        messages: [
          { role: 'system', content: SYSTEM_PROMPT },
          { role: 'user', content: message.trim() },
        ],
        temperature: 0,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const errorMsg = errorData?.error?.message || `OpenAI returned ${response.status}`;
      return res.status(502).json({ error: errorMsg });
    }

    const data = await response.json();
    const answer = data.choices?.[0]?.message?.content || 'Нет ответа';

    return res.status(200).json({ answer });
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}
