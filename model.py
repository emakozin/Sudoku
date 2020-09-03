# program reši sudoku primerne stopnje brez uporabe "preizkušanja posameznih števk na vsakem polju"
# uporablja dva pristopa - eksplicitni in implicitni (bolje opisana spodaj)
# oba pristopa sta ljubiteljem sudokuja precej znana in jih v praksi zelo uporabljamo
# če sudokuja ni mogoče na tak način rešiti na program to javi in bi bilo treba uporabiti kakšen drug pristop, ker je sudoku prezahteven.
# Primer prezahtevnega sudokuja je pod 'zelo tezek'

# UPORABA:
# npr:
# s = Sudoku()
# s.generiraj('srednji')
# (s.implicitno())
# (s.eksplicitni())
# s.resi()
# za rešitev sudokuja ne rabimo posebej klicati s.implicitno() ali s.eksplicitno()

import json




class Sudoku:
        
    # program že na začetku naredi matriko v obliki sudokuja s samimi ničlami, tako lahko tudi sami ročno vpisujemo vrednosti
    # in rešimo svoj sudoku, če le ni prezahteven
    def  __init__(self):
        self.stevila = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.puzzle = []
        for i in range(9):
            row = []
            for j in range(9):
                row.append(0)
            self.puzzle.append(row)
        self.izpis = self.izpisi()
        
    
    def __repr__(self):
        return "Sudoko, napisan po vrsticah: {}".format(self.puzzle)

    # s funkcijo generiraj lahko določimo, kateri sudoku bi radi rešili (razlikujejo se po stopnjah)
    # če kličemo le s.generiraj() bo program prevzel, da mislimo lahek sudoku
    def generiraj(self, stopnja = 'lahek'):

        with open('primeri.json') as d:
                vsebina = d.read()
                sudoku = json.loads(vsebina)
        if stopnja == 'zelo težek':
            self.puzzle =  sudoku["zelo tezek"]          
        elif stopnja == 'težek':
            self.puzzle = sudoku["tezek"] 
        elif stopnja == 'srednji':
            self.puzzle = sudoku["srednji"]
        elif stopnja == 'lahek': 
            self.puzzle = sudoku["lahek"] 
        else:
            return False
           

    # funkcija izpisi() izpiše matriko v pravi obliki sudoku, da je bolj pregledno      
    def izpisi(self):
        print()
        for i, vrstica in enumerate(self.puzzle):
            for j, stevilo in enumerate(vrstica):
                if j % 3 == 0 and j < 8 and j > 0:
                    
                    print("|", end=' ')
                print(stevilo, end=' ')
            print()
            if (i-2) % 3 == 0 and i < 8:
                print("_____________________", end='')
                print()
        print()
        

    # s funkcijo vpisi_rocno lahhko posamezne števke vpišemo v naš sudoku
    # par(i, j) predstavlja mesto, ki ga hočemo izpolniti
    def vpisi_rocno(self, vrednost, i, j):
        self.puzzle[i][j] = vrednost

    # izbrisi() počisti navedeno polje in ga postavi na 0
    def izbrisi(self, i, j):
        self.puzzle[i][j] = 0


    # naslednje 3 funkcije so namenjene najdbi vseh števil, ki jih lahko v neko prazno polje vnesemo
    def preglej_vrstico(self, i):
        return self.stevila - set(self.puzzle[i])
    
    def preglej_stolpec(self, j):
        vsebujoca_stevila = []
        for i in range(9):
            vsebujoca_stevila.append(self.puzzle[i][j])
        return self.stevila - set(vsebujoca_stevila)

    def preglej_kvadrat(self, i, j):
        vsebujoca_stevila = []
        u, v = i // 3 , j // 3 
        for x in range(3):
            for y in range(3):
                vsebujoca_stevila.append(self.puzzle[3 * u + x][3 * v + y])
        return self.stevila - set(vsebujoca_stevila)

    # prejšnje funkcije združimo, da dobimo možna števila za vsako polje 
    # glede na omejitve, ki jih dobimo pri vrsticah, stolpcih in kvadratih
    # uporabimo presek in dobimo vsa možna števila, ki jih lahko v polje (i, j) vstavimo
    def dobi_mozna_stevila(self, i, j):
        mozna_stevila = set()
        if self.puzzle[i][j] == 0:
            mozna_st = list(self.preglej_kvadrat(i,j).intersection(self.preglej_vrstico(i)).intersection(self.preglej_stolpec(j)))   #TREBA POPRAVITI!!!L
        else: 
            mozna_st = [self.puzzle[i][j]]
        return mozna_st

    # EKSPLICITNI PRISTOP
    # program pregleduje prazna polja in možna števila, ki jih lahko vnesemo
    # če ima prazno polje le eno možno število, ga s tem številom zapolnimo

    def eksplicitno_resi(self, i ,j):
        if self.puzzle[i][j] == 0 and len(self.dobi_mozna_stevila(i, j)) == 1:
                self.puzzle[i][j] = self.dobi_mozna_stevila(i, j)[0]
   
    # zgornja funkcija izpolni dano prazno polje na eksplicitni način, če je mogoče
    # spodnja funkcija pa poizkusi rešiti celoten sudoku na ta način, če je mogoče
    # če se sudokuja na eksplicitni način ne da rešiti, nam predlaga uporabo implicitnega pristopa

    def eksplicitno(self):
        ponovitve = 0
        while not self.ali_je_ze_resen():
            ponovitve += 1
            if ponovitve > 5:
                return False
            for i in range(9):
                for j in range(9):
                    self.eksplicitno_resi(i, j)
        return self.ali_je_ze_resen()
    


    # IMPLICITNI PRISTOP:  
    # implicitni pristop se verjetno v vsakdanjem življenju največ uporablja
    # deluje na naslednjem principu:
    # če je neka števka možna le v enem polju v vrstici (oz. stolpcu ali kvadratu), jo v to polje vstavimo          

    # naslednje 3 vrstice za posamezno polje pregledajo, če ima lahko vneseno neko števku, ki v drugem polju v isti vrstici, stolpcu ali kvadratu ne sme biti. 
    # če za polje (i, j) to velja, ga zapolnimo s to števku, ki drugje v vrstici/stolpcu/kvadratu ne more biti   
    def implicitno_vrstica(self, i, j):
        vrst_mozna = []
        for y in range(9):
            if y == j:
                continue
            if self.puzzle[i][y] == 0:
                for vrednost in self.dobi_mozna_stevila(i, y):
                      vrst_mozna.append(vrednost)
        if len(set(self.dobi_mozna_stevila(i, j)) - set(vrst_mozna)) == 1:
            self.puzzle[i][j] = list(set(self.dobi_mozna_stevila(i, j)) - set(vrst_mozna))[0]
            
            
    def implicitno_stolpec(self, i, j):
        stolp_mozna = []
        for x in range(9):
            if x == i:
                continue
            if self.puzzle[x][j] == 0:
                for vrednost in self.dobi_mozna_stevila(x,j):
                    stolp_mozna.append(vrednost)
        if len(set(self.dobi_mozna_stevila(i, j)) - set(stolp_mozna)) == 1:
            self.puzzle[i][j] = list(set(self.dobi_mozna_stevila(i, j)) - set(stolp_mozna))[0]
            
        
    def implicitno_kvadrat(self, i, j):
        kvadrat_mozna = []
        u, v = i // 3 , j // 3 
        for x in range(3):
            for y in range(3):
                if self.puzzle[3 * u + x][3 * v + y] == 0:
                    if (i == 3 * u + x) and (j == 3 * v + y):
                        continue
                    for vrednost in self.dobi_mozna_stevila(3 * u + x, 3 * v + y):
                        kvadrat_mozna.append(vrednost)
        if len(set(self.dobi_mozna_stevila(i, j)) - set(kvadrat_mozna)) == 1:
            self.puzzle[i][j] = list(set(self.dobi_mozna_stevila(i, j)) - set(kvadrat_mozna))[0]
            

    # zgornje 3 funkcije združimo, da lahko pregledujemo polje glede na vse tri - vrstico, stolpec in kvadrat
    def implicitno_resi(self, i, j):
        if self.puzzle[i][j] == 0:
            mozna_st = self.dobi_mozna_stevila(i,j)
            self.implicitno_vrstica(i,j)
            self.implicitno_stolpec(i,j)
            self.implicitno_kvadrat(i,j)

    # naslednja funkcija pregleda cel sudoku in ga implicitno reši, če le lahko
    def implicitno(self):
        ponovitve = 0
        while not self.ali_je_ze_resen():
            ponovitve += 1
            if ponovitve > 5:
                return False
            for i in range(9):
                for j in range(9):
                    self.implicitno_resi(i,j)
        return True



    # spodnja funkcija pregleda ali je sudoku že rešen in nam če ni še rešen, pove, koliko polj je še praznih
    def ali_je_ze_resen(self):
        stevilo_praznih = 0
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] == 0:
                    stevilo_praznih += 1
        if stevilo_praznih == 0:
            return True
        else:
            return False

    # funkcija resi() združi oba pristopa in reši sudoku, če le lahko
    # če ga ne zna rešiti, nam pa to izpiše
    def resi(self):
        ponovitve = 0
        while ponovitve < 5:
            self.eksplicitno()
            self.implicitno()
            ponovitve += 1
        return self.ali_je_ze_resen()
            
        


    
      
       






            
            

                        
                        

