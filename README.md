# Simulation

## Motivation
This is just a mini simulation game. I like programming but I rarely have the need to use several of the things that are more advanced. At least not for now, most of what I use I usually already know so I want to challenge myself. Also, I really like the balacing aspect of gaming design and data analysis in general so this is a good way of mixing both. 

So far I don't know how to implement any sort of graphics or real-time interactions but these will be left for the future.

In this game, there'll be several fighters of which the user will choose two, then they'll fight automatically. Perhaps, at some point, the user will be able to command something in there.

## General aspects

The core of the game is to have two dwellers fighting and betting on who will win. To make the game more interesting and complete, there will be not only the dwellers but an enviroment, modifiers and the dwellers are not static, their positions will be taken into account (this one might come in later on). As far as I know, most games have at most two status sets: physical and elemental; Characters deal damage according to their specialized status attack versus the target's corresponding defense. Here I chose to add a third category and the status will be physical, elemental or magical. To visualize this think of those as a punch, a fire blast and shadow ball. It is as if each category corresponds to a different source. Now that we've covered the bare basics let's dive a little into the data of a dweller and of their attacks.

### Dweller Status

#### Health 
Just as any other game, health accounts for the amount of damage a character can take. When it reaches zero, the dwellers loses the match.

#### Evasiveness
A base status that influences on how likely they are to dodge an incoming attack

#### Accuracy
The other side of Evasiveness. How likely they are to land an attack.

#### Luck
After confirming that the attack has hit the target, Luck influences the odds of it being a critical hit

#### Stamina
In earlier versions of the game - back in 2016 - I used to have characters with a Speed status and pick the attacking one by weighing an attacking probabily on both dweller's speed, however this showed to be extremely delicate to changes in their values and made the balancing very difficult.

#### Strength and Armor
Equivalent to physical attack and defense. When using a physical attack the damage will be calculated using the attacker's Strength and the defender's Armor plus modifiers.

#### Elemental Attack and Resilience
#### Magical attack and Aura
#### Naturality
Relates to how a dweller's status will change according to the enviroment. Some may gain regeneration, others a Strength boost etc.
#### Trait
Changes modifies the dwellers status or conditions given the context of the fight.
#### Affinity
#### Interactions
A matrix that outputs the modifier from said dweller to target dweller.

### Move's stats

#### Base damage
#### Critical chance
#### Falloff
#### Effectiveness
#### Secondary Effects



## TODO

- [ ] Add positions and mobility
- [ ] Actually implement movesets
- [ ] Make a decent damage function
- [ ] \*Add Naturality (more difficult than I thought)
- [x] Comment the code before I get lost in it 
- [ ] \*Add enviroment (will come with Naturality)
- [ ] \*Add ambient modifiers (will come with Naturality)
- [ ] Buffs and Debuff
- [ ] Status effects like poisoning etc
- [ ] \*Add customization (equip items etc)
- [ ] \*User actively interacts
- [ ] Code for the statistics and balancing
 

