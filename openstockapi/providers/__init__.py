from openstockapi.providers.core import CoreProvider

PROVIDERS = {
    "core": CoreProvider(),
}


def get_provider(name: str):
    return PROVIDERS.get(name.lower())
