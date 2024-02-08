
import random
import time

class Person:
    def __init__(self,name,assets_init,rule) -> None:
        self.name = name
        self.assets_init = assets_init
        self.assets = self.assets_init
        self.rule = rule
        self.rule_function = None

        self.isBanker = False
        self.betRule = None
        self.bet = 0
        self.card_now = [1,2]
        self.isWin_now = True

        self.isWin_last = False
        self.lose_contiuedNumber = 0
        self.winAssets_contiued = 0

        self.personInit()
    def personInit(self):
        if self.rule == 1:
            self.rule_function = self.rule_1
        elif self.rule == 2:
            self.rule_function = self.rule_2
        elif self.rule == 3:
            self.rule_function = self.rule_3

    def rule_1(self):
        return 2
    def rule_2(self):
        return random.randint(1,10)
    def rule_3(self):
        if self.isWin_last:
            return 2
        else:
            return 2**self.lose_contiuedNumber

    
class CardDesk:
    def __init__(self,person_dictionary,settings,max_bet) -> None:
        self.deskPerson_number = None
        self.deskPerson_name = []
        self.deskPerson_dictionary = person_dictionary
        self.deskPerson_personDictionary = {}
        self.deskRounds = None
        self.deskSettings = settings

        self.dice = 6
        self.dice_array = [[3,4,1,2],[2,3,4,1],[1,2,3,4],[4,1,2,3]]
        self.order = True

        self.allCard_init = [1,1,1,1]
        self.allCard_random = [1,2,3,4]
        self.allCard_now = [[],[]]
        self.allCard_up = [1]
        self.allCard_down = [2]
        self.banker = None
        self.allBet_name = []
        self.allBet_once = {}
        self.isCell = False

        self.max_bet = max_bet
        self.deskInit()
    def deskInit(self):
        self.deskPerson_number = len(self.deskPerson_dictionary)
        self.deskPerson_name = list(self.deskPerson_dictionary.keys())
        self.deskPerson_personDictionary = {name:Person(name,self.deskPerson_dictionary[name][0],self.deskPerson_dictionary[name][1]) for name in self.deskPerson_name}
        self.deskRounds = self.deskSettings.deskRounds

        self.allCard_init = [1,1,1,1,
                             2,2,2,2,
                             3,3,3,3,
                             4,4,4,4,
                             5,5,5,5,
                             6,6,6,6,
                             7,7,7,7,
                             8,8,8,8,
                             9,9,9,9]
        self.isCell = self.deskSettings.isCell

    def oneGameRound(self):
        random.seed(time.time())
        random.shuffle(self.allCard_init)
        self.allCard_random = self.allCard_init
        self.allCard_up = self.allCard_random[:len(self.allCard_random)//2]
        self.allCard_down = self.allCard_random[len(self.allCard_random)//2:]
        self.allCard_now = [self.allCard_up,self.allCard_down]
        print("==========================================")
        print("新一轮牌面：")
        f.write("==========================================\n")
        f.write("新一轮牌面：\n")
        print(self.allCard_up)
        print(self.allCard_down)
        f.write(f"{self.allCard_up}\n")
        f.write(f"{self.allCard_down}\n")


        for name in self.deskPerson_name:
            if self.deskPerson_dictionary[name][2]:
                self.banker = name
        self.allBet_name = self.deskPerson_name.copy()
        self.allBet_name.remove(self.banker)

        for i in range((len(self.allCard_random)//2+1)//self.deskPerson_number):
            print("----------")
            f.write("----------\n")
            #下注
            self.allBet_once = {name:self.deskPerson_personDictionary[name].rule_function() for name in self.allBet_name}
            print(f"下注：{self.allBet_once}")
            f.write(f"下注：{self.allBet_once}\n")
            if self.allBet_once['lhb'] > self.max_bet:
                self.max_bet = self.allBet_once['lhb']
                 

            #打筛子
            dice = random.randint(1,6)
            print(f"打筛：{dice}")
            f.write(f"打筛：{dice}\n")
            order_array = self.dice_array[(dice % self.deskPerson_number) - 1].copy()[::-1]

            #分牌
            for name in self.deskPerson_name:
                base_number = (i*self.deskPerson_number)+order_array.pop()-1
                self.deskPerson_personDictionary[name].card_now = [self.allCard_up[base_number],self.allCard_down[base_number]]
                # print(self.deskPerson_personDictionary[name].card_now)
            
            #比牌
            banker_card = self.deskPerson_personDictionary[self.banker].card_now
            for name in self.allBet_name:
                if self.deskPerson_personDictionary[name].card_now[0] == self.deskPerson_personDictionary[name].card_now[1]:
                    if banker_card[0] == banker_card[1] and banker_card[0] >= self.deskPerson_personDictionary[name].card_now[0]:
                        self.deskPerson_personDictionary[name].isWin_now = 0
                    else:
                        self.deskPerson_personDictionary[name].isWin_now = 2
                else:
                    if banker_card[0] == banker_card[1]:
                        self.deskPerson_personDictionary[name].isWin_now = 0
                    else:
                        if (self.deskPerson_personDictionary[name].card_now[0] + self.deskPerson_personDictionary[name].card_now[1])%10 > (banker_card[0] + banker_card[1])%10:
                            self.deskPerson_personDictionary[name].isWin_now = 1
                        else:
                            self.deskPerson_personDictionary[name].isWin_now = 0
            
            #给钱
            for name in self.allBet_name:
                if self.deskPerson_personDictionary[name].isWin_now == 0:
                    self.deskPerson_personDictionary[name].assets = self.deskPerson_personDictionary[name].assets - self.allBet_once[name]
                    self.deskPerson_personDictionary[self.banker].assets = self.deskPerson_personDictionary[self.banker].assets + self.allBet_once[name]
                    if self.deskPerson_personDictionary[name].isWin_last:
                        self.deskPerson_personDictionary[name].lose_contiuedNumber = 1
                    else:
                        self.deskPerson_personDictionary[name].lose_contiuedNumber = self.deskPerson_personDictionary[name].lose_contiuedNumber + 1
                    self.deskPerson_personDictionary[name].isWin_last = False
                elif self.deskPerson_personDictionary[name].isWin_now == 1:
                    self.deskPerson_personDictionary[name].assets = self.deskPerson_personDictionary[name].assets + self.allBet_once[name]
                    self.deskPerson_personDictionary[self.banker].assets = self.deskPerson_personDictionary[self.banker].assets - self.allBet_once[name]
                    self.deskPerson_personDictionary[name].lose_contiuedNumber = 0
                    self.deskPerson_personDictionary[name].isWin_last = False
                elif self.deskPerson_personDictionary[name].isWin_now == 2:
                    self.deskPerson_personDictionary[name].assets = self.deskPerson_personDictionary[name].assets + 2*self.allBet_once[name]
                    self.deskPerson_personDictionary[self.banker].assets = self.deskPerson_personDictionary[self.banker].assets - 2*self.allBet_once[name]
                    self.deskPerson_personDictionary[name].lose_contiuedNumber = 0
                    self.deskPerson_personDictionary[name].isWin_last = False
            
            #钱
            print(f"庄家：{self.banker}")
            f.write(f"庄家：{self.banker}\n")
            for name in self.deskPerson_name:
                print(self.deskPerson_personDictionary[name].card_now,f"{name}本轮结束 剩余钱量：{self.deskPerson_personDictionary[name].assets}")
                f.write(f"{self.deskPerson_personDictionary[name].card_now}  {name}本轮结束 剩余钱量：{self.deskPerson_personDictionary[name].assets}\n")
            print("----------")
            f.write("----------\n")




            

class Settings:
    def __init__(self) -> None:
        self.isCell = False
        self.deskRounds = 100


if __name__ == "__main__":
    max_bet = 0
    person_dictionary = {"lc":[1000,1,False],
                         "wlh":[1000,2,False],
                         "lzk":[1000,2,True],
                         "lhb":[1000,3,False]}
    settings = Settings()
    cardDesk = CardDesk(person_dictionary=person_dictionary,settings=settings,max_bet=max_bet)
    f = open("log.txt",'w')
    for i in range(1000):
        cardDesk.oneGameRound()
    print(cardDesk.max_bet)



