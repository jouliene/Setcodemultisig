# Setcodemultisig  (WIP)

Lightweight Python SDK for the SetcodeMultisig smart contract on TVM blockchains — including TON, Everscale, Venom, Hamster, Humo, and other Tycho‑based networks (https://tychoprotocol.com).

Contract code hash: d66d198766abdbe1253f3415826c946c371f5112552408625aeb0b31e0ef2df3

Uses Python bindings to the Nekoton SDK by Broxus (https://github.com/broxus/nekoton-python)

## Installation

```bash
# 1) Clone or download this repository
git clone https://github.com/jouliene/Setcodemultisig.git
cd Setcodemultisig

# 2) (Recommended) Use a virtual environment
python3 -m venv .venv
source .venv/bin/activate 

# 3) Install dependencies
pip install -U pip
pip install nekoton
```

## Quick Start

```python
import asyncio
import nekoton as nt
from setcodemultisig import SetcodeMultisig

ENDPOINT = "https://rpc-testnet.tychoprotocol.com/proto"
SEED_PHRASE = "replace with your test 12/24 word seed"

async def main():
    # 1) Transport
    transport = nt.ProtoTransport(ENDPOINT)

    # 2) Derive keypair (test seed!)
    seed = nt.Bip39Seed(SEED_PHRASE)
    keypair = nt.KeyPair.from_seed(seed)
    pubkey = keypair.public_key

    # 3) Compute deterministic SetcodeMultisig address (workchain 0 by default)
    msig_addr = SetcodeMultisig.compute_address(pubkey)
    print("SetcodeMultisig address:", msig_addr)

    # 4) Check account state
    state = await transport.get_account_state(msig_addr)
    print("Account state:", state)

    # 5) Send transaction
    dest = nt.Address("0:4594925085dbca1e5660f7d1de89616967b35afd215b35457a93b839e022992d")
    value = nt.Tokens("0.01")
    bounce = True
    flags = 3
    payload = nt.Cell()
    tx = await multisig_wallet.send_transaction(dest, value, bounce, flags, payload, signer=keypair)
    print(f"Send transaction ID: {tx.hash.hex()}")

asyncio.run(main())
```
For more examples see test_send_trx.py and test_setcode.py.
