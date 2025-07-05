from openvino.runtime import Core
core = Core()
print(core.available_devices)

device = "GPU"

print(core.get_property(device, "FULL_DEVICE_NAME"))

print(f"{device} SUPPORTED_PROPERTIES:\n")
supported_properties = core.get_property(device, "SUPPORTED_PROPERTIES")
indent = len(max(supported_properties, key=len))

for property_key in supported_properties:
    if property_key not in ('SUPPORTED_METRICS', 'SUPPORTED_CONFIG_KEYS', 'SUPPORTED_PROPERTIES'):
        try:
            property_val = core.get_property(device, property_key)
        except TypeError:
            property_val = 'UNSUPPORTED TYPE'
        print(f"{property_key:<{indent}}: {property_val}")