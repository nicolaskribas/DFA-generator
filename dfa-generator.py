import csv
AFND = []
states = []
final = []
transitions = []
state = 'S'
realState = 'S'
changes = {'S':'S'}
epsilons = {}
#novo valor -> changes['A'] = 'M'
#if 'A' in changes:
#   temp = changes['A']
def newLine():
    AFND.append([[] for _ in range(len(transitions))])
    final.append(False)

def newCollumn():
    for i in range(len(AFND)):
        AFND[i].append([])

def addRG2(line):
    rule = line.split('::=')[0].strip(' ')[1]
    productions = line.strip('\n').split(' ::= ')[1].split(' | ')
    print(rule)
    print(productions)
    if rule not in changes:
        changes[rule] = nextState()
        states.append(state)
        newLine()
        rule = state
    else:
        rule = changes[rule]
    for production in productions:
        if production[0] not in transitions and production[0] != 'ε' and '<' not in production[0]:
            newCollumn()
            transitions.append(production[0])
        elif production[0] == '<':
            if 'ε' not in transitions:
                newCollumn()
                transitions.append('ε')
            if production[1] not in changes:
                changes[production[1]] = nextState()
                states.append(state)
                newLine()
            AFND[states.index(rule)][transitions.index('ε')].append(changes[production[1]])
            continue;
        if '<' in production:
            if production[2] not in changes:
                changes[production[2]] = nextState()
                states.append(state)
                newLine()
            AFND[states.index(rule)][transitions.index(production[0])].append(changes[production[2]])
        elif 'ε' in production:
            final[states.index(rule)] = True
        elif '<' not in production:
            if 'X' not in states:
                states.append('X')
            newLine()
            AFND[states.index(rule)][transitions.index(production[0])].append('X')
            final[states.index('X')] = True

def nextState():
    global state
    global realState
    if realState == 'S':
        realState = 'A'
    elif realState == 'R':
        realState = 'U'
    elif realState == 'X':
        realState = 'Y'
    else:
        realState = chr(ord(realState)+1)
    state = realState
    return state

def addToken(line):
    global state
    state = 'S'
    for symbol in line:
        if '\n' != symbol:
            if symbol not in transitions:
                newCollumn()
                transitions.append(symbol)
            newLine()
            AFND[states.index(state)][transitions.index(symbol)].append(nextState())
            states.append(state)
    final[states.index(state)] = True

def removeEpsilon():
    if 'ε' in transitions:
        for state in states:
            if state in epsilons:
                epsilons[state] += AFND[states.index(state)][transitions.index('ε')]
            else:
                epsilons[state] = AFND[states.index(state)][transitions.index('ε')]
        mudanca = True
        while mudanca:
            mudanca = False
            for state in epsilons:
                for transition in epsilons[state]:
                    if transition in epsilons:
                        for transition2 in epsilons[transition]:
                            if transition2 not in epsilons[state] and transition2 != state:
                                epsilons[state] += transition2
                                mudanca = True

        print(epsilons)
        for state in epsilons:
            for transition in epsilons[state]:
                for i in range(len(AFND[states.index(transition)])):
                    for production in AFND[states.index(transition)][i]:
                        if production not in AFND[states.index(state)][i]:
                            AFND[states.index(state)][i].append(production)

def determiniza():
    mud = True
    str2 = ''
    while mud:
        mud = False
        for state in states:
            for tr in transitions:
                reg = AFND[states.index(state)][transitions.index(tr)]

                if len(reg) > 1 :
                    print(states.index(state))
                    print(transitions.index(tr))
                    reg.sort()
                    print(reg)
                    for i in range(len(reg)):
                        str1 = reg[i]
                        print('str1'+str1)
                        str2 = str2 + str1
                        print('str2'+str2)
                    if str2 not in states:
                        states.append(str2)
                        newLine()
                        for valor in reg:
                            for i in range(len(transitions)):
                                for production in AFND[states.index(valor)][i]:
                                    if production not in AFND[states.index(str2)][i]:
                                        AFND[states.index(str2)][i].append(production)
                        mud = True
                    str2 = ''





def main():

    file = open("input.txt","r")
    states.append('S')  #Adiciona o estado inicial S
    AFND.append([]) #Adiciona linha na tabela
    final.append(False)


    for line in file:
        if line[0] == '<':  #Caso seja um Gramatica Regular ela é adicionada ao Automato
            addRG2(line)
        else:
            addToken(line)  #Caso seja um Token ele é adicionado ao Automato
    removeEpsilon()
    print(transitions)  #Print AFND final
    for i in range(len(states)):    #Print AFND final
        print(final[i],states[i],AFND[i])    #Print AFND final
    print(changes)
    determiniza()
    print(transitions)  #Print AFND final
    for i in range(len(states)):    #Print AFND final
        print(final[i],states[i],AFND[i])    #Print AFND final
    print(changes)



    file.close()
    with open('output.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(AFND)
    file.close()
main()
