import math

ulang = "0123456789qwertyiopasdfghjklzxcvbnmu"
    
def encryption(sentence: str):
    unicode_list = [ord(t) for t in sentence]
    result = []
    
    for unicode in unicode_list:
        ulang_list = []
        before_num = unicode

        for i in range(int(math.log(unicode, len(ulang[:-1])))):
            ulang_list.append(before_num % len(ulang[:-1]))
            before_num = before_num // len(ulang[:-1])

        ulang_list.append(before_num)
        result.append(list(reversed(ulang_list)))

    final = []
    for r in result:
        final.append("".join([ulang[i] for i in r]))

    return ulang[-1].join(final)

def decryption(sentence: str):
    try:
        final_list = sentence.split(ulang[-1])
        ulang_list = [[ulang.index(t) for t in unu] for unu in final_list]
        unicode_list = [sum([unu[u] * (len(ulang[:-1]) ** (len(unu) - u - 1)) for u in range(len(unu))]) for unu in ulang_list]
        
        return "".join([chr(unicode) for unicode in unicode_list])

    except:
        return None

if __name__ == "__main__":
    sentence = "2zu2vu36u34u31u30u35u3e"
    print(decryption(sentence))
    