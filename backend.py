import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

load_dotenv()
app = FastAPI(title="Chongqing Autonomous AI Agency Backend")

DB_FILE = "database.json"
CUSTOM_AI_URL = "http://localhost:8080/v1/generate"
MY_API_KEY = os.getenv(
    "MY_CUSTOM_API_KEY", "CHONGQING_SECRET_KEY_9999_AI_SENDIRI"
)


def load_db():
  if not os.path.exists(DB_FILE):
    return {"orders": []}
  with open(DB_FILE, "r") as f:
    return json.load(f)


def save_db(data):
  with open(DB_FILE, "w") as f:
    json.dump(data, f, indent=4)


class TaskRequest(BaseModel):
  prompt: str
  client_phone: str


class PaymentWebhook(BaseModel):
  order_id: str
  status: str
  amount: int


def send_whatsapp_alert(message: str):
  admin_phone = os.getenv("WHATSAPP_ADMIN_PHONE", "6280000000000")
  print(
      f"\n[WHATSAPP ALERT KE {admin_phone}]: ⚠️ KENDALA SISTEM AGEN ->"
      f" {message}\n"
  )


@app.post("/run-agent")
def run_autonomous_agent(data: TaskRequest):
  try:
    full_prompt = (
        f"Buatkan hasil riset, copywriting promosi, dan strategi pemasaran"
        f" media sosial secara lengkap untuk produk/ide berikut: {data.prompt}"
    )

    headers = {"X-API-Key": MY_API_KEY}
    response = requests.post(
        f"{CUSTOM_AI_URL}?prompt={full_prompt}", headers=headers, timeout=120
    )

    if response.status_code == 200:
      ai_output = response.json().get("result")
      return {"status": "success", "result": ai_output}
    else:
      err_msg = response.json().get("detail", "Unknown AI error")
      send_whatsapp_alert(err_msg)
      raise HTTPException(status_code=500, detail=err_msg)

  except Exception as e:
    send_whatsapp_alert(str(e))
    raise HTTPException(status_code=500, detail=str(e))


@app.post("/webhook/dana-payment")
def payment_webhook(payment: PaymentWebhook):
  if payment.status in ["settlement", "success"]:
    db = load_db()
    db["orders"].append({
        "order_id": payment.order_id,
        "amount": payment.amount,
        "status": "PAID",
    })
    save_db(db)
    print(
        f"\n[DANA PAYMENT]: 💰 Rp {payment.amount} (ID: {payment.order_id})"
        " berhasil masuk ke akun DANA Anda secara otomatis!\n"
    )
    return {
        "status": "handled",
        "message": (
            "Pembayaran DANA terkonfirmasi! Sistem agen AI mandiri siap bekerja."
        ),
    }
  return {"status": "ignored"}


if __name__ == "__main__":
  import uvicorn

  uvicorn.run(app, host="0.0.0.0", port=8000)
