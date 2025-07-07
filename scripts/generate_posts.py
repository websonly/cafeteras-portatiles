import os, re, openai, time
from openai.error import RateLimitError, APIError

NUM_POSTS = 2
WORDS_PER_POST = 200
ASSOCIATE_TAG = "websonly-21"
DOMAIN = "cafeterasportatiles.online"
RETRIES = 3
BACKOFF = 2

openai.api_key = os.getenv("CHATGPT_API_KEY")

def affiliateify(content):
    pattern = r"(https://www\\.amazon\\.es/dp/([A-Z0-9]{10}))"
    return re.sub(pattern, lambda m: f"{m.group(1)}/?tag={ASSOCIATE_TAG}", content)

def generate_post(prompt):
    for i in range(RETRIES):
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role":"system","content":"Eres un asistente..."},
                    {"role":"user","content":prompt}
                ],
                temperature=0.7,
            )
            return resp.choices[0].message.content
        except RateLimitError:
            time.sleep(BACKOFF ** (i+1))
        except APIError:
            break
    return f"# Artículo provisional sobre {DOMAIN}\n\nContenído en breve."

if __name__ == "__main__":
    os.makedirs("posts", exist_ok=True)
    for i in range(1, NUM_POSTS+1):
        p = f"Genera un artículo de {WORDS_PER_POST} palabras sobre '{DOMAIN}', con enlaces a Amazon."
        content = affiliateify(generate_post(p))
        with open(f"posts/post_{i}.md", "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✔ Generado post_{i}.md")
