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

async def main():
    # 1) Transport
    transport = nt.ProtoTransport(ENDPOINT)

    # 2) Create keypair
    seed = nt.Bip39Seed.generate()
    keypair = seed.derive()
    pubkey = keypair.public_key

    # 3) Compute deterministic SetcodeMultisig address (workchain 0 by default)
    msig_addr = SetcodeMultisig.compute_address(pubkey)
    print("SetcodeMultisig address:", msig_addr)

    # 4) Check account state
    state = await transport.get_account_state(msig_addr)
    print("Account state:", state)

asyncio.run(main())
```
For more examples with deployment see `test_send_trx.py` and `test_setcode.py`
