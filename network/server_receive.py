import os
import json
import pickle
import shutil
import socket
import zipfile

from BFV import *
from utils import *
from BFV import BFV

CLIENT_ENC_PORT = 5000
CLIENT_DEC_PORT = 5001
CLIENT_IP_ADDRESS = '0.0.0.0'

# receive file from client
print("> Cloud Server\n")
print('receiving encrypted file from the client')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((CLIENT_IP_ADDRESS, CLIENT_ENC_PORT)) 
sock.listen(1)
conn, _ = sock.accept()
size = int(conn.recv(10).decode())

fo = open('datas/received/to_compute.zip', "wb") 
while size > 0:
    data = conn.recv(1024 * 1024 * 10)
    fo.write(data)
    size -= len(data)

conn.close()
sock.close()
fo.close()

# unzip received file
print("Unzipping the received file")
with zipfile.ZipFile('datas/received/to_compute.zip', 'r') as zip_ref:
    for member in zip_ref.namelist():
        filename = os.path.basename(member)
        if not filename:
            continue

        source = zip_ref.open(member)
        target = open(os.path.join('datas/received/unzip', filename), 'wb')
        with source, target:
            shutil.copyfileobj(source, target)

# parsing the file config file and init the operators
conf = dict()
with open("datas/received/unzip/config.json", mode="r") as config:
    conf = json.load(config)

print("initialising the evaluator with params")
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
with open("datas/received/unzip/pk.pkl", mode='rb') as fpk_in:
    Evaluator.pk = pickle.loads(fpk_in.read())

# compute the operations
print("Computing on encrypted datas")
enc_list = list()
enc_results = list()
with open("datas/received/unzip/datas.pkl", mode='rb') as fpdatas:
    enc_list = pickle.loads(fpdatas.read())
    for i in range(len(enc_list)):
        ct1 = enc_list[i][0]
        ct2 = enc_list[i][1]
        
        ct = Evaluator.HomomorphicAddition(ct1, ct2)
        enc_results.append(ct)

# save results
print("saving encrypted results")
with open("datas/results.pkl", mode='wb') as fp:
    pickle.dump(enc_results, fp)

# zip results
with zipfile.ZipFile("datas/results.zip", 'w') as zfp:
    zfp.write("datas/results.pkl", compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)