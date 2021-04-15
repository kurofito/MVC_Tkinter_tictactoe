from random import choice as choose


class Model:
    def __init__(self):
        self.game_board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.board_index = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        self.input = None
        self.player_sign = None
        self.opponent_sign = None

        self.result = None
        self.state = None
        self.breaker = True

        self.label_var = None
        self.btn_index = None
        self.btn_var = None
        self.btn_var_list = None
        self.waiting = None

        self.bttn_list = None
        self.three_btn_list = None

        self.command_one = {'I am X Human': {2: self.human_x, 3: self.human_o},
                            'I am O Human': {2: self.human_x, 3: self.human_o},
                            'I am X AI Easy': {2: self.human_x, 3: self.easy_ai_o},
                            'I am O AI Easy': {2: self.easy_ai_x, 3: self.human_o}}

    def assign_signs(self):
        sign_dict = {'I am X Human': {'ai': 'O', 'user': 'X'}, 'I am X AI Easy': {'user': 'X', 'ai': 'O'},
                     'I am X AI Medium': {'user': 'X', 'ai': 'O'}, 'I am X AI Hard': {'user': 'X', 'ai': 'O'},
                     'I am O Human': {'ai': 'O', 'user': 'X'}, 'I am O AI Easy': {'ai': 'O', 'user': 'X'},
                     'I am O AI Medium': {'ai': 'O', 'user': 'X'}, 'I am O AI Hard': {'ai': 'O', 'user': 'X'}}

        opponent_sign, self.opponent_sign = sign_dict[self.input]['ai'], sign_dict[self.input]['ai']
        player_sign, self.player_sign = sign_dict[self.input]['user'], sign_dict[self.input]['user']

        return opponent_sign, player_sign

    def switch_btn_state(self, state):
        if state["state"] == 'normal':
            state["state"] = 'disabled'
        else:
            state["state"] = 'normal'

    def disable_btn(self):
        for btn in self.bttn_list:
            self.switch_btn_state(btn)

    def enable_btn(self):
        for btn in self.bttn_list:
            self.switch_btn_state(btn)

    def switch_start_state(self):
        self.switch_btn_state(self.three_btn_list[0])

    def switch_options_state(self):
        self.switch_btn_state(self.three_btn_list[1])
        self.switch_btn_state(self.three_btn_list[2])

    def make_btns_var_empty(self):
        for btn in self.btn_var_list:
            btn.set('')

    def checker(self, sign):
        while True:
            self.btn_waiting()
            space_check = self.game_board[self.btn_index]
            if space_check == 'X' or space_check == 'O':
                self.turn_on_waiting()
            else:
                self.game_board[self.btn_index] = sign
                self.board_index.remove(self.btn_index)
                self.btn_var.set(sign)
                self.turn_on_waiting()
                break

    def turn_off_waiting(self):
        self.waiting.set(False)

    def turn_on_waiting(self):
        self.waiting.set(True)

    def btn_waiting(self):
        self.bttn_list[0].wait_variable(self.waiting)

    def reset(self):
        self.game_board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.board_index = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    def game_state(self):
        matrix = [self.game_board[:3], self.game_board[3:6], self.game_board[6:]]
        transposed = [[matrix[j][i] for j in range(3)] for i in range(3)]
        diagonal = [[matrix[0][0], matrix[1][1], matrix[2][2]], [matrix[0][2], matrix[1][1], matrix[2][0]]]
        return matrix + transposed + diagonal

    def parser(self):
        self.state = self.game_state()
        self.result = ['null' if ' ' not in x else x for x in self.state]
        checker = [x for dat in self.state for x in dat]
        rd = [''.join(x) for x in self.state]
        return rd, checker

    def win_check(self):
        parsed = self.parser()
        if 'XXX' in parsed[0]:
            self.label_var.set('X wins, click start to play again')
            self.reset()
            self.end_game()
        elif 'OOO' in parsed[0]:
            self.label_var.set('O wins, click start to play again')
            self.reset()
            self.end_game()
        elif ' ' not in parsed[1]:
            self.label_var.set('Draw, click start to play again')
            self.reset()
            self.end_game()

    def end_game(self):
        self.breaker = False

    def human_move(self, sign, index, info):
        self.label_var.set(info)
        self.checker(sign[index])
        self.win_check()

    def human_x(self):
        self.human_move(self.assign_signs(), 1, 'Player X turn')

    def human_o(self):
        self.human_move(self.assign_signs(), 0, 'Player O turn')

    def ai(self, x):
        self.disable_btn()
        ai = choose(self.board_index)
        self.btn_var_list[ai].set(x)
        self.game_board[ai] = x
        self.board_index.remove(ai)
        self.win_check()
        self.enable_btn()

    def easy_ai_x(self):
        self.ai(self.player_sign)

    def easy_ai_o(self):
        self.ai(self.opponent_sign)

    def game_playing(self, dict_name, x, o):
        self.breaker = True
        while self.breaker:
            dict_name[self.input][x]()
            if not self.breaker:
                break
            else:
                dict_name[self.input][o]()
        self.switch_states_in_game()

    def switch_states_in_game(self):
        self.switch_start_state()
        self.switch_options_state()
        self.disable_btn()

    def playing(self):
        self.game_playing(self.command_one, 2, 3)


class Medium(Model):
    def __init__(self):
        super().__init__()
        self.player_pos = None
        self.opponent_pos = None

        self.id = {0: {0: 0, 1: 1, 2: 2}, 1: {3: 3, 4: 4, 5: 5},
                   2: {6: 6, 7: 7, 8: 8}, 3: {0: 0, 3: 3, 6: 6},
                   4: {1: 1, 4: 4, 7: 7}, 5: {2: 2, 5: 5, 8: 8},
                   6: {0: 0, 4: 4, 8: 8}, 7: {6: 6, 4: 4, 2: 2}}

        self.command_two = {'I am X Human': {1: self.playing}, 'I am O AI Easy': {1: self.playing},
                            'I am X AI Easy': {1: self.playing}, 'I am O Human': {1: self.playing},
                            'I am X AI Medium': {1: self.mplaying, 2: self.human_x, 3: self.medium_ai_o},
                            'I am O AI Medium': {1: self.mplaying, 2: self.medium_ai_x, 3: self.human_o}}

    def game_analyzer(self):
        super().parser()
        player_counter = [x.count(self.player_sign) for x in self.result]  # analyzer
        opponent_counter = [x.count(self.opponent_sign) for x in self.result]
        self.player_pos = [index for index in range(len(player_counter)) if player_counter[index] == 2]
        self.opponent_pos = [index for index in range(len(opponent_counter)) if opponent_counter[index] == 2]

    def medium_move(self, position, sign):
        for i in list(self.id[position[0]].values()):
            self.board_index.remove(i) if self.game_board[i] == ' ' else None
            if self.game_board[i] == ' ':
                self.game_board[i] = sign
                self.btn_var_list[i].set(sign)
        self.win_check()

    def executing_move(self, my_position, my_sign, enemy_position):
        if my_position and ' ' in self.result[my_position[0]]:
            self.medium_move(my_position, my_sign)
        elif enemy_position and ' ' in self.result[enemy_position[0]]:
            self.medium_move(enemy_position, my_sign)
        else:
            self.ai(my_sign)

    def medium_ai_x(self):
        self.game_analyzer()
        self.executing_move(self.player_pos, self.player_sign, self.opponent_pos)

    def medium_ai_o(self):
        self.game_analyzer()
        self.executing_move(self.opponent_pos, self.opponent_sign, self.player_pos)

    def mplaying(self):
        self.game_playing(self.command_two, 2, 3)


class Hard(Medium):
    def __init__(self):
        Medium.__init__(self)
        self.command_three = {'I am X Human': {1: self.playing}, 'I am O AI Easy': {1: self.playing},
                              'I am X AI Easy': {1: self.playing}, 'I am O Human': {1: self.playing},
                              'I am X AI Medium': {1: self.mplaying}, 'I am O AI Medium': {1: self.mplaying},
                              'I am X AI Hard': {1: self.hplaying, 2: self.human_x, 3: self.hard_ai_o},
                              'I am O AI Hard': {1: self.hplaying, 2: self.hard_ai_x, 3: self.human_o}}

    def empty_index(self):
        return [index for index in range(len(self.game_board)) if self.game_board[index] == ' ']

    def winning(self, maxer, miner):
        rd = [''.join(x) for x in self.game_state()]
        if maxer * 3 in rd:
            return 10
        elif miner * 3 in rd:
            return -10
        else:
            return 0

    def minimax(self, depth, isMax, playerX, playerO, alpha, beta):
        spots = self.empty_index()
        score = self.winning(playerX, playerO)

        # terminal state
        if score == 10:
            return score - depth  # making AI smarter by subtracting and adding depth for max and min player
        elif score == -10:
            return score + depth
        elif len(spots) == 0:  # checking for empty spots
            return 0

        if isMax:
            best = -1000
            for i in range(len(self.game_board)):
                if self.game_board[i] == ' ':
                    self.game_board[i] = playerX
                    best = max(best, self.minimax(depth + 1, not isMax, playerX, playerO, alpha, beta))
                    self.game_board[i] = ' '
                    if best >= beta:
                        return best
                    if best > alpha:
                        alpha = best
            return best
        else:
            best = 1000
            for i in range(len(self.game_board)):
                if self.game_board[i] == ' ':
                    self.game_board[i] = playerO
                    best = min(best, self.minimax(depth + 1, not isMax, playerX, playerO, alpha, beta))
                    self.game_board[i] = ' '
                    if best <= alpha:
                        return best
                    if best < beta:
                        beta = best
            return best

    def bestmove(self, xplayer, oplayer, isMax, alpha, beta):
        best = None
        bestval = -1000
        for i in range(len(self.game_board)):
            if self.game_board[i] == ' ':
                self.game_board[i] = xplayer
                moveval = self.minimax(0, isMax, xplayer, oplayer, alpha, beta)
                self.game_board[i] = ' '
                if moveval > bestval:
                    best = i
                    bestval = moveval
        return best

    def hard_move(self, my_sign, enemy_sign):
        i = self.bestmove(my_sign, enemy_sign, False, -1000, 1000)
        self.game_board[i] = my_sign
        self.board_index.remove(i)
        self.btn_var_list[i].set(my_sign)
        self.win_check()

    def hard_ai_x(self):
        self.hard_move(self.player_sign, self.opponent_sign)

    def hard_ai_o(self):
        self.hard_move(self.opponent_sign, self.player_sign)

    def hplaying(self):
        self.game_playing(self.command_three, 2, 3)

    def start_game(self):
        self.command_three[self.input][1]()
