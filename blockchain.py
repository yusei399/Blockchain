import hashlib
import logging
import time 
import sys
import json

from ecdsa import NIST256p
from ecdsa import VerifyingKey

import utils
import wallet

MINING_DFFICULTY = 3
MINING_SENDER = 'THE BLOCKCAHIN'
MINING_REWARD = 1.0

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

class BlockChain(object):

	def __init__ (self, blockchain_address=None):
		self.transaction_pool = []
		self.chain = []
		self.create_block(0, self.hash({}))
		self.blockchain_address = blockchain_address
	
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
		#sorted_block = json.dumps(block, sort_keys=True)
		return hashlib.sha256(str(block).encode()).hexdigest()
	
	def add_transaction(self, sender_blockchain_address, recipient_blockchain_adress, value, sender_public_key=None, signature=None):
		transaction = utils.sorted_dict_by_key({
			'sender_blockchain_address' : sender_blockchain_address,
			'recipient_blockchain_adress' : recipient_blockchain_adress,
			'value' : float(value)
		})
		if sender_blockchain_address == MINING_SENDER:
			self.transaction_pool.append(transaction)
			return True

		if self.verify_transaction_signature(sender_public_key, signature, transaction):
			self.transaction_pool.append(transaction)
			return True
		return False

	def verify_transaction_signature(self, sender_public_key, signature, transaction):
		sha256 = hashlib.sha256()
		sha256.update(str(transaction).encode('utf-8'))
		message = sha256.digest()
		signature_bytes = bytes().fromhex(signature)
		verifying_Key = VerifyingKey.from_string(bytes().fromhex(sender_public_key), curve=NIST256p)
		verified_key = verifying_Key.verify(signature_bytes,message)
		return verified_key
		
	
	def valid_proof(self, transactions, previous_hash, nonce, difficulty=MINING_DFFICULTY):
		guess_block = utils.sorted_dict_by_key({
			'transactions' : transactions,
			'nonce' : nonce,
			'previous_hash' : previous_hash
		})
		guess_hash = self.hash(guess_block)
		return guess_hash[:difficulty] == '0' * difficulty

	def proof_of_work(self):
		transactions = self.transaction_pool.copy()
		previous_hash = self.hash(self.chain[-1])
		nonce = 0
		while self.valid_proof(transactions, previous_hash, nonce) is False:
			nonce += 1
		return nonce

	def mining(self):
		nonce = self.proof_of_work()
		self.add_transaction(
		sender_blockchain_address=MINING_SENDER,
		recipient_blockchain_adress=self.blockchain_address,
		value=MINING_REWARD 
		)
		previous_hash = self.hash(self.chain[-1])
		self.create_block(nonce, previous_hash)
		logger.info({'action' :'mining', 'status' : 'success'})
		return True

	def calculate_total_amount(self,blockchain_address):
		total_amount = 0.0
		for block in self.chain:
			for transaction in block['transactions']:
				value = float(transaction['value'])
				if blockchain_address == transaction['recipient_blockchain_adress']:
					total_amount += value
				if blockchain_address == transaction['sender_blockchain_address']:
					total_amount -= value
		return total_amount



