import matplotlib.pyplot as plt
from matplotlib.figure import Figure

x = list()
y = list()
with open("DepthAddition.txt", mode='r', encoding='utf-8') as fp:
    datas = fp.readlines()
    i = 0
    for line in datas:
        l = line.split()
        x.append(i)
        y.append(float(l[0]))
        i+=1

    fig = Figure(figsize=(13, 8), dpi=150)

    # tracé en fonction des paramètres choisis
    plot = fig.add_subplot(111)

    plot.plot(x, y, c='orange')
    plot.axhline(y=sum(y) / len(y), color='red', linestyle='--', linewidth=3, label='Average : {:.2f}iters'.format(sum(y) / len(y)))
    fig.suptitle("Profondeur du Schéma BFV Pour l'Opérateur Addition")
    fig.legend()
    plot.set_xlabel('Itérations')
    plot.set_ylabel("Profondeur")
    fig.savefig('HAdd_Depth.png', format='png')