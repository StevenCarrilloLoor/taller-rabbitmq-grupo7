"""
Setup: crea exchanges, queues y bindings en RabbitMQ.
Ejecutar UNA VEZ antes de arrancar los servicios.
"""
import pika

RABBITMQ_HOST = "localhost"
RABBITMQ_USER = "admin"
RABBITMQ_PASS = "admin123"

def setup():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    params = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # --- Dead Letter Exchange para mensajes inválidos ---
    channel.exchange_declare(exchange="dlx.exchange", exchange_type="direct", durable=True)
    channel.queue_declare(queue="invalid-message.queue", durable=True)
    channel.queue_bind(queue="invalid-message.queue", exchange="dlx.exchange", routing_key="invalid")

    # --- Point-to-Point: billing.queue ---
    channel.queue_declare(
        queue="billing.queue",
        durable=True,
        arguments={
            "x-dead-letter-exchange": "dlx.exchange",
            "x-dead-letter-routing-key": "invalid"
        }
    )

    # --- Publish/Subscribe: orders.exchange (fanout) ---
    channel.exchange_declare(exchange="orders.exchange", exchange_type="fanout", durable=True)
    channel.queue_declare(queue="notification.queue", durable=True)
    channel.queue_declare(queue="analytics.queue", durable=True)
    channel.queue_bind(queue="notification.queue", exchange="orders.exchange", routing_key="")
    channel.queue_bind(queue="analytics.queue", exchange="orders.exchange", routing_key="")

    connection.close()
    print("[SETUP] Exchanges y queues creados correctamente.")
    print("  - dlx.exchange         -> invalid-message.queue")
    print("  - billing.queue        (Point-to-Point, DLX configurado)")
    print("  - orders.exchange      (Publish/Subscribe, fanout)")
    print("    -> notification.queue")
    print("    -> analytics.queue")

if __name__ == "__main__":
    setup()
