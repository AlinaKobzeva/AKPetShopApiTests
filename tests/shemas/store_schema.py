STORE_SCHEMA = {
    "type": "object",
    "properties": {
        "approved": {
            "type": "integer"
        },
        "delivered": {
            "type": "integer"
        }
    },
    "additionalProperties": False,
    "required": [
        "approved",
        "delivered"
    ]
}

ORDER_SCHEMA  = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "petId": {
            "type": "integer"
        },
        "quantity": {
            "type": "integer"
        },
        "shipDate": {
            "type": "string"
        },
        "status": {
            "type": "string"
        },
        "complete": {
            "type": "boolean"
        }
    },
    "additionalProperties": False,
    "required": [
        "id",
        "petId",
        "quantity",
        "status",
        "complete"
    ]
}