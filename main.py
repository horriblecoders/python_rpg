import random
import time

#Class for all player and hostile characters
class Character:
    def __init__(self, name):

        No_Armor = Armor('None',0,0)
        Fists = Weapon('Fists', '1')

        self.name = name
        self.weapon = Fists
        self.armor = No_Armor
        self.food = []
        self.base_health = 10
        self.health = self.base_health + self.armor.bonus
        self.money = 0

    def give_money(self,amount):
        self.money += amount

    def fight(self):
        #Choose an enemy
        try:
            enemy = random.choice(self.opponents)

            #Hit enemy
            if self.health > 0:
                self.weapon.use(enemy)
            if enemy.health <= 0:
                print(self.name,'killed',enemy.name,'and looted',enemy.money,'gold!')
                self.money += enemy.money
                enemy.money = 0
                self.opponents.remove(enemy)
        except:
            #Something died and there are no enemies to choose from
            pass

    def heal(self,amount= -1):
        if amount == -1:
            self.health = self.base_health + self.armor.bonus
            print(self.name,'Fully Healed!')
        else:
            self.health += amount
            if self.health > self.base_health + self.armor.bonus:
                self.health = self.base_health + self.armor.bonus

#Class for all weapons
class Weapon:
    def __init__(self,name,damage='1d4',value=0):
        self.name = name
        self.damage = damage
        self.value = value

    def use(self,target):
        rolled_damage = roll(self.damage)
        target.health -= rolled_damage
        print(target.name,'is dealt',rolled_damage,'and has',max(target.health,0),'hitpoints remaining!')

#Class for all armor
class Armor:
    def __init__(self,name,bonus,value):
        self.name = name
        self.bonus = bonus
        self.value = value

#Class for all food
class Food:
    def __init__(self,name,healing,value):
        self.name = name
        self.healing = healing
        self.value = value

#Store to buy and sell items
class Store:
    def __init__(self):
        self.weapons = []
        self.armor = []
        self.food = []

        #Create weapons
        Sword = Weapon('Sword', '1d6',50)
        Long_Sword = Weapon('Long Sword','1d8',100)
        Magic_Sword = Weapon('Magic Sword','2d8',500)
        Sacred_Sword = Weapon('Sacred Sword','4d8',3000)
        self.weapons += Sword,Long_Sword,Magic_Sword,Sacred_Sword

        #Create armor
        Cloth_Armor = Armor('Cloth Armor',5,25)
        Leather_Armor = Armor('Leather Armor',15,100)
        Iron_Armor = Armor('Iron Armor',30,300)
        Magic_Armor = Armor('Magic Armor',100,1500)
        self.armor += Cloth_Armor,Leather_Armor,Iron_Armor,Magic_Armor

        #Create Food
        Bread = Food('Bread',5,10)
        Lobster = Food('Lobster',14,30)
        self.food += Bread,Lobster

    def replace_item(self, item, field, append=False):
        if not append:
            if getattr(self.customer,field).value//2 + self.customer.money >= item.value:
                print("Are you sure you want to replace your",getattr(self.customer,field).name,'with',item.name + '?')
                x = input()
                if x == 'y' or x == 'yes':
                    self.customer.money += getattr(self.customer,field).value//2
                    self.customer.money -= item.value
                    setattr(self.customer, field, item)
                    print("Bought", item.name + '!')
            else:
                print("You don't have enough gold!")
        else:
            if self.customer.money >= item.value:
                self.customer.money -= item.value
                getattr(self.customer, field).append(item)
                print("Bought", item.name + '!')
            else:
                print("You don't have enough gold!")

    def buy(self):
        print('{:20}'.format('Weapon Name'), '{:>7}'.format('Damage'), '{:>10}'.format('Cost'))
        for weapon in self.weapons:
            print('{:20}'.format(weapon.name), '{:>7}'.format(weapon.damage), '{:>10}'.format(weapon.value))
        print('{:20}'.format('Armor Type'), '{:>7}'.format('Armor'), '{:>10}'.format('Cost'))
        for armor in self.armor:
            print('{:20}'.format(armor.name), '{:>7}'.format(armor.bonus), '{:>10}'.format(armor.value))
        print('{:20}'.format('Food Type'), '{:>7}'.format('HP Gain'), '{:>10}'.format('Cost'))
        for food in self.food:
            print('{:20}'.format(food.name), '{:>7}'.format(food.healing), '{:>10}'.format(food.value))

    def view_inv(self):
        print('{:20}'.format('Weapon Name'), '{:>7}'.format('Damage'), '{:>10}'.format('Trade-in'))
        print('{:20}'.format(self.customer.weapon.name), '{:>7}'.format(self.customer.weapon.damage),
              '{:>10}'.format(self.customer.weapon.value // 2))
        if self.customer.armor.name != 'None':
            print('{:20}'.format('Armor Type'), '{:>7}'.format('Armor'), '{:>10}'.format('Trade-in'))
            print('{:20}'.format(self.customer.armor.name), '{:>7}'.format(self.customer.armor.bonus),
                  '{:>10}'.format(self.customer.armor.value // 2))
        if self.customer.food != []:
            print('{:20}'.format('Food Type'), '{:>7}'.format('HP Gain'), '{:>10}'.format('Value'))
            for food in self.customer.food:
                print('{:20}'.format(food.name), '{:>7}'.format(food.healing),
                      '{:>10}'.format(food.value // 2))

    def view_gold(self):
        print("You have", self.customer.money, 'gold.')

    def shop(self):
        shopping = True

        while shopping:

            command = input("Do you want to buy, view inventory, or leave?")

            # List items available to buy
            if command.lower() == 'b' or command.lower() == 'buy':
                self.buy()

            #View inventory
            elif command.lower() == 'v' or command.lower() == 'view' or command.lower() == 'view inventory':
                self.view_inv()

            #Leave the shop
            elif command.lower() == 'l' or command.lower() == 'leave':
                shopping = False

            #Show the players gold
            elif command.lower() == 'bal' or command.lower() == 'balance':
                self.view_gold()

            #Handle buy commands
            else:
                command = command.split(' ', 1)
                if command[0].lower() == 'b' or command[0].lower() == 'buy':
                    for weapon in self.weapons:
                        if weapon.name.lower() == command[1].lower():
                            self.replace_item(weapon, "weapon")
                    for armor in self.armor:
                        if armor.name.lower() == command[1].lower():
                            self.replace_item(armor, "armor")
                    for food in self.food:
                        if food.name.lower() == command[1].lower():
                            self.replace_item(food, "food", append=True)


#Used to roll dice to calculate damage and other random events
def roll(dice_str):
    if dice_str.isdigit():
        return int(dice_str)
    dice_num = int(dice_str[:dice_str.find('d')])
    dice_sides = int(dice_str[dice_str.find('d')+1:])
    output = 0
    for die in range(dice_num):
        output += random.randint(1,dice_sides)
    return output

#Used to battle two teams of characters
def battle(team1,team2):
    turn = 1
    for team_member in team1:
        team_member.opponents = team2
    for team_member in team2:
        team_member.opponents = team1
    while any(team_member.health > 0 for team_member in team1) > 0 and any(enemy.health > 0 for enemy in team2):
        print('Starting turn',turn)
        for team_member in team1:
            team_member.fight()
        for enemy in team2:
            enemy.fight()
        print('Ending turn',turn)
        turn += 1

#Handle character creation and loading saved characters
def set_up_player():
    file = False
    #File IO goes here
    if not file:
        print("No save file found.")
        pname = input("Name your character:")
        Player = Character(pname)
        Player.give_money(10)
        return Player

#I should probably make arena a class
class Arena:
    def __init__(self):
        self.round = 1

    def round1(self):
        Bat = Character('Bat')
        Bat2 = Character('Bat')
        Claws = Weapon('Claws', '1d2')
        Bat.weapon = Claws
        Bat2.weapon = Claws
        enemies = [Bat,Bat2]
        battle([self.player],enemies)
        if self.player.health > 0:
            print("You beat the first round of the arena and earned 100 gold!")
            self.player.give_money(100)
            self.round += 1
    def round2(self):
        print('Round 2 of arena is not yet implemented.')
    def round3(self):
        pass
    def boss_fight(self):
        pass

    def fight(self):
        if self.round == 1:
            self.round1()
        elif self.round == 2:
            self.round2()
        elif self.round == 3:
            self.round3()
        elif self.round == 4:
            self.boss_fight()

def main():
    Player = set_up_player()
    General_Store = Store()
    Fight_Arena = Arena()
    Fight_Arena.player = Player
    General_Store.customer = Player

    playing = True
    while playing:
        var = input("What do you want to do? (Arena,Shop,Work,Inn,Quit)")
        if var.lower() == 'arena' or var.lower() == 'a':
            Fight_Arena.fight()
        elif var.lower() == 'shop' or var.lower() == 's':
            General_Store.shop()
        elif var.lower() == 'inn' or var.lower() == 'i':
            print('You travel to the inn and rest...')
            time.sleep(1)
            Player.heal()
        elif var.lower() == 'work' or var.lower() == 'w':
            jobs = ['Woodcutting','Mining']
            work_time = input("How many minutes would you like to work? (10gp per minute)")
            work_time = int(work_time) * 60
            job = random.choice(jobs)
            print('You go',job)
            print('Working...')
            time.sleep(work_time)
            Player.give_money(int(work_time/60*10))
            print('Worked',int(work_time/60),'minutes and gained',int(work_time/60*10),'gold!')

        elif var.lower() == 'quit' or var.lower() == 'q':
            playing = False
    #save game


if __name__ == '__main__':
    main()
