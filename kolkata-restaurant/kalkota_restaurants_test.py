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
    game.fps = 5  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 15 # default
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

    
    
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    
    
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]

    
    
    # on localise tous les objets  ramassables (les restaurants)
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]

    nbRestaus = len(goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)

    # on liste toutes les positions permises
    allowedStates = [(x,y) for x in range(nbLignes) for y in range(nbColonnes)\
                     if (x,y) not in wallStates or  goalStates] 
    
    #-------------------------------
    # Placement aleatoire des joueurs, en évitant les obstacles
    #-------------------------------

    liste_gains=[0]*nbPlayers
       
    for i in range(iterations):
        terminé=False
        ite=0

        posPlayers = initStates

        
        x,y=random.choice(allowedStates)
        players[0].set_rowcol(x,y)
        game.mainiteration()
        posPlayers[0]=(x,y)


            
        print('positions de depart')
        print(posPlayers)
        #-------------------------------
        # chaque joueur choisit un restaurant
        #-------------------------------

        restau=[0]
        c=strats.strat_proche(posPlayers[0],goalStates)
            #c=strats.strat_tetue(j,nbRestaus)
            #c = strats.strat_alea(nbRestaus)
        print(c)
        restau=c

        paths=[0]
        


        paths=pathfinding.Astar(posPlayers[0],goalStates[restau],wallStates)


        print(paths)

        for i in range(iterations):
            terminé=False
            ite=0

        while(not(terminé)):
            fin=0
    
            if len(paths)>ite :
                next_row,next_col=paths[ite]
                print (paths[ite])
                ite+=1
                players[0].set_rowcol(next_row,next_col)
                print ("pos :", next_row,next_col)
                game.mainiteration()
                posPlayers[0]=(next_row,next_col)
            else :
                print(("Le joueur ", " a terminé"))
                terminé=True
                fin+=1
                game.mainiteration()
        
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
    


