import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import requests

load_dotenv()
app = FastAPI(title="Custom Local AI Engine & API Gateway")

MY_SECRET_API_KEY = os.getenv(
    "MY_CUSTOM_API_KEY", "CHONGQING_SECRET_KEY_9999_AI_SENDIRI"
)
LLM_BACKEND = os.getenv("LLM_BACKEND", "ollama")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key == MY_SECRET_API_KEY:
        return api_key
    raise HTTPException(
        status_code=403, detail="Akses Ditolak: API Key buatan Anda tidak valid!"
    )


def call_ollama(prompt: str) -> str:
    """Call Ollama API"""
    ollama_url = "http://localhost:11434/api/generate"
    model = os.getenv("OLLAMA_MODEL", "llama3")
    payload = {
        "model": model,
        "prompt": f"Bertindaklah sebagai AI Agency profesional bergaya Chongqing Cyberpunk. Tugas: {prompt}",
        "stream": False,
    }
    response = requests.post(ollama_url, json=payload, timeout=120)
    if response.status_code == 200:
        return response.json().get("response", "")
    raise Exception(f"Gagal terhubung ke Ollama di {ollama_url}")


def call_lm_studio(prompt: str) -> str:
    """Call LM Studio (OpenAI-compatible endpoint)"""
    lm_url = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1/chat/completions")
    payload = {
        "model": "local-model",
        "messages": [
            {
                "role": "system",
                "content": "Anda adalah AI Agency profesional bergaya Chongqing Cyberpunk."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }
    response = requests.post(lm_url, json=payload, timeout=120)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    raise Exception(f"Gagal terhubung ke LM Studio di {lm_url}")


def call_text_generation_webui(prompt: str) -> str:
    """Call Text Generation WebUI"""
    webui_url = os.getenv("TEXT_GEN_WEBUI_URL", "http://localhost:5000/api/v1/generate")
    payload = {
        "prompt": f"Bertindaklah sebagai AI Agency profesional bergaya Chongqing Cyberpunk. Tugas: {prompt}",
        "max_new_tokens": 1024,
        "temperature": 0.7
    }
    response = requests.post(webui_url, json=payload, timeout=120)
    if response.status_code == 200:
        return response.json().get("results", [{}])[0].get("text", "")
    raise Exception(f"Gagal terhubung ke Text Generation WebUI di {webui_url}")


def call_localai(prompt: str) -> str:
    """Call LocalAI (OpenAI-compatible endpoint)"""
    localai_url = os.getenv("LOCALAI_URL", "http://localhost:8080/v1/chat/completions")
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "Anda adalah AI Agency profesional bergaya Chongqing Cyberpunk."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }
    response = requests.post(localai_url, json=payload, timeout=120)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    raise Exception(f"Gagal terhubung ke LocalAI di {localai_url}")


def call_llm(prompt: str) -> str:
    """Route to appropriate LLM backend"""
    if LLM_BACKEND == "ollama":
        return call_ollama(prompt)
    elif LLM_BACKEND == "lm_studio":
        return call_lm_studio(prompt)
    elif LLM_BACKEND == "text_gen_webui":
        return call_text_generation_webui(prompt)
    elif LLM_BACKEND == "localai":
        return call_localai(prompt)
    else:
        raise Exception(f"Unknown LLM backend: {LLM_BACKEND}")


@app.post("/v1/generate")
def generate_local_ai(prompt: str, api_key: str = Security(verify_api_key)):
    """Menghubungkan ke model AI lokal yang fleksibel"""
    try:
        result_text = call_llm(prompt)
        return {
            "status": "success",
            "engine": f"100% Custom Self-Hosted AI ({LLM_BACKEND})",
            "result": result_text,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error server AI lokal: {str(e)}. Pastikan {LLM_BACKEND} menyala."
        )


@app.get("/health")
def health_check():
    """Check if AI server is running"""
    return {
        "status": "running",
        "backend": LLM_BACKEND,
        "api_key_required": True
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
