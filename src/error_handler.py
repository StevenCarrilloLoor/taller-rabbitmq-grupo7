"""
Ruta E - Error Handler:
  Consume de invalid-message.queue (Invalid Message Channel / Dead Letter Queue).
  Registra los mensajes inválidos o fallidos para auditoría.
"""
import pika, json

RABBITMQ_HOST = "localhost"
RABBITMQ_USER = "admin"
RABBITMQ_PASS = "admin123"

def callback(ch, method, properties, body):
    print(f"[ERROR-HANDLER] Mensaje inválido/fallido recibido en invalid-message.queue:")
    try:
        data = json.loads(body)
        print(f"  - Contenido: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except Exception:
        print(f"  - Contenido (raw): {body.decode(errors='replace')}")
    print(f"[ERROR-HANDLER] Mensaje registrado en log de auditoría.")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    params = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.basic_consume(queue="invalid-message.queue", on_message_callback=callback)
    print("[ERROR-HANDLER] Esperando mensajes inválidos en invalid-message.queue...")
    channel.start_consuming()

if __name__ == "__main__":
    main()
