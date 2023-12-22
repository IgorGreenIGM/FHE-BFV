import os
import csv
import pickle
import socket
import zipfile
import pandas as pd
from time import sleep
from zipfile import ZipFile

SERVER_PORT = 5000
SERVER_IP_ADDRESS = '192.168.56.105'

# custom modules
from BFV import *
from utils import *
from BFV import BFV

#init the encrypter
print('initialising the encrypter')
t = 16;   n, q, psi = 1024, 132120577, 73993
psiv= modinv(psi,q)
w   = pow(psi,2,q)
wv  = modinv(w,q)
mu, sigma = 0, 0.5 * 3.2
T = 256
p = q**3 + 1
w_table    = [1]*n
wv_table   = [1]*n
psi_table  = [1]*n
psiv_table = [1]*n
for i in range(1,n):
    w_table[i]    = ((w_table[i-1]   *w)    % q)
    wv_table[i]   = ((wv_table[i-1]  *wv)   % q)
    psi_table[i]  = ((psi_table[i-1] *psi)  % q)
    psiv_table[i] = ((psiv_table[i-1]*psiv) % q)
qnp = [w_table,wv_table,psi_table,psiv_table]


#generate pk and sk
print('Generating pblic key and private key')
Evaluator = BFV(n, q, t, mu, sigma, qnp)
Evaluator.GenererCleSecrete()
Evaluator.GenererClePublique()
Evaluator.EvaluerGenererCleV1(T)


# saving keys
print('saving public key')
with open("datas/encrypted/pk.pkl", mode="wb") as fpk:
    pickle.dump(Evaluator.pk, fpk)

print('saving private key')
with open("datas/encrypted/sk.pkl", mode="wb") as fsk:
    pickle.dump(Evaluator.sk, fsk)


# reading data file and encrypting
print('Encrypting operands and saving\n')
with open("datas/datas.csv", mode='r', encoding='utf-8') as fpdata:
    df = pd.read_csv(fpdata, sep='\t')
    enc_list = list()

    for i in range(100): #range(len(df)):
        n1 = df['salaires'][i]; n2 = df['primes'][i]
        m1 = Evaluator.IntEncode(n1); m2 = Evaluator.IntEncode(n2)
        e1 = Evaluator.Chiffrer(m1); e2 = Evaluator.Chiffrer(m2)
        
        enc_list.append((e1, e2))

    print("Saving encrypted datas")
    with open("datas/encrypted/datas.pkl", mode='wb') as fp:
        pickle.dump(enc_list, fp)


# zip and send to the cloud server
with ZipFile("datas/to_compute.zip", 'w') as zfp:
    zfp.write("config.json", compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    for file in os.listdir("datas/encrypted"):
        if file == "sk.pkl":
            continue
        zfp.write("datas/encrypted/" + file, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


# send file to cloud server
print("Sending encrypted file to the cloud server")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.connect((SERVER_IP_ADDRESS, SERVER_PORT))   
while True: 
    filename = 'datas/to_compute.zip'
    size = os.path.getsize(filename)
    sock.send(f'{size}'.encode())
    try: 
        fi = open(filename, "rb") 
        data = fi.read()
        if not data:
            break
        else:
            sock.sendall(data)
            break
        fi.close()

    except IOError: 
        break