import json
import random

with open("C:/Users/pc/Desktop/python/NatachaGen/out.json", encoding='utf-8', mode='r') as fp:
    data = json.load(fp)

    with open("datas/datas.csv", mode='w', encoding='utf-8') as fp1:
        fp1.write("nom\temail\tsalaire\tprime\n")
        for pers in data["results"]:
            fp1.write(f"{pers['full name']}" + f"\t{pers['email']}" + f"\t{round(random.randint(50_000, 1_000_000) / 100_000) * 100_000}" + f"\t{round(random.randint(10_000, 50_000) / 10_000) * 10_000}\n")