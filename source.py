import requests
from html import unescape
from bs4 import BeautifulSoup 
from tkinter import *
from tkinter import ttk 
import os

def review_button():
    tp = Toplevel()
    tp.title("Flashcard_Studio/Sets")
    tp.geometry("800x350")
    global res
    global resSV
    global g
    e = 0
    c = 0
    res = []
    label2 = Label(tp, text = "Sets:")
    label2.pack()
    for path in os.listdir("flashdata/"):
        c += 1
        res.append(path)
    resSV = StringVar()
    resSV.set(res[0])
    dropdownsetsel = ttk.OptionMenu(tp, resSV, *res)
    setselbut = Button(tp, text = "Set Options:", command = selsetops)
    dropdownsetsel.pack()
    setselbut.pack()

def selsetops():
    global g
    e = resSV.get()
    with open(f"flashdata/{e}", "r") as f:
        g = []
        f.seek(0)
        g = f.read().splitlines()
        f.close()
    tpp = Toplevel()
    tpp.title("Flashcard_Studio/Sets/Mode")
    flashcardmodebutton = Button(tpp, text = "Flashcards", command = flashcardmode)
    flashcardmodebutton.pack()

def flashcardmode():
    global zz
    global flipped
    global flashcardflip
    flipped = False
    zz = 0
    fw = Toplevel()
    fw.geometry("1200x625")
    fw.title("Flashcard_Studio/Sets/Mode/Flashcards")
    flashcardflip = Button(fw, text = g[zz], height = 10, width = 120, command = flip)
    prevflashbutton = Button(fw, text = "<", command = prevfl)
    nextflashbutton = Button(fw, text = ">", command = nextfl)
    flashcardflip.pack()
    prevflashbutton.pack()
    nextflashbutton.pack()


def flip():
    global flipped
    if flipped == False:
        flashcardflip.config(text = g[zz+1])
        flipped = True
    else:
        flashcardflip.config(text = g[zz])
        flipped = False

def prevfl():
    global zz
    zz = zz - 2
    print(zz)

def nextfl():
    global zz
    zz = zz + 2
    print(zz)

def scrape():
    flshlinelen = 0
    print("Button pressed")
    HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    soup = BeautifulSoup(requests.get(entry_text.get(), headers=HEADERS).text, "html.parser")
    flashcard_title = soup.find("h1").text

    f = open(f'flashdata/{flashcard_title}.txt', 'w')

    flsh = soup.find_all("div", class_ = "SetPageTerms-term")
    flsh += soup.find_all("div", class_ = "SetPageTerms-term SetPageTerms-term--beyondSignupThreshold")

    for index, flashcards in enumerate(flsh):
        flshlst = flsh[index]
        flash1 = flshlst.find("a", class_ = "SetPageTerm-wordText").text
        flash2 = flshlst.find("a", class_ = "SetPageTerm-definitionText").text
        with open(f"flashdata/{flashcard_title}.txt", "a") as f:
            f.write(f"w: {flash1}\n")
            f.write(f"def: {flash2}\n")
            flshlinelen += 2
            print(f"w: {flash1}\n")
            print(f"def: {flash2}\n")
    opener = open("flashdata/" + flashcard_title + ".txt", "a")
    opener.write(str(flshlinelen))
    print(flshlinelen)
    opener.close()
    f.close()
    x = open(f"flashdata/{flashcard_title}.txt", "r")
    print(x.read())

root = Tk()

root.title("Flashcard_Studio/Scrape")
root.minsize(700,100)
root.maxsize(700,100)

label = Label(text = "Quizlet Link:")
entry_text = StringVar()
entry = Entry(textvariable = entry_text, width = 75)
button1 = Button(text = "Get Flashcards", command = scrape)
button2 = Button(root, text = "Review Sets", command = review_button)
label.pack()
entry.pack()
button1.pack()
button2.pack()


root.mainloop()
