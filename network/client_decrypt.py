import os
import json
import pickle
import shutil
import socket
import zipfile
import pandas as pd

from BFV import *
from BFV import BFV
from utils import *

SERVER_PORT = 5000
SERVER_IP_ADDRESS = '0.0.0.0'

# load config file
conf = dict()
with open("config.json", mode="r") as config:
    conf = json.load(config)

t = conf['t'];   n, q, psi = conf['n'], conf['q'], conf['psi']
psiv= modinv(psi,q)
w   = pow(psi,2,q)
wv  = modinv(w,q)
mu, sigma = conf['mu'], conf['sigma']
T = conf['T']
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

# init the evaluator
Evaluator = BFV(n, q, t, mu, sigma, qnp)

# load secret key
with open("datas/encrypted/sk.pkl", mode='rb') as fsk_in:
    Evaluator.sk = pickle.loads(fsk_in.read())

# load public key
with open("datas/encrypted/pk.pkl", mode='rb') as fpk_in:
    Evaluator.pk = pickle.loads(fpk_in.read())

# receive file from client
print("> Client \n")
print('receiving encrypted results from cloud server')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((SERVER_IP_ADDRESS, SERVER_PORT)) 
sock.listen(1)
conn, _ = sock.accept()
size = int(conn.recv(10).decode())

fo = open('datas/results/results.zip', "wb") 
while size > 0:
    data = conn.recv(1024 * 1024 * 10)
    fo.write(data)
    size -= len(data)

conn.close()
sock.close()
fo.close()

#unzip results
with zipfile.ZipFile('datas/results/results.zip', 'r') as zip_ref:
    for member in zip_ref.namelist():
        filename = os.path.basename(member)
        if not filename:
            continue

        source = zip_ref.open(member)
        target = open(os.path.join('datas/results', filename), 'wb')
        with source, target:
            shutil.copyfileobj(source, target)


# load results
enc_results = list()
with open('datas/results/results.pkl', mode='rb') as fp:
    enc_results = pickle.loads(fp.read())

results = list()
for i in range(len(enc_results)):
    ct = enc_results[i]
    mt = Evaluator.Dechiffrer(ct)
    r = Evaluator.IntDecode(mt)
    results.append(r)

# writing results
with open("datas/datas.csv", mode='r', encoding='utf-8') as fpdata:
    df = pd.read_csv(fpdata, sep='\t')
    df = df.head(len(results))
    df['salaire_final'] = results
    df.to_csv("datas/results/final.csv", encoding='utf-8')