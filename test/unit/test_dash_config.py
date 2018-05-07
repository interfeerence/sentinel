import pytest
import os
import sys
import re
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
os.environ['SENTINEL_ENV'] = 'test'
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))
import config
from exilium_config import ExiliumConfig


@pytest.fixture
def exilium_conf(**kwargs):
    defaults = {
        'rpcuser': 'exiliumrpc',
        'rpcpassword': 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk',
        'rpcport': 29241,
    }

    # merge kwargs into defaults
    for (key, value) in kwargs.items():
        defaults[key] = value

    conf = """# basic settings
testnet=1 # TESTNET
server=1
rpcuser={rpcuser}
rpcpassword={rpcpassword}
rpcallowip=127.0.0.1
rpcport={rpcport}
""".format(**defaults)

    return conf


def test_get_rpc_creds():
    exilium_config = exilium_conf()
    creds = ExiliumConfig.get_rpc_creds(exilium_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'exiliumrpc'
    assert creds.get('password') == 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk'
    assert creds.get('port') == 29241

    exilium_config = exilium_conf(rpcpassword='s00pers33kr1t', rpcport=8000)
    creds = ExiliumConfig.get_rpc_creds(exilium_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'exiliumrpc'
    assert creds.get('password') == 's00pers33kr1t'
    assert creds.get('port') == 8000

    no_port_specified = re.sub('\nrpcport=.*?\n', '\n', exilium_conf(), re.M)
    creds = OmegaConfig.get_rpc_creds(no_port_specified, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'exiliumrpc'
    assert creds.get('password') == 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk'
    assert creds.get('port') == 17778


# ensure omegacoin network (mainnet, testnet) matches that specified in config
# requires running omegacoind on whatever port specified...
#
# This is more of a omegacoind/jsonrpc test than a config test...
