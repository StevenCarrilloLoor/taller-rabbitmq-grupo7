"""
Validador de mensajes según las reglas del taller.
Retorna (True, None) si el mensaje es válido,
o (False, "motivo") si es inválido.
"""
import json

def validate_command_message(data: dict):
    """Valida un Command Message (e.g. GenerarFactura)."""
    if not data.get("messageId"):
        return False, "Falta messageId"
    if not data.get("orderId"):
        return False, "Falta orderId"
    if not data.get("customerId"):
        return False, "Falta customerId"
    total = data.get("total")
    if total is None or total <= 0:
        return False, f"Total inválido: {total}"
    return True, None

def validate_event_message(data: dict):
    """Valida un Event Message (e.g. PedidoCreado)."""
    if not data.get("eventId"):
        return False, "Falta eventId"
    if not data.get("eventType"):
        return False, "Falta eventType"
    payload = data.get("payload", {})
    if not payload.get("orderId"):
        return False, "Falta payload.orderId"
    if not payload.get("customerId"):
        return False, "Falta payload.customerId"
    total = payload.get("total")
    if total is None or total <= 0:
        return False, f"payload.total inválido: {total}"
    return True, None

def validate_message(body: bytes):
    """Detecta tipo y valida. Retorna (is_valid, data_dict, reason)."""
    try:
        data = json.loads(body)
    except Exception:
        return False, {}, "JSON malformado"

    if "messageId" in data:
        valid, reason = validate_command_message(data)
    elif "eventId" in data:
        valid, reason = validate_event_message(data)
    else:
        return False, data, "Tipo de mensaje desconocido (falta messageId o eventId)"

    return valid, data, reason
