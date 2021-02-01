### Jeu de la vie

import numpy as np
from tkinter import *


taille = 38

class PLAN():

    def __init__(self,largeur,hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.tab_cases = np.ones((hauteur,largeur),dtype = CASE)
        self.tk = None
        self.canvas = None
        self.creation_fenetre()
        self.creer_cases()
        self.pas = None
        self.test_jeu = False
        self.dict_motif = {'planeur':np.array([[1,1,1],[0,0,1],[0,1,0]]),
                           'canon':np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
                                            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
                                            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
                                            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
                                            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                                            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]),
                           'grenouille':np.array([[0,1,1,1],
                                                  [1,1,1,0]]),
                           'LWSS':np.array([[1,0,0,1,0],
                                            [0,0,0,0,1],
                                            [1,0,0,0,1],
                                            [0,1,1,1,1]]),
                           }
        self.motif = None

    def __str__(self):
        return 'Plan de taille {}x{}'.format(self.largeur,self.hauteur)

    def __repr__(self):
        return 'Plan de jeu'

    def creer_cases(self):
        for i in range(self.hauteur):
            for j in range(self.largeur):
                case = CASE(j,i,False,self)
                self.tab_cases[i,j] = case

    def creation_fenetre(self):
        self.tk = Tk()
        self.tk.title('Jeu de la vie')
        
        #canvas

        h = self.tk.winfo_screenheight()*.95
        w = self.tk.winfo_screenwidth()*.95
        self.canvas = Canvas(self.tk,width = w,height = h)
        self.canvas.pack()
 
        pas1 = w//self.largeur
        pas2 = h//self.hauteur
    
        self.pas = min(pas1,pas2)
        pas = self.pas

        for k in range(self.hauteur+1):
            self.canvas.create_line(0,k*pas,self.largeur*pas,k*pas)
        for k in range(self.largeur+1):
            self.canvas.create_line(k*pas,0,k*pas,self.hauteur*pas)



        self.mb = Menu(self.tk)
        mb = self.mb
        self.tk['menu'] = mb

        self.edition = Menu(mb,tearoff=0)
        edition = self.edition
        mb.add_cascade(label = 'Edition',menu = edition)

        edition.add_command(label='Activer la modification',command=self.modif_enable)
        edition.add_command(label='Arrêter la modification',command=self.modif_disable)
        edition.add_command(label='Reset',command=self.reset)

        self.simulation = Menu(mb,tearoff=0)
        simulation = self.simulation
        
        mb.add_cascade(label='Simulation',menu=simulation)
        simulation.add_command(label='Lancer la simulation',command=self.lancement)
        simulation.add_command(label='Arrêter la simulation',command=self.stop)



    def init_cases(self):
        for case in self.tab_cases.flatten():
            case.s_afficher()

    def modif_enable(self):
        for case in self.tab_cases.flatten():
            case.affiche_bouton()

        self.motif_menu = Menu(self.mb,tearoff=0)
        self.edition.add_cascade(label='Motifs',menu=self.motif_menu)
        for nom_motif in self.dict_motif.keys():
            self.ajout_motif(nom_motif)

    def ajout_motif(self,nom_motif):
        self.motif_menu.add_command(label=nom_motif,command=lambda:self.coord_motif(nom_motif))

    
    def modif_disable(self):
        for case in self.tab_cases.flatten():
            case.supp_bouton()
            case.s_afficher()
        self.edition.delete(self.edition.index('end'))

    def lancement(self):
        self.test_jeu = True
        self.jeu()
        
    
    def jeu(self):
        '''itérations du jeu de la vie'''
        for case in self.tab_cases.flatten():
            voisins_a = case.n_voisins_active()
            if case.state == True:
                if voisins_a<2 or voisins_a>3:
                    case.new_state = False
                else:
                    case.new_state = True
            if case.state == False:
                if voisins_a == 3:
                    case.new_state = True
                else:
                    case.new_state = False
        for case in self.tab_cases.flatten():
            case.state = case.new_state
            case.s_afficher()

        if self.test_jeu == True:
            self.tk.after(50,self.jeu)

    def stop(self):
        self.test_jeu = False

    def reset(self):
        for case in self.tab_cases.flatten():
            case.state = False
            case.new_state = False
            case.s_afficher()

    def coord_motif(self,nom_motif):
        self.motif = self.dict_motif[nom_motif]
        w = Toplevel()
        w.title('Coordonnées')
        labelx = Label(w,text='x =')
        labelx.pack()
        xv = IntVar()
        x = Entry(w,textvariable=xv)
        x.pack()
        labely = Label(w,text='y =')
        labely.pack()
        yv = IntVar()
        y = Entry(w,textvariable=yv)
        y.pack()
        rot = Button(w,text='Rotation motif',command=self.tourne_motif)
        rot.pack()
        b = Button(w,text='Valider',command=lambda:self.place_motif(x,y,w))
        b.pack()

    def tourne_motif(self):
        self.motif=np.rot90(self.motif)

    
    def place_motif(self,x,y,w):
        x = int(x.get())
        y = int(y.get())
        w.destroy()
        n,p = np.shape(self.motif)
        for i in range(n):
            for j in range(p):
                if self.motif[i,j] == 1:
                    self.tab_cases[i+y,j+x].change()
        


class CASE():

    def __init__(self,x,y,state,plan):
        self.x = x
        self.y = y
        self.state = state
        self.new_state = None
        self.plan = plan
        self.pas = plan.pas
        self.rect = self.plan.canvas.create_rectangle(x*self.pas,y*self.pas,(x+1)*self.pas,(y+1)*self.pas,fill='black',width=0)
        self.bouton = None
        self.fen = None

    def __str__(self):
        return 'Case à la position {},{} en état {}'.format(self.x,self.y,self.state)

    def __repr__(self):
        return 'Case à la position {},{} en état {}'.format(self.x,self.y,self.state)
    

    def s_afficher(self):
        if self.state == True:
            self.plan.canvas.itemconfigure(self.rect,fill='white')
        else:
            self.plan.canvas.itemconfigure(self.rect,fill='black')

    def change(self):
        if self.state == True:
            self.state = False
            self.bouton.configure(bg='black')
        else:
            self.state = True
            self.bouton.configure(bg='white')


    def affiche_bouton(self):
        x = self.x
        y = self.y
        pas = self.pas
        if self.state == False:
            self.bouton = Button(self.plan.tk,command=self.change,background='black',cursor='hand2')
        else:
            self.bouton = Button(self.plan.tk,command=self.change,background='white',cursor='hand2')
        self.fen = self.plan.canvas.create_window(x*pas,y*pas,anchor='nw',window=self.bouton,height = pas, width = pas)

    def supp_bouton(self):
        self.plan.canvas.delete(self.fen)

    def n_voisins_active(self):
        n = 0 
        l_x = [-1,-1,0,1,1,1,0,-1]
        l_y = [0,-1,-1,-1,0,1,1,1]
        liste_cases = [(x,y) for x,y in zip(l_x,l_y)]
        x,y = self.x, self.y
        if x == 0:
            liste_cases[0] = None
            liste_cases[1] = None
            liste_cases[-1] = None
        if x == self.plan.largeur-1:
            liste_cases[3] = None
            liste_cases[4] = None
            liste_cases[5] = None
        if y == 0:
            liste_cases[1] = None
            liste_cases[2] = None
            liste_cases[3] = None
        if y == self.plan.hauteur-1:
            liste_cases[-1] = None
            liste_cases[-2] = None
            liste_cases[-3] = None
        
        for pos_case_voisine in liste_cases:
            if pos_case_voisine != None:
                j,i = pos_case_voisine
                case_voisine = self.plan.tab_cases[y+i,x+j]
                if case_voisine.state == True:
                    n = n+1
        return n


plan = PLAN(taille,taille*9//16)
plan.tk.mainloop()