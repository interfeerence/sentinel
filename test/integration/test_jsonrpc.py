import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from exiliumd import ExiliumDaemon
from exilium_config import ExiliumConfig


def test_exiliumd():
    config_text = ExiliumConfig.slurp_config_file(config.exilium_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000254161b06b5477d23be9c9098a3938682e1526032ff70a3ee112312ebfc'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c'

    creds = ExiliumConfig.get_rpc_creds(config_text, network)
    exiliumd = ExiliumDaemon(**creds)
    assert exiliumd.rpc_command is not None

    assert hasattr(exiliumd, 'rpc_connection')

    # Omega testnet block 0 hash == 0000041a9498884aa2506b9dc832af53de1cbee3dca196a8d7b4319ee3a0f27c
    # test commands without arguments
    info = exiliumd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert exiliumd.rpc_command('getblockhash', 0) == genesis_hash
