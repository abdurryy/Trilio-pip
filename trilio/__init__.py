from datetime import datetime
import hashlib, random
# New storage models

class Trilio:
    def __init__(self):
        self.trilio = Blockchain(
            name="Trilio", 
            difficulty=4,
            minimum_transactions=1
        )
        # Create genisis
        self.trilio.chain.append(Block(datetime.now().timestamp(), ["genisis block"]))
        self.wallet = self.Wallet()
        self.TradeStorage = self.TradeStorage()
        self.CollectionStorage = self.CollectionStorage()
        self.AssetStorage = self.AssetStorage()
    
    def validate_chain(self):
        for i in range(len(self.trilio.chain)):
            if self.trilio.chain[i].transactions[0] != "genisis block":
                if self.trilio.chain[i].get_hash() != self.trilio.chain[i].hash:
                    return False
                
                if self.trilio.chain[i].previous_hash != self.trilio.chain[i-1].hash:
                    return False
        return True
    
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
    
    class Wallet():
        def __init__(self):
            self.addresses = []
        
        def create_wallet(self):
            pve = random.randint(100000000000,99999999999999)
            pbc = random.randint(100000000000,99999999999999)
            private_key = "pve"+str(hashlib.sha256(str(pve).encode('utf-8')).hexdigest())
            public_key =  "pbc"+str(hashlib.sha256(str(pbc).encode('utf-8')).hexdigest())
            cred_keys = { 
                "address": {
                    "pve":private_key, 
                    "pbc":public_key 
                }, 
                "info": {
                    "balance":float(0),
                    "assets" : [],
                    "collections" : []
                }
            }
            if self.validate_address(private_key, public_key) == False:
                self.addresses.append(cred_keys)
                return cred_keys
            else:
                return self.create_address()        

        def get_balance(self, private_key=None, public_key=None):
            r = self.require(private_key, public_key)
            if r == False:
                return "Private and Public keys are required"
                
            for address in self.addresses:
                if address["address"]["pbc"] == public_key and address["address"]["pve"] == private_key:
                    return float(address["info"]["balance"])
            
        def get_assets(self, private_key=None, public_key=None):
            r = self.require(private_key, public_key)
            if r == False:
                return "Private and Public keys are required"
                
            for address in self.addresses:
                if address["address"]["pbc"] == public_key and address["address"]["pve"] == private_key:
                    return address["info"]["assets"]
        
        def get_collections(self, private_key=None, public_key=None):
            r = self.require(private_key, public_key)
            if r == False:
                return "Private and Public keys are required"
                
            for address in self.addresses:
                if address["address"]["pbc"] == public_key and address["address"]["pve"] == private_key:
                    return address["info"]["collections"]
        
        def get_public_key(self, private_key=None):
            if private_key == None:
                return "Failed"
            
            for address in self.addresses:
                if address["address"]["pve"] == private_key:
                    return address["address"]["pbc"]
            return "Failed"
        
        def credit_wallet(self, public_key = None, amount = None):
            if public_key == None or amount == None:
                return "Failed"
            
            for address in self.addresses:
                if address["address"]["pbc"] == public_key:
                    address["info"]["balance"] += amount
                    return address["info"]["balance"]
            return "Failed"
        
        def validate_address(self, private_key=None, public_key=None):
            r = self.require(private_key, public_key)
            if r == False:
                return "Private and Public keys are required"
            
            for address in self.addresses:
                if address["address"]["pbc"] == public_key and address["address"]["pve"] == private_key:
                    return True
            return False        

        def require(self, private_key=None, public_key=None):
            if private_key == None or public_key == None:
                return False
            return True

    class TradeStorage():
        def __init__(self):
            self.trades = []

    class CollectionStorage():
        def __init__(self):
            self.collections = []

    class AssetStorage():
        def __init__(self):
            self.assets = []

class Asset:
    def __init__(self, timestamp, public_key, collection_id, name, description, mint_number, _ad=None, _as=None):
        self.id = len(_as.assets) + 1
        self.name = name
        self.description = description
        self.collection_id = collection_id
        self.created_at = timestamp
        self.owner = public_key
        self.mint = mint_number+1
        self.trading = False
        self.selling = False
        _as.assets.append(self)
        for address in _ad.addresses:
            if address["address"]["pbc"] == public_key:
                address["info"]["assets"].append(self.id)

class Transaction:
    def __init__(self, timestamp, data):
        self.timestamp = timestamp
        self.input = data
        self.hash = self.get_hash()
    
    def get_hash(self):
        return hashlib.sha256(str(self.timestamp).encode('utf-8')+str(self.input).encode('utf-8')).hexdigest()

class Trade:
    def __init__(self, timestamp, _to, _from, fassets, tassets, tradestorage):
        self.id = len(tradestorage.trades) + 1
        self._to = _to
        self._from = _from
        self.fassets = fassets
        self.tassets = tassets
        self.state = 0 # 0 = pending # 1 = accepted # 2 = decline
        self.created_at = timestamp
        tradestorage.trades.append(self)
    
    def get_id(self):
        return self.id

class TradeHandler():
    def accept_trade(self, id, private_key, address, assets, _ad, tradestorage):
        for trade in tradestorage.trades:
            if trade.id == id:
                if trade.state == 2 or trade.state == 1:
                    return # This trade has already been interacted with
                if trade._to == address.get_public_key(private_key):
                    tassets = 0
                    for asset_id in trade.tassets:
                        for asset in assets.assets:
                            if asset.id == asset_id and asset.owner == trade._to:
                                tassets += 1
                    if tassets == len(trade.tassets):
                        for asset_id in trade.tassets:
                            assets.assets[asset_id-1].owner = address.get_public_key(trade._from)
                            for address in address.addresses:
                                if address["address"]["pve"] == trade._from:
                                    address["info"]["assets"].append(asset_id)
                            for address in _ad.addresses:
                                if address["address"]["pbc"] == trade._to:
                                    address["info"]["assets"].pop(address["info"]["assets"].index(asset_id))

                                    

                        for asset_id in trade.fassets:
                            assets.assets[asset_id-1].owner = trade._to
                            for address in _ad.addresses:
                                if address["address"]["pbc"] == trade._to:
                                    address["info"]["assets"].append(asset_id)
                                
                        trade.state = 1
                else:
                    print("worng address")
        
    def decline_trade(self, id, private_key ,address, assets, _ad, tradestorage):
        for trade in tradestorage.trades:
            if trade.id == id:
                if trade.state == 2 or trade.state == 1:
                    return # This trade has already been interacted with
                if trade._from == private_key or trade._to == address.get_public_key(private_key):
                    for asset in assets.assets:
                        try:
                            if asset.owner["refund"] == address.get_public_key(trade._from) and asset.owner["trade_id"] == id:
                                asset.owner = address.get_public_key(trade._from)
                                for _address in _ad.addresses:
                                    if _address["address"]["pve"] == trade._from:
                                        _address["info"]["assets"].append(asset.id)
                        except:
                            pass
                trade.state = 2

class CollectionHandler():
    def create_collection(self, timestamp, public_key, url, icon, name, description, tags, _ad=None, _co=None):
        self.id = len(_co.collections) + 1
        self.name = name
        self.description = description
        self.tags = tags
        self.icon = icon
        self.url = url
        self.owner = public_key
        self.created_at = timestamp
        self.blacklisted = False
        _co.collections.append(self)
        for address in _ad.addresses:
            if address["address"]["pbc"] == public_key:
                address["info"]["collections"].append(self.id)
    
    def validate_collection_name(self, name, _co):
        for collection in _co.collections:
            if collection.name == name:
                return False
        
        if len(name) > 4 and len(name) < 15: return True
        return False
    
    def validate_collection_owner(self, public_key, collection_id, _co):
        for collection in _co.collections:
            if collection.id == collection_id:
                if collection.owner == public_key:
                    return True
        return False

class Block:
    def __init__(self, timestamp, transactions, previous_hash="",addresses = "", collections="", assets="", trades="", asset=""):
        self.addresses = addresses
        self.asset = asset
        self.collections = collections
        self.assets = assets
        self.trades = trades
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.get_hash()
        self.status = 0 # 0 = pending, 1 = completed 
        self.complete()
    
    def complete(self):

        for transaction in self.transactions:
            try:
                pbc = self.addresses.get_public_key(transaction.input["data"]["from"])
                pve = transaction.input["data"]["from"]
            except:
                pass

            if transaction == "genisis block":
                return
            
            if transaction.input["type"] == "token-transfer":
                if float(transaction.input["data"]["amount"]) >= 0:
                    if self.addresses.get_balance(pve, pbc) >= float(transaction.input["data"]["amount"]):
                        self.addresses.credit_address(transaction.input["data"]["to"], float(transaction.input["data"]["amount"]))
                        self.addresses.credit_address(pbc, -float(transaction.input["data"]["amount"]))
            elif transaction.input["type"] == "contract-action":
                # if collection name is valid continue
                # create collection
                if transaction.input["action"] == "collection-creation":
                    is_valid_name = CollectionHandler().validate_collection_name(transaction.input["data"]["name"], self.collections)
                    if is_valid_name:
                        pbc = self.addresses.get_public_key(transaction.input["data"]["signer"])
                        CollectionHandler().create_collection(datetime.now().timestamp(), pbc, transaction.input["data"]["url"], transaction.input["data"]["icon"], transaction.input["data"]["name"], transaction.input["data"]["description"], transaction.input["data"]["tags"], self.addresses, self.collections)
                # fix minting
                elif transaction.input["action"] == "asset-creation":
                    pbc = self.addresses.get_public_key(transaction.input["data"]["signer"])
                    is_collection_owner = CollectionHandler().validate_collection_owner(pbc, transaction.input["data"]["collection_id"], self.collections)
                    if is_collection_owner:
                        for i in range(transaction.input["data"]["quantity"]):
                            Asset(datetime.now().timestamp(), pbc, transaction.input["data"]["collection_id"], transaction.input["data"]["name"], transaction.input["data"]["description"], i, self.addresses, self.assets)
                elif transaction.input["action"] == "accept-trade":
                    TradeHandler().accept_trade(transaction.input["data"]["id"],transaction.input["data"]["signer"], self.addresses, self.assets, self.addresses, self.trades)
                elif transaction.input["action"] == "decline-trade":
                    self.TradeHandler().decline_trade(transaction.input["data"]["id"],transaction.input["data"]["signer"], self.addresses, self.assets, self.addresses, self.trades)
            elif transaction.input["type"] == "asset-transfer":
                # check if the user owns the assets
                # check if the other user owns the assets
                fassets = 0
                tassets = 0
                for asset_id in transaction.input["data"]["fassets"]: # this is what they sending
                    for asset in self.assets.assets:
                        if asset.id == asset_id and asset.owner == self.addresses.get_public_key(transaction.input["data"]["_from"]):
                            fassets += 1

                for asset_id in transaction.input["data"]["tassets"]: # this is what they other are sending
                    for asset in self.assets.assets:
                        if asset.id == asset_id and asset.owner == transaction.input["data"]["_to"]:
                            tassets += 1

                if fassets == len(transaction.input["data"]["fassets"]):
                    if tassets == len(transaction.input["data"]["tassets"]):
                        for asset_id in transaction.input["data"]["fassets"]:
                            #need a fix
                            for asset in self.assets.assets:
                                if asset.id == asset_id:
                                    pbc = self.addresses.get_public_key(transaction.input["data"]["_from"])
                                    print(asset.id)
                                    for address in self.addresses.addresses:
                                        if address["address"]["pve"] == transaction.input["data"]["_from"]:
                                            address["info"]["assets"].pop(address["info"]["assets"].index(asset.id))
                                    print(transaction.input["data"]["fassets"])
                                    idd = self.Trade(datetime.now().timestamp(), transaction.input["data"]["_to"], transaction.input["data"]["_from"], transaction.input["data"]["fassets"], transaction.input["data"]["tassets"], self.trades)
                                    asset.owner = {"info":"This asset is being traded.","trade_id":idd.get_id(),"refund":pbc}
                
        self.status = 1
    
    def get_hash(self):
        return hashlib.sha256(str(self.timestamp).encode('utf-8')+str(self.transactions).encode('utf-8')+str(self.previous_hash).encode('utf-8')).hexdigest()

class Blockchain:
    def __init__(self, name="", difficulty=2, minimum_transactions=2):
        self.name = name
        self.difficulty = difficulty
        self.minimum_transactions = minimum_transactions
        self.chain = [
        ]
        self.pending_transactions = [

        ]