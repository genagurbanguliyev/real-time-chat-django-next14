const CryptoJS = require('crypto-js');


export const encryptText = (text: string): string => {
  return text ? CryptoJS.AES.encrypt(text, process.env.NEXT_PUBLIC_CRYPT_KEY).toString() : null;
};

export const decryptText = (data: string): string => {
  return data ? CryptoJS.AES.decrypt(data, process.env.NEXT_PUBLIC_CRYPT_KEY).toString(CryptoJS.enc.Utf8) : null;
};