const CryptoJS = require('crypto-js');


export const encryptText = (text: string): string => {
  return text ? CryptoJS.AES.encrypt(JSON.stringify(text), process.env.NEXT_PUBLIC_CRYPT_KEY).toString() : null;
};

export const decryptText = (data: string): string => {
  if(data){
    const info = CryptoJS.AES.decrypt(data, process.env.NEXT_PUBLIC_CRYPT_KEY).toString(CryptoJS.enc.Utf8)
    return JSON.parse(info)
  }
  return null;
};