import time

import pygame
import sys

ADANCIME_MAX = 3


def elem_identice(lista):
    if (all(elem == lista[0] for elem in lista[1:])):
        return lista[0] if lista[0] != Joc.GOL else False
    return False


class Joc:
    """
	Clasa care defineste jocul. Se va schimba de la un joc la altul.
	"""
    NR_COLOANE = None
    NR_LINII = None
    j1_protectii = None
    j2_protectii = None
    j1_bombe = None
    j2_bombe = None
    j1_mutari = None
    j2_mutari = None
    JMIN = None
    JMAX = None
    GOL = '#'

    @classmethod
    def initializeaza(cls, matr, display, NR_LINII, NR_COLOANE, dim_celula=100):
        cls.display = display
        cls.matr = matr
        cls.j2_protectii = 0
        cls.j1_protectii = 0
        cls.j1_mutari = 0
        cls.j2_mutari = 0
        cls.j1_bombe = []
        cls.j2_bombe = []
        cls.dim_celula = dim_celula
        cls.p1_img = pygame.image.load('p1.png')
        cls.p1_img = pygame.transform.scale(cls.p1_img, (dim_celula, dim_celula))
        cls.p2_img = pygame.image.load('p2.png')
        cls.p2_img = pygame.transform.scale(cls.p2_img, (dim_celula, dim_celula))
        cls.ba_img = pygame.image.load('BA.png')
        cls.ba_img = pygame.transform.scale(cls.ba_img, (dim_celula, dim_celula))
        cls.bi_img = pygame.image.load('BI.png')
        cls.bi_img = pygame.transform.scale(cls.bi_img, (dim_celula, dim_celula))
        cls.ba2_img = pygame.image.load('BA2.png')
        cls.ba2_img = pygame.transform.scale(cls.ba2_img, (dim_celula, dim_celula))
        cls.bi2_img = pygame.image.load('BI2.png')
        cls.bi2_img = pygame.transform.scale(cls.bi2_img, (dim_celula, dim_celula))
        cls.prot_img = pygame.image.load("protectie.png")
        cls.prot_img = pygame.transform.scale(cls.prot_img, (dim_celula, dim_celula))
        cls.celuleGrid = []  # este lista cu patratelele din grid
        cls.NR_LINII = NR_LINII
        cls.NR_COLOANE = NR_COLOANE
        for linie in range(NR_LINII):
            for coloana in range(NR_COLOANE):
                patr = pygame.Rect(coloana * (dim_celula + 1), linie * (dim_celula + 1), dim_celula, dim_celula)
                cls.celuleGrid.append(patr)

    def deseneaza_grid(self, marcaj=None, mapa=None):  # tabla de exemplu este ["#","x","#","0",......]
        if mapa != None:
            self.matr = mapa
        for ind in range(self.__class__.NR_COLOANE * self.__class__.NR_LINII):
            linie = ind // self.__class__.NR_COLOANE  # // inseamna div
            coloana = ind % self.__class__.NR_COLOANE
            if marcaj == ind:
                # daca am o patratica selectata, o desenez cu galben
                culoare = (255, 255, 0)
            elif self.matr[linie][coloana] == "#":
                culoare = (105, 105, 105)
            else:
                culoare = (255, 255, 255)
            pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[ind])  # alb = (255,255,255)
            if self.matr[linie][coloana] == '1':
                self.__class__.display.blit(self.__class__.p1_img, (
                    coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
            elif self.matr[linie][coloana] == '2':
                self.__class__.display.blit(self.__class__.p2_img, (
                    coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
            elif self.matr[linie][coloana] == 'b':
                self.__class__.display.blit(self.__class__.bi_img, (
                    coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
            elif self.matr[linie][coloana] == 'a':
                self.__class__.display.blit(self.__class__.ba_img, (
                    coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
            elif self.matr[linie][coloana] == 'q':
                self.__class__.display.blit(self.__class__.ba2_img, (
                    coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
            elif self.matr[linie][coloana] == 'w':
                self.__class__.display.blit(self.__class__.bi2_img, (
                    coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
            elif self.matr[linie][coloana] == 'p':
                self.__class__.display.blit(self.__class__.prot_img, (
                    coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
        pygame.display.flip()  # obligatoriu pentru a actualiza interfata (desenul)

        pygame.display.update()

        pygame.display.flip()  # obligatoriu pentru a actualiza interfata (desenul)

        pygame.display.update()

    def __init__(self, matr=None, NR_LINII=None, NR_COLOANE=None):
        self.ultima_mutare = None
        # ii vom da tabla mereu deoarece aceasta este luata din fisier si nu avem cum sa o initializam
        self.matr = matr
        self.NR_LINII = NR_LINII
        self.NR_COLOANE = NR_COLOANE

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def final(self):
        rez = (elem_identice(self.matr[0:3])
               or elem_identice(self.matr[3:6])
               or elem_identice(self.matr[6:9])
               or elem_identice(self.matr[0:9:3])
               or elem_identice(self.matr[1:9:3])
               or elem_identice(self.matr[2:9:3])
               or elem_identice(self.matr[0:9:4])
               or elem_identice(self.matr[2:8:2]))
        if (rez):
            return rez
        elif self.__class__.GOL not in self.matr:
            return 'remiza'
        else:
            return False

    def mutari(self, jucator_opus):
        l_mutari = []
        for i in range(len(self.matr)):
            if self.matr[i] == self.__class__.GOL:
                matr_tabla_noua = list(self.matr)
                matr_tabla_noua[i] = jucator_opus
                l_mutari.append(Joc(matr_tabla_noua))
        return l_mutari

    # linie deschisa inseamna linie pe care jucatorul mai poate forma o configuratie castigatoare
    # practic e o linie fara simboluri ale jucatorului opus
    def linie_deschisa(self, lista, jucator):
        jo = self.jucator_opus(jucator)
        # verific daca pe linia data nu am simbolul jucatorului opus
        if not jo in lista:
            return 1
        return 0

    def linii_deschise(self, jucator):
        return (self.linie_deschisa(self.matr[0:3], jucator)
                + self.linie_deschisa(self.matr[3:6], jucator)
                + self.linie_deschisa(self.matr[6:9], jucator)
                + self.linie_deschisa(self.matr[0:9:3], jucator)
                + self.linie_deschisa(self.matr[1:9:3], jucator)
                + self.linie_deschisa(self.matr[2:9:3], jucator)
                + self.linie_deschisa(self.matr[0:9:4], jucator)  # prima diagonala
                + self.linie_deschisa(self.matr[2:8:2], jucator))  # a doua diagonala

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        # if (adancime==0):
        if t_final == self.__class__.JMAX:
            return (99 + adancime)
        elif t_final == self.__class__.JMIN:
            return (-99 - adancime)
        elif t_final == 'remiza':
            return 0
        else:
            return (self.linii_deschise(self.__class__.JMAX) - self.linii_deschise(self.__class__.JMIN))

    def __str__(self):
        sir = (" ".join([str(x) for x in self.matr[0:3]]) + "\n" +
               " ".join([str(x) for x in self.matr[3:6]]) + "\n" +
               " ".join([str(x) for x in self.matr[6:9]]) + "\n")

        return sir


class Stare:
    """
	Clasa folosita de algoritmii minimax si alpha-beta
	Are ca proprietate tabla de joc
	Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
	De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
	"""

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta > stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare

            if (beta > stare_noua.estimare):
                beta = stare_noua.estimare
                if alpha >= beta:
                    break
    stare.estimare = stare.stare_aleasa.estimare

    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if (final):
        if (final == "remiza"):
            print("Remiza!")
        else:
            print("A castigat " + final)

        return True

    return False


class GrupButoane:
    def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0):
        self.listaButoane = listaButoane
        self.indiceSelectat = indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.updateDreptunghi()
            leftCurent += (spatiuButoane + b.w)

    def selecteazaDupacoord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                return True
        return False

    def deseneaza(self):
        # atentie, nu face wrap
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare


class Buton:
    def __init__(self, display=None, left=0, top=0, w=0, h=0, culoareFundal=(53, 80, 115),
                 culoareFundalSel=(89, 134, 194), text="", font="arial", fontDimensiune=16, culoareText=(255, 255, 255),
                 valoare=""):
        self.display = display
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        # creez obiectul font
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        # aici centram textul
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare = valoare

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteazaDupacoord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)


############# ecran initial ########################
def deseneaza_alegeri(display, tabla_curenta):
    btn_alg = GrupButoane(
        top=30,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="minimax", valoare="minimax"),
            Buton(display=display, w=80, h=30, text="alphabeta", valoare="alphabeta")
        ],
        indiceSelectat=1)
    btn_juc = GrupButoane(
        top=100,
        left=30,
        listaButoane=[
            Buton(display=display, w=35, h=30, text="1", valoare="1"),
            Buton(display=display, w=35, h=30, text="2", valoare="2")
        ],
        indiceSelectat=0)
    ok = Buton(display=display, top=170, left=30, w=40, h=30, text="ok", culoareFundal=(155, 0, 55))
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if not btn_juc.selecteazaDupacoord(pos):
                        if ok.selecteazaDupacoord(pos):
                            display.fill((0, 0, 0))  # stergere ecran
                            tabla_curenta.deseneaza_grid()
                            return btn_juc.getValoare(), btn_alg.getValoare()
        pygame.display.update()


def harta():
    k=0
    with open("harta.txt", "r") as f:
        linie = f.readline().split("\n")[0]
        lista_linie = []
        for i in linie:
            lista_linie.append(i)
        harta = []
        while linie:
            if len(linie) == 1:
                k = linie[0]
                linie = f.readline().split("\n")[0]
                break
            else:
                harta.append(lista_linie)
                lista_linie = []
                linie = f.readline().split("\n")[0]
                if len(linie):
                    for i in linie:
                        lista_linie.append(i)
        return [harta,int(k)]


def main():
    # initializare algoritm
    pygame.init()
    ok = 0

    pygame.display.set_caption("Omu cu bombe")
    mapa = harta()[0]
    k=harta()[1]
    nc = len(mapa[0])
    nl = len(mapa)
    w = 30
    ecran = pygame.display.set_mode(size=(nc * (w + 1) - 1, nl * (w + 1) - 1))  # N *w+ N-1= N*(w+1)-1
    Joc.initializeaza(mapa, ecran, NR_LINII=nl, NR_COLOANE=nc, dim_celula=w)
    # initializare tabla
    tabla_curenta = Joc(mapa, NR_LINII=nl, NR_COLOANE=nc)
    Joc.JMIN, tip_algoritm = deseneaza_alegeri(ecran, tabla_curenta)
    print(Joc.JMIN, tip_algoritm)
    Joc.JMAX = '1' if Joc.JMIN == '2' else '2'
    print("Tabla initiala")
    print(str(tabla_curenta))
    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, '1', ADANCIME_MAX)
    tabla_curenta.deseneaza_grid()
    while True:

        if (stare_curenta.j_curent == Joc.JMIN):

            for event in pygame.event.get():
                ok = 0  # pentru mutari
                if event.type == pygame.QUIT:
                    # iesim din program
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        for i in range(nl):
                            if ok: break
                            for j in range(nc):
                                if mapa[i][j] == "1" and mapa[i][j - 1] == "p":
                                    mapa[i][j - 1] = "1"
                                    mapa[i][j] = ""
                                    Joc.j1_protectii += 1
                                    Joc.j1_mutari += 1
                                    if Joc.j1_mutari == k:
                                        Joc.j1_mutari = 0
                                        mapa[i][j] = "b"
                                        Joc.j1_bombe.append([i,j])
                                        if len(Joc.j1_bombe)>1: #daca jucatorul avea deja minim o bomba pusa
                                            i1, i2 = Joc.j1_bombe[len(Joc.j1_bombe) - 2]
                                            mapa[i1][i2]="a"
                                    ok = 1
                                    break
                                elif mapa[i][j] == "1" and mapa[i][j - 1] != "#" and mapa[i][j - 1] != "b" and mapa[i][j - 1] != "a":
                                    mapa[i][j - 1] = "1"
                                    mapa[i][j] = ""
                                    ok = 1
                                    Joc.j1_mutari += 1
                                    if Joc.j1_mutari == k:
                                        Joc.j1_mutari = 0
                                        mapa[i][j] = "b"
                                        Joc.j1_bombe.append([i, j])
                                        if len(Joc.j1_bombe) > 1:  # daca jucatorul avea deja minim o bomba pusa
                                            i1, i2 = Joc.j1_bombe[len(Joc.j1_bombe) - 2]
                                            mapa[i1][i2] = "a"
                                    break
                        stare_curenta.tabla_joc.deseneaza_grid(mapa=mapa)

                    if event.key == pygame.K_RIGHT:
                        for i in range(nl):
                            if ok:
                                break
                            for j in range(nc):
                                if mapa[i][j] == "1" and mapa[i][j + 1] == "p" :
                                    mapa[i][j + 1] = "1"
                                    mapa[i][j] = ""
                                    Joc.j1_protectii += 1
                                    ok = 1
                                    Joc.j1_mutari += 1
                                    if Joc.j1_mutari == k:
                                        Joc.j1_mutari = 0
                                        mapa[i][j] = "b"
                                        Joc.j1_bombe.append([i, j])
                                        if len(Joc.j1_bombe) > 1:  # daca jucatorul avea deja minim o bomba pusa
                                            i1, i2 = Joc.j1_bombe[len(Joc.j1_bombe) - 2]
                                            mapa[i1][i2] = "a"
                                    break
                                elif mapa[i][j] == "1" and mapa[i][j + 1] != "#" and mapa[i][j + 1] != "b" and mapa[i][j +1] != "a" :
                                    mapa[i][j + 1] = "1"
                                    mapa[i][j] = ""
                                    ok = 1
                                    Joc.j1_mutari += 1
                                    if Joc.j1_mutari == k:
                                        Joc.j1_mutari = 0
                                        mapa[i][j] = "b"
                                        Joc.j1_bombe.append([i, j])
                                        if len(Joc.j1_bombe) > 1:  # daca jucatorul avea deja minim o bomba pusa
                                            i1, i2 = Joc.j1_bombe[len(Joc.j1_bombe) - 2]
                                            mapa[i1][i2] = "a"
                                    break
                        stare_curenta.tabla_joc.deseneaza_grid(mapa=mapa)

                    if event.key == pygame.K_UP:
                        for i in range(nl):
                            if ok:
                                break
                            for j in range(nc):
                                if mapa[i][j] == "1" and mapa[i - 1][j] == "p":
                                    mapa[i - 1][j] = "1"
                                    mapa[i][j] = ""
                                    Joc.j1_protectii += 1
                                    ok = 1
                                    Joc.j1_mutari += 1
                                    if Joc.j1_mutari == k:
                                        Joc.j1_mutari = 0
                                        mapa[i][j] = "b"
                                        Joc.j1_bombe.append([i, j])
                                        if len(Joc.j1_bombe) > 1:  # daca jucatorul avea deja minim o bomba pusa
                                            i1, i2 = Joc.j1_bombe[len(Joc.j1_bombe) - 2]
                                            mapa[i1][i2] = "a"
                                    break
                                elif mapa[i][j] == "1" and mapa[i - 1][j] != "#" and mapa[i - 1][j] != "b" and mapa[i-1][j] != "a":
                                    mapa[i - 1][j] = "1"
                                    mapa[i][j] = ""
                                    ok = 1
                                    Joc.j1_mutari += 1
                                    if Joc.j1_mutari == k:
                                        Joc.j1_mutari = 0
                                        mapa[i][j] = "b"
                                        Joc.j1_bombe.append([i, j])
                                        if len(Joc.j1_bombe) > 1:  # daca jucatorul avea deja minim o bomba pusa
                                            i1, i2 = Joc.j1_bombe[len(Joc.j1_bombe) - 2]
                                            mapa[i1][i2] = "a"
                                    break
                        stare_curenta.tabla_joc.deseneaza_grid(mapa=mapa)
                    if event.key == pygame.K_DOWN:
                        for i in range(nl):
                            if ok:
                                break
                            for j in range(nc):
                                if mapa[i][j] == "1" and mapa[i + 1][j] == "p":
                                    mapa[i + 1][j] = "1"
                                    mapa[i][j] = ""
                                    Joc.j1_protectii += 1
                                    ok = 1
                                    Joc.j1_mutari += 1
                                    if Joc.j1_mutari == k:
                                        Joc.j1_mutari = 0
                                        mapa[i][j] = "b"
                                        Joc.j1_bombe.append([i, j])
                                        if len(Joc.j1_bombe) > 1:  # daca jucatorul avea deja minim o bomba pusa
                                            i1, i2 = Joc.j1_bombe[len(Joc.j1_bombe) - 2]
                                            mapa[i1][i2] = "a"
                                    break
                                elif mapa[i][j] == "1" and mapa[i + 1][j] != "#" and mapa[i + 1][j] != "b" and mapa[i+1][j] != "a":
                                    mapa[i + 1][j] = "1"
                                    mapa[i][j] = ""
                                    ok = 1
                                    Joc.j1_mutari += 1
                                    if Joc.j1_mutari == k:
                                        Joc.j1_mutari = 0
                                        mapa[i][j] = "b"
                                        Joc.j1_bombe.append([i, j])
                                        if len(Joc.j1_bombe) > 1:  # daca jucatorul avea deja minim o bomba pusa
                                            i1, i2 = Joc.j1_bombe[len(Joc.j1_bombe) - 2]
                                            mapa[i1][i2] = "a"
                                    break
                        stare_curenta.tabla_joc.deseneaza_grid(mapa=mapa)
                    #print(Joc.j1_protectii)
                    print(Joc.j1_bombe)

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == 'minimax':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm=="alphabeta"
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc

            print("Tabla dupa mutarea calculatorului\n" + str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

            stare_curenta.tabla_joc.deseneaza_grid()
            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)


if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
