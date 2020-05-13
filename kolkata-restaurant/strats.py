import random
import math
def strat_alea(nbRestaus):
    return random.randint(0,nbRestaus-1)

def strat_tetue(i,tot):
    return i%tot

def strat_proche(start,list_goals):
    x1,y1=start
    best_dist=math.inf
    best_goal=None

    for i in range (len(list_goals)):
        x2,y2=list_goals[i]
        dist=abs(x1 - x2) + abs(y1 - y2)
        if best_dist>dist :
            best_dist=dist
            best_goal=i
    return best_goal

class Strat_Analyse(object) :
    def __init__(self,nb_goals):
        self.liste_inscrits=[]
        self.coups_precedents=[]
        self.nb_goals=nb_goals

    def suscribe(self,i):
        self.liste_inscrits.append(i)
        self.coups_precedents.append([0]*self.nb_goals)

    def is_inscrit(self,i):
        return (i in self.liste_inscrits)

    def actualiser_resultats(self, i, end_i, list_resultats) :
        for k in range(0,self.nb_goals):
            self.coups_precedents[i][k]+=list_resultats[k]
        self.coups_precedents[i][end_i]-=1

    def best_strat(self,i):
        b_goal=[]
        nb_max=math.inf
        for k in range (0,self.nb_goals):
            if self.coups_precedents[i][k]<=nb_max :
                nb_max=self.coups_precedents[i][k]
                b_goal.append(k)
        return random.choice(b_goal)



