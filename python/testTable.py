from tkinter import Button, END, Listbox, Tk
from time import sleep

root = Tk()

# My version of Tkinter doesn't have a MultiListbox
# So, I use its closest alternative, a regular Listbox
listbox = Listbox(root)
listbox.pack(side='left')

def start():
    """This is where your loop would go"""

    for i in range(17):
        # The sleeping here represents a time consuming process
        # such as making a PDF
        #sleep(0.5)

        listbox.insert(END, Button(listbox, text=str(i)).pack())

        # You must update the listbox after each entry
        listbox.update()

# You must create a button to call a function that will start the loop
# Otherwise, the display won't appear until after the loop exits
Button(root, text="Start", command=start).pack()

root.mainloop()