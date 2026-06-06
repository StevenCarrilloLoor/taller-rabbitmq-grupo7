# Taller Semana 8 - Patrones Básicos de Mensajería con RabbitMQ
**Integración de Sistemas | UDLA | Grupo 7**

## Descripción
Implementación de patrones de mensajería empresarial usando RabbitMQ y Apache Camel (rutas en XML).
Incluye: Point-to-Point, Publish/Subscribe, Command Message, Event Message, Invalid Message Channel y Dead Letter Exchange.

## Prerrequisitos
- Python 3.8+
- Docker Desktop (corriendo)
- Git

## Instalación y Ejecución (paso a paso)

### Windows:
```
ejecutables/1_instalar.bat
ejecutables/2_levantar_rabbitmq.bat
ejecutables/3_iniciar_servicios.bat
ejecutables/4_enviar_mensajes.bat
ejecutables/5_correr_tests.bat
```

### Linux / Mac:
```bash
bash ejecutables/1_instalar.sh
bash ejecutables/2_levantar_rabbitmq.sh
bash ejecutables/3_iniciar_servicios.sh
bash ejecutables/4_enviar_mensajes.sh
bash ejecutables/5_correr_tests.sh
```

## Arquitectura
```
orders-api (producer)
    |
    +--[Command Message]--> billing.queue -----------> billing-service (A o B)
    |   (Point-to-Point)                               (solo UNA instancia procesa)
    |
    +--[Event Message]---> orders.exchange (fanout)
        (Publish/Subscribe)     |
                                +---> notification.queue ---> notification-service
                                +---> analytics.queue   ---> analytics-service

Validación fallida --> invalid-message.queue <-- (Dead Letter Exchange)
                                                      |
                                               error-handler
```

## Exchanges y Queues
| Nombre | Tipo | Patrón |
|---|---|---|
| `billing.queue` | Direct Queue | Point-to-Point |
| `orders.exchange` | Fanout Exchange | Publish/Subscribe |
| `notification.queue` | Queue (bind a orders.exchange) | Suscriptor |
| `analytics.queue` | Queue (bind a orders.exchange) | Suscriptor |
| `dlx.exchange` | Dead Letter Exchange | Error handling |
| `invalid-message.queue` | Queue | Invalid Message Channel |

## RabbitMQ Management UI
- URL: http://localhost:15672
- Usuario: `admin`
- Contraseña: `admin123`

## Tests
```bash
bash ejecutables/5_correr_tests.sh
```

## Estructura del proyecto
```
rabbitmq-taller/
├── docker-compose.yml
├── requirements.txt
├── README.md
├── src/
│   ├── setup_rabbitmq.py       # Configura exchanges y queues
│   ├── orders_producer.py      # Orders API - publica mensajes
│   ├── billing_service.py      # Consumidor Point-to-Point
│   ├── notification_service.py # Consumidor Pub/Sub
│   ├── analytics_service.py    # Consumidor Pub/Sub
│   ├── error_handler.py        # Consumidor cola de errores
│   ├── validator.py            # Lógica de validación de mensajes
│   └── camel_routes.xml        # Rutas equivalentes en Apache Camel DSL
├── tests/
│   └── test_validator.py       # Tests unitarios (pytest)
└── ejecutables/
    ├── 1_instalar.bat / .sh
    ├── 2_levantar_rabbitmq.bat / .sh
    ├── 3_iniciar_servicios.bat / .sh
    ├── 4_enviar_mensajes.bat / .sh
    ├── 5_correr_tests.bat / .sh
    └── 6_detener_todo.bat / .sh
```
