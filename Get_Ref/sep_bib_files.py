import os,sys
import zipfile

import extract_refs

seed="/media/beingcooper/New Volume/xyz"

for f1 in os.listdir(seed):
    in1 = seed+str("/" + f1)

    for f2 in os.listdir(in1):
        bib_available = False
        in2 = in1 + str("/" + f2)
        item_count = len(os.listdir(in2))
        try:
            f3 = os.listdir(in2)[0]
        except:
            continue

        in3 = (in2 + str("/" + f3)).replace(".zip","")

        if item_count == 1:
            with zipfile.ZipFile(in2+"/"+f3,"r") as zeep:
                os.makedirs(in3)
                zeep.extractall(in3)
        print in3

        for f4 in os.listdir(in3):
                if f4.lower().endswith(".bbl"):
                    bib_available = True
                    with open(in3+ '/' +f4) as f:
                        text = f.read()
                    break

        if not bib_available:
            for f4 in os.listdir(in3):
                if f4.lower().endswith(".tex"):
                    with open(in3+ '/' +f4) as f:
                        text = f.read()
                    break

        extract_refs.lets_hit_it(text)







