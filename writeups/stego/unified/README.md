## hackthebox - unified (20)

- stego
- by berzerk0

files:
BOD_30079.txt

i'm not very familiar with unicode stego so i googled it and first choice popped up with a [unicode stego solver](https://www.irongeek.com/i.php?page=security/unicode-steganography-homoglyph-encoder)

when you input the seemingly gibberish part of the msg into the decoder:
```
该系统以许多语言工作. يعمل النظام في العديد من اللغات. 
���� ���� �� �������� ��� ����� � ���� ��� ��
Το σύστημα λειτουργεί σε πολλές γλώσσες.Система работает на многих языках.
```
it gives you:
> HTB{tr1th3m1u5_1499}
