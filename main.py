import glob
from pathlib import Path
import os
import send2trash
import tkinter as tk
from tkinter import filedialog

#  os.path.isdir(d) To check if file is directory
# path.cwd() - Current working directory

found_empty_directories = []


def check_folder(folder_path):
    # print(f'!!! Started checking path: "{folder_path}" !!!')
    if not glob.glob(f'{folder_path}/*'):
        print(f"Directory is empty: '{folder_path}'")
        found_empty_directories.append(folder_path)
        # delete_empty_folder(file)
    else:
        # print('Inside of it:')
        for file in glob.glob(f'{folder_path}/*'):
            if file:
                if os.path.isdir(file):
                    # print(f'"{file}" is folder. Checking this folder as well')
                    check_folder(Path(file).absolute())
    return found_empty_directories


def delete_empty_folder(file):
    send2trash.send2trash(file)


class Application(tk.Frame):
    """ GUI for DiskCleanupProject"""
    def __init__(self, master=None, **kw):
        tk.Frame.__init__(self, master)
        self.current_search = None
        self.folder_path_show = tk.StringVar()
        self.pack()
        self.create_widgets()

    def browse_button(self):
        # try:
        # self.previous_search = self.current_search
        found_empty_directories = []
        self.current_search = filedialog.askdirectory()  # Buffer so we don't change "self.folder_path" value from None
        self.folder_path_show.set(self.current_search)
        # return filename

    def search_directories(self):
        if self.current_search is None:
            print('No folder is chosen')
        elif self.current_search == self.previous_search:
            print(f"You've just searched this folder")
        else:
            print(found_empty_directories)
            self.list_of_results.delete(0, tk.END)
            # self.list_of_results.destroy()

            for index, folder in enumerate(check_folder(folder_path=self.current_search), 0):
                print(folder)
                self.list_of_results.insert(index, folder)

            self.previous_search = self.current_search  # Prevents checking same folder

    def create_widgets(self):
        self.canvas = tk.Canvas(scrollregion=(0, 0, 500, 500), height=200, width=200)
        self.canvas.pack(side=tk.LEFT)

        self.exit = tk.Button(text="Exit", fg="red", command=self.quit)
        self.exit.pack(side=tk.RIGHT, anchor=tk.SE)

        self.hi_there = tk.Button(text="Choose Folder", command=self.browse_button)
        self.hi_there.pack(side=tk.BOTTOM, anchor=tk.S)

        self.search = tk.Button(text="Search Chosen Folder", command=self.search_directories)
        self.search.pack(side=tk.BOTTOM, anchor=tk.S)

        self.prog_label = tk.Label(textvariable=self.folder_path_show)
        self.prog_label.pack(side=tk.TOP, anchor=tk.N)

        self.x_scrollbar = tk.Scrollbar(orient=tk.HORIZONTAL)
        self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.y_scrollbar = tk.Scrollbar()
        self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.list_of_results = tk.Listbox(yscrollcommand=self.y_scrollbar.set, xscrollcommand=self.x_scrollbar.set, width=54)
        self.list_of_results.pack(side=tk.BOTTOM)

        self.x_scrollbar.config(command=self.list_of_results.xview)
        self.y_scrollbar.config(command=self.list_of_results.yview)




        # self.delete_directories = Button(text="Delete Results", command=self.browse_button)
        # self.delete_directories.pack({"side": "right"})








if __name__ == '__main__':
    # initial_folder = f'{Path.cwd()}\\TestFolder\\'  # Path where user chooses to start checking folders
    # initial_file = 'TestFolder'
    # check_folder(initial_folder)

    root = tk.Tk(className='Disk Cleanup Project')
    app = Application(master=root)
    app.mainloop()
    root.destroy()
