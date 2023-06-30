def batalha(player, inimigo):
    morteInimigo = False
    while not morteInimigo:
        inimigo.attack(player)
        print(inimigo.name + " atacou " + player.name + " que ficou com " + str(player.health) + " de vida.\n")

        if player.died():
            print(player.name + " morreu!\n")
            input()
            return player

        player.attack(inimigo)
        print(player.name + " atacou " + inimigo.name + " que ficou com " + str(inimigo.health) + " de vida.\n")

        if inimigo.died():
            print(inimigo.name + " foi morto!\n\n")
            morteInimigo = True
            break

    return player
