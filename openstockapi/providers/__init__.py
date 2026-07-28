from openstockapi.providers.vn_stock.providers.mas import MASProvider
from openstockapi.providers.vn_stock.providers.dnse import DNSEProvider
from openstockapi.providers.vn_stock.providers.vndirect import VNDIRECTProvider
from openstockapi.providers.vn_stock.providers.vci import VCIProvider
from openstockapi.providers.vn_stock.providers.mbk import MBKProvider
from openstockapi.providers.vn_stock.providers.fmarket import FmarketProvider
from openstockapi.providers.vn_stock.providers.kbs import KBSProvider
from openstockapi.providers.vn_stock.providers.tcbs import TCBSProvider
from openstockapi.providers.vn_stock.providers.msn import MSNProvider
from openstockapi.providers.core import CoreProvider

# In Phase 1, we also instantiate the VCI provider as stub or simple registry
PROVIDERS = {
    "mas": MASProvider(),
    "dnse": DNSEProvider(),
    "vndirect": VNDIRECTProvider(),
    "vci": VCIProvider(),
    "mbk": MBKProvider(),
    "fmarket": FmarketProvider(),
    "kbs": KBSProvider(),
    "tcbs": TCBSProvider(),
    "msn": MSNProvider(),
    "core": CoreProvider(),
}


def get_provider(name: str):
    return PROVIDERS.get(name.lower())
