import os
import time
import openai
from openai.error import RateLimitError, APIError

# Ajusta aquí la cantidad de posts
NUM_POSTS = 2
WORDS_PER_POST = 200

openai.api_key = os.getenv("CHATGPT_API_KEY")
DOMAIN = "cafeterasportatiles.online"
RETRIES = 3
BACKOFF = 2  # segundos

def generate_post(prompt):
    for attempt in range(1, RETRIES + 1):
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role":"system","content":"Eres un asistente que crea artículos de blog en Markdown con título y subtítulos."},
                    {"role":"user","content":prompt}
                ],
                temperature=0.7,
            )
            return resp.choices[0].message.content
        except RateLimitError:
            wait = BACKOFF ** attempt
            print(f"⚠️ RateLimitError, retrying in {wait}s (attempt {attempt}/{RETRIES})")
            time.sleep(wait)
        except APIError as e:
            print(f"❌ APIError: {e}. Generando placeholder.")
            break
    # Fallback placeholder tras reintentos fallidos
    return (
        f"# Artículo provisional sobre {DOMAIN}\n\n"
        "Lo sentimos, estamos completando tu contenido. Vuelve a intentarlo pronto."
    )

if __name__ == "__main__":
    os.makedirs("posts", exist_ok=True)
    for i in range(1, NUM_POSTS + 1):
        prompt = (
            f"Genera un artículo de {WORDS_PER_POST} palabras sobre '{DOMAIN}'. "
            "Incluye título descriptivo y subtítulos en Markdown."
        )
        content = generate_post(prompt)
        filename = f"posts/post_{i}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✔ Generado {filename}")
