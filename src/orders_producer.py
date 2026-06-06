"""
Ruta 1 - Orders Producer (orders-api):
  - Publica Command Message a billing.queue  (Point-to-Point)
  - Publica Event Message a orders.exchange  (Publish/Subscribe)
  - Opcionalmente envía mensajes inválidos para probar el error handler
"""
import pika, json, time

RABBITMQ_HOST = "localhost"
RABBITMQ_USER = "admin"
RABBITMQ_PASS = "admin123"

def get_channel():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    params = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    connection = pika.BlockingConnection(params)
    return connection, connection.channel()

def send_billing_command(channel, order_id, customer_id, total, msg_id):
    """Ruta A: Point-to-Point -> billing.queue (Command Message)"""
    message = {
        "messageId": msg_id,
        "messageType": "GenerarFactura",
        "orderId": order_id,
        "customerId": customer_id,
        "total": total
    }
    channel.basic_publish(
        exchange="",
        routing_key="billing.queue",
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # mensaje persistente
            content_type="application/json"
        )
    )
    print(f"[PRODUCER] Command Message enviado a billing.queue: {message}")

def send_order_event(channel, order_id, customer_id, total, event_id):
    """Ruta B: Publish/Subscribe -> orders.exchange (Event Message)"""
    event = {
        "eventId": event_id,
        "eventType": "PedidoCreado",
        "occurredAt": "2026-06-06T10:30:00Z",
        "source": "orders-api",
        "payload": {
            "orderId": order_id,
            "customerId": customer_id,
            "total": total
        }
    }
    channel.basic_publish(
        exchange="orders.exchange",
        routing_key="",
        body=json.dumps(event),
        properties=pika.BasicProperties(
            delivery_mode=2,
            content_type="application/json"
        )
    )
    print(f"[PRODUCER] Event Message publicado en orders.exchange: {event}")

def send_invalid_message(channel):
    """Ruta E (prueba): mensaje sin orderId -> debe ir a invalid-message.queue"""
    invalid = {
        "messageId": "msg-invalid-001",
        "messageType": "GenerarFactura",
        "customerId": "CLI-9999",
        "total": 0  # total inválido
    }
    channel.basic_publish(
        exchange="",
        routing_key="billing.queue",
        body=json.dumps(invalid),
        properties=pika.BasicProperties(delivery_mode=2, content_type="application/json")
    )
    print(f"[PRODUCER] Mensaje INVÁLIDO enviado (sin orderId, total=0): {invalid}")

if __name__ == "__main__":
    conn, ch = get_channel()

    # Caso 1: Facturación válida
    send_billing_command(ch, "ORD-1001", "CLI-2001", 59.90, "msg-001")
    time.sleep(0.3)

    # Caso 2: Evento PedidoCreado válido
    send_order_event(ch, "ORD-1001", "CLI-2001", 59.90, "evt-001")
    time.sleep(0.3)

    # Segundo pedido (para probar dos consumidores de billing)
    send_billing_command(ch, "ORD-1002", "CLI-2002", 120.00, "msg-002")
    time.sleep(0.3)
    send_order_event(ch, "ORD-1002", "CLI-2002", 120.00, "evt-002")
    time.sleep(0.3)

    # Caso 3 y 4: Mensajes inválidos
    send_invalid_message(ch)

    # Caso adicional: JSON totalmente inválido
    ch.basic_publish(
        exchange="",
        routing_key="billing.queue",
        body=b"esto no es json {{{",
        properties=pika.BasicProperties(delivery_mode=2, content_type="application/json")
    )
    print("[PRODUCER] Mensaje con JSON malformado enviado a billing.queue")

    conn.close()
    print("\n[PRODUCER] Todos los mensajes enviados.")
