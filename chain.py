import logging
import sys
import time
import hashlib
import json

import utils

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

class BlockChain(object):

	def __init__(self):
		self.transaction_pool = []
		self.chain = []
		self.create_block(0, self.hash({}))

	def create_block(self, nonce, previous_hash):
		block = utils.sorted_dict_by_key({
			'timestamp' : time.time(),
			'transactions' : self.transaction_pool,
			'nonce' : nonce,
			'previous_hash' : previous_hash
		})
		self.chain.append(block)
		self.transaction_pool = []
		return block

	def hash(self, block):
		sorted_block = json.dumps(block, sort_keys=True)
		return hashlib.sha256(sorted_block.encode()).hexdigest()

	def add_transaction(self, sender_block_addres,recipient_blockchain_ddress, value):
		transaction = utils.sorted_dict_by_key({
			'sender_block_addres': sender_block_addres,
			'recipient_blockchain_ddress' : recipient_blockchain_ddress,
			'value' : float(value)
		})
		self.transaction_pool.append(transaction)
		return True


def pprint(chains):
	for i, chain in enumerate(chains):
		print(f'{"="*25} Chain{i} {"="*25}')
		for k, v in chain.items():
			if k == 'transactions':
				print(k)
				for d in v:
					print(f'{"-"*40}')
					for kk, vv, in d.items():
						print(f' {kk:30}{vv}')
			else:
				print(f'{k:15}{v}')
	print(f'{"*"*25}')

	
if __name__ == '__main__':
	block_chain = BlockChain()
	pprint(block_chain.chain)

	block_chain.add_transaction('A', 'B', 1.0)
	previous_hash = block_chain.hash(block_chain.chain[-1])
	block_chain.create_block(5, previous_hash)
	pprint(block_chain)

	block_chain.add_transaction('A', 'B', 2.0)
	block_chain.add_transaction('X', 'Y', 3.0)
	block_chain.create_block(2, previous_hash)
	pprint(block_chain.chain)



