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

    print(f"=== Step 3: Create multisig credentials for multi-owner ===")
    deployer_seed = nt.Bip39Seed.generate()
    deployer_keypair = deployer_seed.derive()
    print(f"Deployer seed: \"{deployer_seed}\"")
    print(f"Deployer public key: {deployer_keypair.public_key}")

    seed1 = nt.Bip39Seed.generate()
    keypair1 = seed1.derive()
    print(f"Owner1 seed: \"{seed1}\"")
    print(f"Owner1 public key: {keypair1.public_key}")

    seed2 = nt.Bip39Seed.generate()
    keypair2 = seed2.derive()
    print(f"Owner2 seed: \"{seed2}\"")
    print(f"Owner2 public key: {keypair2.public_key}")

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

    print("=== Step 5: Deploy multi-owner SetcodeMultisig (req_confirms=2) ===")
    owners = [keypair1.public_key.to_int(), keypair2.public_key.to_int()]
    req_confirms = 2    
    print(f"Deploying {msig_addr}...")
    multisig_wallet, tx = await SetcodeMultisig.deploy(transport, deployer_keypair, owners, req_confirms)    
    print(f"Deployment transaction: {tx.hash.hex()}")
    account_state = await transport.get_account_state(multisig_wallet.address)
    print(f"After-deployment state: {account_state}")    
    print("")
    
    print("=== Step 6: Get parameters on multi-owner ===")
    params = await multisig_wallet.get_parameters()
    print(f"Parameters: {params}")
    print("")

    print("=== Step 7: Get custodians on multi-owner ===")
    custodians = await multisig_wallet.get_custodians()
    print(f"Custodians: {custodians}")
    print("")

    print("=== Step 8: Get public key on multi-owner ===")
    pubkey = await multisig_wallet.get_public_key()
    print(f"Public key (deployer): {pubkey}")
    print("")

    print("=== Step 9: Submit transaction on multi-owner ===")
    dest = nt.Address("0:4594925085dbca1e5660f7d1de89616967b35afd215b35457a93b839e022992d")
    value = nt.Tokens("0.01")     
    tx, transId = await multisig_wallet.submit_transaction(dest, value, True, False, nt.Cell(), signer=keypair1)
    print(f"Submit transaction: {tx.hash.hex()}")
    print(f"Submit transaction_id: {transId}")        
    print("")

    print("=== Step 10: Get transactions (pending) ===")
    transactions = await multisig_wallet.get_transactions()
    print(f"Transactions: {transactions}")
    print("")

    print("=== Step 11: Get transaction by ID (pending) ===")
    transaction = await multisig_wallet.get_transaction(transId)
    print(f"Transaction: {transaction if transaction else 'Not found'}")
    print("")

    print("=== Step 11.5: Test is_confirmed after submit transaction (partial confirmation) ===")
    transactions = await multisig_wallet.get_transactions()
    if transactions:
        transaction = transactions[0]
        mask = transaction.confirmations_mask
        creator_index = transaction.index
        other_index = 1 if creator_index == 0 else 0
        confirmed_creator = await multisig_wallet.is_confirmed(mask, creator_index)
        confirmed_other = await multisig_wallet.is_confirmed(mask, other_index)
        print(f"Confirmed by creator (index {creator_index}): {confirmed_creator}")
        print(f"Confirmed by other (index {other_index}): {confirmed_other}")
    else:
        print("No transactions found")
    print("")

    print("=== Step 12: Confirm transaction on multi-owner ===")
    tx2 = await multisig_wallet.confirm_transaction(transId, signer=keypair2)
    print(f"Confirm transaction: {tx2.hash.hex()}")
    account_state = await transport.get_account_state(multisig_wallet.address)
    print(f"After-transaction state: {account_state}")    
    print("")

    print("=== Step 13: Get transactions (after confirm, should be empty) ===")
    transactions_after = await multisig_wallet.get_transactions()
    print(f"Transactions after: {transactions_after}")
    print("")

    print("=== Step 14: Get transaction by ID (after confirm, should be None) ===")
    transaction_after = await multisig_wallet.get_transaction(transId)
    print(f"Transaction after: {transaction_after if transaction_after else 'Not found'}")
    print("")

    print("=== Step 15: Submit update ===")
    owners = [keypair1.public_key.to_int()]    
    tx, update_id = await multisig_wallet.submit_update(keypair1, owners=owners)
    print(f"Transaction: {tx.hash.hex()}")
    print(f"Update ID: {update_id}")
    print("")

    print("=== Step 16: Get update requiests ===")
    update_requests = await multisig_wallet.get_update_requests()
    print(f"Update requests: {update_requests}")
    print("")

    print("=== Step 16.5: Test is_confirmed after submit update (partial confirmation) ===")    
    if update_requests:
        update_request = update_requests[0]
        mask = update_request.confirmations_mask
        creator_index = update_request.index
        other_index = 1 if creator_index == 0 else 0
        confirmed_creator = await multisig_wallet.is_confirmed(mask, creator_index)
        confirmed_other = await multisig_wallet.is_confirmed(mask, other_index)
        print(f"Confirmed by creator (index {creator_index}): {confirmed_creator}")
        print(f"Confirmed by other (index {other_index}): {confirmed_other}")
    else:
        print("No update requests found")
    print("")

    print("=== Step 17: Confirm update ===")
    tx = await multisig_wallet.confirm_update(keypair2, update_id)
    print(f"Transaction update: {tx.hash.hex()}")
    print("")

    print("=== Step 18: Get update requiests after it has been confirmed ===")
    update_requests = await multisig_wallet.get_update_requests()
    print(f"Update requests: {update_requests}")
    print("")

    print("=== Step 18.5: Test is_confirmed after confirm update (full confirmation) ===")
    update_requests = await multisig_wallet.get_update_requests()
    if update_requests:
        update_request = update_requests[0]
        mask = update_request.confirmations_mask
        creator_index = update_request.index
        other_index = 1 if creator_index == 0 else 0
        confirmed_creator = await multisig_wallet.is_confirmed(mask, creator_index)
        confirmed_other = await multisig_wallet.is_confirmed(mask, other_index)
        print(f"Confirmed by creator (index {creator_index}): {confirmed_creator}")
        print(f"Confirmed by other (index {other_index}): {confirmed_other}")
    else:
        print("No update requests found")
    print("")

    print("=== Step 19: Execute update ===")
    tx = await multisig_wallet.execute_update(keypair1, update_id)
    print(f"Transaction execute update: {tx.hash.hex()}")
    print("")

    print("=== Step 20: Get parameters on multi-owner ===")
    params = await multisig_wallet.get_parameters()
    print(f"Parameters: {params}")
    print("")

    print("=== Step 21: Get custodians on multi-owner ===")
    custodians = await multisig_wallet.get_custodians()
    print(f"Custodians: {custodians}")
    print("")

    print("=== Step 22: Send transaction on newly updated single-owner ===")
    value = nt.Tokens("0.03")
    tx = await multisig_wallet.send_transaction(dest, value, True, 3, nt.Cell(), keypair1)
    print(f"Send transaction: {tx.hash.hex()}")
    print("")

    print("=== Step 23: Test get methods with pre-fetched account state on multi-owner ===")
    account_state = await transport.get_account_state(multisig_wallet.address)
    print(f"Pre-fetched account state: {account_state}")
    params_state = await multisig_wallet.get_parameters(account_state)
    print(f"Parameters with state: {params_state}")
    custodians_state = await multisig_wallet.get_custodians(account_state)
    print(f"Custodians with state: {custodians_state}")
    transactions_state = await multisig_wallet.get_transactions(account_state)
    print(f"Transactions with state: {transactions_state}")
    transaction_state = await multisig_wallet.get_transaction(transId, account_state)
    print(f"Transaction with state: {transaction_state if transaction_state else 'Not found'}")


if __name__ == "__main__":
    asyncio.run(main())