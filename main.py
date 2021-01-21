import glob
from pathlib import Path
import os
import send2trash
import tkinter as tk
from tkinter import filedialog

#  os.path.isdir(d) To check if file is directory
# path.cwd() - Current working directory


def check_folder(folder_path, found_empty_directories):
    if not glob.glob(f'{folder_path}/*'):
        # Here we find new empty directories and add them to list
        found_empty_directories.append(folder_path)
    else:
        # Here we go deeper and check every subfolder
        for file in glob.glob(f'{folder_path}/*'):
            if file:  # Not 100% sure this step is required
                if os.path.isdir(file):
                    check_folder(Path(file).absolute(), found_empty_directories)
    return found_empty_directories


def delete_empty_folder(file):
    # Can make a choice between delete to Recycle Bin or permanently (By using checkmark in GUI)
    send2trash.send2trash(file)


class Application(tk.Frame):
    """ GUI for DiskCleanupProject"""
    def __init__(self, master=None, **kw):
        tk.Frame.__init__(self, master)
        self.current_search = None
        self.previous_search = None
        self.folder_path_show = tk.StringVar()
        self.pack()
        self.create_widgets()

    def browse_button(self):
        if self.current_search is not None:
            self.previous_search = self.current_search
        self.current_search = filedialog.askdirectory()  # Buffer so we don't change "self.folder_path" value from None
        self.folder_path_show.set(self.current_search)

    def search_directories(self):
        self.found_empty_directories = []  # Needed to reset search results
        if self.current_search is None:
            print('No folder is chosen')
        elif self.current_search == self.previous_search:
            print(f"You've just searched this folder")
        else:
            self.list_of_results.delete(0, tk.END)

            for index, folder in enumerate(check_folder(self.current_search, self.found_empty_directories), 0):
                self.list_of_results.insert(index, folder)

            self.previous_search = self.current_search  # Prevents checking same folder

    def create_widgets(self):
        # self.canvas = tk.Canvas(scrollregion=(0, 0, 500, 500), height=200, width=200)
        # self.canvas.pack(side=tk.LEFT)

        self.exit = tk.Button(text="Exit", fg="red", command=self.quit)
        self.exit.pack(side=tk.RIGHT, anchor=tk.SE)

        self.choose_folder = tk.Button(text="Choose Folder", command=self.browse_button)
        self.choose_folder.pack(side=tk.BOTTOM, anchor=tk.S)

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
