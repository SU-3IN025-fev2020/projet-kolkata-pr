# -*- coding: utf-8 -*-

# Nicolas, 2020-03-20

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo
import pathfinding
import strats
from strats import Strat_Analyse

import random 
import numpy as np
import sys



    
# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'kolkata_6_10'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 144  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 5 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    
    
    

    
    #-------------------------------
    # Initialisation
    #-------------------------------
    nbLignes = game.spriteBuilder.rowsize
    nbColonnes = game.spriteBuilder.colsize
    print("lignes", nbLignes)
    print("colonnes", nbColonnes)
    
    
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    
    
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    
    # on localise tous les objets  ramassables (les restaurants)
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
    nbRestaus = len(goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)
    print('init',initStates)
    print('goal',goalStates)
    print('wall',wallStates)
    # on liste toutes les positions permises
    allowedStates = [(x,y) for x in range(nbLignes) for y in range(nbColonnes)\
                     if (x,y) not in wallStates or  goalStates] 

    analyse=Strat_Analyse(len(goalStates))
    
    #-------------------------------
    # Placement aleatoire des joueurs, en évitant les obstacles
    #-------------------------------

    liste_gains=[0]*nbPlayers
    freqentation=[]
    analyse.suscribe(0)
    analyse.suscribe(1)
    analyse.suscribe(2)
    analyse.suscribe(3)
       
    for i in range(iterations):
        terminé=False
        ite=0

        posPlayers = initStates

        
        for j in range(nbPlayers):
            x,y = random.choice(allowedStates)
            players[j].set_rowcol(x,y)
            game.mainiteration()
            posPlayers[j]=(x,y)


            

        #-------------------------------
        # chaque joueur choisit un restaurant
        #-------------------------------

        restau=[0]*nbPlayers
        for j in range(nbPlayers):
            if analyse.is_inscrit(j):
                c=analyse.best_strat(j)
                print("Strat_Analyse pour joueur",j,c)
            else :                
                #c=strats.strat_proche(posPlayers[j],goalStates)
                c=strats.strat_tetue(j,nbRestaus)
                #c=5
                print(c)
                #c = strats.strat_alea(nbRestaus)
            restau[j]=c

        paths=[0]*nbPlayers

        

        for i in range(nbPlayers):
            paths[i]=pathfinding.Astar(posPlayers[i],goalStates[restau[i]],wallStates)

        for i in range(iterations):
            terminé=False
            ite=0

        while(not(terminé)):
            fin=0
        
            for j in range(nbPlayers): # on fait bouger chaque joueur séquentiellement
                if len(paths[j])>ite :
                    next_row,next_col=paths[j][ite]
                    players[j].set_rowcol(next_row,next_col)
                    print ("pos :", j, next_row,next_col)
                    game.mainiteration()
                    posPlayers[j]=(next_row,next_col)
                else :
                    print(("Le joueur ", j, " a terminé"))
                    fin+=1
                    game.mainiteration()
            ite+=1
            if fin==10 :
                terminé=True
                print('Fin du tour : distribution des gains')
                for v in range(len(goalStates)):
                    gagnants=[]
                    for g in range(nbPlayers):
                        if posPlayers[g]==goalStates[v] :
                            gagnants.append(g)
                    if len(gagnants)!=0 :
                        gagnant=random.choice(gagnants)
                        liste_gains[gagnant]+=1
                    tab_fin=[0]*len(goalStates)
                for q in range(len(tab_fin)):
                    for y in range(nbPlayers):
                        if posPlayers[y]==goalStates[q] :
                            tab_fin[q]+=1
                print("fin",tab_fin)
                for u in range(nbPlayers):
                    if analyse.is_inscrit(u) :
                        fin=-1
                        for p in range(len(goalStates)) :
                            if posPlayers[u]==goalStates[p]:
                                fin=p
                        print(p)
                        analyse.actualiser_resultats(u ,p,tab_fin)

                print('gains_actuels')
                print(liste_gains)

                
        
    
    #-------------------------------
    # Boucle principale de déplacements 
    #-------------------------------
    
       


    # bon ici on fait juste plusieurs random walker pour exemple...
    '''
    for i in range(iterations):
        
        for j in range(nbPlayers): # on fait bouger chaque joueur séquentiellement
            row,col = posPlayers[j]

            x_inc,y_inc = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
            next_row = row+x_inc
            next_col = col+y_inc
            # and ((next_row,next_col) not in posPlayers)
            if ((next_row,next_col) not in wallStates) and next_row>=0 and next_row<=19 and next_col>=0 and next_col<=19:
                players[j].set_rowcol(next_row,next_col)
                print ("pos :", j, next_row,next_col)
                game.mainiteration()
    
                col=next_col
                row=next_row
                posPlayers[j]=(row,col)
            
      
        
            
            # si on est à l'emplacement d'un restaurant, on s'arrête
            if (row,col) == restau[j]:
                #o = players[j].ramasse(game.layers)
                game.mainiteration()
                print ("Le joueur ", j, " est à son restaurant.")
               # goalStates.remove((row,col)) # on enlève ce goalState de la liste
                
                
                break'''
            
    
    pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()
    


