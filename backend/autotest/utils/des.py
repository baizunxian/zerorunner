import base64
import traceback

import rsa
from loguru import logger

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC2YZVJzRrn1kyJHZS+7O5/oteO
YOkbiNk3ndRLQscgdDf3k+RaRomzvHro5w2h6T9A5rd45vM0kyKcBezE/Za1pOKq
meovah1zxxoofQJ8k91ybVFXYJx99k9ravCMr+wKuCpuuwPe8he10iBZ465vVZ6g
5Nbg4gM2PcV7OMVLaQIDAQAB
-----END PUBLIC KEY-----"""

PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQC2YZVJzRrn1kyJHZS+7O5/oteOYOkbiNk3ndRLQscgdDf3k+Ra
RomzvHro5w2h6T9A5rd45vM0kyKcBezE/Za1pOKqmeovah1zxxoofQJ8k91ybVFX
YJx99k9ravCMr+wKuCpuuwPe8he10iBZ465vVZ6g5Nbg4gM2PcV7OMVLaQIDAQAB
AoGABgNhutMngjyVcta4omgOhS3jLcjJ8sbrA4Y220w5DhvALc+7XBMejpWmAfMT
8YekAWGsq7CwqjDON7Gge3kRdz7PDwjaPBwkOebD1aYNWDM0TfQiINVxCkZpPoKg
KTpIELQUoD6KMWw8NUwcasqHcz1HCC6DnRYpG3XJXYhdJDECQQDCvQ/tkHOi92He
RioTHSiJd/5TvgPgBH7dqsldT6mwS67EbrWFEiSSRbzref6wv+r8sXb9d436Ltno
4lngQWZZAkEA78FX7EzS/TAV/PDfWh/ncozY9tFqfPNk4w96LVb5wy8oc9M419K9
yLWeSfiBcXK2l+S2XYk49OhuznklZWiLkQJAL1c+1AXV1rxE8oAkIlloTWL6VOlQ
j9kH7mNiaGjBW7ZKWj5/qkXq1hRWBPi3TciaG6wYvS2fOj7BgrfkGXxMoQJBAIbT
zNUHEvPtMcBP2Nr+7BJgILcUZ3UjDw4dqxCKQ+S+xVn1Y5cDXVTcxcpFZM3eu85J
gUCypYQcngug1yXjF/ECQQCBZZAZ+GhpzqwerwqyfNHvrahSrfp14l6STktaCjKy
IR4n5TomCkHRaeXPgn1YVIhz5/LaVZJuKK3eiN2Wbdwy
-----END RSA PRIVATE KEY-----"""


def generate_secret_key():
    """
    公钥私钥生成
    :return:
    """
    # 生成 RSA 密钥对
    (pubkey, privkey) = rsa.newkeys(1024)

    # 将公钥和私钥导出为 PEM 格式字符串
    private_key = privkey.save_pkcs1().decode('utf-8')
    public_key = pubkey.save_pkcs1().decode('utf-8')
    return private_key, public_key


def encrypt_rsa_password(password):
    """
    密码加密
    :param password:
    :return:
    """
    try:
        # 导入公钥
        public_key = rsa.PublicKey.load_pkcs1_openssl_pem(PUBLIC_KEY.encode('utf8'))
        # 使用公钥进行加密
        encrypted_password = rsa.encrypt(password.encode('utf-8'), public_key)
        # 将加密后的字节序列进行 Base64 编码
        return base64.b64encode(encrypted_password).decode('utf-8')
    except Exception as err:
        logger.error(f"加密失败 😭\n{traceback.format_exc(limit=1)}")
        return password


def decrypt_rsa_password(password):
    """
    密码解密
    :param password:
    :return:
    """
    try:
        private_key = rsa.PrivateKey.load_pkcs1(PRIVATE_KEY.encode("utf8"))
        decrypt_password = rsa.decrypt(base64.b64decode(password), private_key)
        return decrypt_password.decode()
    except Exception as err:
        logger.error(f"解密失败 😭\n{traceback.format_exc()}")
        return password

if __name__ == '__main__':
    print(encrypt_rsa_password('Aa123456'))
    print(decrypt_rsa_password(
        'rjEAdq5BWN15fEEdtqqpKCBvoRd10rhJR3mznpCekVgnhOnfi1rC6dRt4RZ1XcVpDXAIxUevGuCj9r6GYfTqx+1Iqt3EEuxM0D5yRkiCtWs+PpqoNAGgD+8DMdWlu3DfmhvTFK/00WXjv+pw6jtZYjgNdHwz78f4hnpXSRtNh5o='))
