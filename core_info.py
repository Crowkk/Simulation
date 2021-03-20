import numpy as np
from copy import *

###INFO about the dweller
class Dweller:
    def __init__(self,name,stats,lore,naturality,interactions,trait,move_set): #i think **kwargs solve the problem of ()
        self.name = name #Name of the Dweller
        if not isinstance(stats,np.ndarray) or len(stats)!= 11: #this one was just for practice
            raise Exception("error")
        else:
            self.stats = stats #the stats will be an array containing all the base data about the Dweller
        #Health Evasiveness Acc Luck Stamina Strength Armor Elemental Attack Resilience Magical Attack Aura
        self.lore = lore #the backstory of the Dweller
        self.naturality = naturality #how it interacts with the enviroment
        self.interactions = interactions #a matrix containing modifiers for the Dweller
        self.trait = trait #changes the behavior depending on the context of the fight this might be tough to code
        #need to have still current_hp, buffs, conditional_effects, external_info
    def update_health(self,stats): #current_hp, cond_effects and external_info too
        ...
    def priority(self):
        return self.stats[4]/(2**self.streak)

#INFO about the move
class Move: #this class will probably have an instance that is the Statuses/Conditions Class
    def __init__(self,name,stats,kind,element,secondary=None): #and additional info for secondary effects etc
        self.name = name
        self.stats = stats #damage crit acc falloff area 
        self.kind = kind #physical elemental etc
        self.element = element #fire etc
        self.secondary = secondary

Fae_stats = np.array([500,0.05,0.95,0.05,0.5,50,50,50,50,50,50])
Arson_stats = np.array([500,0.05,0.95,0.05,0.5,50,50,50,50,50,50])
Flamethrower = Move("Flamethrower",np.array([50,0.05,0.98,4]),2,0)
Fae_dust = Move("Fae Dust",np.array([50,0.05,0.98,4]),2,0)
Fairy = Dweller("Fae",Fae_stats,1,1,1,1,np.array([Flamethrower,Fae_dust]))
Arsonist = Dweller("Arson",Arson_stats,1,1,1,1,np.array([Flamethrower,Fae_dust]))

#Each turn will go as follows (in the most basic way)
#firstly the attacker is picked according to a function
#then it chooses an attack to use
#then it checks whether or not it hits
#then if it's a critical
#then subtracts from defender's current HP
def turn(Dweller1,Dweller2):
    Dweller1.streak = 0
    Dweller2.streak = 0
    attacker, defender = who_attacks(Dweller1,Dweller2) 

def who_attacks(Dweller1,Dweller2):
    eff_speed1 = Dweller1.priority() #i have to adjust speed and stamina
    eff_speed2 = Dweller2.priority()
    prob_dweller1 = eff_speed1/(eff_speed1+eff_speed2)
    attacker_choice = np.random.choice([Dweller1,Dweller2],p=[prob_dweller1,1-prob_dweller1],size = 2,replace=False)
    attacker = attacker_choice[0]
    defender = attacker_choice[1]
    return [deepcopy(attacker),deepcopy(defender)] #have to understand np.random.choice so I generate a list with the selected results in order and return them

def damage(base_damage,kind,attack_stats,def_stats): #probably better within a Dweller class
    ...

def does_hit(move,attacker,defender):
    ...

def is_crit(move,attacker,defender):
    ...

turn(Fairy,Arsonist)



