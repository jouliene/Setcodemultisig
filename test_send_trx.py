import nekoton as nt
import asyncio
from setcodemultisig import SetcodeMultisig
import time

ENDPOINT = "https://rpc-testnet.tychoprotocol.com/proto"
GIVER_SEED_PHRASE = "obvious puzzle rifle dirt wash address notable dune include exhibit idea usual" 

async def main():
    print(f"=== Step 1: Setting up transport ===")
    transport = nt.ProtoTransport(ENDPOINT)    
    print(f"Endpoint: {ENDPOINT}")
    print("")
      
    print(f"=== Step 2: Setup giver wallet ===")
    giver_seed = nt.Bip39Seed(GIVER_SEED_PHRASE)
    giver_keypair = giver_seed.derive()
    giver_wallet = nt.contracts.ever_wallet.EverWallet(transport, giver_keypair)
    giver_balance = await giver_wallet.get_balance()
    print(f"Giver address: {giver_wallet.address}")
    print(f"Giver balance: {giver_balance}")    
    print("")

    print(f"=== Step 3: Create multisig credentials for single-owner ===")
    deployer_seed = nt.Bip39Seed.generate()
    deployer_keypair = deployer_seed.derive()
    print(f"Deployer seed: \"{deployer_seed}\"")
    print(f"Deployer public key: {deployer_keypair.public_key}")    

    msig_addr = SetcodeMultisig.compute_address(deployer_keypair.public_key)
    print(f"Multi-owner MSIG ADDR: {msig_addr}")
    print("")
    
    print("=== Step 4: Topping up multi-owner msig address with 0.3 TYCHO ===")
    print(f"Sending 0.3 TYCHO to {msig_addr} ...")
    start_time = time.time()
    await giver_wallet.give(msig_addr, nt.Tokens("0.3"))
    elapsed_time = time.time() - start_time
    print(f"[DEBUG] It took {elapsed_time:.2f} secs to send transaction.")
    account_state = await transport.get_account_state(msig_addr)    
    print(f"Pre-deployment state: {account_state}")    
    print(f"Account status: {account_state.status}")    
    print("")

    print("=== Step 5: Deploy single-owner SetcodeMultisig (req_confirms=1) ===")
    owners = [deployer_keypair.public_key.to_int()]
    req_confirms = 1    
    print(f"Deploying {msig_addr}...")
    multisig_wallet, tx = await SetcodeMultisig.deploy(transport, deployer_keypair, owners, req_confirms)    
    print(f"Deployment transaction: {tx.hash.hex()}")
    account_state = await transport.get_account_state(multisig_wallet.address)
    print(f"After-deployment state: {account_state}")    
    print("")
    
    print("=== Step 6: Get parameters on single-owner ===")
    params = await multisig_wallet.get_parameters()
    print(f"Parameters: {params}")
    print("")

    print("=== Step 7: Get custodians on single-owner ===")
    custodians = await multisig_wallet.get_custodians()
    print(f"Custodians: {custodians}")
    print("")

    print("=== Step 8: Get public key on single-owner ===")
    pubkey = await multisig_wallet.get_public_key()
    print(f"Public key (deployer): {pubkey}")
    print("")

    print("=== Step 9: Send transaction on single-owner ===")    
    dest = nt.Address("0:4594925085dbca1e5660f7d1de89616967b35afd215b35457a93b839e022992d")
    value = nt.Tokens("0.01")     
    st = time.time()
    tx = await multisig_wallet.send_transaction(dest, value, True, 3, nt.Cell(), signer=deployer_keypair)
    print(f"[DEBUG] It took {(time.time() - st):.2f} secs")
    print(f"Send transaction: {tx.hash.hex()}")    
    print("")


if __name__ == "__main__":
    asyncio.run(main())
