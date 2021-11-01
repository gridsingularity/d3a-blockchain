from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException

template_type_registry = {
  "runtime_id": 2,
  "types": {
    "MyCustomInt": "u32",
    "MyStruct": {
      "type": "struct",
      "type_mapping": [
         ["account", "AccountId"],
         ["message", "Vec<u8>"]
      ]
    }
  },
  "versioning": [
  ]
}

verifier_node_url = "wss://verifier-node.dev.gridsingularity.com"
template_call_module = 'TemplateModule'
template_call_function = 'do_something'
address_type = 42

substrate = SubstrateInterface(
    url=verifier_node_url,
    ss58_format=42,
    type_registry_preset='substrate-node-template',
    type_registry=template_type_registry
)

keypair = Keypair.create_from_mnemonic(mnemonic='', ss58_format=0)

# block_hash=None by default gives the genesis block
block = substrate.get_block(block_hash=None)

# ensure you have enough funds before calling this module
balance_call_params = {
    'dest': '14E5nqKAp3oAJcmzgZhUD2RcptBeUBScxKHgJKU4HPNcKVf3',
    'value': 1000
}
balance_call = substrate.compose_call(
    call_module='Balances',
    call_function='transfer',
    call_params=balance_call_params
)

template_call_params = {'something': 5}
template_call = substrate.compose_call(
    template_call_module,
    template_call_function,
    template_call_params
)

extrinsic = substrate.create_signed_extrinsic(call=template_call, keypair=keypair)

try:
    receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
    print("Extrinsic '{}' sent and included in block '{}'".format(receipt.extrinsic_hash,
                                                                  receipt.block_hash))

except SubstrateRequestException as e:
    print("Failed to send: {}".format(e))
