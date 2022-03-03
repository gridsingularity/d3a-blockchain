"""
Copyright 2018 Grid Singularity
This file is part of D3A.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import logging
import uuid
from datetime import datetime

from gsy_dex.trade_store import template_type_registry
from gsy_dex.trade_store.constants import (
    mnemonic, BOB_STASH_ADDRESS, ALICE_STASH_ADDRESS, ENERGY_SCALING_FACTOR, RATE_SCALING_FACTOR,
    default_call_module, default_call_function,
    TEMPLATE_NODE_ADDRESS_TYPE, DEFAULT_SUBSTRATE_URL)
from substrateinterface import Keypair  # NOQA
from substrateinterface import SubstrateInterface
from substrateinterface.exceptions import SubstrateRequestException

logger = logging.getLogger()


class SubstrateBlockchainInterface:
    def __init__(self, market_id, simulation_id=None):
        self.market_id = market_id
        self.simulation_id = simulation_id
        self.substrate = SubstrateInterface(
            url=DEFAULT_SUBSTRATE_URL,
            ss58_format=TEMPLATE_NODE_ADDRESS_TYPE,
            type_registry_preset='substrate-node-template',
            type_registry=template_type_registry
        )

    def load_keypair(self):
        return Keypair.create_from_mnemonic(mnemonic, ss58_format=TEMPLATE_NODE_ADDRESS_TYPE)

    def compose_call(self, call_module, call_function, call_params):
        call = self.substrate.compose_call(
            call_module=call_module,
            call_function=call_function,
            call_params=call_params
        )
        return call

    def create_new_offer(self, energy, price, seller):
        return str(uuid.uuid4())

    def cancel_offer(self, offer):
        pass

    def change_offer(self, offer, original_offer, residual_offer):
        pass

    def handle_blockchain_trade_event(self, offer, buyer, original_offer, residual_offer):
        return str(uuid.uuid4()), residual_offer

    def track_trade_event(self, time_slot, trade):
        call_params = {
            'simulation_id': str(self.simulation_id),
            'market_id': str(self.market_id),
            'market_slot': datetime.timestamp(time_slot),
            'trade_id': trade.id,
            'buyer': ALICE_STASH_ADDRESS,
            'seller': BOB_STASH_ADDRESS,
            'energy': int(trade.offer_bid.energy * ENERGY_SCALING_FACTOR),
            'rate': int(trade.offer_bid.energy_rate * RATE_SCALING_FACTOR)
        }

        call = self.substrate.compose_call(
            default_call_module,
            default_call_function,
            call_params
        )

        keypair = Keypair.create_from_mnemonic(mnemonic)
        extrinsic = self.substrate.create_signed_extrinsic(call=call, keypair=keypair)

        try:
            result = self.substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
            logger.info("Extrinsic '{}' sent and included in block '{}'".format(
                result['extrinsic_hash'], result['block_hash']))

        except SubstrateRequestException as e:
            logger.info("Failed to send: {}".format(e))

    def bc_listener(self):
        pass
