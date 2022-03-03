import os

mnemonic = os.environ.get("SUBSTRATE_MNEMONIC", "MNEMONIC_TO_RESTORE_YOUR_KEYPAIR")

DEFAULT_SUBSTRATE_URL = os.getenv('DEFAULT_SUBSTRATE_URL',"wss://verifier-node.dev.gridsingularity.com/")
TEMPLATE_NODE_ADDRESS_TYPE = os.getenv('TEMPLATE_NODE_ADDRESS_TYPE',42)

BC_NUM_FACTOR = 10 ** 12
BOB_STASH_ADDRESS = "5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK1iQ7qUsSWFc"
ALICE_STASH_ADDRESS = "5GNJqTPyNqANBkUVMN1LPPrxXnFouWXoe2wNSmmEoLctxiZY"
ENERGY_SCALING_FACTOR = 1e6  # kWh to Wh with 3 decimal point
RATE_SCALING_FACTOR = 1e3  # cents/kWh with 3 decimal point

default_call_module = 'Tradestorage'
default_call_function = 'store_trade_map'
default_energy: 1 * BC_NUM_FACTOR
default_rate = 12
