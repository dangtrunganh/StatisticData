from collections import OrderedDict

dictFinal = OrderedDict()
dictFinal["<500"] = 0
dictFinal[">=500 & <1000"] = 0
dictFinal[">=1000 & <2000"] = 0
dictFinal[">=2000 & <3000"] = 0
dictFinal[">=3000 & <4000"] = 0
dictFinal[">=4000 & <5000"] = 0
dictFinal[">=5000 & <6000"] = 0
dictFinal[">=6000 & <7000"] = 0
dictFinal[">=7000 & <8000"] = 0
dictFinal[">=8000 & <9000"] = 0
dictFinal[">=9000 & <10000"] = 0
dictFinal[">=10000 & <11000"] = 0
dictFinal[">=11000 & <12000"] = 0
dictFinal[">=12000 & <13000"] = 0
dictFinal[">=13000 & <14000"] = 0
dictFinal[">=14000 & <15000"] = 0
dictFinal[">=15000 & <16000"] = 0
dictFinal[">=16000 & <17000"] = 0
dictFinal[">=17000 & <18000"] = 0
dictFinal[">=18000 & <19000"] = 0
dictFinal[">=19000 & <20000"] = 0
dictFinal[">=20000 & <21000"] = 0
dictFinal[">=21000"] = 0
# print("average: " + str(average))
print dictFinal
setValue = [value for key, value in dictFinal.items()]
print(str(setValue))
setIndex = [key for key, value in dictFinal.items()]
print(str(setIndex))
# dictFinalVer = dict(dictFinal)
# print("dictFinal: " + str(dictFinalVer))
