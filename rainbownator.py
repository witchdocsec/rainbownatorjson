import hashlib
import json
import threading
from os.path import exists
import numpy as np
import argparse

def parser():
	parser = argparse.ArgumentParser(description="rainbownator args")
	parser.add_argument("--hash")
	parser.add_argument("--algo")
	parser.add_argument("--wlist")
	args = parser.parse_args()
	check_args(args)

table={}
def jsoncrack(jsonf, hashin):
	with open(jsonf,"r") as f:
		table=json.loads(f.read())
		print(f"from tables - {hashin} : {table[hashin]}")
		exit()

def crack(hashin, algo, passcomp):
	match algo:
		case "md5":
			hashtype=hashlib.md5
		case "sha1":
			hashtype=hashlib.sha1
		case "sha244":
			hashtype=hashlib.sha244
		case "sha256":
			hashtype=hashlib.sha256
		case "sha384":
			hashtype=hashlib.sha384
		case "sha512":
			hashtype=hashlib.sha512

	table[hashtype(passcomp.encode()).hexdigest()]=passcomp

	if hashtype(passcomp.encode()).hexdigest() == hashin:
		print(f"{hashin} : {passcomp}")

def split(a,n):
	return(np.array_split(a, n))

def check_args(args):
	if exists(f"{args.wlist}-{args.algo}.json"):
		jsoncrack(f"{args.wlist}-{args.algo}.json",args.hash)

	else:
		with open(args.wlist,"r") as wf:
			lines=wf.readlines()
		number=int(len(lines)/40)
		chunks=split(lines,number)
		for chunk in chunks:
			threads=[]
			for line in chunk:
				t=threading.Thread(target=crack, args=(args.hash, args.algo, line.replace("\n","")))
				threads.append(t)
				t.start()
			for t in threads:
				t.join()
		with open(f"{args.wlist}-{args.algo}.json","w") as f:
			f.write(json.dumps(table))

with open("banner.txt","r") as banner:
	print(banner.read())
try:
	parser()
except TypeError:
	print("usage: crack.py [-h] [--hash HASH] [--algo ALGO] [--wlist WLIST]")