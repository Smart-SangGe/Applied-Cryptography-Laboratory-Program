import hashlib
import hmac


def compute_hmac(message, key, hash_func):
    """计算HMAC
    :param message: 需要计算HMAC的信息
    :param key: 密钥
    :param hash_func: 用于HMAC的hash函数,如hashlib.sha256
    :return: HMAC值
    """
    hmac_object = hmac.new(key, message, hash_func)
    return hmac_object.hexdigest()


# 示例：使用SHA256计算HMAC
message = b"123456111111444"
key = b"654321"
hash_func = hashlib.sha256

hmac_result = compute_hmac(message, key, hash_func)
print(f"HMAC for the message using SHA256: {hmac_result}")
