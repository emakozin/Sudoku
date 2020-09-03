from model import Sudoku

sudoku = Sudoku()

def pozdrav():
    ime = input( 'Kako ti je ime? ')
    print('Živjo, {}'.format(ime))


# Pomožne funkcije za vnos

def izberi(mozni_odgovori):
    for indeks, odgovor in enumerate(mozni_odgovori):
        print('{}) {}'.format(indeks + 1, odgovor))
    izbira = int(input('> '))
    return izbira - 1

def izberi_stopnjo(stopnje):
    for indeks, odgovor in enumerate(stopnje):
        print('{}) {}'.format(indeks + 1, odgovor))
    stopnja = input('> ')
    return int(float(stopnja)) - 1

def izberi_nacin(nacini):
    for indeks, odgovor in enumerate(nacini):
        print('{}) {}'.format(indeks + 1, odgovor))
    nacin = int(input('> '))
    return nacin - 1

def izberi_vrednost(vrednosti):
    for indeks, odgovor in enumerate(vrednosti):
        print('{}) {}'.format(indeks + 1, odgovor))
    vrednost = input('> ')
    return int(float(vrednost)) - 1

def izberi_vrstico(vrstice):
    for indeks, odgovor in enumerate(vrstice):
        print('{}) {}'.format(indeks + 1, odgovor))
    vrstica = input('> ')
    return int(float(vrstica)) - 1

def izberi_stolpec(stolpci):
    for indeks, odgovor in enumerate(stolpci):
        print('{}) {}'.format(indeks + 1, odgovor))
    stolpec = input('> ')
    return int(float(stolpec)) - 1



def napaka(niz):
    print('\033[1;91m' + niz + '\033[0m')

def uspeh(niz):
    print('\033[1;92m' + niz + '\033[0m')

# Glavni meni

def meni():
    while True:
        print('Ali bi rešil(a) sudoku? ')
        izbira = izberi(['ja', 'ne'])
        if izbira == 0:
            izberi_sudoku()
            resuj_sudoku()
        elif izbira == 1:
            print('Škoda, morda pa kdaj drugič. ')
            return False
        else:
            napaka('Izberi 1 ali 2. ')
            meni()

# Funkcije 

def izberi_sudoku():
    print('Kakšno stopnjo sudokuja si želiš rešiti? ')
    stopnja = izberi_stopnjo(['lahek', 'srednji', 'težek', 'zelo težek', 'prazen'])
    if stopnja == 0:
        sud = sudoku.generiraj('lahek')    
    elif stopnja == 1:
        sud = sudoku.generiraj('srednji')
    elif stopnja == 2:
        sud = sudoku.generiraj('težek')
    elif stopnja == 3:
        sud = sudoku.generiraj('zelo težek')
    elif stopnja == 4:
        sud = sudoku.puzzle
        print('Sam vpiši svoj sudoku.')
        vpisi_sudoku()
    else:
        napaka('Izberi, kakšen sudoku želiš! Pritisni številko med 1 in 5.')
        izberi_sudoku()
    sudoku.izpisi()

def vpisi_sudoku():
    print('Izberi vrednost in polje, ki ga želiš napolniti')
    print('Vrednost:')
    vrednost = izberi_vrednost([i for i in range(1,10)])
    print('V vrstici:')
    vrstica = izberi_vrstico([i for i in range(1, 10)])
    print('V stolpcu: ')
    stolpec = izberi_stolpec([i for i in range(1, 10)])
    sudoku.vpisi_rocno(vrednost + 1, vrstica, stolpec)
    vpisi_se_eno_polje()


def vpisi_se_eno_polje():
    print('Ali želiš vpisati še kakšno polje? ')
    izbira = izberi(['ja', 'ne'])
    if izbira == 0:
        vpisi_sudoku()
    elif izbira == 1:
            resuj_sudoku()
    else:
        napaka('Izberi 1 ali 2. ')
        vpisi_se_eno_polje()


def resuj_sudoku():
    print('Na kakšen način bi ga rad rešil? ')
    nacin = izberi_nacin(['eksplicitno', 'implicitno', 'oboje', 'dodaj novo številko', 'izberi drug sudoku'])
    if nacin == 0:
        sudoku.eksplicitno()
        if sudoku.ali_je_ze_resen():
            uspeh('Rešili smo sudoku!')
            return sudoku.izpisi()
        else:
            print('Poskusi še kak drug način. ')
            resuj_sudoku()
    elif nacin == 1:
        sudoku.implicitno()
        if sudoku.ali_je_ze_resen():
            uspeh('Rešili smo sudoku!')
            return sudoku.izpisi()
        else:
            print('Poskusi še kak drug način. ')
            resuj_sudoku()
    elif nacin == 2:
        sudoku.resi()
        if sudoku.resi():
            uspeh('Rešili smo sudoku!')
        else:
            napaka('Sudokuja ne znamo rešiti, izberi lažjo stopnjo ali pa dodaj še kakšno polje. ')
            resuj_sudoku()
    elif nacin == 3:
        vpisi_se_eno_polje()
    elif nacin == 4:
        izberi_sudoku()
    else:
        napaka('Izberi 1, 2 ali 3.')
        resuj_sudoku()
    sudoku.izpisi()
    
# main

def main():
    pozdrav()
    meni()


main()