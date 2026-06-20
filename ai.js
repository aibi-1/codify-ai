import { CONFIG } from "./config.js";
import { SYSTEM_PROMPT } from "./prompts.js";

export async function askAI(message) {

    const response = await fetch(
        "https://api.openai.com/v1/chat/completions",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                Authorization:
                    `Bearer ${CONFIG.API_KEY}`
            },

            body: JSON.stringify({
                model: CONFIG.MODEL,

                messages: [
                    {
                        role: "system",
                        content: SYSTEM_PROMPT
                    },
                    {
                        role: "user",
                        content: message
                    }
                ],

                temperature: 0
            })
        }
    );

    const data = await response.json();

    return data.choices[0].message.content;
}