from architectures.blockchain import Blockchain
from architectures.block import Block
from architectures.address import Address
from architectures.transaction import Transaction
from architectures.nft import CollectionStorage, AssetStorage, TradeStorage
from datetime import datetime

class Trilio:
    def __init__(self):
        self.trilio = Blockchain(
            name="Trilio", 
            difficulty=4,
            minimum_transactions=1
        )
        # Create genisis
        self.trilio.chain.append(Block(datetime.now().timestamp(), ["genisis block"]))
        self.Address = Address()
        self.TradeStorage = TradeStorage()
        self.CollectionStorage = CollectionStorage()
        self.AssetStorage = AssetStorage()
    
    def create_block(self,addresses=None, collections=None, assets=None, trades=None):
        nonce = self.trilio.difficulty ** 12

        for i in range(nonce):
            pass

        if len(self.trilio.pending_transactions) >= self.trilio.minimum_transactions:
            # block.hash, block.timestamp, block.transactions, block.previous_hash
            transactions = self.trilio.pending_transactions
            self.trilio.pending_transactions = []
            
            block = Block(datetime.now().timestamp(), transactions, self.trilio.chain[len(self.trilio.chain)-1].hash, addresses, collections, assets, trades)
            self.trilio.chain.append(block)
            return block
        else:
            return False
        

        
    
    def create_transaction(self, timestamp, data):
        self.trilio.pending_transactions.append(
            Transaction(timestamp,data=data)
        )
        self.create_block(
            addresses=self.Address,
            collections=self.CollectionStorage,
            trades=self.TradeStorage,
            assets=self.AssetStorage
        )
    

    def get_transaction(self, data):
        for block in self.trilio.chain:
            for transaction in block.transactions:
                if transaction.hash == data:
                    return transaction
    
    class Address(Address):
        pass

    class TradeStorage(TradeStorage):
        pass

    class CollectionStorage(CollectionStorage):
        pass

    class AssetStorage(AssetStorage):
        pass