from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

# 生成RSA密钥对
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

# 示例数据
message = b"1234442fssvwrt34tqfq4fqeeqr"

# 创建RSA签名对象
signer = PKCS1_v1_5.new(RSA.import_key(private_key))

# 对数据进行签名
hash_obj = SHA256.new(message)
signature = signer.sign(hash_obj)

# 打印签名结果
print("Signature:", signature)

# 创建RSA验证对象
verifier = PKCS1_v1_5.new(RSA.import_key(public_key))

# 验证签名
is_valid = verifier.verify(hash_obj, signature)
print("Signature is valid:", is_valid)
