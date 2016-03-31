from quest import System, import_all_quest_hooks


import_all_quest_hooks()


with open('./big.txt', 'rt') as source:
    sys = System(filter(lambda line: len(line.strip()), source))

    data = sys.run()
    print(data['statistics'])