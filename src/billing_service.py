"""
Ruta A - Billing Service:
  Consume de billing.queue (Point-to-Point Channel).
  Solo UN consumidor procesa cada mensaje.
  Valida el mensaje; si es inválido lo reenvía a invalid-message.queue (NACK + DLX).
"""
import pika, json, sys
from validator import validate_message

RABBITMQ_HOST = "localhost"
RABBITMQ_USER = "admin"
RABBITMQ_PASS = "admin123"
INSTANCE_ID = sys.argv[1] if len(sys.argv) > 1 else "A"

def callback(ch, method, properties, body):
    is_valid, data, reason = validate_message(body)

    if not is_valid:
        print(f"[BILLING-{INSTANCE_ID}] Mensaje INVÁLIDO recibido -> enviando a DLX. Razón: {reason}")
        print(f"[BILLING-{INSTANCE_ID}] Cuerpo: {body.decode(errors='replace')}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)  # DLX lo captura
        return

    print(f"[BILLING-{INSTANCE_ID}] Procesando factura:")
    print(f"  - OrderId:    {data.get('orderId')}")
    print(f"  - CustomerId: {data.get('customerId')}")
    print(f"  - Total:      ${data.get('total'):.2f}")
    print(f"  - MessageId:  {data.get('messageId')}")
    print(f"[BILLING-{INSTANCE_ID}] Factura generada con exito.")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    params = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)  # garantiza distribución equitativa entre instancias
    channel.basic_consume(queue="billing.queue", on_message_callback=callback)
    print(f"[BILLING-{INSTANCE_ID}] Esperando mensajes en billing.queue (Point-to-Point)...")
    channel.start_consuming()

if __name__ == "__main__":
    main()
