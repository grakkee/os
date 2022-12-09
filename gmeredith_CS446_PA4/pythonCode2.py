#Grace Meredith
#CS446 PA4
#Create a Dockerfile & Certificate
#Due: 2 May 2022

#Set up a docker environment for this code, and don't try to include superfluous packages!
from PIL import Image, ImageDraw
import csv
from scipy import constants
import numpy as np
import os
import socket
from OpenSSL import crypto, SSL
from pprint import pprint
from time import gmtime, mktime
from os.path import exists, join

def certificate():
    CName = "gmeredith_selfSignedCertificate.crt"
    CFile = "%s.crt" % CN
    KFile = "%s.key" % CName
    CF = join(".", CFile)
    KF = join(".", KFile)
    if not exists(CF) or not exists(KF):
        cmd = "openssl rsa -in gmeredith_privatekey.key -pubout -out gmeredith_publickey.key"
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)
        
        cert = crypto.X509()
        cert.get_subject().C = "US"
        cert.get_subject().ST = "NV"
        cert.get_subject().L = "Reno"
        cert.get_subject().O = "University of Nevada, Reno"
        cert.get_subject().OU = "CSE"
        cert.get_subject().CN = socket.gethostname()
        cert.set_serial_number(42)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(157800000)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha512')

        open(C_F, "wb").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        open(K_F, "wb").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

        os.system(cmd)

def image():
    color = 128 * np.ones(shape=[3], dtype=np.uint8)
    tuplevals = tuple(color)
    im = Image.new('RGB', (512, 512), tuplevals)
    draw = ImageDraw.Draw(im)
    draw.rectangle((200, 100, 300, 200), fill=(0, 192, 192), outline=(255, 255, 255))
    draw.text((100, 200), "You did it!", fill=(int(constants.speed_of_light), 0, 0))
    im.save( "pythonCode2Image.png")

    try:
        with open('temp.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
    except:
        pass

def main():
    image()
    certificate()

if __name__ == "__main__":
    main()

#modify this code so that it also generates self signed certificate and keys