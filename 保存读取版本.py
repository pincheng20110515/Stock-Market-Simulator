import time
import random
import pygame
import json
size = 700, 500
screen = pygame.display.set_mode(size)
greedy = 90
maxq = [10.0]*72
smaxq = [10.0]*72
tmaxq = [10.0]*72
save_package={}
ai_data_list=[]
def save_data():
    for ai in ai_list:
        ai_data_list.append({
            "money": ai.money,
            "shares": ai.shares,
            "timer": ai.timer,
            "Qtable": ai.Qtable,
            "last_state": ai.last_state,
            "price_change": ai.price_change,
            "last_money": ai.last_money,
            "last_action": ai.last_action,
            "last_price": ai.last_price,
            "new_state": ai.new_state,
            "IR": ai.IR,
            "gamma": ai.gamma,
            "last_total_asset": ai.last_total_asset,
            "last_position_state": ai.last_position_state,
            "life": ai.life,
            "neww_state": ai.neww_state
        })
    save_package={
        "market_cash": market_cash,
        "market_shares": market_shares,
        "user_money": user_money,
        "user_shares": user_shares,
        "greedy": greedy,
        "maxq": maxq,
        "smaxq": smaxq,
        "tmaxq": tmaxq,
        "pi": pi,
        "cool_down": cool_down,
        "loan": loan,
        "coodinate_y": coodinate_y,
        "ai_list": ai_data_list
    }
    with open('D:\桌面\离线股票模拟器存档', 'w', encoding='utf-8') as f:
        json.dump(save_package, f)
        quit()
def load_data():
    global market_shares, market_cash, user_money, user_shares, greedy, maxq, smaxq, tmaxq, pi, cool_down, loan, coodinate_y, ai_list,neww_state
    try:
        with open('D:\桌面\离线股票模拟器存档', "r", encoding="utf-8") as f:
            pack = json.load(f)
            market_cash = pack["market_cash"]
            market_shares = pack["market_shares"]
            user_money = pack["user_money"]
            user_shares = pack["user_shares"]
            greedy = pack["greedy"]
            maxq = pack["maxq"]
            smaxq = pack["smaxq"]
            tmaxq = pack["tmaxq"]
            pi = pack["pi"]
            cool_down = pack["cool_down"]
            loan = pack["loan"]
            coodinate_y = pack["coodinate_y"]
            ai_data_list = pack["ai_list"]
        for i in range(100):
            data = ai_data_list[i]
            ai = ai_list[i]
            ai.money = data["money"]
            ai.shares = data["shares"]
            ai.timer = data["timer"]
            ai.Qtable = data["Qtable"]
            ai.last_state = data["last_state"]
            ai.price_change = data["price_change"]
            ai.last_money = data["last_money"]
            ai.last_action = data["last_action"]
            ai.last_price = data["last_price"]
            ai.new_state = data["new_state"]
            ai.IR = data["IR"]
            ai.gamma = data["gamma"]
            ai.last_total_asset = data["last_total_asset"]
            ai.last_position_state = data["last_position_state"]
            ai.life = data["life"]
            ai.neww_state=data['neww_state']
    except:
        pass
class AI:
    def __init__(self):
        self.money = 100
        self.shares = 0
        self.timer = random.randint(0, 10)
        self.Qtable = [10.0]*72
        self.last_state = 4
        self.price_change = 0
        self.last_money = 100
        self.last_action = 0
        self.last_price = 1
        self.new_state = 1
        self.IR = 0.1
        self.gamma = 0.9
        self.last_total_asset = 100
        self.last_position_state = 0
        self.life = random.randint(700000, 1400000)

    def ai_action(self, price):
        global market_shares, market_cash, greedy, maxq, smaxq, tmaxq
        self.timer += 1
        if self.timer >= 0:
            self.life -= 1
            if self.life <= 0:
                self.Qtable = []
                x = 0
                for i in range(24):
                    choice = random.randint(1, 3)
                    if choice == 1:
                        self.Qtable.append(maxq[x]/10)
                        self.Qtable.append(maxq[x+1]/10)
                        self.Qtable.append(maxq[x+2]/10)
                    elif choice == 2:
                        self.Qtable.append(smaxq[x]/10)
                        self.Qtable.append(smaxq[x+1]/10)
                        self.Qtable.append(smaxq[x+2]/10)
                    else:
                        self.Qtable.append(tmaxq[x]/10)
                        self.Qtable.append(tmaxq[x+1]/10)
                        self.Qtable.append(tmaxq[x+2]/10)
                    x += 3
                market_shares += self.shares
                market_cash += self.money-100
                self.money = 100
                self.shares = 0
                self.timer = random.randint(0, 10)
                self.last_state = 4
                self.price_change = 0
                self.last_money = 100
                self.last_action = 0
                self.last_price = 1
                self.new_state = 1
                self.IR = 0.1
                self.gamma = 0.9
                self.last_total_asset = 100
                self.last_position_state = 0
                self.life = random.randint(700000, 1400000)
            current_total_asset = self.money + self.shares * price
            r = current_total_asset - self.last_total_asset
            total_value = self.money + self.shares * price
            self.last_total_asset = self.money + self.shares * price
            if total_value > 0:
                position_ratio = (self.shares * price) / total_value
            else:
                position_ratio = 0
            # if position_ratio > 0.8:
            #     r -= (position_ratio - 0.8) /2
            # if position_ratio < 0.2:
            #     r -= (0.2 - position_ratio) /2
            self.timer = 0
            if position_ratio < 0.2:
                position_state = 0
            elif position_ratio < 0.7:
                position_state = 1
            else:
                position_state = 2
            q_index = (self.last_state*3)+self.last_action + \
                24*self.last_position_state
            self.last_price_change = (
                self.last_price - self.new_state) / self.new_state if self.new_state != 0 else 0
            if self.last_price_change <= -0.03:
                self.neww_state = 0  # 暴跌 15% 以上
            elif self.last_price_change <= -0.02:
                self.neww_state = 1  # 大跌 10% ~ 15%
            elif self.last_price_change <= -0.01:
                self.neww_state = 2  # 中跌 5% ~ 10%
            elif self.last_price_change <= 0.0:
                self.neww_state = 3  # 微跌 0% ~ 5%
            elif self.last_price_change <= 0.01:
                self.neww_state = 4  # 微涨 0% ~ 5%
            elif self.last_price_change <= 0.02:
                self.neww_state = 5  # 中涨 5% ~ 10%
            elif self.last_price_change <= 0.03:
                self.neww_state = 6  # 大涨 10% ~ 15%
            else:
                self.neww_state = 7  # 暴涨 15% 以上
            old_q_index0 = (self.neww_state*3)+0+position_state*24
            old_q_index1 = (self.neww_state*3)+1+position_state*24
            old_q_index2 = (self.neww_state*3)+2+position_state*24
            self.Qtable[q_index] += self.IR*(r+self.gamma*max(self.Qtable[old_q_index0], self.Qtable[old_q_index1],
                                             self.Qtable[old_q_index2]) - self.Qtable[q_index])  # 打分:oa+=lr*(r+y*max(na0,na1,na2)-oa)
            self.new_state = price
            self.price_change = (price - self.last_price) / \
                self.last_price if self.last_price != 0 else 0
            if self.price_change <= -0.03:
                self.last_state = 0  # 暴跌 15% 以上
            elif self.price_change <= -0.02:
                self.last_state = 1  # 大跌 10% ~ 15%
            elif self.price_change <= -0.01:
                self.last_state = 2  # 中跌 5% ~ 10%
            elif self.price_change <= 0.0:
                self.last_state = 3  # 微跌 0% ~ 5%
            elif self.price_change <= 0.01:
                self.last_state = 4  # 微涨 0% ~ 5%
            elif self.price_change <= 0.02:
                self.last_state = 5  # 中涨 5% ~ 10%
            elif self.price_change <= 0.03:
                self.last_state = 6  # 大涨 10% ~ 15%
            else:
                self.last_state = 7  # 暴涨 15% 以上
            position0 = self.last_state*3+position_state*24
            position1 = self.last_state*3+1+position_state*24
            position2 = self.last_state*3+2+position_state*24
            position_dictionary = {'position0': self.Qtable[position0],
                                   'position1': self.Qtable[position1],
                                   'position2': self.Qtable[position2]}
            self.last_position_state = position_state
            choice = max(position_dictionary, key=position_dictionary.get)
            randomposibility = random.randint(1, 100)
            self.last_money = self.money  # 钱的更新
            if randomposibility < greedy:
                randomchoice = random.randint(1, 30)
                if randomchoice <= 10:
                    if self.money >= price and market_shares > 1:
                        self.money -= price
                        self.shares += 1
                        market_shares -= 1
                        market_cash += price
                        self.last_action = 1
                    else:
                        self.last_action = 1
                elif randomchoice <= 20:
                    if self.shares > 0 and market_cash >= price+1:
                        self.money += price
                        self.shares -= 1
                        market_shares += 1
                        market_cash -= price
                        self.last_action = 2
                    else:
                        self.last_action = 2
                else:
                    self.last_action = 0
            else:
                if choice == 'position0':
                    self.last_action = 0
                elif choice == 'position1':
                    if self.money >= price and market_shares > 1:
                        self.money -= price
                        self.shares += 1
                        market_shares -= 1
                        market_cash += price
                        self.last_action = 1
                    else:
                        self.last_action = 1
                else:
                    if self.shares > 0 and market_cash > price+1:
                        self.money += price
                        self.shares -= 1
                        market_shares += 1
                        market_cash -= price
                        self.last_action = 2
                    else:
                        self.last_action = 2
            self.last_price = price  # 市场价格更新


market_shares = 10000
market_cash = 10000
user_money = 100
user_shares = 0


def show_information():
    print('market_cash', market_cash)
    print('market_shares', market_shares)
    print('price', price)
    print('user_money', user_money)
    print('user_shares', user_shares)
    print('greedy', greedy)
    print(ai_list[0].money, ai_list[0].shares)
    print(ai_list[1].money, ai_list[1].shares)
    print(ai_list[2].money, ai_list[2].shares)
    print(ai_list[3].money, ai_list[3].shares)
    print(ai_list[4].money, ai_list[4].shares)


def user_buy():
    global user_money, user_shares, market_cash, market_shares
    user_money -= price
    user_shares += 1
    market_cash += price
    market_shares -= 1
    show_information()


def user_sell():
    global user_money, user_shares, market_cash, market_shares
    user_money += price
    user_shares -= 1
    market_cash -= price
    market_shares += 1
    show_information()


ai_list = [AI() for q in range(100)]
green = 0, 255, 0
coodinate_y = []
black = 0, 0, 0

pi = 0
cool_down = 0
loan = 0


def ai_threading():
    global price, market_cash, market_shares, pi, loan, cool_down, greedy, maxq, smaxq, tmaxq
    while True:
        if greedy > 20:
            greedy *= 0.9999
        screen.fill(black)
        price = market_cash/max(market_shares, 1)
        compare = []
        for i in ai_list:
            compare.append(
                i.shares*(market_cash/max(market_shares, 1))+i.money)
        number = max(compare)
        index = compare.index(number)
        on = compare[index]
        compare[index] = -1
        numbers = max(compare)
        indexs = compare.index(numbers)
        ano = compare[indexs]
        compare[indexs] = -1
        numbert = max(compare)
        indext = compare.index(numbert)
        compare[indexs] = ano
        compare[index] = on
        maxq = ai_list[index].Qtable[:]
        smaxq = ai_list[indexs].Qtable[:]
        tmaxq = ai_list[indext].Qtable[:]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_1]:
                if user_money >= price and market_shares > 1:
                    user_buy()
            if keys[pygame.K_2]:
                if user_shares > 0 and market_cash >= price+1:
                    user_sell()
            if keys[pygame.K_3]:
                if user_money >= price*10 and market_shares > 10:
                    for a in range(10):
                        user_buy()
            if keys[pygame.K_4]:
                if user_shares > 10 and market_cash >= price*10+1:
                    for a in range(10):
                        user_sell()
            if keys[pygame.K_5]:
                if user_money >= price*100 and market_shares > 100:
                    for a in range(100):
                        user_buy()
            if keys[pygame.K_6]:
                if user_shares > 100 and market_cash >= price*100+1:
                    for a in range(100):
                        user_sell()
            if keys[pygame.K_0]:
                print([ai_list[0].Qtable])
                print([ai_list[1].Qtable])
                print([ai_list[2].Qtable])
                print([ai_list[3].Qtable])
                print([ai_list[4].Qtable])
                show_information()
                print('-------------------------------------------')
            if keys[pygame.K_9]:
                save_data()
        for ai in ai_list:
            ai.ai_action(market_cash/max(market_shares, 1))
        coodinate_y.append(price)
        if max(coodinate_y) != min(coodinate_y):
            price_range = max(coodinate_y) - min(coodinate_y)
        else:
            price_range = 1
        if len(coodinate_y) > 700:
            coodinate_y.pop(0)
        for i in range(len(coodinate_y)):
            yyy = int(460 - (coodinate_y[i] -
                      min(coodinate_y)) / price_range * 420)
            yyyy = int(460 - (coodinate_y[i-1] -
                       min(coodinate_y)) / price_range * 420)
            pygame.draw.line(screen, green, (i - 1, yyyy), (i, yyy), 1)
        pygame.display.flip()
        if market_cash <= 1000 or market_shares <= 1000:
            if pi == 0:
                pi = 10
                print('央行救市')
        if pi != 0:
            pi -= 1
            market_shares += 10
            market_cash += 10
            loan += 1
        else:
            pass
        if market_cash >= 7000 and market_shares > 3000 and loan > 0 and cool_down == 0:
            cool_down = 100
            market_shares -= 10
            market_cash -= 10
            loan -= 1
            print('还债')
        if cool_down > 0:
            cool_down -= 1
        time.sleep(0.001)
load_data()
ai_threading()
