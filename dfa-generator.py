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

def addRG(line):
    rule = line.split('::=')[0].strip(' ')[1]
    productions = line.strip('\n').split(' ::= ')[1].split(' | ')
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

        for state in epsilons:
            for transition in epsilons[state]:
                for i in range(len(AFND[states.index(transition)])):
                    for production in AFND[states.index(transition)][i]:
                        if production not in AFND[states.index(state)][i]:
                            AFND[states.index(state)][i].append(production)
                if final[states.index(transition)]:
                    final[states.index(state)] = True
        for state in AFND:
            state.pop(transitions.index('ε'))
        transitions.pop(transitions.index('ε'))

def determiniza():
    mud = True
    str2 = ''
    while mud:
        mud = False
        for state in states:
            for tr in transitions:
                reg = AFND[states.index(state)][transitions.index(tr)]

                if len(reg) > 1 :
                    reg.sort()
                    for i in range(len(reg)):
                        str1 = reg[i]
                        str2 = str2 + str1
                    if str2 not in states:
                        states.append(str2)
                        newLine()
                        for valor in reg:
                            if final[states.index(valor)]:
                                final[states.index(str2)] = True
                            for i in range(len(transitions)):
                                for production in AFND[states.index(valor)][i]:
                                    if production not in AFND[states.index(str2)][i]:
                                        AFND[states.index(str2)][i].append(production)

                        mud = True
                    AFND[states.index(state)][transitions.index(tr)] = [str2]
                    str2 = ''
def buscaAtingiveis(inicial):
    accessible = [inicial]
    for state in accessible:
        if state in states:
            for production in AFND[states.index(state)]:
                if len(production) == 1:
                    if production[0] not in accessible:
                        accessible.append(production[0])
    return accessible

def removeID():
    accessible = buscaAtingiveis('S')
    for state in states:
        if state not in accessible:
            print('Removendo estado'+state)
            AFND.pop(states.index(state))
            final.pop(states.index(state))
            states.pop(states.index(state))
    #até aqui remove os inalcancaveis
    print('inalcancaveis')
    # for state in states:
    #     morto = True
    #     accessible = buscaAtingiveis(state)
    #     for stateAtingivel in accessible:
    #         if final[states.index(stateAtingivel)]:
    #             morto = False
    #             break
    #     if morto:
    #         print('Removendo estado morto'+state)
    #         AFND.pop(states.index(state))
    #         final.pop(states.index(state))
    #         states.pop(states.index(state))
    #remove os mortos



def main():

    file = open("input.txt","r")
    states.append('S')  #Adiciona o estado inicial S
    AFND.append([]) #Adiciona linha na tabela
    final.append(False)


    for line in file:
        if line[0] == '<':  #Caso seja um Gramatica Regular ela é adicionada ao Automato
            addRG(line)
        else:
            addToken(line)  #Caso seja um Token ele é adicionado ao Automato
    print("TABELA MONTADA")
    print(transitions)  #Print AFND final
    for i in range(len(states)):    #Print AFND final
        print(final[i],states[i],AFND[i])    #Print AFND final
    print(changes)
    removeEpsilon()
    print("\n\nTABELA SEM EPSILONS")
    print(transitions)  #Print AFND final
    for i in range(len(states)):    #Print AFND final
        print(final[i],states[i],AFND[i])    #Print AFND final
    print(changes)
    determiniza()
    print("\n\nTABELA DETERMINIZADA")
    print(transitions)  #Print AFND final
    for i in range(len(states)):    #Print AFND final
        print(final[i],states[i],AFND[i])    #Print AFND final
    print(changes)
    removeID()
    print("\n\nTABELA SEM INALCANSAVEIS")
    for i in range(len(states)):    #Print AFND final
        print(final[i],states[i],AFND[i])    #Print AFND final
    print(changes)

    file.close()
    with open('output.csv', 'w') as file:
        writer = csv.writer(file)
        linha = ['']
        linha += transitions
        writer.writerow(linha)
        for i in range(len(states)):
            if final[i]:
                linha = ['*'+states[i]]
            else:
                linha = [states[i]]
            linha += AFND[i]
            writer.writerow(linha)
    file.close()
main()
