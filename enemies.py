class Enemies:
    def __init__(self, name, weakness, immunity, health, attack, element):
        self.name = name
        self.weakness = weakness
        self.attack = attack
        self.health = health
        self.element = element
        self.immunity = immunity

    def attackAction(self, player):
        return player.takeDamage(self.attack, self.element)

    def isAlive(self):
        return self.health > 0
    
    def takeDamage(self, damage, element):
        if self.weakness.casefold() in element.casefold():
            self.health -= damage * 1.3
        elif self.immunity.casefold() in self.element.casefold():
            return "Immune"
        else:
            self.health -= damage



enemies = []

fslime = Enemies("Fire Slime", "Water", "Grass", 40, 5, "Fire")
wslime = Enemies("Water Slime", "Grass", "Fire", 40, 5, "Water")
gslime = Enemies("Grass Slime", "Fire", "Water", 40, 5, "Grass")


fspirit = Enemies("Fire Spirit", "Water", "Grass", 70, 15, "Fire")