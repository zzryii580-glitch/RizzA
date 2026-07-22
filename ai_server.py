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
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)):
  if api_key == MY_SECRET_API_KEY:
    return api_key
  raise HTTPException(
      status_code=403, detail="Akses Ditolak: API Key buatan Anda tidak valid!"
  )


@app.post("/v1/generate")
def generate_local_ai(prompt: str, api_key: str = Security(verify_api_key)):
  """Menghubungkan langsung ke model AI lokal (Ollama / Llama 3) tanpa API luar"""
  try:
    ollama_url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": f"Bertindaklah sebagai AI Agency profesional bergaya Chongqing Cyberpunk. Tugas: {prompt}",
        "stream": False,
    }

    response = requests.post(ollama_url, json=payload, timeout=120)
    if response.status_code == 200:
      result_text = response.json().get("response", "")
      return {
          "status": "success",
          "engine": "100% Custom Self-Hosted AI",
          "result": result_text,
      }
    else:
      raise HTTPException(
          status_code=500,
          detail=(
              "Gagal terhubung ke Ollama. Pastikan aplikasi Ollama menyala dan"
              " model 'llama3' sudah diunduh."
          ),
      )
  except Exception as e:
    raise HTTPException(
        status_code=500,
        detail=(
            f"Error server AI lokal: {str(e)}. Jalankan 'ollama run llama3' di"
            " terminal Anda."
        ),
    )


if __name__ == "__main__":
  import uvicorn

  uvicorn.run(app, host="0.0.0.0", port=8080)
