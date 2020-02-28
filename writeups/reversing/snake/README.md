## hackthebox - snake (10)
- reversing
- by 3XPL017

> Flag should be in the format: HTB{username:password}

files:
- snake.py

printing _slither_ will give you:
> anaconda

next, let's analyze the pwd
```python
pass_input = raw_input('Enter your password\n')
for passes in pass_input:
    for char in chars:
        if passes == str(chr(char)):
            print 'Good Job'
            break
        else:
            print 'Wrong password try harder'
            exit(0)
```
we can see that the nested loop goes through the user input, character by character, to compare it to the array _chars_
above, we find that _chars_ is determined by the _keys_ and _chains_ loops

```python
keys = [0x70, 0x61, 0x73, 0x73, 0x77, 0x6f, 0x72, 0x64, 0x21, 0x21]
chains = [0x74, 0x68, 0x69, 0x73, 0x20, 0x69, 0x73, 0x20, 0x61, 0x20, 0x74, 0x72, 0x6f, 0x6c, 0x6c]
for key in keys:
    keys_encrypt = lock ^ key
    chars.append(keys_encrypt)
for chain in chains:
    chains_encrypt = chain + 0xA
    chars.append(chains_encrypt)
```

we can leverage this code by joining the completed chars and printing it, getting:
> udvvrjwa$$\~rs}*s}*k*\~|yvv

wtf is this? the challenge doesn't accept this for the flag HTB{usr:pwd}???
leveraging the code once again, i checked what the loop for just _keys_ spat out, giving:
> udvvrjwa$$

i assume this is what the challenge creator was going for as the correct flag is:
> HTB{anaconda:udvvrjwa$$}
