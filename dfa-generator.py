AFND = []
states = []
transitions = []
def newCollumn():
    for i in range(len(AFND)):
        AFND[i].append([])

def addRG(line):
    print("Devia adicionar '"+line+"'ao automato");
    aux = line.split('|')
    regra = aux[0][1:2]
    aux[0] = aux[0].split('=')
    aux[0] = aux[0][1]
    if regra not in states:
        states.append(regra)
    for valor in aux:
        valor = valor.strip(' ')
        print(valor)
        #separado cada parte da regra.
    #implementar

def addToken(line):
    state = 'S'
    for symbol in line:
        if symbol not in transitions and '\n' not in symbol:
            newCollumn()
            transitions.append(symbol)

    print("Adicionando '"+line+"'ao automato")



def main():
    file = open("text.txt","r")
    states.append('S')  #Adiciona o estado inicial S
    AFND.append([]) #Adiciona linha na tabela
    for line in file:
        if line[0] == '<':  #Caso seja um Gramatica Regular ela é adicionada ao Automato
            addRG(line)
        else:
            addToken(line)  #Caso seja um Token ele é adicionado ao Automato
    print(states)
    print(transitions)
    print(AFND)
    file.close()
main()
