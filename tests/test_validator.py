"""
Tests unitarios para el módulo validator.py
Cubre los 5 casos de prueba del taller + casos adicionales.
"""
import sys
import os
import json
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from validator import validate_message, validate_command_message, validate_event_message

# ─────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────

def make_billing(msg_id="msg-001", order_id="ORD-1001", customer_id="CLI-2001", total=59.90):
    return {
        "messageId": msg_id,
        "messageType": "GenerarFactura",
        "orderId": order_id,
        "customerId": customer_id,
        "total": total
    }

def make_event(event_id="evt-001", order_id="ORD-1001", customer_id="CLI-2001", total=59.90):
    return {
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

# ─────────────────────────────────────────────
# CASO 1: Command Message válido (GenerarFactura)
# ─────────────────────────────────────────────

class TestCaso1FacturacionValida:
    def test_billing_valido_retorna_true(self):
        data = make_billing()
        valid, reason = validate_command_message(data)
        assert valid is True
        assert reason is None

    def test_billing_valido_via_validate_message(self):
        body = json.dumps(make_billing()).encode()
        is_valid, data, reason = validate_message(body)
        assert is_valid is True
        assert reason is None
        assert data["orderId"] == "ORD-1001"

# ─────────────────────────────────────────────
# CASO 2: Event Message PedidoCreado válido
# ─────────────────────────────────────────────

class TestCaso2EventoPedidoCreado:
    def test_evento_valido_retorna_true(self):
        data = make_event()
        valid, reason = validate_event_message(data)
        assert valid is True
        assert reason is None

    def test_evento_valido_via_validate_message(self):
        body = json.dumps(make_event()).encode()
        is_valid, data, reason = validate_message(body)
        assert is_valid is True
        assert data["eventId"] == "evt-001"

    def test_evento_llega_a_dos_consumidores(self):
        """Verifica que el mensaje de evento es válido para múltiples consumidores."""
        body = json.dumps(make_event()).encode()
        # Simula notification-service
        is_valid_notif, _, _ = validate_message(body)
        # Simula analytics-service (mismo mensaje)
        is_valid_analyt, _, _ = validate_message(body)
        assert is_valid_notif is True
        assert is_valid_analyt is True

# ─────────────────────────────────────────────
# CASO 3: Mensaje sin orderId → inválido
# ─────────────────────────────────────────────

class TestCaso3SinOrderId:
    def test_sin_order_id_retorna_false(self):
        data = {k: v for k, v in make_billing().items() if k != "orderId"}
        valid, reason = validate_command_message(data)
        assert valid is False
        assert "orderid" in reason.lower()

    def test_sin_order_id_via_validate_message(self):
        msg = make_billing()
        del msg["orderId"]
        body = json.dumps(msg).encode()
        is_valid, _, reason = validate_message(body)
        assert is_valid is False
        assert reason is not None

    def test_sin_order_id_en_evento(self):
        """Evento con payload sin orderId también es inválido."""
        msg = make_event()
        del msg["payload"]["orderId"]
        body = json.dumps(msg).encode()
        is_valid, _, reason = validate_message(body)
        assert is_valid is False

# ─────────────────────────────────────────────
# CASO 4: Total inválido (0 o negativo)
# ─────────────────────────────────────────────

class TestCaso4TotalInvalido:
    def test_total_cero_es_invalido(self):
        data = make_billing(total=0)
        valid, reason = validate_command_message(data)
        assert valid is False
        assert "total" in reason.lower()

    def test_total_negativo_es_invalido(self):
        data = make_billing(total=-10.5)
        valid, reason = validate_command_message(data)
        assert valid is False

    def test_total_positivo_es_valido(self):
        data = make_billing(total=0.01)
        valid, reason = validate_command_message(data)
        assert valid is True

    def test_total_cero_en_evento(self):
        msg = make_event(total=0)
        body = json.dumps(msg).encode()
        is_valid, _, reason = validate_message(body)
        assert is_valid is False

# ─────────────────────────────────────────────
# CASO 5: Sin messageId/eventId
# ─────────────────────────────────────────────

class TestSinIdentificador:
    def test_sin_message_id_es_invalido(self):
        data = make_billing()
        del data["messageId"]
        valid, reason = validate_command_message(data)
        assert valid is False

    def test_sin_event_id_es_invalido(self):
        data = make_event()
        del data["eventId"]
        valid, reason = validate_event_message(data)
        assert valid is False

# ─────────────────────────────────────────────
# JSON malformado
# ─────────────────────────────────────────────

class TestJsonMalformado:
    def test_json_invalido_retorna_false(self):
        body = b"esto no es json {{{invalid}}}"
        is_valid, _, reason = validate_message(body)
        assert is_valid is False
        assert "json" in reason.lower()

    def test_body_vacio_retorna_false(self):
        body = b""
        is_valid, _, reason = validate_message(body)
        assert is_valid is False

    def test_tipo_desconocido_retorna_false(self):
        """Mensaje sin messageId ni eventId es tipo desconocido."""
        msg = {"foo": "bar", "orderId": "ORD-001"}
        body = json.dumps(msg).encode()
        is_valid, _, reason = validate_message(body)
        assert is_valid is False

# ─────────────────────────────────────────────
# Sin customerId
# ─────────────────────────────────────────────

class TestSinCustomerId:
    def test_sin_customer_id_es_invalido(self):
        data = make_billing()
        del data["customerId"]
        valid, reason = validate_command_message(data)
        assert valid is False
        assert "customerid" in reason.lower()
