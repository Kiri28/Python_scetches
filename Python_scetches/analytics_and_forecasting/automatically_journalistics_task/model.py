import random as rand
import csv
import numpy as np
import pandas as pd
from collections import Counter, OrderedDict
import re
import urllib.request


# Let's create our class

    @classmethod
    def __init__(self):
        # Read the news, and if it has such words as "доллар" and "курс" or "доллар" and "евро"..
        # ..that's we are including them in our list
        starter_list = [] # words list, that can start a new item.
        data = ''
        if __name__ == "__main__":
            csv_path = "lenta-ru-news.csv"
            with open(csv_path, "r") as f_obj:
                reader = csv.reader(f_obj)
                for row in reader:
                    if (('курс ' in row[1]) and ('доллар' in row[1])) or 
                    (('курс ' in row[1]) and ('евро' in row[1])):
                        data+=' '+row[1]
                        starter_list.append((row[1].split(' '))[0])

        # Now, let's try to parse the data from exchange's daily data
        link = urllib.request.urlopen('http://www.cbr.ru/scripts/XML_daily.asp')
        l = str(link.readlines()[0])
        self.data = data
        self.l = l
        self.starter_list = starter_list
        Currence_dict = self.currency_finder(self)
        self.Currence_dict = Currence_dict

        # Manual words list
        badlist = ['поднял', 'упал', "вырос", "повысил", "понизил", 
                   "снизился", "уронил", "опустил", "поднялся", "превысил", "опустился"]

        scn = 0
        while scn < 7:
            # first attempt
            marker = 0
            sentense = []
            sentense.append(self.random_choice_starter(self))
            for i in range(10):

                # Let's make the prohibition for program to creating new sentences in old ones
                cac = 0
                if sentense[-1] != '':
                    rand_word = self.random_choice_word(sentense[-1])
                    # While words from our list occur more then one time
                    # While there are words from startwords -list   
                    while (rand_word in self.news_starter(self)) or 
                    (len(set(sentense + [rand_word])) - 
                     len(set(sentense + [rand_word]) - set(badlist)) >= 2):
                        rand_word = self.random_choice_word(sentense[-1])
                        cac += 1
                        # If we can't find any useful variants
                        if cac > 100:
                            break
                    # Checking algo by circularity and finish words
                    if cac>100 or rand_word == '-1':
                        marker = 1
                        break
                    sentense.append(rand_word)

            # If all of limitations passed, we can public the news
            lean = len(set(sentense + [rand_word])) - len(set(sentense + [rand_word]) - set(badlist))
            if len(sentense) > 4 and marker == 0 and lean < 2 and lean > 0:
                solid = self.sent_decomposition(self, ' '.join(sentense))
                if solid != '-1':
                    print(solid)
                    scn += 1

# ____next_section__________________________________


    # Take ever word and building a wordslist which can staying after them
    # Reading all data for this, and if finding my word, checking which word was after them
    # But, if we have dot after sentence, we are stopping

    @staticmethod
    def sm(self, trigger):

        result = []
        words_list = self.data.replace('\xa0', ' ').split(' ')
        trig = False
        for word in words_list:
            if trig == True:
                result.append(word)
                trig = False
                continue

            # We can find the trigger-word and it now in the end of news
            if trigger in word and word[-1] != '.':
                trig = True
                continue

        return result


    # Now let's try to find wrods with capital letter
    @staticmethod
    def news_starter(self):
        words = self.data.replace('\xa0', ' ').split(' ')
        return list(filter(lambda wow: str.isupper((wow + 'n')[0]), words))
    # But doing this by first-words-list


    # Create massiv generation function
    # We can make our choice with random-choice function
    # Random choice-function for starting

    @staticmethod
    def random_choice_starter(self):
        sch = 0
        # ordering the occurrence array
        decision_mass = Counter(self.starter_list)
        for sl in decision_mass:
            sch += decision_mass[sl]
            decision_mass[sl] = sch

        sch += 150
        # If we want to add the "курс" word...
        decision_mass['курс'] = sch

        rand_choice = rand.randint(0,sch)
        for slov in decision_mass:
            if rand_choice <= decision_mass[slov]:
                return(slov)
                break

    @classmethod
    def random_choice_word(self,word):
        # создадим словарь слов, которые кажутся очень странными в своём поведении и будем делать для них отедельное решение
        strange_list={'до':0,'с':0,'в':0,'к':0,'о':0}
        strange_list['до']={'нового':5,'старого':3,'полугодового': 3,'двухлетнего': 2,'максимума': 2,'73': 2,'трехмесячного': 2,'50': 1,'30':5}
        strange_list['с']={'нового':5,'финансов':3,'полугодового': 3,'двухлетнего': 2,'2008': 2,'73': 2,'длинных': 2,'трехмесячного': 2,'50': 1,'30':5}
        strange_list['в']={'докризисный':4,'отставку':3,'свой': 3,'помощь': 3,'рекордный': 2,'4': 2,'адекватный': 2,'50': 1,'44':3}
        strange_list['к']={'доллару':4,'евро':3,'рублю': 2,'отметке': 2,'71': 1,'50': 1,'44':2}
        strange_list['о']={'евро':3,'ещё': 3,'50': 1,'почти':2,'более': 1,'введении': 1}
        sch=0
        #если слово из нормального списка то всё ок
        if word not in strange_list:
            decision_mass=dict(Counter(self.sm(self,word)).most_common(10))
        else:
        #если оно относится к списку странных слов, то для неё строим отдельно
            decision_mass=strange_list[word]

        # если словарь не пустой, то всё ок, иначе выдаём "-1"
        if len(decision_mass)!=0:
            for sl in decision_mass:
                sch+=decision_mass[sl]
                decision_mass[sl]=sch

            rand_choice=rand.randint(0,sch)
            for slov in decision_mass:
                if rand_choice<=decision_mass[slov]:
                    return(slov)
                    break
        else:
            return '-1'
        
        
    #функция для преобразования окончаний
    @staticmethod
    def default_dict(numb):
        if int(numb)==1:
            return 'рубль'
        elif int(numb)<=4 and int(numb)!=0:
            return 'рубля'
        elif int(numb)<10 or int(numb)==0:
            return 'рублей'

    #преобразуем предложение, вставляя нужные цифры
    @staticmethod
    def sent_decomposition(self,sent):
        Currence_dict=self.Currence_dict
        rules_dict={'1':{' к ':'рублю','ниже':'рубля','выше':'рубля',' до ':'рубля'}}
        sent_new=sent
        #дадим пока возможность появляться предложениям без цифр
        if len(re.findall('(\d+)',sent))!=0:
            # не надо преобразовывать года
            if float(re.findall('(\d+)',sent)[0])<2000:
                inserter=''
                if sent.find('доллар')!=-1:
                    inserter=str(Currence_dict['USD'])
                elif sent.find('евро')!=-1:
                    inserter=str(Currence_dict['EUR'])

                if len(re.findall('(\d+)',sent))==0:
                    print('333')
                sent=sent.replace(re.findall('(\d+)',sent)[0],inserter)
                if len(inserter)!=0:
                    lastr=inserter[-1]
                else:
                    lastr='1'

                znak=False
                sent_new=sent

                start=sent_new.find('рубл')
                if start==-1:
                    start=sent_new.find('копе')
                if start==-1:
                    return '-1'

                finish=sent_new[start:].find(' ')
                if finish==-1:
                    finish=len(sent_new)

                if lastr in rules_dict:
                    for predl in list(rules_dict[lastr].keys()):
                        if predl in sent_new and znak==False:
                            #print('wow',' ',sent_new,' ',predl)
                            sent_new=sent.replace(sent_new[start:start+finish],rules_dict[lastr][predl])
                            znak=True

                    if znak==False:
                        #print('yet')
                        sent_new=sent_new.replace(sent_new[start:start+finish],self.default_dict(lastr))


                else:
                    sent_new=sent_new.replace(sent_new[start:start+finish],self.default_dict(lastr))

        return sent_new
    
    
    #функция для вывода курсов валют
    @staticmethod
    def currency_finder(self,value='<Value>',currence='<CharCode>'):
        dat=self.l
        tag=0
        mass={}
        keyw_closer_curr='</'+currence[1:]
        keyw_closer_val='</'+value[1:]
        while keyw_closer_curr in dat:
            curr=str(dat[dat.find(currence)+len(currence):dat.find(keyw_closer_curr)])
            vall=float(str(dat[dat.find(value)+len(value):dat.find(keyw_closer_val)])[:5].replace(',','.'))
            mass[curr]=vall
            dat=dat[dat.find(keyw_closer_val)+len(keyw_closer_val):]
        return mass
