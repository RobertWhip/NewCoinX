import rsa

# !!! TODO: do we need this script at all?

'''
    Logic description:
    1. You should generate RSA public and private keys (OpenSSL):
        a. openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -pkeyopt rsa_keygen_publexp:3 -out private_key.pem
        b. openssl pkey -in private_key.pem -out public_key.pem -pubout
    2. You can encrypt messages with receiver's public key
    3. You can decrypt messages with your private key
    4. You can sign and verify messages
'''

# TODO: test wether the keys are correct
def generate_keys():
    (public, private) = rsa.newkeys(1024)
    return public.save_pkcs1('PEM'), private.save_pkcs1('PEM')

# TODO: do we need this function?
def write_keys(public, private):
    with open('../../test/keys/public_key_3.pem', 'wb') as p:
        p.write(public)
    with open('../../test/keys/private_key_3.pem', 'wb') as p:
        p.write(private)

# TODO: do we need this function?
def load_keys(public_path, private_path):
    with open(public_path, 'rb') as p:
        public = rsa.PublicKey.load_pkcs1(p.read())
    with open(private_path, 'rb') as p:
        private = rsa.PrivateKey.load_pkcs1(p.read())

    return public, private

# encypt message using reveiver's public key
def encrypt(msg, public_key):
    return rsa.encrypt(msg.encode('ascii'), public_key)

# decrypt message using your private key
def decrypt(ciphertext, private_key):
    try:
        return rsa.decrypt(ciphertext, private_key).decode('ascii')
    except:
        return False

# create signature using your private key
def sign(message, key):
    return rsa.sign(message.encode('ascii'), key, 'SHA-1')

# verify signature using sender's public key
def verify(message, signature, key):
    try:
        return rsa.verify(message.encode('ascii'), signature, key,) == 'SHA-1'
    except:
        return False

if __name__ == '__main__':
    # reading generated keys with OpenSSL
    publicA, privateA = load_keys(
        '../../test/keys/public_key_A.pem',
        '../../test/keys/private_key_A.pem'
    )

    publicB, privateB = load_keys(
        '../../test/keys/public_key_B.pem',
        '../../test/keys/private_key_B.pem'
    )

    # user A prepares a message
    message = '<transaction data>'
    print('Message: ', message)

    # user A encrypts message with receiver's public key
    ciphertext = encrypt(message, publicB)

    # user A creates signature for the receiver, so the receiver can verify the message
    signature = sign(message, privateA)


    # user B received ciphertext and signature
    # user B decrypts ciphertext with his private key
    text = decrypt(ciphertext, privateB)
    print('Decrypted text: ', text)

    # user B verifies the correctness of user A's message
    if verify(text, signature, publicA):
        print('Successfully verified signature')
    else:
        print('The message signature could not be verified')

