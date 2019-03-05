# -*- coding: utf-8 -*-
import os
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
from io import open as open_unicode
import re
import numpy as np
from tokenizer.tokenizer import Tokenizer
import unicodedata
from collections import OrderedDict

import utils

normalize_special_mark = re.compile(u'(?P<special_mark>[\.,\(\)\[\]\{\};!?:“”\"\'\`\~\^\<\>])')
normalize_space = re.compile(u' +')

tokenizer = Tokenizer()
dm_single_close_quote = u'\u2019'  # unicode
dm_double_close_quote = u'\u201d'

DICT_EXTRACT = ['/dataTrungAnh/PreProcessingVietnamese/Data/BaoMoiTest/BaoMoi/BaoMoiExtract',
                '/dataTrungAnh/PreProcessingVietnamese/Data/BaoMoiTest/Vbee/VbeeExtract']
# DICT_EXTRACT = ['/dataTrungAnh/PreProcessingVietnamese/Data/BaoMoiTest/BaoMoi/BaoMoiExtract']

OUTPUT_DIR = '/dataTrungAnh/PreProcessingVietnamese/Data/BaoMoiTest/BaoMoiDataset/DataTrain'
DIR_OUT_TOKENIZER = OUTPUT_DIR + "/TokenizedDir"

if not os.path.exists(DIR_OUT_TOKENIZER):
    os.makedirs(DIR_OUT_TOKENIZER)


def fix_missing_period(line):
    """Adds a period to a line that is missing a period"""
    line = line.strip()
    if line == u'': return line
    if is_end_tokens(line[-1]): return line
    # print line[-1]
    return line + u' .'


def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)


END_TOKENS = {u'.': True, u'!': True, u'?': True, u'...': True, u"'": True,
              u"`": True, u'"': True, u'“': True, u'”': True,
              dm_single_close_quote: True, dm_double_close_quote: True, u")": True}


def is_end_tokens(token):
    try:
        _ = END_TOKENS[token]
        return True
    except:
        return False


def normalize_story(story_info):
    story_info = tokenizer.predict(story_info)
    story_info = normalize_special_mark.sub(u' \g<special_mark> ', story_info)
    story_info = normalize_space.sub(u' ', story_info)
    story_info = tokenizer.spliter.split(story_info)
    story_info = filter(lambda x: len(x.strip()) > 0, story_info)
    story_info = map(lambda x: fix_missing_period(x), story_info)
    story_info = u' '.join(story_info)
    # convert unicode to bytes string
    story_info = utils.safe_unicode(story_info)
    story_info = story_info.encode('utf-8')
    return story_info


def ExtractDataSetTokenized(listDir):
    # input is list file extract
    # outputDirectory = '/dataTrungAnh/PreProcessingVietnamese/Data/BaoMoiTest/BaoMoiDataset/DataTrain'
    dictOut = {}
    count = 0
    for directory in listDir:
        # directory là folder BaoMoi hoặc Vbee
        # dirs là list các folder trong folder BaoMoi hoặc Vbee
        dirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
        # k = 0
        for dir in dirs:
            ## onlyfiles: list file in (directory trong folder Bao Moi hoặc Vbee)
            onlyfiles = [f for f in listdir(directory + '/' + dir) if isfile(join(directory + '/' + dir, f))]
            # if not os.path.exists(outputDirectory):
            #     os.makedirs(outputDirectory)
            for i in range(len(onlyfiles)):
                ## for trên list các file
                document = directory + '/' + dir + '/' + onlyfiles[i]
                ## print(document)
                with open_unicode(document, 'r', encoding='utf-8') as myfilesnew:
                    # x = unicodedata.normalize('NFKC', x)
                    data = unicodedata.normalize('NFKC', myfilesnew.read())
                    data = data.split(u'\n')
                    ranger = len(data)
                    # if (len(data[0]) > 20 and len(data[0]) + 10 < len(data[1])):
                    # dirOut = outputDirectory + '/FinalTokenzied/'
                    # outputfile = dirOut + onlyfiles[i]
                    # print(outputfile)
                    # k += 1
                    flag = True
                    for h in range(0, ranger):
                        data[h] = normalize_story(data[h])
                        data[h] = data[h].lower()
                        data[h] = re.sub(u'https?:\/\/.*[\r\n]*', '', data[h], flags=re.MULTILINE)
                        data[h] = re.sub(u'\<a href', '', data[h])
                        data[h] = re.sub(u'["()|+=*!?:#$@\[\]]', '', data[h])
                        data[h] = re.sub(u'<br />', ' ', data[h])
                        data[h] = ' '.join(data[h].split())

                    print("Step " + str(count) + ", link: " + document)
                    ## print(outputfile + ", length: " + len(data[2]))
                    ##===========
                    ##count number of words
                    dictOut[count] = 0
                    for indexing, contenting in enumerate(data):
                        if indexing == 0 or indexing == 1:
                            continue
                        words = contenting.split()
                        dictOut[count] += len(words)
                    # ===========
                    ## dictOut[count] = len(data[2])
                    print("Step " + str(count) + " :" + str(dictOut[count]))
                    count += 1
                    # if not os.path.exists(dirOut):
                    #     os.makedirs(dirOut)
                    # outputfile = DIR_OUT_TOKENIZER + "/" + str(count)
                    outputfile = DIR_OUT_TOKENIZER + "/" + onlyfiles[i]
                    with open_unicode(outputfile, 'w+', encoding='utf-8') as writeFile:
                        for index, content in enumerate(data):
                            if index == ranger - 1:
                                # x = safe_unicode(content)
                                # x = unicodedata.normalize('NFKC', x)
                                try:
                                    x = unicode(content, encoding='utf-8')
                                    writeFile.write(x)
                                except:
                                    x = unicode(content, encoding='utf-8')
                                    writeFile.write(x)
                                    pass
                            else:
                                try:
                                    x = unicode(content, encoding='utf-8')
                                    x += u'\n'
                                    writeFile.write(x)
                                except:
                                    x = unicode(content, encoding='utf-8')
                                    x += u'\n'
                                    writeFile.write(x)
                                    pass
        # print(k)
    return dictOut


# def tokenizedd(x, buffer):
#     y = ViTokenizer.tokenize(x)
#     buffer.append(y)


def StatisticAndWireFile():
    dictoutt = ExtractDataSetTokenized(DICT_EXTRACT)
    average = sum(dictoutt.values()) / len(dictoutt)

    # dictFinal = {}
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
    print("average: " + str(average))



    setValueX = [value for key, value in dictoutt.items()]
    print("Max value: ", max(setValueX))
    print("Min value: ", min(setValueX))
    for key, value in dictoutt.items():
        if value < 500:
            dictFinal["<500"] += 1
        elif value < 1000:
            dictFinal[">=500 & <1000"] += 1
        elif value < 2000:
            dictFinal[">=1000 & <2000"] += 1
        elif value < 3000:
            dictFinal[">=2000 & <3000"] += 1
        elif value < 4000:
            dictFinal[">=3000 & <4000"] += 1
        elif value < 5000:
            dictFinal[">=4000 & <5000"] += 1
        elif value < 6000:
            dictFinal[">=5000 & <6000"] += 1
        elif value < 7000:
            dictFinal[">=6000 & <7000"] += 1
        elif value < 8000:
            dictFinal[">=7000 & <8000"] += 1
        elif value < 9000:
            dictFinal[">=8000 & <9000"] += 1
        elif value < 10000:
            dictFinal[">=9000 & <10000"] += 1
        elif value < 11000:
            dictFinal[">=10000 & <11000"] += 1
        elif value < 12000:
            dictFinal[">=11000 & <12000"] += 1
        elif value < 13000:
            dictFinal[">=12000 & <13000"] += 1
        elif value < 14000:
            dictFinal[">=13000 & <14000"] += 1
        elif value < 15000:
            dictFinal[">=14000 & <15000"] += 1
        elif value < 16000:
            dictFinal[">=15000 & <16000"] += 1
        elif value < 17000:
            dictFinal[">=16000 & <17000"] += 1
        elif value < 18000:
            dictFinal[">=17000 & <18000"] += 1
        elif value < 19000:
            dictFinal[">=18000 & <19000"] += 1
        elif value < 20000:
            dictFinal[">=19000 & <20000"] += 1
        elif value < 21000:
            dictFinal[">=20000 & <21000"] += 1
        else:
            dictFinal[">=21000"] += 1

    # dictFinalVer = dict(dictFinal)
    print("dictFinal: " + str(dictFinal))

    outputDirectory = OUTPUT_DIR
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)
    dictOutFile = outputDirectory + "/" + "DictCount.txt"
    print(dictoutt)
    print("Link file statistic: " + dictOutFile)
    with open_unicode(dictOutFile, 'w+', encoding='utf-8') as writeFile:
        writeFile.write("\n######\nStatistic Final\n" + unicode(dictFinal) + "\n######\nMin-Max value\n" +
                        "Max value: " + unicode(max(setValueX)) +
                        "\nMin value: " + unicode(min(setValueX)))
    plot_bar_x(dictFinal)


def plot_bar_x(dictOutput):
    setValue = [value for key, value in dictOutput.items()]
    print(str(setValue))
    setIndex = [key for key, value in dictOutput.items()]
    print(str(setIndex))
    index = np.arange(len(setIndex))
    plt.bar(index, setValue)
    plt.xlabel('Size', fontsize=5)
    plt.ylabel('Number of articles', fontsize=5)
    plt.xticks(index, setIndex, fontsize=5, rotation=30)
    plt.title('Statistic Vietnamese Data')
    plt.show()


StatisticAndWireFile()
