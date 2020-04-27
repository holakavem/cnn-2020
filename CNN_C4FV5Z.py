import tkinter as tk
from tkinter import *
import random,time

#globalis valtozok 
kezdeti_fekete, kezdeti_feher, kezdeti_piros = 0, 0, 0
akt_fekete, akt_feher, akt_piros = 0, 0, 0
sugar=1 #a sugar amiben levo mezok hatnak a kozepso mezore(pixelben) -valtoztathato
generaciok = 1000 #ahany generacion keresztul fut a szimulacio -valtoztathato
racsmeret = 10 #cellak merete(pixelben) -valtoztathato
kepernyomeret = 600 #kepernyo merete(pixelben) -allando
cellaszam = int(kepernyomeret/racsmeret) 

#kepernyo kirajzolasa - Tkinter-e dolgoztam
root=Tk()
ablak = Canvas(root,height=kepernyomeret,width=kepernyomeret)
ablak.grid(row=0,columnspan=2) 

#fo kepernyo szovegeinek es bemeneti mezoinek kirajzolasa
Label(root,text='Írd be a rács méretét(pixelben)! =>',font=('Arial',12)).grid(row=1)
racs_Input=StringVar()
e1=Entry(root,textvariable=racs_Input)
e1.grid(row=1,column=1)
racs_Input.set(10)

Label(root,text='Generációk száma =>',font=('Arial',12)).grid(row=2)
generacio_Input=StringVar()
e1=Entry(root,textvariable=generacio_Input)
e1.grid(row=2,column=1)
generacio_Input.set(1000)

Label(root,text='Szomszédsági sugár =>',font=('Arial',12)).grid(row=3)
sugar_Input=StringVar()
e1=Entry(root,textvariable=sugar_Input)
e1.grid(row=3,column=1)
sugar_Input.set(1)

#Matrixom amiben tarolom az egyes cellak allapotat
CA = [[0 for x in range(cellaszam)] for y in range(cellaszam)]

#racsozottsag kirajzolasa
def InitCanvas():
    #elso lepeskent torlunk mindent
    ablak.delete('all')

    #kirajzolja a racsot
    for i in range(cellaszam):
		#racssorok generalasa x,y koordinatak menten
        ablak.create_line(0,racsmeret * i, kepernyomeret, racsmeret * i)
        ablak.create_line(racsmeret * i, 0, racsmeret * i, kepernyomeret)
	

#az aktualis CA matrixbol kirajzoljuk a mezoket
def racsfrissites():
    global CA # globalis CA matrix hasznalata

    InitCanvas()

    #vegig iteralok a cellakon
    for i in range(cellaszam):
        for j in range(cellaszam):
			#ha az adott racspont egyenlo eggyel akkor el tehat befestjuk feketere. Ha kettovel akkor pirosra. Maradek feher.
            if CA[i][j] == 1:
                x1 = racsmeret * i
                y1 = racsmeret * j
				#adott racspontot feketere festjuk
                ablak.create_rectangle(x1,y1,x1+racsmeret,y1+racsmeret,fill='black')
            if CA[i][j] == 2:
                x1 = racsmeret * i
                y1 = racsmeret * j
                ablak.create_rectangle(x1,y1,x1+racsmeret,y1+racsmeret,fill='red')
    ablak.update() #rafrissitunk

#egyes cellakba random ertekek generalasa megadott aranyokkal
def kezdeti_CA():
    global CA

    for i in range(cellaszam):
        for j in range(cellaszam):
            rand_szam = random.randint(1,100) #random ertek generalasa
            if rand_szam < 10:
                CA[i][j] = 2
            elif 10 <= rand_szam < 43:
                CA[i][j] = 1
            else:
                CA[i][j] = 0

#a beadott liastabol visszaadja hogy melyik elem a leggyakrabban elofordulo
def most_frequent(List): 
    return max(set(List), key = List.count) 

#CA matrixbol kiszamolja hogy az egyes cella ertekekbol osszesen mennyi van
def counter(round):
    
    global CA
    global kezdeti_fekete, kezdeti_feher, kezdeti_piros
    global akt_fekete, akt_feher, akt_piros

    countList = [] #list amibe belepakoljuk az osszeset
    for i in range(cellaszam):
        for j in range(cellaszam):
            countList.append(CA[i][j])
    #a kezdeti ertekek meghatarozása meg mielott a szimulacio elindul
    if round == 1 :
        kezdeti_fekete = countList.count(1)
        kezdeti_feher = countList.count(0)
        kezdeti_piros = countList.count(2)
    #aktualis ertekek meghatarozasa generacionkent
    elif round == 2:
        akt_fekete = countList.count(1)
        akt_feher = countList.count(0)
        akt_piros = countList.count(2)

#majority rule definialasa
def MajorityRule():
    global CA

    #egy ideiglenes CA matrix letrehozasa
    CAkovetkezo = [[0 for x in range(cellaszam)] for y in range(cellaszam)]
    #vegig iteralunk a "jatektere". kiveve a legszelso cellakat hogy ne fussunk ki vizsgalatkor a kepernyorol. ezert a legszelso elemek nemis valtoznak (jobb megoldast nem talaltam ra)
    for i in range(sugar,cellaszam-sugar):
        for j in range(sugar,cellaszam-sugar):
            elokList = [] #a sugarba eso cellakat ebbe pakoljuk
            #szomszedokon es onmagan valo vegig iteralas 'sugar' tavolsagban
            for r in range((i-sugar),(i+sugar+1)): 
                for t in range((j-sugar),(j+sugar+1)):
                    elokList.append(CA[r][t])
            
            #a szomszedsagban ha a leggyakrabban elofordulo elembol 5-nel tobb van arra az ertekre valtozik a vizsgalt cellank
            if most_frequent(elokList)==1 and elokList.count(most_frequent(elokList)) >=5 :
                CAkovetkezo[i][j] = 1
            elif most_frequent(elokList)==2 and elokList.count(most_frequent(elokList)) >=5 :
                CAkovetkezo[i][j] = 2
            else:
                CAkovetkezo[i][j] = CA[i][j] #egyebkent marad onmaga
                
    CA = CAkovetkezo #eredeti matrix felveszi az ideiglenes ertekeit
    counter(2) #megszamoljuk az aranyokat
    racsfrissites() #majd frissitunk

#ahany generacio van annyiszor kalkulaljuk ki a cellak ertekeit a majority szabalyal
def runMR():
    for i in range(generaciok):
        MajorityRule()

# 'Adatok' felugro ablak megrajzolasa
def popup():
    info = Toplevel()		  
    info.geometry('200x300') #felugro ablak merete(pixelben)
    info.title('Adatok') #ablak neve
    #kulonbozo feliratok kiirasa
    Label(info,text='Kezdeti arányok:',font=('Arial',12)).grid(row=1,column=1)
    Label(info,text='Piros',font=('Arial',12)).grid(row=2,column=1)
    Label(info,text= kezdeti_piros,font=('Arial',12)).grid(row=2,column=2)
    Label(info,text='Fekete',font=('Arial',12)).grid(row=3,column=1)
    Label(info,text=kezdeti_fekete,font=('Arial',12)).grid(row=3,column=2)
    Label(info,text='Fehér',font=('Arial',12)).grid(row=4,column=1)
    Label(info,text=kezdeti_feher,font=('Arial',12)).grid(row=4,column=2)

    Label(info,text=' ',font=('Arial',12)).grid(row=5,column=1)

    Label(info,text='Aktuális arányok:',font=('Arial',12)).grid(row=6,column=1)
    Label(info,text='Piros',font=('Arial',12)).grid(row=7,column=1)
    Label(info,text= akt_piros,font=('Arial',12)).grid(row=7,column=2)
    Label(info,text='Fekete',font=('Arial',12)).grid(row=8,column=1)
    Label(info,text=akt_fekete,font=('Arial',12)).grid(row=8,column=2)
    Label(info,text='Fehér',font=('Arial',12)).grid(row=9,column=1)
    Label(info,text=akt_feher,font=('Arial',12)).grid(row=9,column=2)

    Label(info,text=' ',font=('Arial',12)).grid(row=10,column=1)
    #bezaro gomb definialasa
    Button(info, text='Bezár', command=info.destroy).grid(row=11,column=2)
    info.transient(root) 	    #megtiltjuk az ablak ujra rajzolasat
    info.grab_set()	            #Imegtiltjuk az interakciot az ablakkal
    root.wait_window(info)          #a szimulaciot szuneteltetjuk amig az ablak nyitva van

#szimulacio fobb folyamatainak inditasa
def _draw():

    global CA
    global racsmeret, cellaszam, generaciok, sugar

    racsmeret = int(racs_Input.get()) #racsmeret megvaltoztatasa a beirt ertekre
    cellaszam = int(kepernyomeret/racsmeret) #cellaszam ujra kalkulalasa
    sugar =int(sugar_Input.get()) #sugar megvaltoztatasa a beirt ertekre
    CA = [[0 for x in range(cellaszam)] for y in range(cellaszam)] #CA matrix ujra generalasa

    generaciok = int(generacio_Input.get()) #generacioszam megvaltoztatasa a beirt ertekre
    kezdeti_CA() #kezdeti ertekek generalasa
    counter(1) #kezdeti ertekek megszamolasa
    racsfrissites() #mezok kirajzolasa
    runMR() #majority szabaly futtatasa
    
#'Futtatas' gomb definialasa
btn = Button(root,text='Futtatás',command=_draw,font=('Arial',12))
btn.grid(row=4,column=0)
btn = Button(root,text='Adatok',command=popup,font=('Arial',12))
btn.grid(row=4,column=1)

#main fuggveny
if __name__ == '__main__':
   
   root.mainloop() #program futtatasa