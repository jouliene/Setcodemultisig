# setcodemultisig.py

"""
Lightweight SDK for SetcodeMultisig contract on TVM blockchains: 
TON, Everscale, Venom, Hamster, Humo and other Tycho-based networks (tychoprotocol.com)

Code hash: d66d198766abdbe1253f3415826c946c371f5112552408625aeb0b31e0ef2df3

It uses Python bindings to Nekoton SDK by Broxus (pip install nekoton)
"""

import nekoton as nt
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass

MULTISIG_ABI_STR = """{
	"ABI version": 2,
	"version": "2.3",
	"header": ["pubkey", "time", "expire"],
	"functions": [
		{
			"name": "constructor",
			"inputs": [
				{"name":"owners","type":"uint256[]"},
				{"name":"reqConfirms","type":"uint8"},
				{"name":"lifetime","type":"uint32"}
			],
			"outputs": [
			]
		},
		{
			"name": "sendTransaction",
			"inputs": [
				{"name":"dest","type":"address"},
				{"name":"value","type":"uint128"},
				{"name":"bounce","type":"bool"},
				{"name":"flags","type":"uint8"},
				{"name":"payload","type":"cell"}
			],
			"outputs": [
			]
		},
		{
			"name": "submitTransaction",
			"inputs": [
				{"name":"dest","type":"address"},
				{"name":"value","type":"uint128"},
				{"name":"bounce","type":"bool"},
				{"name":"allBalance","type":"bool"},
				{"name":"payload","type":"cell"},
				{"name":"stateInit","type":"optional(cell)"}
			],
			"outputs": [
				{"name":"transId","type":"uint64"}
			]
		},
		{
			"name": "confirmTransaction",
			"inputs": [
				{"name":"transactionId","type":"uint64"}
			],
			"outputs": [
			]
		},
		{
			"name": "isConfirmed",
			"inputs": [
				{"name":"mask","type":"uint32"},
				{"name":"index","type":"uint8"}
			],
			"outputs": [
				{"name":"confirmed","type":"bool"}
			]
		},
		{
			"name": "getParameters",
			"inputs": [
			],
			"outputs": [
				{"name":"maxQueuedTransactions","type":"uint8"},
				{"name":"maxCustodianCount","type":"uint8"},
				{"name":"expirationTime","type":"uint64"},
				{"name":"minValue","type":"uint128"},
				{"name":"requiredTxnConfirms","type":"uint8"},
				{"name":"requiredUpdConfirms","type":"uint8"}
			]
		},
		{
			"name": "getTransaction",
			"inputs": [
				{"name":"transactionId","type":"uint64"}
			],
			"outputs": [
				{"components":[{"name":"id","type":"uint64"},{"name":"confirmationsMask","type":"uint32"},{"name":"signsRequired","type":"uint8"},{"name":"signsReceived","type":"uint8"},{"name":"creator","type":"uint256"},{"name":"index","type":"uint8"},{"name":"dest","type":"address"},{"name":"value","type":"uint128"},{"name":"sendFlags","type":"uint16"},{"name":"payload","type":"cell"},{"name":"bounce","type":"bool"},{"name":"stateInit","type":"optional(cell)"}],"name":"trans","type":"tuple"}
			]
		},
		{
			"name": "getTransactions",
			"inputs": [
			],
			"outputs": [
				{"components":[{"name":"id","type":"uint64"},{"name":"confirmationsMask","type":"uint32"},{"name":"signsRequired","type":"uint8"},{"name":"signsReceived","type":"uint8"},{"name":"creator","type":"uint256"},{"name":"index","type":"uint8"},{"name":"dest","type":"address"},{"name":"value","type":"uint128"},{"name":"sendFlags","type":"uint16"},{"name":"payload","type":"cell"},{"name":"bounce","type":"bool"},{"name":"stateInit","type":"optional(cell)"}],"name":"transactions","type":"tuple[]"}
			]
		},
		{
			"name": "getCustodians",
			"inputs": [
			],
			"outputs": [
				{"components":[{"name":"index","type":"uint8"},{"name":"pubkey","type":"uint256"}],"name":"custodians","type":"tuple[]"}
			]
		},
		{
			"name": "submitUpdate",
			"inputs": [
				{"name":"codeHash","type":"optional(uint256)"},
				{"name":"owners","type":"optional(uint256[])"},
				{"name":"reqConfirms","type":"optional(uint8)"},
				{"name":"lifetime","type":"optional(uint32)"}
			],
			"outputs": [
				{"name":"updateId","type":"uint64"}
			]
		},
		{
			"name": "confirmUpdate",
			"inputs": [
				{"name":"updateId","type":"uint64"}
			],
			"outputs": [
			]
		},
		{
			"name": "executeUpdate",
			"inputs": [
				{"name":"updateId","type":"uint64"},
				{"name":"code","type":"optional(cell)"}
			],
			"outputs": [
			]
		},
		{
			"name": "getUpdateRequests",
			"inputs": [
			],
			"outputs": [
				{"components":[{"name":"id","type":"uint64"},{"name":"index","type":"uint8"},{"name":"signs","type":"uint8"},{"name":"confirmationsMask","type":"uint32"},{"name":"creator","type":"uint256"},{"name":"codeHash","type":"optional(uint256)"},{"name":"custodians","type":"optional(uint256[])"},{"name":"reqConfirms","type":"optional(uint8)"},{"name":"lifetime","type":"optional(uint32)"}],"name":"updates","type":"tuple[]"}
			]
		}
	],
	"data": [
	],
	"events": [
	],
	"fields": [
		{"name":"_pubkey","type":"uint256"},
		{"name":"_timestamp","type":"uint64"},
		{"name":"_constructorFlag","type":"bool"},
		{"name":"m_ownerKey","type":"uint256"},
		{"name":"m_requestsMask","type":"uint256"},
		{"components":[{"name":"id","type":"uint64"},{"name":"confirmationsMask","type":"uint32"},{"name":"signsRequired","type":"uint8"},{"name":"signsReceived","type":"uint8"},{"name":"creator","type":"uint256"},{"name":"index","type":"uint8"},{"name":"dest","type":"address"},{"name":"value","type":"uint128"},{"name":"sendFlags","type":"uint16"},{"name":"payload","type":"cell"},{"name":"bounce","type":"bool"},{"name":"stateInit","type":"optional(cell)"}],"name":"m_transactions","type":"map(uint64,tuple)"},
		{"name":"m_custodians","type":"map(uint256,uint8)"},
		{"name":"m_custodianCount","type":"uint8"},
		{"components":[{"name":"id","type":"uint64"},{"name":"index","type":"uint8"},{"name":"signs","type":"uint8"},{"name":"confirmationsMask","type":"uint32"},{"name":"creator","type":"uint256"},{"name":"codeHash","type":"optional(uint256)"},{"name":"custodians","type":"optional(uint256[])"},{"name":"reqConfirms","type":"optional(uint8)"},{"name":"lifetime","type":"optional(uint32)"}],"name":"m_updateRequests","type":"map(uint64,tuple)"},
		{"name":"m_updateRequestsMask","type":"uint32"},
		{"name":"m_requiredVotes","type":"uint8"},
		{"name":"m_defaultRequiredConfirmations","type":"uint8"},
		{"name":"m_lifetime","type":"uint32"}
	]
}"""

MULTISIG_ABI = nt.ContractAbi(MULTISIG_ABI_STR)
MULTISIG_CODE_BASE64 = "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"
MULTISIG_CODE = nt.Cell.decode(MULTISIG_CODE_BASE64)
MIN_BALANCE_REQUIRED = nt.Tokens("0.1")


class MultisigError(Exception):
    """Base error for SetcodeMultisig operations."""
    pass


@dataclass
class MultisigTransaction:
    """Represents a transaction in the multisig wallet."""
    id: int
    confirmations_mask: int
    signs_required: int
    signs_received: int
    creator: int
    index: int
    dest: nt.Address
    value: int
    send_flags: int
    payload: nt.Cell
    bounce: bool
    state_init: Optional[nt.Cell]
    

@dataclass
class MultisigParameters:
    """Represents the parameters of the multisig wallet."""
    max_queued_transactions: int
    max_custodian_count: int
    expiration_time: int
    min_value: int
    required_txn_confirms: int
    required_upd_confirms: int
    

@dataclass
class MultisigCustodian:
    """Represents a custodian (owner) of the multisig wallet."""
    index: int
    pubkey: int


@dataclass
class MultisigUpdateRequest:
    """Represents an update request for the multisig wallet configuration."""
    id: int
    index: int
    signs: int
    confirmations_mask: int
    creator: int
    code_hash: Optional[int]
    custodians: Optional[List[int]]
    req_confirms: Optional[int]
    lifetime: Optional[int]
    

class SetcodeMultisig:
    """SDK for interacting with a SetcodeMultisig contract.

    This class provides methods for deploying the contract, sending transactions,
    and updating a multisig wallet on TVM-blockchains.
    """
    abi = MULTISIG_ABI
    code = MULTISIG_CODE


    def __init__(
        self,
        transport: nt.Transport,
        address: nt.Address,                
        timeout: int = 60,
        signature_id: Optional[int] = None
    ):
        """Initialize the SetcodeMultisig instance.

        Args:
            transport: The transport to use for blockchain interactions.
            address: The address of the multisig contract.
            timeout: Message expiration timeout in seconds (default: 60).
            signature_id: Optional signature ID for signing messages.
        """
        self.transport = transport
        self.address = address        
        self.timeout = timeout
        self.signature_id = signature_id        


    async def setup_signature_id(self):
        """Set up the signature ID if not provided during initialization."""
        try:
            self.signature_id = await self.transport.get_signature_id()
        except Exception as e:
            raise MultisigError(f"[ERROR] Failed to setup signature ID: {str(e)}") from e

    
    @classmethod
    def compute_state_init(cls, deployer_public_key: nt.PublicKey) -> nt.StateInit:
        """Compute the state init for the multisig contract.

        Args:
            deployer_public_key: Public key of the deployer.

        Returns:
            The computed StateInit object.

        Raises:
            MultisigError: If state init computation fails.
        """
        try:
            init_data = cls.abi.encode_init_data({}, public_key=deployer_public_key)
            return nt.StateInit(cls.code, init_data)
        except Exception as e:
            raise MultisigError(f"[ERROR] Failed to compute state init: {str(e)}") from e


    @classmethod
    def compute_address(cls, deployer_public_key: nt.PublicKey, workchain: int = 0) -> nt.Address:
        """Compute the address of the multisig contract.

        Args:
            deployer_public_key: Public key of the deployer.
            workchain: Workchain ID (default: 0).

        Returns:
            The computed address.

        Raises:
            MultisigError: If address computation fails.
        """
        try:
            state_init = cls.compute_state_init(deployer_public_key)
            return state_init.compute_address(workchain)
        except Exception as e:
            raise MultisigError(f"[ERROR] Failed to compute address: {str(e)}") from e


    @classmethod
    async def deploy(
        cls,
        transport: nt.Transport,
        deployer_keypair: nt.KeyPair,
        owners: List[int],
        req_confirms: int,
        lifetime: int = 3600,
        workchain: int = 0,
        timeout: int = 60,
        signature_id: Optional[int] = None
    ) -> Tuple["SetcodeMultisig", nt.Transaction]:
        """Deploy a new multisig contract.

        Args:
            transport: The transport to use for deployment.
            deployer_keypair: Keypair of the deployer.
            owners: List of owner public keys (max 32).
            req_confirms: Required number of confirmations.
            lifetime: Lifetime of transaction in seconds (default: 3600).
            workchain: Workchain ID (default: 0).
            timeout: Message timeout in seconds (default: 60).
            signature_id: Optional signature ID.

        Returns:
            Tuple of the deployed SetcodeMultisig instance and the deployment transaction.

        Raises:
            MultisigError: If deployment fails.
        """
        try:            
            if not (1 <= req_confirms <= len(owners)):
                raise MultisigError("Owners must be 1-32, req_confirms <= number of owners")
            state_init = cls.compute_state_init(deployer_keypair.public_key)
            address = state_init.compute_address(workchain)
            state = await transport.get_account_state(address)
            if state and state.status != nt.AccountStatus.Uninit:
                raise MultisigError(f"[ERROR] Address {address} is already {state.status}; deployment skipped")
            if state.balance < MIN_BALANCE_REQUIRED:
                raise MultisigError(f"[ERROR] Account balance {state.balance} is less than minimal required {MIN_BALANCE_REQUIRED} for deployment")
            multisig_wallet = cls(transport, address, timeout, signature_id)
            if multisig_wallet.signature_id is None:        
                await multisig_wallet.setup_signature_id()            
            input_data = {
            	"owners": owners,
            	"reqConfirms": req_confirms,
            	"lifetime": lifetime
        	}        
            tx = await multisig_wallet._send_external_message("constructor", input_data, deployer_keypair, state_init)        
            return multisig_wallet, tx
        except Exception as e:
            raise MultisigError(f"Failed to deploy multisig: {str(e)}") from e
            

    async def _send_external_message(
        self,
        function_name: str,
        input_data: Dict,
        signer: nt.KeyPair,
		state_init: Optional[nt.StateInit] = None                
    ) -> nt.Transaction:
        """Internal method to send an external message to the contract.

        Args:
            function_name: Name of the contract function to call.
            input_data: Input data for the function.
            signer: Keypair used to sign the message.
            state_init: Optional state init for deployment.

        Returns:
            The resulting transaction.

        Raises:
            MultisigError: If message sending fails.
        """
        try:    
            func = self.abi.get_function(function_name)        
            unsigned_msg = func.encode_external_message(
				dst=self.address,
				input=input_data,
				public_key=signer.public_key,
				state_init=state_init,
				timeout=self.timeout
			)        
            signed_msg = unsigned_msg.sign(signer, self.signature_id)
            tx = await self.transport.send_external_message(signed_msg)            
            return tx
        except Exception as e:
            raise MultisigError(f"Failed to send external message for {function_name}: {str(e)}") from e
    

    async def submit_transaction(
        self,        
        dest: nt.Address,
        value: nt.Tokens,
        bounce: bool,
        all_balance: bool,
        payload: nt.Cell,        
        signer: nt.KeyPair,
        state_init: Optional[nt.StateInit] = None        
	) -> Tuple[nt.Transaction, int]:
        """Submit a new transaction for confirmation.

        Args:
            dest: Destination address.
            value: Amount to send.
            bounce: Whether to bounce if destination is invalid.
            all_balance: Whether to send all balance.
            payload: Payload cell.
            signer: Signer keypair.
            state_init: Optional state init for the destination.

        Returns:
            Tuple of the transaction and the transaction ID.

        Raises:
            MultisigError: If submission fails.
        """        
        try:
            input_data = {
                "dest": dest,
                "value": value,
                "bounce": bounce,
                "allBalance": all_balance,
                "payload": payload,
                "stateInit": state_init
            }
            tx = await self._send_external_message("submitTransaction", input_data, signer)
            decoded = self.abi.decode_transaction(tx)        
            transaction_id = decoded.output["transId"]
            return tx, transaction_id
        except Exception as e:
            raise MultisigError(f"Failed to submit transaction: {str(e)}") from e
        

    async def confirm_transaction(
        self,
        transaction_id: int,
        signer: nt.KeyPair
    ) -> nt.Transaction:
        """Confirm a pending transaction.

        Args:
            transaction_id: ID of the transaction to confirm.
            signer: Signer keypair.

        Returns:
            The confirmation transaction.

        Raises:
            MultisigError: If confirmation fails.
        """
        try:        
            input_data = {"transactionId": transaction_id}
            tx = await self._send_external_message("confirmTransaction", input_data, signer)
            return tx
        except Exception as e:
            raise MultisigError(f"Failed to confirm transaction: {str(e)}") from e
    

    async def send_transaction(
        self,
        dest: nt.Address,
        value: nt.Tokens,
        bounce: bool,
        flags: int,
        payload: nt.Cell,
        signer: nt.KeyPair
	) -> nt.Transaction:
        """Send a transaction directly (for single-owner wallet).

        Args:
            dest: Destination address.
            value: Amount to send.
            bounce: Whether to bounce if invalid.
            flags: Send flags (use flag=3 for most cases).
            payload: Payload cell.
            signer: Signer keypair.

        Returns:
            The sent transaction.

        Raises:
            MultisigError: If sending fails.
        """        
        try:            
            input_data = {
                "dest": dest,
                "value": value,
                "bounce": bounce,
                "flags": flags,
                "payload": payload
            }
            tx = await self._send_external_message("sendTransaction", input_data, signer)
            return tx
        except Exception as e:
            raise MultisigError(f"Failed to send transaction: {str(e)}") from e
    

    async def get_parameters(self, account_state: Optional[nt.AccountState] = None) -> MultisigParameters:
        """Get the parameters of the multisig wallet.

        Args:
            account_state: Optional pre-fetched account state.

        Returns:
            MultisigParameters object.

        Raises:
            MultisigError: If query fails.
        """
        try:
            if account_state is None:
               account_state = await self.transport.get_account_state(self.address)        
            func = self.abi.get_function("getParameters")
            result = func.call(account_state, {})
            return MultisigParameters(
			    max_queued_transactions=result.output["maxQueuedTransactions"],
			    max_custodian_count=result.output["maxCustodianCount"],
			    expiration_time=result.output["expirationTime"],
			    min_value=result.output["minValue"],
			    required_txn_confirms=result.output["requiredTxnConfirms"],
			    required_upd_confirms=result.output["requiredUpdConfirms"]
		    )
        except Exception as e:
            raise MultisigError(f"Failed to get parameters: {str(e)}") from e          
    

    async def get_custodians(self, account_state: Optional[nt.AccountState] = None) -> List[MultisigCustodian]:
        """Get the list of custodians (wallet owners).

        Args:
            account_state: Optional pre-fetched account state.

        Returns:
            List of MultisigCustodian objects.

        Raises:
            MultisigError: If query fails.
        """
        try:
            if account_state is None:
               account_state = await self.transport.get_account_state(self.address)		
            func = self.abi.get_function("getCustodians")
            result = func.call(account_state, {})
            custodians = [
			    MultisigCustodian(
				    index=custodian["index"],
				    pubkey=custodian["pubkey"]
			    )
			    for custodian in result.output["custodians"]
		    ]
            custodians.sort(key=lambda c: c.index)
            return custodians
        except Exception as e:
            raise MultisigError(f"Failed to get custodians: {str(e)}") from e            


    async def get_transactions(self, account_state: Optional[nt.AccountState] = None) -> List[MultisigTransaction]:
        """Get the list of pending transactions.

        Args:
            account_state: Optional pre-fetched account state.

        Returns:
            Sorted list of MultisigTransaction objects.

        Raises:
            MultisigError: If query fails.
        """
        try:
            if account_state is None:
               account_state = await self.transport.get_account_state(self.address)
            func = self.abi.get_function("getTransactions")
            result = func.call(account_state, {})
            transactions = [
                MultisigTransaction(
                    id=tx["id"],
                    confirmations_mask=tx["confirmationsMask"],
            	    signs_required=tx["signsRequired"],
                    signs_received=tx["signsReceived"],
            	    creator=tx["creator"],
            	    index=tx["index"],
            	    dest=tx["dest"],
            	    value=tx["value"],
            	    send_flags=tx["sendFlags"],
            	    payload=tx["payload"],
            	    bounce=tx["bounce"],
            	    state_init=tx["stateInit"]
			    )
                for tx in result.output["transactions"]
		    ]
            transactions.sort(key=lambda t: t.id)
            return transactions
        except Exception as e:
            raise MultisigError(f"Failed to get transactions: {str(e)}") from e


    async def get_transaction(self, transaction_id: int, account_state: Optional[nt.AccountState] = None) -> Optional[MultisigTransaction]:
        """Get a specific transaction by ID.

        Args:
            transaction_id: ID of the transaction.
            account_state: Optional pre-fetched account state.

        Returns:
            MultisigTransaction if found, else None.

        Raises:
            MultisigError: If query fails.
        """
        try:
            if account_state is None:
               account_state = await self.transport.get_account_state(self.address)        
            func = self.abi.get_function("getTransaction")
            input_data = {"transactionId": transaction_id}
            result = func.call(account_state, input_data)
            if result.output is None:
                return None            
            tx = result.output.get("trans")            
            return MultisigTransaction(
                id=tx["id"],
                confirmations_mask=tx["confirmationsMask"],
                signs_required=tx["signsRequired"],
                signs_received=tx["signsReceived"],
                creator=tx["creator"],
                index=tx["index"],
                dest=tx["dest"],
                value=tx["value"],
                send_flags=tx["sendFlags"],
                payload=tx["payload"],
                bounce=tx["bounce"],
                state_init=tx["stateInit"]
		    )
        except Exception as e:
            raise MultisigError(f"Failed to get transaction: {str(e)}") from e
    

    async def get_public_key(self) -> nt.PublicKey:
        """Get the public key of the multisig wallet.

        Returns:
            The public key used for address calculation and deployment. 
            Could be different from custodians (wallet owners).

        Raises:
            MultisigError: If query fails.
        """
        try:
            account_state = await self.transport.get_account_state(self.address)
            fields = self.abi.decode_fields(account_state)
            pubkey_int = int(fields["_pubkey"])        
            return nt.PublicKey.from_int(pubkey_int)        
        except Exception as e:
            raise MultisigError(f"Failed to get public key: {str(e)}") from e
    
	    
    async def submit_update(
        self,
        signer: nt.KeyPair,
        code_hash: Optional[int] = None,
        owners: Optional[List[int]] = None,
        req_confirms: Optional[int] = None,
        lifetime: Optional[int] = None        
    ) -> Tuple[nt.Transaction, int]:
        """Submit an update request for the multisig configuration.

        Args:
            signer: Signer keypair.
            code_hash: Optional new code hash.
            owners: Optional new list of owners.
            req_confirms: Optional new required confirmations.
            lifetime: Optional new lifetime.

        Returns:
            Tuple of the transaction and update ID.

        Raises:
            MultisigError: If no parameters provided or submission fails.
        """
        try:
            input_data = {
                "codeHash": code_hash,
                "owners": owners,
                "reqConfirms": req_confirms,
                "lifetime": lifetime
            }
            if all(v is None for v in input_data.values()):
                raise MultisigError("At least one update parameter (code_hash, owners, req_confirms, lifetime) must be provided")
            state = await self.get_account_state()
            if state is None:
                raise MultisigError(f"[ERROR] Account state of {self.address} is not found. Cannot update non-existing account.")
            if state.status == nt.AccountStatus.Frozen:
                raise MultisigError(f"[ERROR] Address {self.address} is Frozen. Unfreeze account before updating.")
            if state.status == nt.AccountStatus.Uninit:
                raise MultisigError(f"[ERROR] Address {self.address} is Uninit. Deploy contract before updating.")            
            if state.balance < MIN_BALANCE_REQUIRED:
                raise MultisigError(f"[ERROR] Account balance {state.balance} is less than minimal required {MIN_BALANCE_REQUIRED}.")
            tx = await self._send_external_message("submitUpdate", input_data, signer)
            decoded = self.abi.decode_transaction(tx)
            update_id = decoded.output["updateId"]
            return tx, update_id
        except Exception as e:
            raise MultisigError(f"Failed to submit update: {str(e)}") from e
        

    async def confirm_update(
        self,
        signer: nt.KeyPair,
        update_id: int        
    ) -> nt.Transaction:
        """Confirm an update request.

        Args:
            signer: Signer keypair.
            update_id: ID of the update to confirm.

        Returns:
            The confirmation transaction.

        Raises:
            MultisigError: If confirmation fails.
        """
        try:
            input_data = {"updateId": update_id}
            tx = await self._send_external_message("confirmUpdate", input_data, signer)
            return tx
        except Exception as e:
            raise MultisigError(f"Failed to confirm update: {str(e)}") from e


    async def execute_update(
        self,
        signer: nt.KeyPair,
        update_id: int,
        code: Optional[nt.Cell] = None,
    ) -> nt.Transaction:
        """Execute a confirmed update request.

        Args:
            signer: Signer keypair.
            update_id: ID of the update to execute.
            code: Optional new code cell (if updating code).

        Returns:
            The execution transaction.

        Raises:
            MultisigError: If execution fails.
        """
        try:
            input_data = {"updateId": update_id, "code": code}
            tx = await self._send_external_message("executeUpdate", input_data, signer)
            return tx
        except Exception as e:
            raise MultisigError(f"Failed to execute update: {str(e)}") from e


    async def get_update_requests(self, account_state: Optional[nt.AccountState] = None) -> List[MultisigUpdateRequest]:
        """Get the list of pending update requests.

        Args:
            account_state: Optional pre-fetched account state.

        Returns:
            List of MultisigUpdateRequest objects.

        Raises:
            MultisigError: If query fails.
        """
        try:
            if account_state is None:
               account_state = await self.transport.get_account_state(self.address)
            func = self.abi.get_function("getUpdateRequests")
            result = func.call(account_state, {})
            updates = [
                MultisigUpdateRequest(
                    id=u["id"],
                    index=u["index"],
                    signs=u["signs"],
                    confirmations_mask=u["confirmationsMask"],
                    creator=u["creator"],
                    code_hash=u["codeHash"],
                    custodians=u["custodians"],
                    req_confirms=u["reqConfirms"],
                    lifetime=u["lifetime"]
                )
                for u in result.output["updates"]
            ]
            return updates
        except Exception as e:
            raise MultisigError(f"Failed to get update requests: {str(e)}") from e
        

    async def is_confirmed(self, mask: int, index: int, account_state: Optional[nt.AccountState] = None) -> bool:
        """Check if a custodian has confirmed using the mask.

        Args:
            mask: Confirmations mask.
            index: Custodian index.
            account_state: Optional pre-fetched account state.

        Returns:
            True if confirmed, False otherwise.

        Raises:
            MultisigError: If query fails.
        """
        try:
            if account_state is None:
                account_state = await self.transport.get_account_state(self.address)
            func = self.abi.get_function("isConfirmed")
            input_data = {"mask": mask, "index": index}
            result = func.call(account_state, input_data)
            return result.output["confirmed"]
        except Exception as e:
            raise MultisigError(f"Failed to check if confirmed: {str(e)}") from e
    

    async def get_balance(self) -> nt.Tokens:
        """Get the current balance of the multisig wallet.

        Returns:
            The balance in Tokens.

        Raises:
            MultisigError: If query fails.
        """
        try:
            state = await self.get_account_state()
            return state.balance
        except Exception as e:
            raise MultisigError(f"Failed to get balance: {str(e)}") from e


    async def get_account_state(self) -> nt.AccountState:
        """Fetch the current account state.

        Returns:
            The account state.

        Raises:
            MultisigError: If query fails.
        """
        try:
            return await self.transport.get_account_state(self.address)
        except Exception as e:
            raise MultisigError(f"Failed to get account state: {str(e)}") from e
    

    async def get_required_confirms(self) -> int:
        """Get the required transaction confirmations.

        Returns:
            The required confirms.

        Raises:
            MultisigError: If query fails.
        """
        try:
            params = await self.get_parameters()
            return params.required_txn_confirms
        except Exception as e:
            raise MultisigError(f"Failed to get required transaction confirmation: {str(e)}") from e


    async def get_owner_index(self, pubkey: int) -> Optional[int]:
        """Get the index of an owner by public key.

        Args:
            pubkey: The public key (as int).

        Returns:
            The index if found, else None.

        Raises:
            MultisigError: If query fails.
        """
        try:
            custodians = await self.get_custodians()
            for c in custodians:
                if c.pubkey == pubkey:
                    return c.index
            return None
        except Exception as e:
            raise MultisigError(f"Failed to get owner index: {str(e)}") from e
        

