import fitz
from tkinter import *
# import os
# import PyPDF2
import tkinter as tk
from tkinter import filedialog
# from tkinter.filedialog import askopenfile
from PIL import ImageTk, Image

window = tk.Tk()
window.title("Reading Speed Tracker from PDF")
canvas = tk.Canvas(window, width=600, height=300)

# hex allowed
window.config(background="#5c5ce5")

# image
pictureFile = "output-onlinepngtools.png"
logo = Image.open(pictureFile)
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo, bg="#5c5ce5")
logo_label.image = logo
logo_label.grid(column=0, row=0)

# label
pdfLabel = Label(window, text="Select your book (PDF with regular fonts)", bg="#5c5ce5", fg="black",
                 font="none 12 bold")
pdfLabel.grid(row=7, column=0)

wordsLabel = Label(window, text="Words: ", bg="#5c5ce5", fg="blue", font="none 12 bold")
wordsLabel.grid(row=6, column=0, sticky= "W")

minutesLabel = Label(window, text="Minutes: ", bg="#5c5ce5", fg="blue", font="none 12 bold")
minutesLabel.grid(row=6, column=0, sticky="E")

wpmLabel = Label(window, text="WPM: ", bg="#5c5ce5", fg="red", font="none 12 bold")
wpmLabel.grid(row=6, column=0)

enterMinutes = Label(window, text="Enter minutes below ", bg="#5c5ce5", fg="black", font="none 12 bold")
enterMinutes.grid(row=8, column=0)

# input

text_entry = Entry(window, width=20, bg="white")
text_entry.grid(row=9, column=0)

enter_txt = tk.StringVar()

enter_txt.set("Calculate WPM")

# Button
def click():
    entered_text = text_entry.get()
    print(entered_text)
    open_file()


def open_file():
    #
    filepath = filedialog.askopenfilename(title="Open PDF",   filetypes=[('pdf file', '*.pdf')])
    print(filepath)
    filename = fitz.open(filepath)
    page = filename.load_page(7)
# print(page)
    words = page.get_text()
# print(words)
    return filename



def load_wpm():
    pass


def calculate():
    # you want page 4, its load page (3)
    file = open_file()

    page8 = file.load_page(7)
    page9 = file.load_page(8)
    page10 = file.load_page(9)
    page11 = file.load_page(10)

    wordsOnPage8 = page8.get_text()
    wordsOnPage9 = page9.get_text()
    wordsOnPage10 = page10.get_text()
    wordsOnPage11 = page11.get_text()

    # looks like 2% error
    spaces = [s for s in wordsOnPage8 if s == ' ' or s == '\n']
    spaces += [s for s in wordsOnPage9 if s == ' ' or s == '\n']
    spaces += [s for s in wordsOnPage10 if s == ' ' or s == '\n']
    spaces += [s for s in wordsOnPage11 if s == ' ' or s == '\n']

    # pagesRead = 4

    # for x in range(pagesRead):
    # print(x)

    words = len(spaces)
    # pages 8 , 9 , 10  and 11 = 1107 words

    # readingTime = int(input("How many minutes did you read? "))
    readingTime = int(text_entry.get())

    readingSpeed = words / readingTime

    minutesLabel.config(text="Minutes: " + str(readingTime))
    wpmLabel.config(text="WPM: " + str(readingSpeed))

    file.close()

    load_wpm()


# file = open_file()
# file = fitz.open("Essays.pdf")
# run the main loop

enter_btn = Button(window, textvariable=enter_txt, width=12, command=calculate, height=1)
enter_btn.grid(row=10, column=0)


def save():
    #actual saved info
    save_txt.set("Saved ")
    pass

# SAVE


save_txt = tk.StringVar()
save_txt.set("Save WPM")

save_btn = Button(window, textvariable=save_txt, width=8, command=save, height=2)
save_btn.grid(row=10, column=1)
#


# View stats, maybe write to text file, then retrieve it
view_text = tk.StringVar()
view_text.set("See your stats" )

# End window
window.mainloop()
