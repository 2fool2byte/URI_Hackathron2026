class Character:
    def __init__(self, name, weakness, immunity, health, max_health, attacks):
        self.name = name
        self.weakness = weakness
        self.immunity = immunity
        self.health = health
        self.max_health = max_health
        self.attacks = attacks

    def attackAction(self, target, attack_name):
        if attack_name is None:
            attack_name, attack_info = list(self.attacks.items())[0]
        else:
            attack_info = self.attacks[attack_name]

        damage = attack_info["damage"]
        element = attack_info["element"]

        return target.takeDamage(damage, element)

    def isAlive(self):
        return self.health > 0
    
    def takeDamage(self, damage, element):
        if element.casefold() == self.weakness.casefold():
            damage = damage * 1.3
        elif element.casefold() == self.immunity.casefold():
            return "Immune"
        
        damage = int(damage)
        self.health -= damage

        self.health = max(self.health, 0)

        return damage


class Boss(Character):
    def heal(self, amount):
        if self.health <= 0:
            return 0
        self.health += amount
        self.health = min(self.health, self.max_health)
        return amount