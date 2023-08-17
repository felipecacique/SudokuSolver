"Sudoku Solver"
"Student: Felipe Vital Cacique"

import numpy as np
import time

def SudokuToCsp(sudoku,csp,a=3):
    "Transform the sudoku matrix in the class Csp, for using in our AC_3 algorithm"
    n=int(a*a)      # size of the sudoku
    int_to_char = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B','C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                   'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U']
    "Define the domain for each variable x"
    for j in range(0,n):
        for i in range(0,n):
            csp.X.append((j,i))
            if sudoku[j][i] == '' or sudoku[j][i] == None:
                #csp.D[(j, i)] = list(range(1,n+1))  # create the domain d=[1,2,3, ... n] for each variable x
                csp.D[(j, i)] = [int_to_char[z] for z in list(range(1, n + 1))]     # create the domain d=[1,2,3, ... n]
                                                                                    # for each variable x
            else:
                csp.D[(j, i)] = [sudoku[j][i]]
            "Define the x neighbours being as units in the same line, column and box"
            neighbours = []
            neighboursColumn = []
            neighboursLine = []
            neighboursBox = []

            neighboursColumn = [(line,i) for line in range(0,n) if line!=j]         # all elements from same column
            csp.NC[(j, i)] = list(neighboursColumn)
            neighbours += neighboursColumn

            neighboursLine = [(j,column) for column in range(0, n) if column!=i]    # all elements from same line
            csp.NL[(j, i)] = list(neighboursLine)
            neighbours += neighboursLine

            neighboursBox = []
            for column in range(int(i/a)*a, int(i/a)*a + a):        # all elements from same box
                neighboursBox = neighboursBox + [(line,column) for line in range(int(j/a)*a, int(j/a)*a + a)]
            csp.NB[(j, i)] = list(neighboursBox)
            neighbours += neighboursBox

            neighbours = list(set(neighbours).difference(set([(j, i)])))
            csp.N[(j,i)] = list(neighbours)

class Csp:
    def __init__(self):
        self.X = []     # variables X=[xi1, xi2, ...]
        self.D = {}     # domains for each x
        self.N = {}     # neighbors N={xi1=[xj1, xj2, ...] xi2=...}

        self.NC = {}  # neighbors N={xi1=[xj1, xj2, ...] xi2=...}
        self.NL = {}  # neighbors N={xi1=[xj1, xj2, ...] xi2=...}
        self.NB = {}  # neighbors N={xi1=[xj1, xj2, ...] xi2=...}
    def SatisfyConstrain(self, x,y):
        "Return true if they satisfy the constrain"
        if x!=y:
            return True
        else:
            return False

def Select_Unassigned_Variable(assignment,csp, heuristics):
    "getting variable with more arc constrained first (smaller domain)"
    if heuristics == True:
        min=float('inf')
        for x in csp.X:
            if len(csp.D[x])!=1:
                if not (x in assignment):
                    if len(csp.D[x])<min:
                        min=len(csp.D[x])
                        x_min=x
        return x_min

    if heuristics == False:
        "getting variable at any order"
        for x in csp.X:
            if len(csp.D[x])!=1:
                if not(x in assignment):
                    return x
        return "error"

def Order_Domain_Values(var,assignment,csp,heuristics):
    "fist get values from domain with less conflicts"
    "count how many times each value from the domain repeat in the neighbor domains"
    if heuristics == True:
        counts={}
        for value in csp.D[var]:
            counts[value] = 0
        for xj in csp.N[var]:
            for value in csp.D[xj]:
                if value in counts:
                    counts[value]=counts[value]+1
        # for value,count in counts.values():
        #     if count>count_max:
        #         count_max=count

        sorted(counts.items(), key=lambda x: x[1])
        d=[]
        for value in counts:
            d.append(value)
        return reversed(d)

    if heuristics == False:
        return csp.D[var]

def IsComplete(assignment,csp):
    "Check weather we already solved the Sudoku completely"
    count=0
    for d in csp.D:
        if len(csp.D[d])>1:
            count += 1
    if len(assignment) == count:
        return True
    else: False

def NoConflict(value,assignment,csp,var, ac_3):
    "Check if there are any conflict with the value and any other from csp constrains"
    noconflict = True
    for xj in csp.N[var]:
        if xj in assignment:
            if not(csp.SatisfyConstrain(value, assignment[xj])):
                noconflict = False
    if ac_3 == False:
        "Necessary if we are using only backtracking (without AC-3)"
        for xj in csp.N[var]:
                if not(csp.SatisfyConstrain([value], csp.D[xj])):
                    noconflict = False
    return noconflict

def Backtrack_Search(csp, ac_3=False, heuristics=True):
    "Implementation of the backtrack algorithm."
    result = Backtrack({},csp,ac_3,heuristics)
    if result!= 'failure':
        for x in result:
            csp.D[x] = [result[x]]
    return Backtrack({},csp,ac_3,heuristics)

def Backtrack(assignment,csp,ac_3,heuristics):
    #The assignment has the structure: Assignment = {x:value}
    if IsComplete(assignment,csp):
        # print(assignment)
        return assignment
    var = Select_Unassigned_Variable(assignment,csp,heuristics)    # get the variable x in X that we haven't attribute value yet
                                                        # in order by the more arc constrained - who has smaller domain
                                                        # is selected fist (heuristic_1)
    for value in Order_Domain_Values(var,assignment,csp,heuristics):   # sorted by values from x domain with less conflicts between
                                                            # its neighbours (heuristic_2)
        assignment[var] = value  # add{var=value} to assignment
        if NoConflict(value,assignment,csp,var,ac_3):    # if there is no conflicts between the value and any other
                                                    # from csp constrains
            result=Backtrack(assignment,csp,ac_3,heuristics)    # at this point we have already assigned a value for x, and now we call
                                                # Backtrack recursivelly
            if result != 'failure':
                return result
        assignment.pop(var)     # remove{var=value} and inferences from assignment because there was a conflict
    return 'failure'

def CreateSudoku(a):
    n=a**2  # size
    sudoku=np.empty((n,n),dtype=object)
    for j in range(0,n):
        for i in range(0,n):
            sudoku[j][i]=None
    return sudoku

def ImportSudoku(n,level,id):
    sudoku=[]
    name = ("Sudoku_%ix%i_%s_%i - Sheet1.csv" % (n,n,level,id))
    f = open(name,'r')
    for line in f:
        sudoku_line = []
        for x in list(line.split(',')):
            sudoku_line.append(x.strip('\n'))
        sudoku.append(sudoku_line)
    sudoku = np.array(sudoku, dtype=object)
    sudoku.reshape((n, n))
    return sudoku




import queue
def AC_3(csp):
    "Arc-Consistency Algorithm AC-3"
    "csp = (X, D, C)"
    "queue contain all arcs = (Xi, Xj)"
    q=queue.Queue()
    for xi, xjs in csp.N.items():   # put to queue all binary arcs
        for xj in xjs:
            q.put((xi,xj))

    while not(q.empty()):
        xi, xj = q.get()
        if Revise(csp,xi,xj):
            if csp.D[xi] == []:
                return False
            for x in csp.N[xi]:
                if x != xj:
                    q.put((x,xi))
    return True

def Revise(csp,xi,xj):
    revised=False
    for x in csp.D[xi]:
        aux=False
        for y in csp.D[xj]:
            if csp.SatisfyConstrain(x, y) == True:
                aux=True
        if aux==False:
            del csp.D[xi][csp.D[xi].index(x)]
            revised = True
        # if filter(lambda y: csp.SatisfyConstrain(x,y)==True,csp.D[xj])==[]: # testa x todos os valores do dominio D[xj]
        #                                                                     # atraves da funcao, e retorna um vetor
        #                                                                     # correspondente (V) a D[xj]. Se V é vazio,
        #                                                                     # então nenhum valor de D[xi] satisfaz o
        #                                                                     # constain com x.
        #     del csp.D[xi][csp.D[xi].index(x)]
        #     revised=True
    return revised


def NumeroSozinhoOculto(csp, a=3):
    flag = False    # sinaliza se a funcao atuou solucionando alguma coisa, ou não
    dominio_size = a*a
    int_to_char = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B','C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                   'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U']
    dominio = int_to_char[1: dominio_size+1]
    for n in dominio:   # para cada valor pertencente ao dominio
        for i in range(0,dominio_size):  # percorro todas as colunas
            count = 0
            for j in range(0,dominio_size):  # percorro todas as linhas de cada coluna
                # if len(csp.D[(j,i)]) >1:    # se ainda nao tiver resolvido
                if n in csp.D[(j,i)]:   # verifica se o numero n está no dominio
                    count += 1          # se estiver, conte quantos n existem na "vizinhanca"
                    indx = (j,i)        # salva o par de index
            if count == 1:      # se contamos apenas um, n é um numero sozinho oculto. Então ele é a solucao para aquela posicao.
                if n in csp.D[indx]:    # só pra certificar que o n esta la
                    csp.D[indx] = [n]
                    flag = True

        for j in range(0,dominio_size):  # percorro todas as linhas
            count = 0
            for i in range(0,dominio_size):  # percorro todas as colunas de cada linha
                # if len(csp.D[(j,i)]) >1:    # se ainda nao tiver resolvido
                if n in csp.D[(j,i)]:   # verifica se o numero n está no dominio
                    count += 1          # se estiver, conte quantos n existem na "vizinhanca"
                    indx = (j,i)        # salva o par de index
            if count == 1:      # se contamos apenas um, n é um numero sozinho oculto. Então ele é a solucao para aquela posicao.
                if n in csp.D[indx]:    # só pra certificar que o n esta la
                    csp.D[indx] = [n]
                    flag = True


        for jb in range (0,a):
            for ib in range(0, a):
                count = 0
                # percorro todos os elementos de um determinado box
                for column in range(int(ib) * a, int(ib) * a + a):  # all elements from same box
                    for line in range(int(jb) * a, int(jb) * a + a): # neighbours in the same box
                        if n in csp.D[(line, column)]:  # verifica se o numero n está no dominio
                            count += 1  # se estiver, conte quantos n existem na "vizinhanca"
                            indx = (line, column)  # salva o par de index

                if count == 1:  # se contamos apenas um, n é um numero sozinho oculto. Então ele é a solucao para aquela posicao.
                    if n in csp.D[indx]:  # só pra certificar que o n esta la
                        csp.D[indx] = [n]
                        flag = True



        #     csp.NB[(j, i)] = list(neighboursBox)
        # for j in range(0, a * a):
        #     for i in range(0, a * a):
        #         for column in range(int(i / a) * a, int(i / a) * a + a):  # all elements from same box
        #             neighboursBox = [(line, column) for line in range(int(j / a) * a, int(j / a) * a + a)]
        #             csp.NB[(j, i)] = list(neighboursBox)

        # for j in range(0, a * a, a):
        #     for i in range(0, a * a, a):
        #         count = 0
        #         for neighbour in csp.NB[(j, i)]:
        #
        #             # if len(csp.D[neighbour]) > 1:  # se ainda nao tiver resolvido
        #             if n in csp.D[neighbour]:  # verifica se o numero n está no dominio
        #                 count += 1  # se estiver, conte quantos n existem na "vizinhanca"
        #                 indx = neighbour  # salva o par de index
        #         if count == 1:  # se contamos apenas um, n é um numero sozinho oculto. Então ele é a solucao para aquela posicao.
        #             if n in csp.D[indx]:  # só pra certificar que o n esta la
        #                 csp.D[indx] = [n]
        #                 flag = True

    return flag

def ParesSozinhos(csp, a=3, k=2):
    flag = False    # sinaliza se a funcao atuou solucionando alguma coisa, ou não

    def ParesSozinhos_In(csp, neighbours, k=2):
        flag = False
        for key, item in csp.D.items():
            if len(item) == k:  # encontreum um par de tamanho k
                                # se houver k pares de tamanho k com os mesmos elementos 'e' na coluna, remova 'e' dos outros vizinhos
                count = 1
                for v_key in neighbours[key]:    # para cada vizinhos pertencente a mesma coluna de key
                    if item == csp.D[v_key] and key != v_key:    # se o vizinho tiver os mesmo k elementos
                        count +=1

                if count == k:  # se tenho k elemntos de tamanho k
                    for v_key in neighbours[key]:   # para cada vizinho
                        if item != csp.D[v_key]:    # que nao seja um dos que eu contei anteriormente
                            for element in item:    # vou tirar os elemetos do dominio item dos outros vizinhos
                                if element in csp.D[v_key]: # se o vizinho tiver esse elemento, ele sera removido do vizinho
                                    # print("asda",csp.D[v_key])
                                    csp.D[v_key].remove(element)    # removo o elemento
                                    # print("asda2", csp.D[v_key])
                                    flag=True
                                    # print ('dkajhdkafdfsfsdfs')
        return flag

    flag = flag or ParesSozinhos_In(csp,csp.NC,k=2)
    flag = flag or ParesSozinhos_In(csp,csp.NL,k=2)
    flag = flag or ParesSozinhos_In(csp,csp.NB,k=2)

    # flag = flag or ParesSozinhos_In(csp,csp.NC,k=3)
    # flag = flag or ParesSozinhos_In(csp,csp.NL,k=3)
    # flag = flag or ParesSozinhos_In(csp,csp.NB,k=3)
    #
    # flag = flag or ParesSozinhos_In(csp,csp.NC,k=4)
    # flag = flag or ParesSozinhos_In(csp,csp.NL,k=4)
    # flag = flag or ParesSozinhos_In(csp,csp.NB,k=4)
    #
    # flag = flag or ParesSozinhos_In(csp,csp.NC,k=5)
    # flag = flag or ParesSozinhos_In(csp,csp.NL,k=5)
    # flag = flag or ParesSozinhos_In(csp,csp.NB,k=5)

    for k in range(2, a*a):
        flag = flag or ParesSozinhos_In(csp,csp.NC,k=k)
        flag = flag or ParesSozinhos_In(csp,csp.NL,k=k)
        flag = flag or ParesSozinhos_In(csp,csp.NB,k=k)

    return flag



def SubsetEscondido(csp, a=3):
    flag = False    # sinaliza se a funcao atuou solucionando alguma coisa, ou não

    for i in range(0,a*a):  # percorro todas as colunas
        count = 0
        dct = {}
        for j in range(0,a*a):  # percorro todas as linhas de cada coluna
            for n in csp.D[(j,i)]:   # para cada valor do dominio
                if n in dct:
                    dct[n].append( (j,i) )
                else:
                    dct[n]=[(j, i)]

        if dct != {}:
            for key, item in dct.items():
                for key2, item2 in dct.items(): # combinacao de todos os valores
                    if key != key2 and len(item)==2 and item == item2:
                        # remover elementos in item from the neighbours
                        # print(dct)
                        # print(key, key2)
                        for j in range(0, a * a):   # percoro todos a linhas da coluna
                            if item[0] != (j,i) and item[1] != (j,i):  # que nao seja um dos que eu contei anteriormente
                                # print("balblabla")
                                # print(key,key2, csp.D[(j,i)])
                                if key in csp.D[(j,i)]:
                                    # removo key do dominio
                                    csp.D[(j,i)].remove(key)
                                    flag = True
                                    # print("hdakjhdkjsahgdfgdfgdfgdfgdfgdfgfd")
                                if key2 in csp.D[(j,i)]:
                                    # removo key do dominio
                                    csp.D[(j,i)].remove(key2)
                                    flag =True
                                    # print("hdakjhdkjsahgdfgdfgdfgdfgdfgdfgfd")




    for j in range(0,a*a):  # percorro todas as colunas
        count = 0
        dct = {}
        for i in range(0,a*a):  # percorro todas as linhas de cada coluna
            for n in csp.D[(j,i)]:   # para cada valor do dominio
                if n in dct:
                    dct[n].append( (j,i) )
                else:
                    dct[n]=[(j, i)]

        if dct != {}:
            for key, item in dct.items():
                for key2, item2 in dct.items(): # combinacao de todos os valores
                    if key != key2 and len(item)==2 and item == item2:
                        # remover elementos in item from the neighbours
                        # print(dct)
                        # print(key, key2)
                        for i in range(0, a * a):   # percoro todos a linhas da coluna
                            if item[0] != (j,i) and item[1] != (j,i):  # que nao seja um dos que eu contei anteriormente
                                # print("balblabla")
                                # print(key, key2, csp.D[(j,i)])
                                if key in csp.D[(j,i)]:
                                    # removo key do dominio
                                    csp.D[(j,i)].remove(key)
                                    flag = True
                                    # print("hdakjhdkjsahgdfgdfgdfgdfgdfgdfgfd")
                                if key2 in csp.D[(j,i)]:
                                    # removo key do dominio
                                    csp.D[(j,i)].remove(key2)
                                    flag =True
                                    # print("hdakjhdkjsahgdfgdfgdfgdfgdfgdfgfd")

    return flag



def Block_Column_Row_Interaction(csp, a=3):
    flagA = False    # sinaliza se a funcao atuou solucionando alguma coisa, ou não
    dominio_size = a*a
    int_to_char = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B','C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                   'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U']
    dominio = int_to_char[1: dominio_size+1]
    for element in dominio:   # para cada valor pertencente ao dominio
        vizited_nc = set([])
        for key, nc in csp.NC.items():
            if not key in vizited_nc:
                nc_set = set(nc + [key])
                vizited_nc.update(nc_set)
                vizited_nb = set([])
                for key2, nb in csp.NB.items():
                    if not key2 in vizited_nc:
                        # check if the sets overlap
                        nb_set = set(nb + [key2])
                        vizited_nb.update(nb_set)
                        intersection = nc_set.intersection(nb_set)
                        if int(len(intersection))>0: # conjuntos overlap
                            flag = False
                            for neighbour in intersection:  # o elemento faz parte da intersecao
                                if element in csp.D[neighbour]:
                                    flag = True
                                    break
                            if flag == True:

                                difference_nb = nb_set.difference(nc_set)
                                # print('nb', nb_set)
                                # print('nc', nc_set)
                                # print('nd', difference_nb)
                                flag2 = False
                                for neighbour in difference_nb:      # se element nao pertencer a difference_nb, entao element nao pertence a difference_nc
                                    if element in csp.D[neighbour]:
                                        flag2 = True
                                        break
                                if flag2 == False: # element nao pertence a difference_nb
                                    # remover element de difference_nc
                                    difference_nc = nc_set.difference(nb_set)
                                    for neighbour in difference_nc:
                                        if element in csp.D[neighbour]:
                                            if len(csp.D[neighbour])>1:
                                                # print(csp.D[neighbour])
                                                csp.D[neighbour].remove(element)
                                                flagA = True
                                                # print((csp.D[neighbour]))
    for element in dominio:   # para cada valor pertencente ao dominio
        vizited_nc = set([])
        for key, nc in csp.NL.items():
            if not key in vizited_nc:
                nc_set = set(nc + [key])
                vizited_nc.update(nc_set)
                vizited_nb = set([])
                for key2, nb in csp.NB.items():
                    if not key2 in vizited_nc:
                        # check if the sets overlap
                        nb_set = set(nb + [key2])
                        vizited_nb.update(nb_set)
                        # print("nb", len(nb_set))
                        # print("nc", len(nc_set))
                        intersection = nc_set.intersection(nb_set)
                        if int(len(intersection))>0: # conjuntos overlap
                            flag = False
                            for neighbour in intersection:  # o elemento faz parte da intersecao
                                if element in csp.D[neighbour]:
                                    flag = True
                                    break
                            if flag == True:

                                difference_nb = nb_set.difference(nc_set)
                                # print('nb', nb_set)
                                # print('nc', nc_set)
                                # print('nd', difference_nb)
                                flag2 = False
                                for neighbour in difference_nb:      # se element nao pertencer a difference_nb, entao element nao pertence a difference_nc
                                    if element in csp.D[neighbour]:
                                        flag2 = True
                                        break
                                if flag2 == False: # element nao pertence a difference_nb
                                    # remover element de difference_nc
                                    difference_nc = nc_set.difference(nb_set)
                                    for neighbour in difference_nc:
                                        if element in csp.D[neighbour]:
                                            if len(csp.D[neighbour])>1:
                                                # print(csp.D[neighbour])
                                                csp.D[neighbour].remove(element)
                                                flagA = True
                                                # print((csp.D[neighbour]))
    return flagA


import numpy as np
import random
import copy
def Solve_by_GeneticAlgorthm(csp, m_rate = .08, r = .8):

    def Evaluate(population, csp):
        def count_n_conflicts(individual,csp):
            csp2 = individual[1]
            n_conflics = 0
            for key, item in csp2.D.items():
                for neighbour_key in csp.N[key]:
                    if item == csp2.D[neighbour_key] and key != neighbour_key:
                        n_conflics+=1
                    if len(item)>1 or len(csp2.D[neighbour_key])>1:
                        #   n_conflics += 1
                        print("sadasdsadasda")


            individual[0] = n_conflics
            # print(n_conflics)
            return

        for individual in population:
            count_n_conflicts(individual, csp)
        return True

    def Mutation(bests, csp, m_rate):
        m_rate = m_rate
        for i in range(0, len(bests), 1):
            for key, item in bests[i][1].D.items():
                if len(csp.D[key]) > 1:
                    # exchange character in the same line
                    if random.random() < m_rate:
                        # chose random key in same line
                        rand = random.random()
                        if rand < 1.33:
                            key_n = random.choice(csp.NL[key])
                        elif rand < .66:
                            key_n = random.choice(csp.NC[key])
                        else:
                            key_n = random.choice(csp.NB[key])

                        if len(csp.D[key_n]) > 1:
                            if bests[i][1].D[key][-1] in csp.D[key_n]:
                                # if bests[i][1].D[key_n][-1] in csp.D[key]:
                                # i can safely exchange cuz the value pertence aos dos dominios
                                aux = bests[i][1].D[key]
                                bests[i][1].D[key] = bests[i][1].D[key_n]
                                bests[i][1].D[key_n] = aux
        return bests


    def Create_Individual(csp):
        csp_copy = Csp()
        csp_copy.D = copy.deepcopy(csp.D)
        # for key, domain in csp_copy.D.items():
        #     if len(domain) > 1:
        #         csp_copy.D[key] = [random.choice(domain)]



        # relaxo as restricoes, mantendo apenas nas linhas
        csp_copy.X = copy.deepcopy(csp.X)

        rand=random.random()
        if rand<1.33:
            csp_copy.N = copy.deepcopy(csp.NL)
        # elif rand<.66:
        #     csp_copy.N = copy.deepcopy(csp.NB)
        # else:
        #     csp_copy.N = copy.deepcopy(csp.NC)

        Backtrack_Search(csp_copy, ac_3=True, heuristics=False)
        csp_copy.X = {}
        csp_copy.N = {}



        return csp_copy

    def Create_Population(csp, n):
        population = []
        for i in range(0,n):
            individual = Create_Individual(csp)
            population.append([ 10 ,individual])


            population=Mutation(population, csp, .8)

        return population

    def New_Generation(population,m_rate,r, csp):
        def Crossolver(bests, csp, m_rate):
            if len(bests)%2 ==0 or len(bests)%2 ==1:
                # print("yeh")
                # if random.random()<.5:
                random.shuffle(bests)
                # m_rate = random.random() / 10
                visited = set([])
                visitedC = set([])
                for i in range(0, len(bests)-1,2-1):

                    if random.random()<.70:
                        for key, item in bests[i][1].D.items():
                            "Crossover"
                            rand = random.random()
                            # if rand<0.01:
                            #     aux = copy.copy(bests[i][1].D[key])
                            #     bests[i][1].D[key] =  bests[i+1][1].D[key]
                            #     bests[i + 1][1].D[key] = aux
                            # # elif rand>1-0.3:
                            # #     aux = copy.copy(bests[i+1][1].D[key])
                            # #     bests[i+1][1].D[key] =  bests[i][1].D[key]
                            # #     bests[i][1].D[key] = aux

                            neighbours = csp.NL[key] + [key]
                            if not key in visited:
                                if rand < 0.25:
                                    for key_n in neighbours:
                                        aux = bests[i][1].D[key_n]
                                        bests[i][1].D[key_n] = bests[i+1][1].D[key_n]
                                        bests[i+1][1].D[key_n] = aux
                            visited.update(set(neighbours))

                            # neighbours = csp.NC[key] + [key]
                            # if not key in visitedC:
                            #     if rand < 0.5:
                            #         for key_n in neighbours:
                            #             aux = bests[i][1].D[key_n]
                            #             bests[i][1].D[key_n] = bests[i+1][1].D[key_n]
                            #             bests[i+1][1].D[key_n] = aux
                            # visitedC.update(set(neighbours))



                            m_rate = 0.005
                            # m_rate = random.random()/10
                            "Mutation"
                            # if len(csp.D[key]) > 1:
                            #     if random.random() < m_rate :
                            #         bests[i][1].D[key] = [random.choice(csp.D[key])]
                            #     if random.random() < m_rate :
                            #         bests[i+1][1].D[key] = [random.choice(csp.D[key])]

                m_rate = 0.3
                for i in range(0, len(bests), 2):
                    for key, item in bests[i][1].D.items():
                        if len(csp.D[key]) > 1:
                            # exchange character in the same line
                            if random.random() < m_rate:
                                #chose random key in same line
                                rand = random.random()
                                if rand < 1.33:
                                    key_n = random.choice(csp.NL[key])
                                elif rand < .66:
                                    key_n = random.choice(csp.NC[key])
                                else:
                                    key_n = random.choice(csp.NB[key])

                                if len(csp.D[key_n]) > 1:
                                    if bests[i][1].D[key][-1] in csp.D[key_n]:
                                        #     if bests[i][1].D[key_n][-1] in csp.D[key]:
                                        # i can safely exchange cuz the value pertence aos dos dominios
                                        aux = bests[i][1].D[key]
                                        bests[i][1].D[key] = bests[i][1].D[key_n]
                                        bests[i][1].D[key_n] = aux


            return bests

        # def Mutation(children, m_rate):



        n=len(population)
        population =  sorted(population, key=lambda tup: (tup[0]))
        print(population[0][0])
        # for i in range(0,len(population)):
        #     print(population[i][0])

        bests = population[0:int(r*n)]
        # bests[-1] = population[-1]
        # bests[-2] = population[-2]
        # bests[-1] = random.choice(population[int(r*n):])
        # bests[-2] = random.choice(population[int(r*n):])
        very_bests = copy.deepcopy(population[0:int((1-r)*n)])
        # random.shuffle(population)
        # very_bests = very_bests  + copy.deepcopy(population[0:int(((1-r)/2)*n)])
        children = Crossolver(bests, csp, m_rate)
        # children = Mutation(children, m_rate, csp)
        children = children + very_bests

        # p=0
        # for i in range(len(children), len(population)):
        #     # if p < 2:
        #     #     # children.append(population[-(p+1)])
        #     #     children.append(random.choice(population))
        #     if p<30:
        #         children.append(population[p])
        #     else:
        #         children.append(random.choice(population))
        #     p += 1
        # children = random.shuffle(children)
        return children

    def Complete(csp,population):
        for individual in population:
            if individual[0] == 0:
                csp.D = copy.deepcopy(individual[1].D)
                return True
        return False


    population = Create_Population(csp, n=24)
    Evaluate(population, csp)
    while 1:
        if Complete(csp,population) == True: return True
        population = New_Generation(population,m_rate,r, csp)
        Evaluate(population,csp)
        # print(a)








if __name__=="__main__":
    n=None
    sudoku=[    [n,n,3,  n,2,n,  6,n,n],
                [9,n,n,  3,n,5,  n,n,1],
                [n,n,1,  8,n,6,  4,n,n],

                [n,n,8,  1,n,2,  9,n,n],
                [7,n,n,  n,n,n,  n,n,8],
                [n,n,6,  7,n,8,  2,n,n],

                [n,n,2,  6,n,9,  5,n,n],
                [8,n,n,  2,n,3,  n,n,9],
                [n,n,5,  n,1,n,  3,n,n]     ]   #book


    sudoku=[    [5,8,6,  n,7,2,  n,n,n],
                [n,n,n,  9,n,1,  6,n,n],
                [n,n,n,  6,n,n,  n,n,n],

                [n,n,7,  n,n,n,  n,n,n],
                [9,n,2,  n,1,n,  3,n,5],
                [n,n,5,  n,9,n,  n,n,n],

                [n,9,n,  n,4,n,  n,n,8],
                [n,n,3,  5,n,n,  n,6,n],
                [n,n,n,  n,2,n,  4,7,n]     ]   #matheus

    a, n, level, id = 5, 25, "Hard", 1
    a, n, level, id = 3, 9, "Hard", 1

    a, n, level, id = 3, 9, "Very_Easy", 1
    a, n, level, id = 3, 9, "Easy", 1
    a, n, level, id = 3, 9, "Medium", 1
    a, n, level, id = 3, 9, "Hard", 1
    a, n, level, id = 3, 9, "Very_Hard", 1
    # # # # #
    a, n, level, id = 4, 16, "Very_Easy", 1
    a, n, level, id = 4, 16, "Easy", 1
    a, n, level, id = 4, 16, "Medium", 1
    a, n, level, id = 4, 16, "Hard", 2
    a, n, level, id = 4, 16, "Very_Hard", 1
    # # # # # # #
    a, n, level, id = 5, 25, "Very_Easy", 3
    a, n, level, id = 5, 25, "Easy", 1
    a, n, level, id = 5, 25, "Medium", 2
    a, n, level, id = 5, 25, "Hard", 1
    a, n, level, id = 5, 25, "Very_Hard", 1

    sudoku=ImportSudoku(n,level,id)
    #print(sudoku)

    # sudoku=np.array(sudoku, dtype=object)
    # sudoku.reshape((9,9))
    # print(sudoku)


    # sudoku=CreateSudoku(a)
    # print(sudoku)

    csp=Csp()
    SudokuToCsp(sudoku,csp,a)

    inicio=time.clock()

    "Backtracking without heuristics"
    # Backtrack_Search(csp, ac_3=False, heuristics = False)

    "Backtracking with heuristics"
    # Backtrack_Search(csp, ac_3=False, heuristics = True)

    "AC_3 + Backtracking"
    def n_domain_complete(csp):
        count=0
        domain_size = 0
        for key, item in csp.D.items():
            if len(item) == 1:
                count += 1
            if len(item) != 1:
                domain_size += len(item)
        return count, domain_size

    # AC_3(csp)
    # print("n_domain:", n_domain_complete(csp))
    # Backtrack_Search(csp, ac_3=True, heuristics = False)

    "AC_3 + Heuristics + Backtracking"


    def AC_3_and_Heuristics(csp):
        ni = n_domain_complete(csp)
        print('AC_3 ', "Initial: ", ni)
        while 1:
            print("")

            inicio = time.clock()
            flag_AC_3=AC_3(csp)
            if(flag_AC_3) == False: return False
            n = n_domain_complete(csp)
            print('AC_3 ', flag_AC_3, n, time.clock()-inicio)
            if(n[1]==0):
                return True

            inicio = time.clock()
            flag_NumeroSozinhoOculto = NumeroSozinhoOculto(csp, a=a)
            # if (flag_NumeroSozinhoOculto) == False: return False
            n2=n_domain_complete(csp)
            print('NSO ', flag_NumeroSozinhoOculto, n2, time.clock()-inicio)
            if(n2[1]==0):
                return True

            inicio = time.clock()
            flag_ParesSozinhos = ParesSozinhos(csp, a=a)
            n3 = n_domain_complete(csp)
            print('PS', flag_ParesSozinhos, n3, time.clock()-inicio)
            if(n3[1]==0):
                return True

            inicio = time.clock()
            flag_SubsetEscondido = SubsetEscondido(csp, a=a)
            n4 = n_domain_complete(csp)
            print('SE', flag_SubsetEscondido, n4, time.clock()-inicio)
            if(n4[1]==0):
                return True

            if n3 == n and flag_ParesSozinhos == False:
                inicio = time.clock()
                flag_Block_Column_Row_Interaction = Block_Column_Row_Interaction(csp, a=a)
                n5 = n_domain_complete(csp)
                print('BCRI', flag_Block_Column_Row_Interaction, n5, time.clock()-inicio)



                if n5 == n and flag_Block_Column_Row_Interaction == False:
                    return True



    print(AC_3_and_Heuristics(csp))
    print(Backtrack_Search(csp, ac_3=True, heuristics = False))
    print(" ")
    print(n_domain_complete(csp))


    "AC_3 + Heuristics + GeneticAlgorithm"
    # print(AC_3_and_Heuristics(csp))
    # Solve_by_GeneticAlgorthm(csp, m_rate=.08, r=.75)
    # print(n_domain_complete(csp))


    print("Time:", time.clock()-inicio)

    def PrintSolvedSudoku(csp,sudoku):
        for x in csp.X:
            sudoku[x[0]][x[1]]=csp.D[x][-1]
        #print(sudoku)
        for row in sudoku:
            for x in row:
                if x=='':
                    print('_', end=' ')
                else: print(x,end=' ')
            print('', end='\n')

    PrintSolvedSudoku(csp,sudoku)

