from model import Hard
from view import View


class Controller:
    def __init__(self):
        self.model = Hard()
        self.view = View(self)
        self.transfer = True

    def main(self):
        self.view.main()

    def btn_click(self, btn): # think of this like an input
        var_list = self.model.btn_var_list
        self.model.btn_index = var_list.index(btn)
        self.model.btn_var = btn
        self.model.turn_off_waiting()

    def start_btn_click(self):
        self.transfer_data()
        self.model.make_btns_var_empty()
        self.input_and_assign_data()
        self.switch_states()
        self.model.start_game()

    def transfer_data(self):
        if self.transfer:
            self.model.waiting = self.view.wait
            self.model.bttn_list = self.view.btn_list
            self.model.three_btn_list = self.view.three_btn_list
            self.model.label_var = self.view.label_var
            self.model.btn_var_list = self.view.button_list_var
            self.transfer = False

    def input_and_assign_data(self):
        a = self.view.player_var.get()
        b = self.view.opponent_var.get()
        self.model.input = a + ' ' + b
        self.model.assign_signs()

    def switch_states(self):
        self.model.enable_btn()
        self.model.switch_options_state()
        self.model.switch_start_state()
        self.model.turn_on_waiting()

    def exit_btn_click(self):
        self.view.destroy()


if __name__ == '__main__':
    tictactoe = Controller()
    tictactoe.main()
