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
        self.move_set = move_set
    def update_health(self,stats): #current_hp, cond_effects and external_info too
        ...
    def priority(self):
        return self.stats[4]/(2**self.streak)

###probably have a raw_dweller class and a class for the mathematics involved

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


def who_attacks(Dweller1,Dweller2):
    eff_speed1 = Dweller1.priority() #i have to adjust speed and stamina
    eff_speed2 = Dweller2.priority()
    prob_dweller1 = eff_speed1/(eff_speed1+eff_speed2)
    attacker_choice = np.random.choice([Dweller1,Dweller2],p=[prob_dweller1,1-prob_dweller1],size = 2,replace=False)
    attacker = attacker_choice[0]
    defender = attacker_choice[1]
    print(attacker.name,defender.name)
    return attacker,defender #have to understand np.random.choice so I generate a list with the selected results in order and return them

def combat(attacker,defender):
    def is_crit(move,attacker):
        c = move.stats[1]*attacker.stats[3]>=np.random.random()
        if c:
            print("Critical hit!")
            return 1+0.5*c
        return 1

    def damage(move,attacker,defender): #probably better within a Dweller class
        return move.stats[0]*attacker.stats[5]/defender.stats[6]
        
    move = np.random.choice(attacker.move_set)
    total_accuracy = attacker.stats[2]*move.stats[2]*(1-defender.stats[1])
    is_hit = np.random.random() <= total_accuracy
    if not is_hit:
        print(defender.name + " dodged the attack")
        return 0
    return is_crit(move,attacker)*damage(move,attacker,defender)
    
def turn(Dweller1,Dweller2):
    while Dweller1.stats[0]*Dweller2.stats[0] >0:
        Dweller1.streak = 0
        Dweller2.streak = 0
        attacker, defender = who_attacks(Dweller1,Dweller2) 
        dmg = combat(attacker,defender)
        if dmg:
            defender.stats[0] -= dmg
            print(defender.name, ' was dealt ',str(dmg),' damage')
        
    if Dweller1.stats[0] <= 0: ##use np.where 
        print(Dweller1.name, " died")
    elif Dweller2.stats[0] <=0:
        print(Dweller2.name, " lost")



#turn(Fairy,Arsonist)
