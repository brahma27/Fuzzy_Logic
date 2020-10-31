import csv 

def baca_file(): #membaca file influencers.csv
    file = open('influencers.csv')
    data = csv.reader(file)
    fol = []
    eng = []
    next(data)
    for line in data:
        fol.append(float(line[1]))
        eng.append(float(line[2]))
    return fol,eng

def sedikit(x,a,b): #fungsi untuk menghitung keanggotaan pada follower dan engagement dengan bagian sedikit/rendah
    hasil = 0
    if (x>b):
        hasil = 0
    elif(x<=a):
        hasil = 1
    elif(x>a) and (x<=b):
        hasil = (b-x)/(b-a)
    return hasil

def sedang(x,a,b,c,d): #fungsi untuk menghitung keanggotaan pada follower dan engagement dengan bagian sedang/cukup
    hasil =0
    if (x<= a) or (x>d):
        hasil = 0
    elif(x>b) and (x<=c):
        hasil = 1
    elif(x>a) and (x<b): #untuk menghitung segitiga banyak
        hasil = (x-a)/(b-a)
    elif(x>c) and (x<=d): #untuk menghitung segitiga sedikit
        hasil = (d-x)/(d-c)
    return hasil

def banyak(x,c,d): #fungsi untuk menghitung keanggotaan pada follower dan engagement dengan bagian banyak/tinggi
    hasil=0
    if (x<= c):
        hasil = 0
    elif(x>d):
        hasil = 1
    elif(x>c) and (x<=d):
        hasil = (x-c)/(d-c)
    return hasil

def keanggotaan_follower(x): # fungsi keanggotaan follower dengan di bagi menjadi 3 bagian sedikit, sedang, banyak
    aT = 8000
    bT = 25000
    cT = 50000
    dT = 76000

    sedikitt = sedikit(x,aT,bT)
    sedangg = sedang(x,aT,bT,cT,dT)
    banyakk = banyak(x,cT,dT)
    return [sedikitt,sedangg,banyakk]

def keanggotaan_engagement(y): # fungsi keanggotaan engagement rate dibagi menjadi 3 bagian rendah, cukup, tinggi
    aT = 1.5
    bT = 3.8
    cT = 5.5
    dT = 7.5

    rendah = sedikit(y,aT,bT)
    cukup = sedang(y,aT,bT,cT,dT)
    tinggi = banyak(y,cT,dT)
    return [rendah,cukup,tinggi]

def output_inferensi(): #rule dalam menentukan inferensi
    engagement = ['rendah','cukup','tinggi']
    follower = ['sedikit','sedang','banyak']
    hasil= []
    if(engagement[0]=='rendah') and (follower[0]=='sedikit'):
        k1 = 'ditolak'
    if(engagement[0]=='rendah') and (follower[1]=='sedang'):
        k2 = 'ditolak'
    if(engagement[0]=='rendah') and (follower[2]=='banyak'):
        k3 = 'dipertimbangkan'
    if(engagement[1]=='cukup') and (follower[0]=='sedikit'):
        y1 = 'ditolak'
    if(engagement[1]=='cukup') and (follower[1]=='sedang'):
        y2 = 'dipertimbangkan'
    if(engagement[1]=='cukup') and (follower[2]=='banyak'):
        y3= 'diterima'

    if(engagement[2]=='tinggi') and (follower[0]=='sedikit'):
        j1 = 'dipertimbangkan'
    if(engagement[2]=='tinggi') and (follower[1]=='sedang'):
        j2 = 'diterima'
    if(engagement[2]=='tinggi') and (follower[2]=='banyak'):
        j3 = 'diterima'
        hasil.append(k1)
        hasil.append(k2)
        hasil.append(k3)
        hasil.append(y1)
        hasil.append(y2)
        hasil.append(y3)
        hasil.append(j1)
        hasil.append(j2)
        hasil.append(j3)
    return hasil
    
# fuzzy rule
#--------------------------------------------------------------------------------#
# engagement\follower |       sedikit     |     sedang        |   banyak         #
#--------------------------------------------------------------------------------#
#    rendah           |   ditolak         |  ditolak          |  dipertimbangkan #
#    cukup            |   ditolak         |  dipertimbangkan  |  diterima        #
#    tinggi           |   dipertimbangkan |  diterima         |  diterima        #
#--------------------------------------------------------------------------------#
def nilai_inferensi(follower,engagement): #fungsi menentuka nilai inferensi yang nilainya akan digunakan pada fungsi defuzzyficatin dengan metode sugeno
    hasil = []
    x = follower
    y = engagement
    for i in x:
        for j in y:
            if(i<j): #membandingkan nilainya apakah i lebih kecil dari j
                hasil.append(i) #menyimpan i karena lebih kecil 

            else:
                hasil.append(j) # menyimpan j karena j lebih kecil dari i
    ditolak1 = (hasil[0])
    ditolak2 = (hasil[1])
    ditolak3 = (hasil[3])
    ditolak = (max(ditolak1,ditolak2,ditolak3)) #mengambil nilai max dari inferensi ditolak

    dipertimbangkan1 = (hasil[2])
    dipertimbangkan2 = (hasil[4])
    dipertimbangkan3 = (hasil[6])
    dipertimbangkan = (max(dipertimbangkan1,dipertimbangkan2,dipertimbangkan3)) #mengambil nilai max dari inferensi dipertimbangkan

    diterima1 = (hasil[5])
    diterima2 = (hasil[7])
    diterima3 = (hasil[8])
    diterima = (max(diterima1,diterima2,diterima3)) #mengambil nilai max dari inferensi diterima
    
    return ditolak,dipertimbangkan,diterima #mendapatkan hasil inferensi ditolak, dipertimbangkan, dan diterima

#keanggotaan fuzzy model sugeno
#
#       ditolak  dipertimbangkan    diterima
#  1 |     |           |               |
#    |     |           |               |
#0.5 |     |           |               |
#    |     |           |               |
#  0 |_____|___________|_______________|____
#        40           70               95   

def defuzzyfication (m,y,n): #defuzzyfication sugeno
    nilai = 0
    x = (m*40) + (y*70) + (n*95)
    y = (m+y+n)
    nilai = (x/y)
    return nilai

def simpan(tampung): #fungsi untuk menyimpan hasil outputan ke dalam csv denga nama file chose.csv
    tampung = tampung
    pilihan = open('chosen.csv', 'w')
    jaw = csv.writer(pilihan, lineterminator='\n')
    for data in tampung:
            jaw.writerow([data])

#------------------------------------------MAIN PROGRAM----------------------------------------------------

tes,coba = baca_file()
jawaban = []
for i in range(0,len(tes)):
    hasil_follower = keanggotaan_follower(tes[i])
    hasil_engagement = keanggotaan_engagement(coba[i])
    j,k,l = nilai_inferensi(hasil_follower,hasil_engagement)
    hasil_defuzy = defuzzyfication(j,k,l)
    jawaban.append([hasil_defuzy,i])
    jawaban.sort(reverse=True) #melakukan sorting dengan nilai yang terbesar hingga terkecil
tampung = []
for i in range (0,20):
    tampung.append(jawaban[i][1])
    print('nomor record : ',jawaban[i][1],' hasil :',jawaban[i][0])
simpan(tampung)