ALLOWED_LAYERS = [
    "IDENTITY",
    "PUBLIC",
    "GOVERNANCE",
    "HIDDEN",
    "POSITION"
]


def validate_layer(layer):
    if layer not in ALLOWED_LAYERS:
        raise ValueError("Invalid layer assignment")
