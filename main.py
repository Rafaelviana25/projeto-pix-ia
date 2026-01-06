import os
from flask import Flask, request, jsonify
import mercadopago
from supabase import create_client

app = Flask(__name__)

# O Render lerá estas variáveis da aba "Environment"
MP_ACCESS_TOKEN = os.environ.get("MP_ACCESS_TOKEN")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

sdk = mercadopago.SDK(MP_ACCESS_TOKEN)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/gerar-pix', methods=['POST'])
def gerar_pix():
    data = request.json
    email = data.get("email_usuario")
    
    payment_data = {
        "transaction_amount": 29.90,
        "description": "Assinatura Pro",
        "payment_method_id": "pix",
        "payer": {"email": email}
    }
    
    result = sdk.payment().create(payment_data)
    pix_data = result["response"]["point_of_interaction"]["transaction_data"]
    
    # Salva no Supabase
    supabase.table("assinaturas_pix").insert({
        "email": email, 
        "status_assinatura": "pendente"
    }).execute()
    
    return jsonify({"pix_code": pix_data["qr_code"]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
