"""UI for Course List"""
import tkinter as tk
from tkinter import ttk
from Database import MovieDB
from graphing import MovieGraph
from functools import reduce


class CourseUI(tk.Tk):
    """Graphical UI to view and modify your courselist."""

    def __init__(self, course_list: CourseList):
        """Initialize and show the user interface.

        :param course_list: reference to a CourseList object
        """
        super().__init__()
        self.course_list = course_list
        self.options = {'font': ('Arial', 16), 'foreground': 'black'}
        self.registrar = Registrar()

        self.course_id = []
        self.course_info = []
        self.sum_credits = 0

        self.store_text = course_list.get_all_courses()

        self.find_courses_info()
        self.init_components()

    def find_courses_info(self):
        self.all_courses = list(self.registrar.get_courses())

        for x in self.all_courses:
            self.course_id.append(x.course_id)
            self.course_info.extend([x.name, x.credits, x.difficulty])


    def init_components(self):
        self.title("Course App")
        self.configure(background='grey')

        self.top_frame = tk.Frame(self)
        self.course_label = tk.Label(self.top_frame, text="Course", background='grey', **self.options)
        self.course_info_current = tk.StringVar()
        self.course_infor_text = tk.Label(self.top_frame, textvariable=self.course_info_current, width=50, **self.options)
        self.create_combo_box()
        self.create_button()

        self.create_mid_frame()

        self.create_bot_frame()

        self.pack_components()


    def create_bot_frame(self):
        self.bot_frame = tk.Frame(self,padx=5, pady=5)
        self.textbox_var = tk.StringVar()
        self.textbox = tk.Text(self.bot_frame, padx=5, pady=5, **self.options, height=3)
        self.scrollbar = ttk.Scrollbar(self.bot_frame, orient='vertical', command=self.textbox.yview)
        self.textbox['yscrollcommand'] = self.scrollbar
        self.textbox['state'] = 'disabled'

    def create_mid_frame(self):
        self.mid_frame = tk.Frame(self, bg='light grey', padx=5, pady=5)
        self.total_label = tk.Label(self.mid_frame, text='Total', **self.options, bg='light grey')
        self.total_credits_var = tk.StringVar()
        self.total_credits_var.set("0")
        self.credits = tk.Label(self.mid_frame, textvariable=self.total_credits_var, **self.options, bg='light grey')
        self.end = tk.Label(self.mid_frame, text='credits', **self.options, background='light grey')

    def create_combo_box(self):
        self.course_combo_var = tk.StringVar()
        self.course_combo_box = ttk.Combobox(self.top_frame, textvariable=self.course_combo_var,
                                             values=self.course_id)
        self.course_combo_box['state'] = 'readonly'
        self.course_combo_box.bind('<<ComboboxSelected>>', self.handle_combobox)

    def textbox_update(self, id):
        self.textbox['state'] = 'normal'
        self.textbox.replace(0.0, tk.END, '')
        info = self.course_list.get_course(self.course_combo_var.get())
        for items in self.store_text:
            self.textbox.insert(0.0, f"{str(items.course_id):6} {str(items.name)} ({str(items.credits)}{')':40.40}  Difficulty: {str(items.difficulty):>5} \n", f"Difficulty: {str(items.difficulty)} \n")

        self.textbox['state'] = 'disabled'
        self.total_credits_var.set(str(self.course_list.get_credits()))

    def enroll_handler(self):
        if self.course_list.get_course(self.course_combo_var.get()) is None:
            self.course_list.add_course(self.course_combo_var.get())
            self.textbox_update(self.course_combo_var.get())
            self.credits['text'] = self.course_list.get_credits()
            self.enroll_button['state'] = 'disabled'
            self.course_combo_var.set('')
            self.course_info_current.set('')

        else:
            self.course_list.remove_course(self.course_combo_var.get())
            self.textbox_update(self.course_combo_var.get())
            self.credits['text'] = self.course_list.get_credits()
            self.enroll_button['state'] = 'disabled'
            self.course_combo_var.set('')
            self.course_info_current.set('')


    def create_button(self):
        self.enroll_button = tk.Button(self.top_frame, text="ENROLL", command=self.enroll_handler)
        self.enroll_button.configure(padx=5, pady=5, **self.options)
        self.enroll_button['state'] = 'disabled'

    def handle_combobox(self, *args):
        self.enroll_button['state'] = 'normal'
        info = self.registrar.get_course(self.course_combo_var.get())
        string = f"{info.name} ({info.credits}) Difficulty={info.difficulty}"
        self.course_info_current.set(string)
        if self.registrar.get_course(self.course_combo_var.get()) in self.store_text:
            self.enroll_button['text'] = "REMOVE"
        else:
            self.enroll_button['text'] = 'ENROLL'

    def pack_components(self):
        padding = {'padx': 5, 'pady':5}

        # Top
        self.enroll_button.pack(side=tk.RIGHT, **padding)
        self.course_label.pack(side=tk.LEFT, **padding)
        self.course_combo_box.pack(side=tk.LEFT, **padding)
        self.course_infor_text.pack(side=tk.LEFT, **padding)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Mid
        self.mid_frame.pack(fill=tk.BOTH,expand=True, **padding)
        self.total_label.pack(side=tk.LEFT, **padding)
        self.credits.pack(side=tk.LEFT, **padding)
        self.end.pack(side=tk.LEFT, **padding)

        #bot
        self.bot_frame.pack(fill=tk.X, expand=True)
        self.textbox.pack(side=tk.LEFT, **padding)
        self.scrollbar.pack(side=tk.RIGHT)

    def run(self):
        self.mainloop()
