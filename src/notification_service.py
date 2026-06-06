"""
Ruta C - Notification Service:
  Consume de notification.queue (Publish/Subscribe via orders.exchange).
  Simula el envío de notificación al cliente.
"""
import pika, json
from validator import validate_message

RABBITMQ_HOST = "localhost"
RABBITMQ_USER = "admin"
RABBITMQ_PASS = "admin123"

def callback(ch, method, properties, body):
    is_valid, data, reason = validate_message(body)

    if not is_valid:
        print(f"[NOTIFICATION] Evento INVÁLIDO: {reason}. Descartando.")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        return

    payload = data.get("payload", {})
    print(f"[NOTIFICATION] Evento PedidoCreado recibido:")
    print(f"  - EventId:    {data.get('eventId')}")
    print(f"  - OrderId:    {payload.get('orderId')}")
    print(f"  - CustomerId: {payload.get('customerId')}")
    print(f"  - Total:      ${payload.get('total'):.2f}")
    print(f"[NOTIFICATION] Notificacion enviada al cliente {payload.get('customerId')} por correo.")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    params = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="notification.queue", on_message_callback=callback)
    print("[NOTIFICATION] Esperando eventos en notification.queue (Publish/Subscribe)...")
    channel.start_consuming()

if __name__ == "__main__":
    main()
