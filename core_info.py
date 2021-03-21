import numpy as np
from copy import *



#SPLIT THE DWELLER CLASS AND THE SECONDCLASS BE DEBUFFS, POSITION ETC
#FROM SECONDCLASS DEFINE ALL THE STATUSES BASED ON STATS_LIST AND MODIFIER_LIST
#CHECK WITHIN SECONDCLASS THE STATUSES EFFECTS

#status does not work

#Poison, Soaked, Burned, Paralyzed, Muted, Cursed

#ADD PROPER DAMAGE STUFF AND TRIGGER EFFECTS AND DIFFERENTIATE THE CATEGORIES

#ADD INTERACTIONS TABLE

#ADD MOVEMENT AND POSITIONING

#ADD MORE DWELLERS

#NATURALITY
#Maybe create a subclass for each naturality special effect

#ENVIROMENT MODIFIERS



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
        self.streak = 0
        self.status = ""
        self.external = None
    @property
    def speed(self):
        return self.stats[4]/(2**self.streak)

    def status_proc(self,proc):
        if self.status == "":
            print(self.name," now has ",proc) 
            self.status = proc
        print("Already status")

    @property
    def accuracy(self):
        return self.stats[2]-0.1*(self.status == "Soaked")

    def check_status(self,stage):
        if self.status == "":
            self.stats[0] =  self.stats[0]
        elif stage == "after life check":
            if self.status == "Poison":
                self.stats[0] = self.stats[0] - 100

#INFO about the move
class Move: #this class will probably have an instance that is the Statuses/Conditions Class
    def __init__(self,name,stats,kind,element,secondary): #and additional info for secondary effects etc
        self.name = name
        self.stats = stats #damage crit acc falloff area 
        self.kind = kind #physical elemental etc
        self.element = element #fire etc
        self.secondary = secondary #an array with numbers corresponding to [who_affects, what_affects, how_affects]

Fae_stats = np.array([500,0.05,0.95,0.05,0.5,50,50,50,50,50,50])
Arson_stats = np.array([500,0.05,0.95,0.05,0.5,50,50,50,50,50,50])
Flamethrower = Move("Flamethrower",np.array([50,0.05,0.98,4]),7,0,np.array([]))
Fae_dust = Move("Fae Dust",np.array([50,0.05,0.98,4]),9,0,secondary = np.array([0.9,[1],[[],[0]],[[],["Poison"]]],dtype = object))
Fairy = Dweller("Fae",Fae_stats,1,1,1,1,np.array([Flamethrower,Fae_dust]))
Arsonist = Dweller("Arson",Arson_stats,1,1,1,1,np.array([Flamethrower,Fae_dust]))
print(len(Flamethrower.secondary))
#Each turn will go as follows (in the most basic way)
#firstly the attacker is picked according to a function
#then it chooses an attack to use
#then it checks whether or not it hits
#then if it's a critical
#then subtracts from defender's current HP


def who_attacks(Dweller1,Dweller2):
    eff_speed1 = Dweller1.speed #outputs a different speed depending on the streak (streak to be implemented)
    eff_speed2 = Dweller2.speed
    prob_dweller1 = eff_speed1/(eff_speed1+eff_speed2) #weighs the prob of being Dweller1 the attacker
    attacker_choice = np.random.choice([Dweller1,Dweller2],p=[prob_dweller1,1-prob_dweller1],size = 2,replace=False)
    attacker = attacker_choice[0]
    defender = attacker_choice[1]
    return attacker,defender #outputs who attacks and who defends

def combat_status_checker(D1,D2,stage):
    D1.check_status(stage)
    D2.check_status(stage)

def status_effect(secondary,who,attacker,defender):
    targets = [attacker,defender]
    if secondary[2][who] == 0: #it's a status
        
        targets[who].status_proc(secondary[3][who])        
    elif secondary[2][who] == 1: #it's buff or debuff
        targets[who].external += secondary[3][who]
    return attacker,defender
            
def combat(attacker,defender): #routine related to the combat alone, outputs the final damage
    def is_crit(move,attacker): #calculates the critical stuff
        c = move.stats[1]*attacker.stats[3]>=np.random.random() #whether or not a critical landed
        if c: #it did
            print("Critical hit!")
            return 1+0.5*c #bonus damage
        return 1 #no bonus modifier

    def damage(move,attacker,defender): #calculates final damage
        return move.stats[0]*attacker.stats[move.kind]/defender.stats[move.kind] #simple formula base damage * (attacker_attack)/defender_defense
        
    move = np.random.choice(attacker.move_set) #randomly choose an attack
    total_accuracy = attacker.stats[2]*move.stats[2]*(1-defender.stats[1]) #combine all accuracy and evasivenesses involved
    print(attacker.name," used ",move.name)
    is_hit = np.random.random() <= total_accuracy #does hit
    if not is_hit:
        print(defender.name + " dodged the attack")
        return 0,np.array([None]),move #ajeitar aqui
    if move.kind !=0:
        if len(move.secondary) != 0:
            does_proc = np.random.random() 
            return is_crit(move,attacker)*damage(move,attacker,defender),move.secondary*(does_proc<=move.secondary[0]),move #damage
        else:
            return is_crit(move,attacker)*damage(move,attacker,defender),0,move
    else:
        return 0,move.secondary,move
def turn(Dweller1,Dweller2): #general turn
    while Dweller1.stats[0]*Dweller2.stats[0] >0: #both are alive
        stage = "before"
        combat_status_checker(Dweller1,Dweller2,stage)
        attacker, defender = who_attacks(Dweller1,Dweller2) #chose the attacker for the turn
        dmg,secondary,move = combat(attacker,defender) #calculated the damage
        if dmg: #was there any damage?
            defender.stats[0] -= dmg #subtracts from total hp
            print(defender.name, ' was dealt ',str(dmg),' damage')
        if len(move.secondary) != 0 and secondary[0] != None:
            for element in secondary[1]:
                attacker,defender = status_effect(secondary,element,attacker,defender)
                    
        if Dweller1.stats[0]*Dweller2.stats[0] >0:
            stage = "after life check"
            combat_status_checker(attacker,defender,stage)
        
    #this snipet will change soon, works fine it's just ugly
    if Dweller1.stats[0] <= 0: ##use np.where 
        print(Dweller1.name, " died")
    elif Dweller2.stats[0] <=0:
        print(Dweller2.name, " lost")


turn(Arsonist,Fairy)
