import binascii
import ecdsa


# Convert ECDSA key to HEX string
#
# Function arguments:
# - key - private or public key that going to be converted to hex
#
# returns ECDSA key HEX in UTF-8
def to_hex(key) -> str:
    return binascii.hexlify(key.to_string()).decode('utf-8')


# Convert public key string to ECDSA public key
#
# Function arguments:
# - public_key - public key string
# - curve - elliptic curve (SECP256k1 is the Bitcoin elliptic curve)
#
# returns ECDSA public key
def to_ecdsa_public(public_key: str, curve=ecdsa.SECP256k1):
    return ecdsa.VerifyingKey.from_string(
        bytes.fromhex(public_key), 
        curve
    )

# Convert private key string to ECDSA private key
#
# Function arguments:
# - private_key - private key string
# - curve - elliptic curve (SECP256k1 is the Bitcoin elliptic curve)
#
# returns ECDSA private key
def to_ecdsa_private(private_key: str, curve=ecdsa.SECP256k1):
    return ecdsa.SigningKey.from_string(
        bytes.fromhex(private_key), 
        curve
    )


# Convert ECDSA private key to ECDSA public key
#
# Function arguments:
# - key - ECDSA private key
#
# returns ECDSA public key
def ecdsa_private_to_public(private_key):
    return private_key.get_verifying_key()


# Key generator function.
#
# Function arguments:
# - curve - elliptic curve (SECP256k1 is the Bitcoin elliptic curve)
# 
# returns private and public key pair
def gen_keys(curve=ecdsa.SECP256k1):
    private_key = ecdsa.SigningKey.generate(curve)
    public_key = private_key.get_verifying_key()

    return private_key, public_key


# Create signature for a message
#
# Function arguments:
# - msg - message (usually transaction hash)
# - private_key - the sender's private key
#
# returns a signature
def create_signature(msg, private_key):
    return private_key.sign(msg.encode('ascii'))


# Verify signature of a message
#
# Function arguments:
# - msg - message (received by sender)
# - sign - signature (received by sender)
# - public_key - sender's public key
#
# returns True (bool) if the message was successfully verified, else throws an error
def verify_signature(msg: str, sign, public_key) -> bool:
    return public_key.verify(sign, msg.encode('ascii'))


# Example of using this module
if __name__ == '__main__':
    # user A generates his keys
    privateA, publicA = gen_keys()
    print('[A] private: ', to_hex(privateA))
    print('[A] public: ', to_hex(publicA), '\n')

    # user B generates his keys
    privateB, publicB = gen_keys()
    print('[B] private: ', to_hex(privateB))
    print('[B] public: ', to_hex(publicB), '\n')

    # user A creates a transaction
    message = '<transaction_hash>'
    print('[A] prepares message: ', message, '\n')

    # user A signs transaction
    signature = create_signature(message, privateA)
    print('[A] creates a signature: ', signature, '\n')

    # user B verifies user A's transaction
    verified = verify_signature(message, signature, publicA)
    print('[B] verified the message: ', verified)    