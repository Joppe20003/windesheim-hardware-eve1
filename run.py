from Modules.main import Main

verwerkings_snelheid = int(input("Voer de verwerkings snelheid in: "))
aankomst_snelheid_interval = int(input("Voer de aankomst snelheid interval in: "))
capiciteit = int(input("Voer de capaciteit in: "))
com = str(input("Voer de com poort voor de arduino: "))

main = Main(aankomst_snelheid_interval, verwerkings_snelheid, capiciteit, com)

main.start()