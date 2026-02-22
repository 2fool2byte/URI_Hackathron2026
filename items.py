class Potion:
    def __init__(self, name, p_type, amount, price):
        self.name = name
        self.p_type = p_type
        self.amount = amount
        self.price = price
    
    def consume(self, player):
        if "health" in self.p_type.casefold():
            player.health += self.amount

        elif "mana" in self.p_type.casefold():
            player.mana += self.amount

shealth_potion = Potion("Small Health Potion", "Health", 15, 5)
mhealth_potion = Potion("Medium Health Potion", "Health", 30, 10)
lhealth_potion = Potion("Large Health Potion", "Health", 60, 20)

smana_potion = Potion("Small Mana Potion", "Mana", 15, 5)
mmana_potion = Potion("Medium Mana Potion", "Mana", 30, 10)
lmana_potion = Potion("Large Mana Potion", "Mana", 60, 20)

potions = [shealth_potion, mhealth_potion, lhealth_potion, smana_potion, mmana_potion, lmana_potion]