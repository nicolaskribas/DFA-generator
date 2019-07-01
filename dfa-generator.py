AFND = []

def addRG(line):
    print("Devia adicionar '"+line+"'ao automato");
    #implementar

def addToken(line):
    for symbol in line:
        i =1
    print("Adicionando '"+line+"'ao automato")



def main():
    file = open("text.txt","r")
    for line in file:
        if line[0] == '<':  #Caso seja um Gramatica Regular ela é adicionada ao Automato
            addRG(line)
        else:
            addToken(line)  #Caso seja um Token ele é adicionado ao Automato

    file.close()
    AFND.append([])
    AFND.append([])
    AFND[0].append('A')
    AFND[1].append('B')
    print(AFND[1][0])
main()
