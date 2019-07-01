AFND = []
states = []
transitions = []
def newCollumn():
    for i in range(len(AFND)):
        AFND[i].append([])

def addRG(line):
    print("Devia adicionar '"+line+"'ao automato");
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
