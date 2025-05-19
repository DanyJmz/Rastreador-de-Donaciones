import hashlib
import json
import time
from typing import List, Dict, Any

class Block:
    def __init__(self, index: int, timestamp: float, data: Dict[str, Any], previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.create_genesis()

    def create_genesis(self):
        genesis = Block(0, time.time(), {'mensaje': 'Bloque Génesis'}, '0')
        self.chain.append(genesis)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, data: Dict[str, Any]) -> Block:
        new_block = Block(
            index=self.last_block.index + 1,
            timestamp=time.time(),
            data=data,
            previous_hash=self.last_block.hash
        )
        self.chain.append(new_block)
        return new_block

    def to_dict(self) -> List[Dict[str, Any]]:
        return [vars(block) for block in self.chain]