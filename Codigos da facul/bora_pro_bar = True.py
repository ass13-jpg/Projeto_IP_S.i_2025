agua = input('Você quer água com gás ou sem gás? ')

if agua == 'com gás' or agua == 'gás':
    print('Você terá que pagar R$2,50')
elif agua == 'sem gás' or agua == 'natural':
    print('Você terá que pagar R$1,50')
elif agua != '':
    print()
else:
    print()