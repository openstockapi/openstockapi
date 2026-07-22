from openstockapi.providers.mas import MASProvider
from openstockapi.providers.dnse import DNSEProvider
from openstockapi.providers.vndirect import VNDIRECTProvider
from openstockapi.providers.vci import VCIProvider
from openstockapi.providers.mbk import MBKProvider
from openstockapi.providers.fmarket import FmarketProvider
from openstockapi.providers.kbs import KBSProvider
from openstockapi.providers.tcbs import TCBSProvider
from openstockapi.providers.msn import MSNProvider

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
}



def get_provider(name: str):
    return PROVIDERS.get(name.lower())
