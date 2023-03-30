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
    global setnames
    global setnamesStrVar
    setnames = []
    label2 = Label(tp, text = "Sets:")
    label2.pack()
    # listdir collects set names to be displayed in OptionMenu() and which when one is selected and the
    # setselbut Button is clicked will run selectsetoptions()
    for path in os.listdir("flashdata/"):
        setnames.append(path)
    setnamesStrVar = StringVar()
    setnamesStrVar.set(setnames[0])
    dropdownsetsel = ttk.OptionMenu(tp, setnamesStrVar, *setnames)
    setselbut = Button(tp, text = "Set Options:", command = selectsetoptions)
    dropdownsetsel.pack()
    setselbut.pack()

def selectsetoptions():
    global selectsetdata
    filenames = setnamesStrVar.get()
    # Gets the name of the set picked to be edited
    with open(f"flashdata/{filenames}", "r") as file:
        selectsetdata = []
        file.seek(0)
        selectsetdata = file.read().splitlines()
        file.close()
    # Opens the slected set file and puts all the data into a 1D list formatted [word, defintion]
    tpp = Toplevel()
    tpp.title("Flashcard_Studio/Sets/Mode")
    flashcardmodebutton = Button(tpp, text = "Flashcards", command = flashcardmode)
    flashcardmodebutton.pack()
    # Currently there is only one option for flashcards available, and that is flashcardmode()

def flashcardmode():
    global dataindex
    global flipped
    global flashcardflip
    flipped = False
    dataindex = 0
    fm = Toplevel()
    fm.geometry("1200x625")
    fm.title("Flashcard_Studio/Sets/Mode/Flashcards")
    flashcardflip = Button(fm, text = selectsetdata[dataindex], height = 10, width = 120, command = flip)
    # The flashcards are just a massive button that uses flip() to change the text on the button.
    prevflashbutton = Button(fm, text = "<", command = prevflash)
    nextflashbutton = Button(fm, text = ">", command = nextflash)
    flashcardflip.pack()
    prevflashbutton.pack()
    nextflashbutton.pack()


def flip():
    global flipped
    if flipped == False:
        flashcardflip.config(text = selectsetdata[dataindex+1])
        # Because of the way the list of flashcards is formatted ([word, definition]), the
        # flashcards are in groups of 2.
        flipped = True
    else:
        flashcardflip.config(text = selectsetdata[dataindex])
        flipped = False

def prevflash():
    global dataindex
    dataindex = dataindex - 2
    print(dataindex)

def nextflash():
    global dataindex
    dataindex = dataindex + 2
    print(dataindex)

def scrape():
    HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    soup = BeautifulSoup(requests.get(entry_text.get(), headers=HEADERS).text, "html.parser")
    # Gets the actual HTML file of the Quizlet that you would like to scrape.
    flashcard_title = soup.find("h1").text

    file = open(f'flashdata/{flashcard_title}.txt', 'w')
    # Creates and opens a new file or opens an old one ready for re/writing

    setdata = soup.find_all("div", class_ = "SetPageTerms-term")
    setdata += soup.find_all("div", class_ = "SetPageTerms-term SetPageTerms-term--beyondSignupThreshold")
    # Collecting the setdata divs, not the raw data.

    for index, flashcards in enumerate(setdata):
        flashlist = setdata[index]
        flashword = flashlist.find("a", class_ = "SetPageTerm-wordText").text
        flashdefinition = flashlist.find("a", class_ = "SetPageTerm-definitionText").text
        with open(f"flashdata/{flashcard_title}.txt", "a") as file:
            file.write(f"w: {flashword}\n")
            file.write(f"def: {flashdefinition}\n")
    file.close()

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
