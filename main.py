import os
from math import floor, log10

import matplotlib.pyplot as plt

# matplotlib.use("TkAgg")
# ?
import fitz
from tkinter import *
# import os as os
# import PyPDF2
import tkinter as tk
from tkinter import filedialog
# from tkinter.filedialog import askopenfile
from PIL import ImageTk, Image
import numpy as np
# import pickle

readingSpeed = 0


if not os.path.exists('speed_wpm.txt'):
    open('speed_wpm.txt', 'w').close()

window = tk.Tk()
window.title("Reading Speed Tracker from PDF")
canvas = tk.Canvas(window, width=600, height=300)

# hex allowed
window.config(background="#009BFF")

# image
pictureFile = "output-onlinepngtools.png"
logo = Image.open(pictureFile)
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo, bg="#009BFF")
logo_label.image = logo
logo_label.grid(column=0, row=0)

# label
pdfLabel = Label(window, text="Select your book (PDF with regular fonts) (after entering all fields)",
                 bg="#009BFF", fg="#FFD500",
                 font="none 12 bold")
pdfLabel.grid(row=8, column=0, sticky="W")

wordsLabel = Label(window, text="Words: ", bg="#009BFF", fg="#13F304", font="none 14 bold")
wordsLabel.grid(row=7, column=0, sticky="W")

minutesLabel = Label(window, text="Minutes: ", bg="#009BFF", fg="#CD00FF", font="none 14 bold")
minutesLabel.grid(row=7, column=0, sticky="E")

wpmLabel = Label(window, text="WPM: ", bg="#009BFF", fg="#090CE7", font="none 20 bold")
wpmLabel.grid(row=6, column=0)

enterMinutes = Label(window, text="Enter minutes below ", bg="#009BFF", fg="black", font="none 12 bold")
enterMinutes.grid(row=12, column=0)

enterRange = Label(window, text="Enter pages completely read below (from in top, to in bottom)", bg="#009BFF",
                   fg="black",
                   font="none 12 bold")
enterRange.grid(row=9, column=0)

# warningLabel = Label(window, text="Enter all fields above before calculating ", bg="#009BFF", fg="#FF6400",
# font="none 12 bold")
# warningLabel.grid(row=17)

# input
minutes_entry = Entry(window, width=5, bg="white")
minutes_entry.grid(row=14, column=0)

from_entry = Entry(window, width=5, bg="white")
from_entry.grid(row=10, column=0)

to_entry = Entry(window, width=5, bg="white")
to_entry.grid(row=11, column=0)

enter_txt = tk.StringVar()
enter_txt.set("Select Book and Calculate WPM")


def open_file():
    filepath = filedialog.askopenfilename(title="Open PDF", filetypes=[('pdf file', '*.pdf')])
    print(filepath)
    # noinspection PyUnresolvedReferences
    filename = fitz.open(filepath)
    return filename


def calculate():
    # you want page 4, its load page (3)
    file = open_file()

    from_page = int(from_entry.get()) - 1
    to_page = int(to_entry.get()) - 1

    words = [s for s in file.load_page(from_page).get_text() if s == ' ' or s == '\n']

    while from_page != to_page:
        from_page = from_page + 1
        words += [s for s in file.load_page(from_page).get_text() if s == ' ' or s == '\n']

    sp = len(words)

    readingTime = int(minutes_entry.get())

    global readingSpeed

    readingSpeed = sp / readingTime

    minutesLabel.config(text="Minutes: " + str(readingTime))
    wpmLabel.config(text="WPM: " + str(readingSpeed))
    wordsLabel.config(text="Words: " + str(sp))

    file.close()


enter_btn = Button(window, textvariable=enter_txt, width=25, command=calculate, height=1)
enter_btn.grid(row=16, column=0)


def round_to_1(x):
    return round(x, -int(floor(log10(abs(x)))))


# save to txt file? and then pull data
def save():
    save_txt.set("Saved ")
    if os.path.getsize("speed_wpm.txt") == 0:
        outfile = open('speed_wpm.txt', 'w')
        outfile.write(str(round(readingSpeed)))
    else:
        outfile = open("speed_wpm.txt", 'a+')
        outfile.write('\n' + str(round(readingSpeed)))
    pass
    # update count, by reading the line amount? or new file


# SAVE
save_txt = tk.StringVar()
save_txt.set("Save WPM")

save_btn = Button(window, textvariable=save_txt, width=8, command=save, height=2)
save_btn.grid(row=16, column=0, sticky="W")
#

# View stats, maybe write to text file, then retrieve it
view_text = tk.StringVar()
view_text.set("See your stats")


# open new window
def view():
    open_new_window()
    pass


view_btn = Button(window, textvariable=view_text, width=10, command=view, height=2)
view_btn.grid(row=16, column=0, sticky="E")


# load history from file
def load_count():
    with open("speed_wpm.txt") as file_in:
        sessions = []
        count = 0
        for line in file_in:
            count = count + 1
            sessions.append(count)
    print(sessions)
    file_in.close()
    return sessions


def load_wpm():
    with open("speed_wpm.txt") as file_in:
        wpm_list = []
        for line in file_in:
            wpm_list.append(float(line.strip()))
    print(wpm_list)
    file_in.close()
    return wpm_list


# also have average to compare
# populate the graph
# chart options
def populate_graph(sessions, wpm_list):
    plt.bar(sessions, wpm_list)
    plt.title("WPM history")

    plt.xlim([0, len(sessions)+1])
    plt.ylim([min(wpm_list) - 10, max(wpm_list)+10])
    plt.xlabel("Session ")
    plt.ylabel("WPM")

    plt.show()


def open_new_window():
    populate_graph(load_count(), load_wpm())
    newWindow = Toplevel(window)

    newWindow.title("Stats")

    newWindow.geometry("1000x500")

    Label(newWindow,
          text="WPM history").pack()


# End window
window.mainloop()
