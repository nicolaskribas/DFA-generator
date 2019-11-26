class FiniteAutomaton(object):

    def __init__(self):
        self.alphabet = []
        self.number_of_states = 1
        self.states_mapping = {'S': 0}
        self.finite_automaton = {}
        self.final = []

    def add_to_mapping(self, rule_name):
        if rule_name not in self.states_mapping:
            self.states_mapping[rule_name] = self.number_of_states
            self.number_of_states = self.number_of_states + 1

    def add_regular_grammar(self, regular_grammar):
        regular_grammar = regular_grammar.split('::=')
        rule_name = regular_grammar[0].strip(' <>')

        self.add_to_mapping(rule_name)

        productions = regular_grammar[1].split('|')
        for production in productions:
            # symbol = production.strip(' ').split('<')[0]
            # state = production.split('<'[])



    def add_to_alphabet(self, symbol):
        if symbol not in self.alphabet:
            self.alphabet.append(symbol)

    def create_transition(self, state, symbol):
        self.finite_automaton[state][symbol].append(self.number_of_states)
        self.number_of_states = self.number_of_states + 1
        return self.number_of_states

    def add_token(self, token):
        state = 0
        for symbol in token:
            self.add_to_alphabet(symbol)
            state = self.create_transition(state, symbol)
        self.final.append(state)



    def remove_epsilon_transitions(self):
        pass

    def determinize(self):
        pass

    def remove_inaccessible(self):
        pass

    def remove_dead(self):
        pass
