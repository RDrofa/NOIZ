import math


dict_gtm = {  'ВПП':[],
              'Дострел':[],
              'ИДН':[],
              'Кислотная ОПЗ':[],
              'Механизация':[],
              'Оптимизация':[],
              'Перестрел':[],
              'Подъем Рзак':[],
              'Промывка/нормализация':[],
              'Прочие ОПЗ':[],
              'Ревизия ППД':[],
              'РИР':[],
              'ГРП':[],
              'Приобщение пласта':[],
              'Смена ЭЦН':[],
              'Прочие ГТМ':[],
              'Не учитывать ГТМ':[]}



'''  Qoil – накопленная добыча нефти, т
     Bo – объемный коэффициент нефти
     Ro – плотность нефти, г/см3
     H – нефтенасыщенная толщина, м
     m – пористость пласта, доли ед.
     So – начальная нефтенасыщенность, доли ед.
     So_min – минимальная нефтенасыщенность, доли ед.
     L  – длина горизонтального ствола
'''

HTM = '<!DOCTYPE html>'
HTM = HTM  + '<html>'
HTM = HTM  + '<head>'
HTM = HTM  + '<metacharset="utf-8"/>'
HTM = HTM  + '<title>Цвет</title>'
HTM = HTM  + '<style>'
HTM = HTM  + '</style>'
HTM = HTM  + '</head>'
HTM = HTM  + '<body>'
HTM = HTM  + '<ul>'
HTM = HTM  + '<li style="color:#FFF8DC; background:black"><b>Нет гидродинамической связи<b></li>'
HTM = HTM  + '<li style="color:#FFE4C4; background:black"><b>Низкая связь/нет связи<b></li>'
HTM = HTM  + '<li style="color:#FFDEAD; background:black"><b>Очень слабая связь<b></li>'
HTM = HTM  + '<li style="color:#FF7F50; background:black"><b>Слабая связь<b></li>'
HTM = HTM  + '<li style="color:#FF6347; background:black"><b>Слабая связь с возможным потенциалом<b></li>'
HTM = HTM  + '<li style="color:#FFA500; background:black"><b>Умеренная связь<b></li>'
HTM = HTM  + '<li style="color:#FF8C00; background:black"><b>Умеренная связь с возможным потенциалом<b></li>'
HTM = HTM  + '<li style="color:#40E0D0; background:black"><b>Заметная связьм<b></li>'
HTM = HTM  + '<li style="color:#00BFFF; background:black"><b>Заметная связь с возможным потенциалом<b></li>'
HTM = HTM  + '<li style="color:#1E90FF; background:black"><b>Заметная связь с возможным промывом<b></li>'
HTM = HTM  + '<li style="color:#00FF00; background:black"><b>Высокая связь<b></li>'
HTM = HTM  + '<li style="color:#32CD32; background:black"><b>Высокая связь с возможным промывом<b></li>'
HTM = HTM  + '<li style="color:#006400; background:black"><b>Очень высокая связь<b></li>'
HTM = HTM  + '<li style="color:white; background:black"><b>Нет данных<b></li>'
HTM = HTM  + '</ul>'
HTM = HTM  + '</body>'
HTM = HTM  + '</html>'



HTM2 = '<!DOCTYPE html>'
HTM2 = HTM2  + '<html>'
HTM2 = HTM2  + '<head>'
HTM2 = HTM2  + '<metacharset="utf-8"/>'
HTM2 = HTM2  + '<title>Цвет</title>'
HTM2 = HTM2  + '<style>'
HTM2 = HTM2  + '</style>'
HTM2 = HTM2  + '</head>'
HTM2 = HTM2  + '<body>'
HTM2 = HTM2  + '<ul>'
HTM2 = HTM2  + '<li style="color:#FF0000; background:black"><b>Не корректное значение<b></li>'
HTM2 = HTM2  + '<li style="color:#1E90FF; background:black"><b>Значение изменено пользователем<b></li>'
HTM2 = HTM2  + '<li style="color:#FF7420; background:black"><b>Значение расчитано программно<b></li>'
HTM2 = HTM2  + '</ul>'
HTM2 = HTM2  + '</body>'
HTM2 = HTM2  + '</html>'



# Получение списка пластов
def getAllForms(plast0):
    plast1 = []
    for i in plast0:
        plast1.extend(i.split(","))
    plast1 = [x.strip(' ') for x in plast1]
    plast1 = list(set(plast1))
    plast1 = list(filter(None, plast1))

    return plast1



def setHTMrezult(L,O,P,S,C):

    if P==' - ':
        P = ' - нет связи'
    else:
        P = '  лаг ' + str(P)

    HTM = ''
    HTM = HTM + "<font color='black' size='5'><red>Результат по всем лагам</font><br><br>"
    HTM = HTM + "<font color='blue' size='4'><red>Жидкость (Kl)  -  лаг " + str(L)+ "</font><br>"
    HTM = HTM + "<font color='blue' size='4'><red>Нефть (Ko)     -  лаг " + str(O) + "</font><br>"
    HTM = HTM + "<font color='blue' size='4'><red>Давление (Kp)"  + P + "</font><br><br>"
    HTM = HTM + "<font color='" + C +"' size='5'><red>" + S +  "</font><br>"

    return HTM


def setHTMrezult_():
    HTM = ''

    for i in range(len(self.cols)):

        self.lineCollor.append('N')

        if self.checkedRanges[i] > 0:

            wells = 'Скважины:   ' + nag + ' - ' + self.cols[i]
            wells = "<font color='black' size='5'><red>" + wells + "</font><br>"
            HTM = HTM + wells

            p = df_result[nag + ' - ' + self.cols[i] + ' Жидкость'].tolist()
            while True:
                try:
                    p.remove('')
                except:
                    break
            HTM = HTM + "<font color='blue' size='5'><red>Жидкость</font><br>"
            for j in range(len(p)):
                if p[j] > 0.4:
                    clr = 'green'
                else:
                    clr = 'red'
                textt = 'Лаг ' + str(j + v) + ' мес.  ->  Rs = ' + str(round(p[j], 2))
                texxt = "<font color='" + clr + "' size='4'><" + clr + ">" + textt + "</font><br>"
                HTM = HTM + texxt

            m1 = max(p)

            p = df_result[nag + ' - ' + self.cols[i] + ' Нефть'].tolist()
            while True:
                try:
                    p.remove('')
                except:
                    break
            HTM = HTM + "<font color='blue' size='5'><red>Нефть</font><br>"
            for j in range(len(p)):
                if p[j] > 0.4:
                    clr = 'green'
                else:
                    clr = 'red'
                textt = 'Лаг ' + str(j + v) + ' мес.  ->  Rs = ' + str(round(p[j], 2))
                texxt = "<font color='" + clr + "' size='4'><" + clr + ">" + textt + "</font><br>"
                HTM = HTM + texxt

            if max(p) > m1:
                m1 = max(p)

            p = df_result[nag + ' - ' + self.cols[i] + ' Давление'].tolist()
            while True:
                try:
                    p.remove('')
                except:
                    break

            if len(p) > 0:
                HTM = HTM + "<font color='blue' size='5'><red>Забойное давление</font><br>"
                for j in range(len(p)):
                    if p[j] > 0.4:
                        clr = 'green'
                    else:
                        clr = 'red'
                    textt = 'Лаг ' + str(j + v) + ' мес.  ->  Rs = ' + str(round(p[j], 2))
                    texxt = "<font color='" + clr + "' size='4'><" + clr + ">" + textt + "</font><br>"
                    HTM = HTM + texxt

                if max(p) > m1:
                    m1 = max(p)

            '''if m1 < 0.3:
                self.lineCollor[i] = ('orangered')
            elif m1 >= 0.3 and m1 < 0.5:
                self.lineCollor[i] = ('orange')
            elif m1 >= 0.5 and m1 < 0.7:
                self.lineCollor[i] = ('dodgerblue')
            elif m1 >= 0.7 and m1 < 0.9:
                self.lineCollor[i] = ('green')
            else:
                self.lineCollor[i] = ('lawngreen')'''

        HTM = HTM + "<br>"



def spearDecodeK(K):
    if K==1:
        S = 'Нет гидродинамической связи'
        clr = '#FFF8DC'
    elif K==2:
        S = 'Низкая связь/нет связи'
        clr = '#FFE4C4'
    elif K==3:
        S = 'Очень слабая связь'
        clr = '#FFDEAD'
    elif K==4:
        S = 'Низкая связь с возможным потенциалом'
        clr = '#FFA07A'
    elif K==5:
        S = 'Слабая связь'
        clr = '#FF7F50'
    elif K==6:
        S = 'Слабая связь с возможным потенциалом'
        clr = '#FF6347'
    elif K==7:
        S = 'Умеренная связь'
        clr = '#FFA500'
    elif K==8:
        S = 'Умеренная связь с возможным потенциалом'
        clr = '#FF8C00'
    elif K==9:
        S = 'Заметная связь'
        clr = '#40E0D0'
    elif K==10:
        S = 'Заметная связь с возможным потенциалом'
        clr = '#00BFFF'
    elif K==11:
        S = 'Заметная связь с возможным промывом'
        clr = '#1E90FF'
    elif K==12:
        S = 'Высокая связь'
        clr = '#00FF00'
    elif K==13:
        S = 'Высокая связь с возможным промывом'
        clr = '#32CD32'
    elif K==14:
        S = 'Очень высокая связь'
        clr = '#006400'
    else:
        S = 'Нет данных'
        clr = '#FFF8DC'
    return S, clr



def gtm_names(s):

    l = s.split(',')
    r = ''
    for itm in l:
        t = itm
        if itm == 'Дострел':
            t =  'Д'
        if itm == 'Перестрел':
            t = 'П'
        if itm == 'Кислотная ОПЗ':
            t = 'К.ОПЗ'
        if itm == 'Прочие ОПЗ':
            t = 'П.ОПЗ'
        if itm == 'Оптимизация':
            t = 'ОПТ'
        if itm == 'Оптимизация производительности УЭЦН':
            t = 'ОПТ'
        if itm == 'Механизация':
            t = 'М'
        if itm == 'Подъем Рзак':
            t = 'Рзак'
        if itm == 'Промывка/нормализация':
            t = 'П/Н'
        if itm == 'Ревизия ППД':
            t = 'Р.ППР'
        r = r + t + ','
    if r!='':
        return r[:-1]
    else:
        return s



def getNumOfDate(L,d):
    for i in range(len(L)):
        if d in str(L[i]):

            return i




def setName(x):
    s=''

    if x==1:
        s = 'Закачка за посл.месяц, м3'
    if x==2:
        s = 'Забойное давление (ТР), атм'
    if x==3:
        s = 'Пластовое давление (ТР), атм'
    if x==4:
        s = 'Приемистость за последний месяц, м3/сут'
    if x==5:
        s = 'Приемистость (ТР), м3/сут'
    if x==6:
        s = 'Дебит жидкости за последний месяц, т/сут'
    if x==7:
        s = 'Дебит жидкости (ТР), м3/сут'
    if x==8:
        s = 'Дебит нефти за последний месяц, т/сут'
    if x==9:
        s = 'Дебит нефти (ТР), т/сут'
    if x==10:
        s = 'Обводненность за посл.месяц, % (вес)'
    if x==11:
        s = 'Обводненность (ТР), % (объём)'
    if x==12:
        s = 'Динамический уровень (ТР), м'
    if x==13:
        s = 'Диаметр штуцера, мм'
    return s

def isFloat(s):
    try:
        x = float(s)
        return False
    except:
        return True


def isInt(s):
    try:
        x = int(s)
        return False
    except:
        return True


def toFloat(s):
    try:
        x = float(s)
        return x
    except:
        return -1

def toFloat2(a,b):
    try:
        x = float(a)
        y = float(b)
        return x - y
    except:
        return -1


def isZero(s):
    x = True
    try:
        if float(s)!=0:
            x =  False
        else:
            x = True

    except:
        x =  True
    return x


def setForParam(l,isNul,val):
    a = l[:]

    if isNul == True:
        a = [-1 if K == 0 else K for K in a]

    a = [val if K == -1 else K for K in a]
    return a



def PstartFill(l, p):
    a=l[:]
    whatAuto = []

    if p==-1:

        for i in range(len(a)):
            if a[i] == '' or a[i] == 0 or a[i] == '0':
                pass
            else:
                p = a[i]
                break

    if p != -1:
        for i in range(len(a)):
            if a[i] == '' or a[i]==0 or a[i]=='0':
                a[i]=p
                whatAuto.append(i)
            else:
                break
    else:
        for i in range(len(a)):
            if a[i] == '' or a[i]==0 or a[i]=='0':
                a[i]=''
            else:
                break

    return a, whatAuto




def averageForParam(l,isNul):

    was_chg = False

    try:

        whatAutoAvrg = []   # для сохранения индексов автозаполненных параметров

        a = l[:]

        a = [-1 if isFloat(K) else K for K in a]    #  если не число, то сделать  -1

        if isNul:                                   # Если не может быль ноль
            a = [-1 if float(K) == 0 else K for K in a]

        a.reverse()

        x = 0
        q = 0
        tmp = []

        if a[x] == -1:                           # Протягивание последнего реального числа до конца списка
            for i in range(len(a)):
                if a[i] == -1:
                    tmp.append(i)
                else:
                    q = a[i]
                    break
            whatAutoAvrg = whatAutoAvrg + [len(a) - z - 1 for z in tmp]
            for j in range(len(tmp)):
                a[j] = float(q)
            was_chg = True

        a.reverse()


        x = 0
        q = 0
        tmp = []

        if a[x] == -1:                            # Протягивание первого реального числа к началу списка
            for i in range(len(a)):
                if a[i] == -1:
                    tmp.append(i)
                else:
                    q = a[i]
                    break
            whatAutoAvrg = whatAutoAvrg + tmp
            for j in range(len(tmp)):
                a[j] = float(q)
            was_chg = True

        x = 1
        while x != len(a) - 1:         # Средние значения, по предыдущему и последующему значениям

            q2 = 0
            tmp = []

            if a[x] == -1:
                q1 = x - 1
                for i in range(x, len(a)):
                    if a[i] == -1:
                        tmp.append(i)
                    else:
                        q2 = i
                        break
                whatAutoAvrg = whatAutoAvrg + tmp

                for j in range(len(tmp)):
                    a[tmp[j]] = round( (float(a[q1]) + float(a[q2])) / 2, 1 )
                was_chg = True

            x = x + 1

        return a, whatAutoAvrg, was_chg

    except Exception as e:
        print(e)
        return l, [], False



def getSkvNfromText(S):
    c = ''
    for i in range(len(S)):
        if S[i]!='|':
            c = c+S[i]
        else:
            break
    return c


def getFormName(S):                        #  Полное имя пласта для sql
    nn = S[len(getSkvNfromText(S)) + 5:]
    return nn


def getPlaceName(S):
    for i, itm in enumerate(S):
        if itm == '|':
            cc = S[i:]
            break
    return cc


# создание диапазона удаляя все лишнее
def doRangeForSpear(l, r1,r2):
    mark = []
    a = r1-1
    b = r2 -1
    L = l[:]

    for i in range(len(L)):
        if i < a or i > b:
            #del L[i]
            mark.append(i)
    for n in sorted(mark, reverse=True):
        del L[n]

    return L


def  pzabRepeat(a):
    max = 0
    i = 0
    while i != len(a) - 1:
        r = 1
        for j in range(i, len(a) - 1):
            if a[j + 1] != a[j]:
                i = i + 1
                break
            else:
                r = r + 1
                if max < r:
                    max = r
            i = i + 1
    z = round(max/len(a)*100, 0)
    return z


def error_type(a):
    if a == 0:
        b = 'Дата'
    if a == 1:
        b = 'Объекты работы'
    if a == 2:
        b = '№ скважины'
    if a == 3:
        b = 'Координата забоя Х'
    if a == 4:
        b = 'Координата забоя Y'
    if a == 5:
        b = 'Закачка за посл.месяц, м3'
    if a == 6:
        b = 'Забойное давление (ТР), атм'
    if a == 7:
        b = 'Пластовое давление (ТР), атм'
    if a == 8:
        b = 'Время работы под закачкой, часы'
    if a == 9:
        b = 'Время работы в добыче, часы'
    if a == 10:
        b = 'Диаметр штуцера, мм'
    if a == 11:
        b = 'Приемистость (ТР), м3/сут'
    if a == 12:
        b = 'Приемистость за последний месяц, м3/сут'
    if a == 13:
        b = 'Обводненность за посл.месяц, % (вес)'
    if a == 14:
        b = 'Обводненность (ТР), % (объём)'
    if a == 15:
        b = 'Дебит нефти за последний месяц, т/сут'
    if a == 16:
        b = 'Дебит жидкости за последний месяц, т/сут'
    if a == 17:
        b = 'Динамический уровень (ТР), м'
    if a == 18:
        b = 'Нефтенасыщенная толщина, м'
    if a ==19:
        b = 'Дебит нефти (ТР), т/сут'
    return b

def InRadius(X0,Y0,X1,Y1,X2,Y2,r):
    rez = False
    if X2>0:
        X3 = (X1+X2)/2
        Y3 = (Y1+Y2)/2
        X4 = (X1+X3)/2
        Y4 = (Y1+Y3)/2
        X5 = (X2+X3)/2
        Y5 = (Y2+Y3)/2
        if lenWell(X0,Y0,X1,Y1)<r:
            rez = True
        if lenWell(X0,Y0,X2,Y2)<r:
            rez = True
        if lenWell(X0,Y0,X3,Y3)<r:
            rez = True
        if lenWell(X0,Y0,X4,Y4)<r:
            rez = True
        if lenWell(X0,Y0,X5,Y5)<r:
            rez = True
    else:
        if lenWell(X0,Y0,X1,Y1)<r:
            rez = True

    return rez


def lenWell_gorizon(x1,y1,x2,y2, xx2, yy2):
    L1 = lenWell(x1, y1, x2, y2)
    L2 = lenWell(x1, y1, xx2, yy2)
    L = lenWell(x2, y2, xx2, yy2)
    if (L1 * L1 > L2 * L2 + L * L) or (L2 * L2 > L1 * L1 + L * L):
        P = min(L1, L2)
    else:
        A = yy2 - y2
        B = x2 - xx2
        C = -1 * x2 * (yy2 - y2) + y2 * (xx2 - x2)
        x3 = (B * x1 / A - C / B - y1) * A * B / (A * A + B * B)
        y3 = B * x3 / A + y1 - B * x1 / A

        P = lenWell(x1, y1, x3, y3)


    return P

# Угол наклона горизонтальной скважины на карте

def degWell(X1,Y1,X2,Y2):
    if X2-X1==0:
        a = 1
    else:
        a = X2-X1
    deg = math.degrees(math.atan((Y2-Y1)/(a)))
    if X2<X1:
        deg = deg + 180

    return deg


def lenWell(X1,Y1,X2,Y2):
    length = ((X2 - X1) ** 2 + (Y2 - Y1) ** 2) ** 0.5
    return length

''' Qinj – накопленная закачка воды, м3
    Bw – объемный коэффициент нефти и воды
    H  – эффективная толщина, м
    m – пористость пласта, доли ед.
    So – начальная нефтенасыщенность, доли ед.
    So_min – минимальная нефтенасыщенность, доли ед.
'''

def R_dob(Qoil, Bo, Ro, H, m, So, So_min, x1, y1 ,x2 ,y2):

    if x2<0:      # нет координаты 2 значит это вертикальная
        a = Qoil * Bo
        b = Ro * math.pi * H * m * (So - So_min)
        R = math.sqrt(a / b)
        return R
    else:
        L = lenWell(x1, x2 ,y1 ,y2)

        a = math.pi * Qoil * Bo
        b = H * m * Ro * (So - So_min)
        R = (-1 * L + math.sqrt(L * L + a / b)) / math.pi
        return R


def R_nag(Qinj, Bw, H, m, So, So_min, x1, y1 ,x2 ,y2):
    if x2 < 0:
        R = math.sqrt(Qinj * Bw / (math.pi * H * m * (So - So_min)))
        return R
    else:
        L = lenWell(x1, x2, y1, y2)
        a = math.pi * Qinj
        b = H * m * (So - So_min)
        R = (-1 * L + math.sqrt(L * L + a / b)) / math.pi
        return R
