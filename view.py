import tkinter as tk
from tkinter import *


class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.title('Tictactoe')
        self.controller = controller

        # instruction variables
        self.player_var = tk.StringVar()
        self.opponent_var = tk.StringVar()
        self.label_var = tk.StringVar()
        self.wait = tk.BooleanVar()

        # start and option menu variables
        self.player_option = None
        self.opponent_option = None
        self.start_button = None

        # 9 button variables
        self.b1_button = tk.StringVar()
        self.b2_button = tk.StringVar()
        self.b3_button = tk.StringVar()

        self.b4_button = tk.StringVar()
        self.b5_button = tk.StringVar()
        self.b6_button = tk.StringVar()

        self.b7_button = tk.StringVar()
        self.b8_button = tk.StringVar()
        self.b9_button = tk.StringVar()

        # Button list
        self.button_list_var = [self.b1_button, self.b2_button, self.b3_button,
                                self.b4_button, self.b5_button, self.b6_button,
                                self.b7_button, self.b8_button, self.b9_button]

        self.btn_list = []
        self.three_btn_list = []

        # Layout
        self._make_main_frame()
        self._make_player_options()
        self._make_label()
        self._make_start_button()
        self._make_buttons()
        self._make_exit_button()

    def main(self):
        self.mainloop()

    def _make_main_frame(self):
        self.main_frm = tk.Frame(self)
        self.main_frm.pack(padx=10, pady=10)

    def _make_player_options(self):
        frm = tk.Frame(self.main_frm)
        frm.pack()
        self.player_var.set('I am X')
        self.opponent_var.set('Human')
        self.player_option = tk.OptionMenu(frm, self.player_var, 'I am X', 'I am O')
        self.opponent_option = tk.OptionMenu(frm, self.opponent_var, 'Human', 'AI Easy', 'AI Medium', 'AI Hard')
        self.player_option.pack(side=LEFT, padx=40)
        self.opponent_option.pack(side=LEFT, padx=40)

    def _make_label(self):
        frm = tk.Frame(self.main_frm)
        frm.pack()
        self.label_var.set('Choose your player and opponent, then click start')
        instruction_label = Label(frm, textvariable=self.label_var, pady=5)
        instruction_label.pack()

    def _make_start_button(self):
        frm = tk.Frame(self.main_frm)
        frm.pack()
        self.start_button = Button(frm, text='Start', width=9,
                                   command=lambda: self.controller.start_btn_click())
        self.three_btn_list = [self.start_button, self.player_option, self.opponent_option]
        self.start_button.pack(pady=10)

    def _make_buttons(self):
        outer_frm = tk.Frame(self.main_frm)
        outer_frm.pack()

        frm = tk.Frame(outer_frm)
        frm.pack()

        buttons_in_row = 0
        max_buttons_per_row = 3
        for btn_var in self.button_list_var:
            if buttons_in_row == max_buttons_per_row:
                frm = tk.Frame(outer_frm)
                frm.pack()
                buttons_in_row = 0

            bttn = tk.Button(frm, textvariable=btn_var, font=('MS Outlook', 20),
                             height=3, width=6, state=DISABLED,
                             command=(lambda btton=btn_var: self.controller.btn_click(btton)))

            self.btn_list.append(bttn)
            bttn.pack(side=LEFT)

            buttons_in_row += 1

    def _make_exit_button(self):
        frm = tk.Frame(self.main_frm)
        frm.pack()
        exit_button = Button(frm, text='Exit', width=9,
                             command=lambda: self.controller.exit_btn_click())
        exit_button.pack(pady=10)
