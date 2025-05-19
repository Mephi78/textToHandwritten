from PIL import Image
from countwordlen import imgwidth
# import pytesseract
import random
import string
import os

width, height = 715, 760
arr = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+,.-?:/*<>}{()=[]$" '
imgsource = "myfont/"
pageheight = 7624
pagewidth = 5940
start = 715
end = 5930
pageno = 0

def getpage():
    global back, pageno
    try:
        pageno += 1
        bg = Image.open("myfont/backpage.png", 'r')
        back = Image.new('RGBA', (5952, 8088), (0, 0, 0, 0))
        back.paste(bg, (0, 0))
    except:
        print("backpage not found")
        exit()

def savepage():
    path = "final\\done"
    i = 1
    while os.path.exists(path + str(i) + ".png"):
        i += 1
    back.save(path + str(i) + ".png", "PNG")
    print("Saved done" + str(i) + ".png .......n")

def pasteimg(case, start, height):
    global back
    try:
        cases = Image.open(imgsource + "%s.png" % case)
        back.paste(cases, (start, height), mask=cases)
        start = start + cases.width + random.randint(5, 15)
    except FileNotFoundError:
        # Silently skip missing image
        pass
    except Exception as e:
        print(f"Unexpected error with case '{case}': {e}")
    return start

def getname(letter):
    if letter.isupper():
        letter = "c" + letter.lower()
    elif letter == ",":
        letter = "coma"
    elif letter == ".":
        letter = "fs"
    elif letter == "?":
        letter = "que"
    elif letter == "<":
        letter = "ang1"
    elif letter == ">":
        letter = "ang2"
    elif letter == "{":
        letter = "cur1"
    elif letter == "}":
        letter = "cur2"
    elif letter == ":":
        letter = "colon"
    elif letter == "/":
        letter = "div"
    elif letter == "-":
        letter = "sub"
    elif letter == "(":
        letter = "par1"
    elif letter == ")":
        letter = "par2"
    elif letter == "[":
        letter = "sqr1"
    elif letter == "]":
        letter = "sqr2"
    elif letter == "*":
        letter = "star"
    elif letter == "=":
        letter = "equal"
    elif letter == "+":
        letter = "plus"
    elif letter == "$":
        letter = "dol" + str((random.randint(1, 2)))
    elif letter == '"':
        letter = "quo"
    return letter

def getwordpix(word):
    wordwid = 0
    for char in word:
        if char in arr:
            img = getname(char)
            try:
                wordwid += imgwidth[img]
            except KeyError:
                continue
            except Exception as e:
                print(f"Unexpected error with character '{img}': {e}")
    return wordwid

def getnewline(start, cur, end, height):
    global back
    height = height + 244
    if height > pageheight:
        getnewpage()
        return start, 760
    else:
        start = 720 + (random.randint(0, 100))
    return start, height

def getnewpage():
    savepage()
    getpage()

def formatting(word, leng, start, cur, ecfnd):
    global height
    if leng >= 2:
        if word[:2] == "^^":
            word = word[2:]
            cur += (2418 - int(getwordpix(word) / 2))
        if word[:2] == "->":
            word = word[2:]
            cur += 400
    return word, cur

def checktag(content, i, height, start, cur, end):
    if content[i] == "<table>":
        try:
            print("Making table....")
            index = content.index("</table>", i + 1)
            content = content[i + 1:index]
            cols = int(content[0])
            total = 0
            ratio = [0]
            for j in range(1, cols + 1):
                total += int(content[j])
                ratio.append(int(content[j]))
            base = (end - start) / total
            content = content[cols + 1:index]
            content = " ".join(content)
            row = content.split("#")
            maxheight = 0
            i = 0
            lastheight = height
            for R in row:
                for C in R.split("|"):
                    C = C.split()
                    start, cur, end, height1 = condition(
                        lastheight, start + base * ratio[i], start + base * ratio[i], start + base * ratio[i + 1], C)
                    if height1 > maxheight:
                        maxheight = height1
                lastheight = maxheight
                i += 1
            return index + 1
        except Exception as e:
            print(e)
            print("     </table> not found")
            exit()
    return 0

def condition(height, start, cur, end, content):
    global arr, back
    first = 1
    for i in range(0, len(content)):
        word = content[i]
        ind = checktag(content, i, height, start, cur, end)
        if ind:
            i = ind
            continue
        halfword = 0
        leng = len(word)
        word, cur = formatting(word, leng, start, cur, end)
        wordwid = getwordpix(word)
        widthafterpaste = cur + wordwid + 70
        cur += 60 + random.randint(0, 35)
        if widthafterpaste > end:
            diff = widthafterpaste - end
            if leng > 5 and diff > ((0.4 * leng) + 250):
                halfword = 1
            else:
                cur, height = getnewline(start, cur, end, height)
        if height > 3500 and first:
            height += 10
            first = 0
        for letter in word:
            if letter == "#":
                cur, height = getnewline(start, cur, end, height)
                continue
            if letter in arr:
                letter = getname(letter)
                if halfword and cur + random.randint(200, 280) >= end:
                    cur, height = getnewline(start, cur, end, height)
                cur = pasteimg(letter, cur, height)
    return start, cur, end, height

def readfile():
    pass

def extract():
    try:
        filepath = "MyText.txt"
        file = open(filepath, encoding="utf8")
        content = file.read()
        file.close()
        print(content)
        content = content.split()
        getpage()
        condition(height, start, start, end, content)
        savepage()
    except Exception as e:
        print(e)

extract()
