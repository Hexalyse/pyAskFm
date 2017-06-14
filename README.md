# pyAskFm
Basic (and imcomplete as of now) python implementation of the Ask.fm API in its 0.8 version, which is outdate but still functional.

## How does it work ?
See the `AskApiDemo.py` file for an example. The rest of the code is pretty much self explanatory and if you're using it, you should logically be able to understand the code.

## What am I seeing ? Why is there Java files ?
Well, the part that generate the HMAC has been decompiled from the AskFM .apk file. The bytecode has been translated back to Java, and I was too lazy to reimplement it in Python, so... yeah.

By the way, the HMAC generation code needs a secret key. I voluntarily censored it from the source code for various reasons (the most obvious one is that if AskFM used it, I guess they wanted to prevent people from reverse engineering their API, and I'm not sure about intellectual property here, so better be safe than sorry - I contacted them asking if they were okay with me using their API to make bots : they did not answer negatively and even communicated with one of the bots I created. Strange, since their ToS seems to prohibite the use of "automation").
If you want to use this code, you'll have to find this key by decompiling the AskFM .apk file yourself... sorry.
