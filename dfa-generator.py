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
        if production[0] not in transitions and production[0] != 'ε':
            newCollumn()
            transitions.append(production[0])
        if '<' in production:
            if production[2] not in changes:
                changes[production[2]] = nextState()
                states.append(state)
                newLine()
            AFND[states.index(rule)][transitions.index(production[0])].append(changes[production[2]])
        elif 'ε' in production:
            final[states.index(rule)] = True


def addRG(line):
    aux = line.split('|')
    regra = aux[0][1:2]
    aux[0] = aux[0].split('=')
    aux[0] = aux[0][1]
    if regra not in states:
        states.append(regra)
        newLine()
    else:
        i=0
        #verificar se a regra é S ou não, se ela não for deve colocar ela no dicionario atribuindo a ela um novo valor que o nextState() vai encontrar
    for valor in aux:
        valor = valor.strip(' ')
        if '<' not in valor:
            #atribuir a regra como sendo final
            if valor[0:1] not in transitions:
                newCollumn()
                transitions.append(valor[0:1])
                AFND[states.index(regra)][transitions.index(valor[0:1])].append('-')
            else:
                AFND[states.index(regra)][transitions.index(valor[0:1])].append('-')
        else:
            #verificar se o valor da letra maiuscula ja esta sendo usado para colocar ela no dicionario e colocar outro valor para ela.
            if valor[0:1] not in transitions:
                newCollumn()
                transitions.append(valor[0:1])
                AFND[states.index(regra)][transitions.index(valor[0:1])].append(valor[2:3])
            else:
                AFND[states.index(regra)][transitions.index(valor[0:1])].append(valor[2:3])

def nextState():
    global state
    global realState
    if realState == 'S':
        realState = 'A'
    elif realState == 'R':
        realState = 'U'
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
            if state in espsilons:
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
                            if transition2 not in epsilons[state]:
                                epsilons[state] += transition2
                                mudanca = True

        for state in epsilons:
            for transition in epsilons[state]:
                for i in range(len(AFND[states.index(transition)])):
                    for production in AFND[states.index(transition)][i]:
                        if production not in AFND[states.index(state)][i]:
                            AFND[states.index(state)][i].append(production)

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

    print(transitions)  #Print AFND final
    for i in range(len(states)):    #Print AFND final
        print(final[i],states[i],AFND[i])    #Print AFND final
    print(changes)

    #removeEpsilon()

    file.close()
    with open('output.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(AFND)
    file.close()
main()
