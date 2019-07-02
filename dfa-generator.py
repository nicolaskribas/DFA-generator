import csv
AFND = []
states = []
final = []
transitions = []
state = 'S'
realState = 'S'
changes = {}
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

def main():

    file = open("input.txt","r")
    states.append('S')  #Adiciona o estado inicial S
    AFND.append([]) #Adiciona linha na tabela
    final.append(False)


    for line in file:
        if line[0] == '<':  #Caso seja um Gramatica Regular ela é adicionada ao Automato
            #addRG(line)
            i=0
        else:
            addToken(line)  #Caso seja um Token ele é adicionado ao Automato
    print(transitions)  #Print AFND final
    for i in range(len(states)):    #Print AFND final
        print(final[i],states[i],AFND[i])    #Print AFND final
    file.close()
    with open('output.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(AFND)
    file.close()
main()
