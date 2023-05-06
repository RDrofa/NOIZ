from mat import isFloat, isZero, toFloat, toFloat2, PstartFill

class dataform():

    def __init__(self, nameform, mesto, pars):
        self.Bw = pars[0]
        self.mu = pars[1]
        self.kw = pars[2]
        self.m = pars[3]
        self.Bo = pars[4]
        self.So = pars[5]
        self.So_min = pars[6]
        self.Ro = pars[7]
        self.P = pars[8]
        self.nameform = nameform
        self.mesto = mesto

        self.form_tuple = ()

        #self.check()

    def isFloat(self, s):
        try:
            x = float(s)
            if x > 0:
                return False
            else:
                return True
        except:
            return True


    def check(self):
        self.err = ''
        if self.isFloat(self.Bw):
            self.err = 'Bw'
        if self.isFloat(self.mu):
            self.err = 'mu'
        if self.isFloat(self.kw):
            self.err = 'kw'
        if self.isFloat(self.m):
            self.err = 'm'
        if self.isFloat(self.Bo):
            self.err = 'Bo'
        if self.isFloat(self.So):
            self.err = 'So'
        if self.isFloat(self.So_min):
            self.err = 'So_min'
        if self.err != 'So' and self.err != 'So_min':
            if self.So - self.So_min <=0:
                self.err = 'So < So_min'
        if self.isFloat(self.Ro):
            self.err = 'Ro'
        if self.isFloat(self.P):
            self.err = 'P'
        if self.nameform == '':
            self.err = 'Нет названия пласта'
        if self.mesto == '':
            self.err = 'Нет названия месторождения'

        if self.err == '':
            self.tupleForBD()


    def tupleForBD(self):

        self.p1 = self.nameform + '|' + self.mesto + '|'
        p2 = self.nameform
        p3 = self.Bw
        p4 = self.mu
        p5 = self.kw
        p6 = self.m
        p7 = self.Bo
        p8 = self.So
        p9 = self.So_min
        p10 = self.Ro
        p11 = self.mesto
        p12 = self.P

        l = [self.p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12]
        self.form_tuple = tuple(l)


class datawell():

    def __init__(self, df, P):
        self.df = df

        #print(self.df['Нефтенасыщенная толщина, м'].tolist())
        #print(self.df['№ скважины'].tolist())

        a = self.df['№ скважины'].tolist()
        self.wellName = a[0]
        a = self.df['Координата забоя Х'].tolist()
        self.XX = int(a[0])
        a = self.df['Координата забоя Y'].tolist()
        self.YY = int(a[0])
        a = self.df['Координата X'].tolist()
        self.X = a[0]
        a = self.df['Координата Y'].tolist()
        self.Y = a[0]
        a = self.df['Характер работы'].tolist()
        self.typ =a[0]
        a = self.df['Нефтенасыщенная толщина, м'].tolist()
        self.H = a[0]
        self.H_check = 0

        self.Re = 0.084
        self.Re_check = 2

        self.currPstart = P



        self.L_dat = self.df['Дата'].tolist()
        self.L_debLiq = self.df['Дебит жидкости за последний месяц, т/сут'].tolist()
        self.L_debOil = self.df['Дебит нефти за последний месяц, т/сут'].tolist()
        self.L_water = self.df['Обводненность за посл.месяц, % (вес)'].tolist()
        self.L_waterTR = self.df['Обводненность (ТР), % (объём)'].tolist()
        self.L_debLiqTR = self.df['Дебит жидкости (ТР), м3/сут'].tolist()
        self.L_debOilTR = self.df['Дебит нефти (ТР), т/сут'].tolist()
        self.L_dynLevel = self.df['Динамический уровень (ТР), м'].tolist()
        self.L_Pzab = self.df['Забойное давление (ТР), атм'].tolist()
        self.L_PriemTR = self.df['Приемистость (ТР), м3/сут'].tolist()
        self.L_Diam = self.df['Диаметр штуцера, мм'].tolist()
        self.L_inject = self.df['Закачка за посл.месяц, м3'].tolist()
        self.L_Pplast = self.df['Пластовое давление (ТР), атм'].tolist()
        self.L_priem = self.df['Приемистость за последний месяц, м3/сут'].tolist()
        self.L_debTime = self.df['Время работы в добыче, часы'].tolist()
        self.L_zakTime = self.df['Время работы под закачкой, часы'].tolist()


        self.L_debLiq_check = [0 for i in range(len(self.L_debLiq))]
        self.L_debOil_check = [0 for i in range(len(self.L_debOil))]
        self.L_debLiqTR_check = [0 for i in range(len(self.L_debLiq))]
        self.L_debOilTR_check = [0 for i in range(len(self.L_debOil))]
        self.L_water_check = [0 for i in range(len(self.L_water))]
        self.L_waterTR_check = [0 for i in range(len(self.L_waterTR))]
        self.L_debLiqTR_check = [0 for i in range(len(self.L_debLiqTR))]
        self.L_debOilTR_check = [0 for i in range(len(self.L_debOilTR))]
        self.L_dynLevel_check = [0 for i in range(len(self.L_dynLevel))]
        self.L_Pzab_check = [0 for i in range(len(self.L_Pzab))]
        self.L_PriemTR_check = [0 for i in range(len(self.L_PriemTR))]
        self.L_Diam_check = [0 for i in range(len(self.L_Diam))]
        self.L_inject_check = [0 for i in range(len(self.L_inject))]
        self.L_Pplast_check = [0 for i in range(len(self.L_Pplast))]
        self.L_priem_check = [0 for i in range(len(self.L_priem))]
        self.L_debTime_check = [0 for i in range(len(self.L_debTime))]
        self.L_zakTime_check = [0 for i in range(len(self.L_zakTime))]

        self.isRec = True


        self.addData()
        self.checkAll()


    def checkAll(self):

        self.err = False



        self.dict_err = {'L_debLiq':4,'L_debOil':4,'L_debLiqTR':4,'L_debOilTR':4,'L_water':4, 'L_waterTR':4, 'L_dynLevel':4, 'L_Pzab':4, 'L_Diam':4, 'L_inject':4, 'L_Pplast':4, 'L_priem':4, 'L_PriemTR':4}



        for i in range(len(self.L_dat)):
            if self.L_Pzab_check[i] == 1:
                self.L_Pzab_check[i] = 0
            if  self.L_Pplast_check[i] == 1:
                self.L_Pplast_check[i] = 0


        if isZero(self.H):
            self.H_check = 1
            self.err = True
        elif self.H_check == 30:
            self.H_check = 3

        if isZero(self.Re):
            self.Re_check = 1
            self.err = True
        elif self.Re_check == 30:
            self.Re_check = 3


        for i in range(len(self.L_dat)):

            if self.typ == 'НЕФ':



                if isFloat(self.L_debLiq[i]):
                    self.L_debLiq_check[i] = 1
                    self.dict_err['L_debLiq'] = 1
                    self.err = True
                elif  self.L_debLiq_check[i] == 30:
                    self.L_debLiq_check[i] = 3

                if isFloat(self.L_debOil[i]):
                    self.L_debOil_check[i] = 1
                    self.dict_err['L_debOil'] = 1
                    self.err = True
                elif self.L_debOil_check[i] == 30:
                    self.L_debOil_check[i] = 3

                if isFloat(self.L_debLiqTR[i]):
                    self.L_debLiqTR_check[i] = 1
                    self.dict_err['L_debLiqTR'] = 1
                    self.err = True
                elif  self.L_debLiqTR_check[i] == 30:
                    self.L_debLiqTR_check[i] = 3

                if isFloat(self.L_debOilTR[i]):
                    self.L_debOilTR_check[i] = 1
                    self.dict_err['L_debOilTR'] = 1
                    self.err = True
                elif self.L_debOilTR_check[i] == 30:
                    self.L_debOilTR_check[i] = 3

                if isFloat(self.L_water[i]):
                    self.L_water_check[i] = 1
                    self.dict_err['L_water'] = 1
                    self.err = True
                elif float(self.L_water[i])>100:
                    self.L_water_check[i] = 1
                    self.err = True
                elif self.L_water_check[i] == 30:
                    self.L_water_check[i] = 3

                if isFloat(self.L_waterTR[i]):
                    self.L_waterTR_check[i] = 1
                    self.dict_err['L_waterTR'] = 1
                    self.err = True
                elif int(self.L_waterTR[i])>100:
                    self.L_waterTR_check[i] = 1
                    self.err = True
                elif self.L_waterTR_check[i] == 30:
                    self.L_waterTR_check[i] = 3

                if isFloat(self.L_dynLevel[i]):
                    self.L_dynLevel_check[i] = 1
                    self.dict_err['L_dynLevel'] = 1
                    self.err = True
                elif self.L_dynLevel_check[i] == 30:
                    self.L_dynLevel_check[i] = 3

            else:


                if isFloat(self.L_Diam[i]):
                    self.L_Diam_check[i] = 1
                    self.dict_err['L_Diam'] = 1
                    self.err = True
                elif  self.L_Diam_check[i] == 30:
                    self.L_Diam_check[i] = 3

                if isFloat(self.L_inject[i]):
                    self.L_inject_check[i] = 1
                    self.dict_err['L_inject'] = 1
                    self.err = True
                elif self.L_inject_check[i] == 30:
                    self.L_inject_check[i] = 3


                if isZero(self.L_priem[i]):
                    self.L_priem_check[i] = 1
                    self.dict_err['L_priem'] = 1
                    self.err = True
                elif self.L_priem_check[i] ==30:
                    self.L_priem_check[i] = 3

                if isFloat(self.L_PriemTR[i]):
                    self.L_PriemTR_check[i] = 1
                    self.dict_err['L_PriemTR'] = 1
                    self.err = True
                elif self.L_PriemTR_check[i] ==30:
                    self.L_PriemTR_check[i] = 3

            if isZero(self.L_Pzab[i]):
                self.L_Pzab_check[i] = 1
                self.dict_err['L_Pzab'] = 1
                self.err = True
            elif self.L_Pzab_check[i] == 30:
                self.L_Pzab_check[i] = 3

            if isZero(self.L_Pplast[i]):
                self.L_Pplast_check[i] = 1
                self.dict_err['L_Pplast'] = 1
                self.err = True
            elif self.L_Pplast_check[i] == 30:
                self.L_Pplast_check[i] = 3


            if self.typ == 'НЕФ' and not isZero(self.L_Pzab[i]) and not isZero(self.L_Pplast[i]) and float(self.L_Pzab[i]) >= float(self.L_Pplast[i]):
                self.L_Pzab_check[i] = 1
                self.L_Pplast_check[i] = 1
                self.err = True
                self.dict_err['L_Pplast'] = 1
                self.dict_err['L_Pzab'] = 1


            if self.typ == 'НАГ' and not isZero(self.L_Pzab[i]) and not isZero(self.L_Pplast[i]) and float(self.L_Pzab[i]) <= float(self.L_Pplast[i]):
                self.L_Pzab_check[i] = 1
                self.L_Pplast_check[i] = 1
                self.err = True
                self.dict_err['L_Pplast'] = 1
                self.dict_err['L_Pzab'] = 1

            if not self.isRec:
                self.err = False



    def  checkDepress(self, Pz, Pp, typ):

        r = 0

        if toFloat(Pz)>0 and toFloat(Pp)>0:
            if typ=='НАГ':
                if Pz>Pp:
                    r = 2
                else:
                    r = 1

            if typ=='НЕФ':
                if Pz<Pp:
                    r = 2
                else:
                    r = 1

        else:
            r = 0

        return r






    def  addData(self):

        # Если последнего значения пластового нет, то скопировать с предпоследнего

        u = len(self.L_Pplast)
        if toFloat(self.L_Pplast[u - 1]) <= 0 and toFloat(self.L_Pplast[u - 2]) > 0:
            self.L_Pplast[u - 1] = self.L_Pplast[u - 2]
            self.L_Pplast_check[u - 1] = 2

        #  Поиск позиций где пропущено Р пласт

        self.autoPplast = []
        for i in range(len(self.L_Pplast)):
            if toFloat(self.L_Pplast[i]) <= 0:
                self.autoPplast.append(i)
            else:
                break

        u = len(self.L_Pzab)

        self.L_Pzab.reverse()
        self.L_Pplast.reverse()
        for i in range(u-1):
            if self.checkDepress(self.L_Pzab[i], self.L_Pplast[i], self.typ) == 1 and self.checkDepress(
                    self.L_Pzab[i + 1], self.L_Pplast[i + 1], self.typ) == 2:
                self.L_Pzab[i] = self.L_Pzab[i + 1]
                self.L_Pzab_check.reverse()
                self.L_Pzab_check[i] = 2
                self.L_Pzab_check.reverse()
                break
        self.L_Pzab.reverse()
        self.L_Pplast.reverse()
        for i in range(u - 1):
            if self.checkDepress(self.L_Pzab[i], self.L_Pplast[i], self.typ) == 1 and self.checkDepress(
                    self.L_Pzab[i + 1], self.L_Pplast[i + 1], self.typ) == 2:
                self.L_Pzab[i] = self.L_Pzab[i + 1]
                self.L_Pzab_check[i] = 2
                break


        # Если последнего значения забойного нет, то скопировать с предпоследнего


        if toFloat(self.L_Pzab[u - 1]) <= 0 and toFloat(self.L_Pzab[u - 2]) > 0:
            self.L_Pzab[u - 1] = self.L_Pzab[u - 2]
            self.L_Pzab_check[u-1] = 2  #  значение было получено программно

        # Если начальных значений нет, но есть значения в будущем, то скопировать первое попавшее значения в прошлое
        '''if toFloat(self.L_Pzab[0]) <= 0 and len(set(self.L_Pzab)) > 1:
            self.L_Pzab, auto = PstartFill(self.L_Pzab, -1)
            for i in auto:
                self.L_Pzab_check[i] = 2'''




    def addDataPplast(self):

        if len(self.autoPplast) > 0:

            for ind in self.autoPplast:
                self.L_Pplast[ind] = int(self.currPstart)
                self.L_Pplast_check[ind] = 2
            self.checkAll()









