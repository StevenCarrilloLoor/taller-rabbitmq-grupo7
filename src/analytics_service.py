"""
Ruta D - Analytics Service:
  Consume de analytics.queue (Publish/Subscribe via orders.exchange).
  Simula el registro analítico del pedido.
"""
import pika, json
from validator import validate_message

RABBITMQ_HOST = "localhost"
RABBITMQ_USER = "admin"
RABBITMQ_PASS = "admin123"

def callback(ch, method, properties, body):
    is_valid, data, reason = validate_message(body)

    if not is_valid:
        print(f"[ANALYTICS] Evento INVÁLIDO: {reason}. Descartando.")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        return

    payload = data.get("payload", {})
    print(f"[ANALYTICS] Evento PedidoCreado registrado en analítica:")
    print(f"  - EventId:    {data.get('eventId')}")
    print(f"  - OrderId:    {payload.get('orderId')}")
    print(f"  - Total:      ${payload.get('total'):.2f}")
    print(f"  - OcurredAt:  {data.get('occurredAt')}")
    print(f"[ANALYTICS] Registro guardado en sistema de BI.")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    params = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="analytics.queue", on_message_callback=callback)
    print("[ANALYTICS] Esperando eventos en analytics.queue (Publish/Subscribe)...")
    channel.start_consuming()

if __name__ == "__main__":
    main()
