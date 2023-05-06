import sqlite3
import pandas as pd
import  numpy  as  np
from mat import getSkvNfromText as S
from mat import getFormName as F
from mat import getFormName as F
from mat import getPlaceName as Place
from dateutil.relativedelta import *
from datetime import datetime


class SQL():

    def __init__(self):
        super(SQL, self).__init__()
        self.connectBD()

        self.createTableChenParam()


    def createTableChenParam(self):

        q = "CREATE TABLE IF NOT EXISTS chenparam (well TEXT  UNIQUE NOT NULL, gtm TEXT  NOT NULL, " \
            "months INTEGER NOT NULL, rdp REAL NOT NULL, mincount INTEGER NOT NULL, " \
            "mininterval REAL NOT NULL, points REAL NOT NULL, PRIMARY KEY(well))"
        self.cursor.execute(q)

    def insChenParam(self, param_tuple):
        q = """INSERT OR REPLACE  INTO chenparam VALUES (?,?,?,?,?,?,?)"""
        self.cursor.executemany(q, param_tuple)
        self.sqlite_conn.commit()

    def getChenParam(self, w):
        q = "SELECT gtm, months, rdp, mincount, mininterval, points from chenparam where well = '" + w + "'"
        self.cursor.execute(q)
        A = self.cursor.fetchone()
        if A is None:
            return [], False
        else:
            if len(A) > 0:
                l=[]
                l.append(A[3])
                l.append(A[5])
                l.append(A[2])
                l.append(A[4])
                l.append(A[1])
                return(l, bool(A[0]))
            else:
                return [], False


    # Определить тип скважины в ГТМ по дате в истории

    def getTypeWellForGTM(self, D, p,w,m):

        d = D+'-01 00:00:00'

        q = "SELECT well from history where dat = '" +d + "'  and well like '"+str(w)+"%" + str(p) + "|" + m +"|'"

        self.cursor.execute(q)
        A = self.cursor.fetchall()

        if len(A)>0:
            A = A[0][0]
            if 'НАГ' in A:
                return 'НАГ'
            elif 'НЕФ' in A:
                return 'НЕФ'
            else:
                return ''
        else:
            return ''


    #  Загрузка данных по пласту для редактирования

    def getForEditForm(self, formID):

        q = "SELECT  bw, mu, kw, m, bo, So, So_min, Ro from form  where ID = ?"
        self.cursor.execute(q, (formID,))
        A = self.cursor.fetchall()
        return A

    #  Изменение данных по пласту
    #L = [bo, ro, m, so, so_min, bw, kw, mu, pn]
    def updateForm(self, formID, L):
        q = "update form set bo = "+L[0]+", Ro="+L[1]+\
            ", m="+L[2]+", So="+L[3]+", So_min="+L[4]+", bw="+L[5]+", kw="+L[6]+", mu="+L[7]+", P="+L[8]+" where ID = ?"

        self.cursor.execute(q, (formID,))
        self.sqlite_conn.commit()

    #  Изменение данных по скважине
    def updateWell(self, wellID, L):
        q = "update well set H = "+L[0]+", Re="+L[1]+" where ID = ?"

        self.cursor.execute(q, (wellID,))
        self.sqlite_conn.commit()


    def dfDellEmpty(self, df):
        def chk(zz,dd):
            if zz!=zz or zz ==0 or dd!=dd or dd ==0:
                return False
            else:
                return True

        N = df['numb'].tolist()
        Z = df['zakTime'].tolist()
        D = df['debTime'].tolist()
        deleted = []

        a = []
        for i in range(len(N)):
            if chk(Z[i],D[i]) == False:
                a.append(0)
            else:
                a.append(1)

        a.append(1)
        a.append(1)
        a.append(1)
        a.append(1)

        i = 0
        while i<len(a)-4:
            if a[i]==0:
                if a[i+1]==1:
                    deleted.append(N[i])
                    i=i+1
                if  a[i+1]==0 and a[i+2]==1:
                    deleted.append(N[i])
                    deleted.append(N[i+1])
                    i = i + 2
                if a[i + 1] == 0 and a[i + 2] == 0 and a[i + 3] == 1:
                    deleted.append(N[i])
                    deleted.append(N[i + 1])
                    deleted.append(N[i + 2])
                    i = i + 3
                if a[i + 1] == 0 and a[i + 2] == 0 and a[i + 3] == 0:
                    for j in range(i+3,len(a)):
                        if a[j]==1:
                            i = j
                            break
                        else:
                            i = len(a)+1
            else:
                i = i+1

        #print(deleted)
        return deleted


    def doEmptyDataframe(self):
        d = pd.DataFrame()
        return d

    def doRepDataframe(self):
        d = pd.DataFrame(columns = ['№ нагнетательной скважины',
              'Объект',
              'Состояние',
              'Накопленная закачка, тыс.м3',
              'Приемистость за последний месяц, м3/сут',
              'Забойное давление (ТР), атм',
              'Диаметр штуцера, мм',
              'Наличие проблемы (НЗ/автоГРП/загрязнение ПЗП)',
              'Объем непроизводительной закачки, м3',
              'Процент непроизводительной закачки, %',
              'Срок окупаемости, мес',
              '№ добывающей скважины',
              'Объект',
              'Состояние',
              'Накопленная добыча нефти, т',
              'Дебит нефти за последний месяц, т/сут',
              'Дебит жидкости за последний месяц, т/сут',
              'Обводненность за посл.месяц, % (вес)',
              'Забойное давление (ТР), атм',
              'Пластовое давление (ТР), атм',
              'Источник обводнения',
              'Дебит нефти - Прогноз, т/сут',
              'Дебит жидкости -  Прогноз, т/сут',
              'Обводненность - Прогноз, %',
              'Объем непроизводительной добычи воды, т',
              'Срок окупаемости РИР, мес',
              'Расстояние между скважинами, м',
              'Временной лаг, мес.',
              'Коэф. Спирмена жидкость',
              'Коэф. Спирмена нефть',
              'Коэф. Спирмена Обводненность',
              'Коэф. Спирмена Синтетика',
              'Временной лаг Рзаб, мес.',
              'Коэф. Спирмена Рзаб',
              'Степень связи',
              'Примечание'])
        return d


    def df_to_date(self,d,x):
        d[x] = pd.to_datetime(d[x], format="%Y/%m/%d")
        return d

    def connectBD(self):
        try:
            #appdir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
            #self.sqlite_conn = sqlite3.connect(os.path.join(appdir, 'data.db'))
            self.sqlite_conn = sqlite3.connect('data.db')
            self.cursor = self.sqlite_conn.cursor()
            self.cursor.execute("PRAGMA foreign_keys=ON")

            #q = """CREATE TABLE IF NOT EXISTS alldates (dat TEXT); """
            #self.cursor.executescript(q)


            print("База данных создана и успешно подключена к SQLite")
            #self.getALLfromBD()
            

        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            #if (sqlite_connection):
             #   sqlite_connection.close()
             #   print("Соединение с SQLite закрыто")
             pass


    def closBD(self):
        self.sqlite_conn.close()


    #----------------------УДАЛЕНИЕ--------------------

    def delPlast(self, form, typ):

        if typ==0:
            q = "DELETE from form where ID =?"
            self.cursor.execute(q, (form,))
            self.sqlite_conn.commit()

        else:
            q = "DELETE from well where formFK =?"
            self.cursor.execute(q, (form,))
            self.sqlite_conn.commit()



    def delWell(self, well):

        if type(well) == list:
            q = "DELETE from well where ID =?"
            self.cursor.executemany(q, well)
            self.sqlite_conn.commit()


        else:

            q = "DELETE from well where ID =?"
            self.cursor.execute(q, (well,))
            self.sqlite_conn.commit()


    #--------------------------------------------------


    #  ВЫГРУЗКА ДЛЯ СПИРМЕНА НОВАЯ!!!


    def doTableAllDates(self, p11):

        q = """DROP  TABLE IF EXISTS D;"""
        self.cursor.executescript(q)

        q = """CREATE TEMP TABLE  D (dat TEXT);"""
        self.cursor.executescript(q)

        q = """SELECT max(dat), min(dat) from (SELECT  dat FROM history WHERE well like '%|"""
        q = q + p11 + """') """
        self.cursor.execute(q)

        rez = self.cursor.fetchone()
        Dmax = rez[0]
        Dmin = rez[1]
        alldat = pd.date_range(start=Dmin, end=Dmax, freq='MS').strftime('%Y-%m-%d 00:00:00').tolist()
        list_tuple = []
        for i in alldat:
            w = []
            w.append(i)
            list_tuple.append(tuple(w))
        q= """INSERT INTO D VALUES (?)"""
        self.cursor.executemany(q, list_tuple)
        self.sqlite_conn.commit()



    # P11 - полное имя пласта первой скв. (как в базе)
    # P12 - полное имя пласта второй скв. (как в базе)
    # P3 - полное имя добывающей
    # P2 - полное имя скважины наг


    def getDataSpearwell(self, p11, p12, p2, p3):

        #print("1 Текущая секунда: %d" % now.microsecond)

        q = """CREATE TEMP TABLE  nef AS
        SELECT dat, debTime, debLiq, debOil, Pzab, water, debLiq*Pzab as synth FROM history WHERE well='"""
        q = q + p3
        q = q + """';CREATE TEMP TABLE  nag AS
        SELECT dat, zakTime, priem FROM history WHERE well='"""
        q = q + p2
        q = q + """';"""


        if 'НЕФ' in p2:
            s = 'НЕФ'
        else:
            s = 'НАГ'
        q = q + """CREATE TEMP TABLE  nagEVT AS
                SELECT dat, GROUP_CONCAT(event) as event FROM event WHERE well='"""
        q = q + S(p2) + """' and form1 ='""" + p11 + """' and type = '""" + s + """' GROUP BY dat;"""

        if 'НЕФ' in p3:
            s = 'НЕФ'
        else:
            s = 'НАГ'
        q = q + """CREATE TEMP TABLE  nefEVT AS
                SELECT dat, GROUP_CONCAT(event) as event FROM event WHERE well='"""
        q = q + S(p3) + """' and form1 ='""" + p12 + """' and type = '""" + s + """' GROUP BY dat;"""

        self.cursor.executescript(q)

        if p2 == '2076|НАГ|1БС10|Суторминское_1|':
            now = datetime.now()



        '''if p2 == '2076|НАГ|1БС10|Суторминское_1|':

            print(datetime.now() - now)
            print(p2)
            print(p3)'''


        q = """SELECT D.dat, nag.zakTime, nag.priem, nef.debTime, nef.debLiq, nef.debOil, nef.Pzab, nef.water, nef.synth, nagEVT.event, nefEVT.event  FROM D
        LEFT JOIN nag
        ON D.dat=nag.dat
        LEFT JOIN nef
        ON D.dat=nef.dat
        LEFT JOIN nagEVT
        ON D.dat=nagEVT.dat
        LEFT JOIN nefEVT
        ON D.dat=nefEVT.dat 
        ORDER BY D.dat;"""

        self.cursor.execute(q)

        df = pd.DataFrame(self.cursor.fetchall(),
                          columns=['D','zakTime','priem','debTime','debLiq','debOil','Pzab', 'water', 'synth', 'nagEVT', 'nefEVT'])



        q = """DROP  TABLE  nef;
        DROP  TABLE  nag;
        DROP  TABLE  nagEVT;
        DROP  TABLE  nefEVT;"""
        self.cursor.executescript(q)

        df = df.fillna(0)

        return df



    # Проверка наличия ГРП
    def getWasGRP(self, well, form):
        q = "SELECT DISTINCT dat from event  where well = ? and form1 = ? and event = 'ГРП' "
        self.cursor.execute(q, (S(well), form))
        dl = len(self.cursor.fetchall())
        if dl>0:
            return True
        else:
            return False



    def getEventfromBD(self, well, form, type):     # ???????????????????????????????????????????????????????????

        q = "SELECT  dat, event from event  where well = ? and form1 = ?  and type = ? order by dat"
        self.cursor.execute(q, (well, form, type))
        df_ev = pd.DataFrame(self.cursor.fetchall(), columns=['Дата', 'ГТМ'])


        # print(df_grp)
        return df_ev



    # Выгрузна данных для ХОЛЛА 2

    def getDataforHallObj(self, wellID, formID):
        nn = '%' + '|НАГ|' + formID

        cols = ['№ скважины', 'Дата', 'Закачка за посл.месяц, м3', 'Время работы под закачкой, часы',
                'Забойное давление (ТР), атм', 'Пластовое давление (ТР), атм', 'Диаметр штуцера, мм',
                'Приемистость за последний месяц, м3/сут', 'Приемистость (ТР), м3/сут', 'Закачка ТР']

        q = "SELECT substr(well,1,length(well)-length(?)+1) as N, dat, inject, zakTime, Pzab, Pplast, Diam, Priem, PriemTR, zakTime/24*PriemTR as injectTR from history where well =? and zakTime > 0"
        self.cursor.execute(q, (nn, wellID))
        df_hall = pd.DataFrame(self.cursor.fetchall(), columns=cols)

        df_hall['Дата'] = pd.to_datetime(df_hall['Дата'], format="%Y/%m/%d")
        df_hall.set_index('Дата')
        df_hall = df_hall.fillna(0)

        return df_hall

        '''df_evt = self.getEventfromBDforAll(wellID, formID, 'НАГ')
        df_evt['Дата'] = pd.to_datetime(df_evt['Дата'], format="%Y/%m/%d")
        df_evt.set_index('Дата')
        df = pd.merge(left=df, right=df_evt, how='left', on="Дата")'''





    # Выгрузна данных для ХОЛЛА
    def getHallFromBD(self, well, form, HallMin):

        nn = '%'+form

        # Пустой датафрейм со всеми датами
        q = "SELECT DISTINCT dat from history  where well like ? order by dat"
        self.cursor.execute(q, (nn,))
        df_dat = pd.DataFrame(self.cursor.fetchall(), columns=['Дата'])

        cols = ['Дата', 'Закачка за посл.месяц, м3','Время работы под закачкой, часы',
            'Забойное давление (ТР), атм','Пластовое давление (ТР), атм','Диаметр штуцера, мм','Приемистость за последний месяц, м3/сут','Приемистость (ТР), м3/сут']
            
        q = "SELECT dat, inject, zakTime, Pzab, Pplast, Diam, Priem, PriemTR from history where well =? and zakTime>"+HallMin
        q2 = "SELECT dat, inject, zakTime, Pzab, Pplast, Diam, Priem, PriemTR from history where well =?"
        self.cursor.execute(q, (well,))
        df = pd.DataFrame(self.cursor.fetchall(), columns = cols)
        self.cursor.execute(q2, (well,))
        df2_ = pd.DataFrame(self.cursor.fetchall(), columns = cols)

        # Объединение датафрейма по НАГ со всеми датами
        df2 = pd.merge(left=df_dat, right=df2_, how='left', on="Дата")
        
        df['Дата'] = pd.to_datetime(df['Дата'], format="%Y/%m/%d")
        df.set_index('Дата')
        df2['Дата'] = pd.to_datetime(df2['Дата'], format="%Y/%m/%d")
        df2.set_index('Дата')
        df2 = df2.fillna(0)

        #df_dat.to_excel('DDDDDDDDDDDDDDD.xlsx')
        #df2.to_excel('MMMMMMMMMMMMMMMMM.xlsx')



        if 'НЕФ' in well:
            s = 'НЕФ'
        else:
            s = 'НАГ'

        df_evt = self.getEventfromBD(S(well), form, s)
        df_evt['Дата'] = pd.to_datetime(df_evt['Дата'], format="%Y/%m/%d")
        df_evt.set_index('Дата')
        df2 = pd.merge(left=df2, right=df_evt, how='left', on="Дата")
        df = pd.merge(left=df, right=df_evt, how='left', on="Дата")

        return df,df2


    def getFormPar(self, form):
        q = "SELECT bw, mu, kw from form where ID =?"
        self.cursor.execute(q, (form,))
        F = self.cursor.fetchone()
        return F[0], F[1], F[2]
        
        
          
    # Выгрузна данных для ЧЕНА
    def getChenFromBD(self, well, form):

        nn = '%' + form

        # Пустой датафрейм со всеми датами
        q = "SELECT DISTINCT dat from history  where well like ? order by dat"
        self.cursor.execute(q, (nn,))
        df_dat = pd.DataFrame(self.cursor.fetchall(), columns=['Дата'])


        cols2 = ['Дата', 'Дебит жидкости за последний месяц, т/сут', 'Дебит жидкости (ТР), м3/сут', 'Дебит нефти за последний месяц, т/сут', 'Дебит нефти (ТР), т/сут',
                'Обводненность за посл.месяц, % (вес)','Обводненность (ТР), % (объём)', 'Забойное давление (ТР), атм', 'Пластовое давление (ТР), атм',
             'Динамический уровень (ТР), м']
        cols = ['Дата', 'Обводненность за посл.месяц, % (вес)', 'Обводненность (ТР), % (объём)',
                'Дебит нефти за последний месяц, т/сут', 'Динамический уровень (ТР), м']
            
        q = "SELECT dat, water, waterTR, debOilTR, dynLevel from history where well =? and debTime>10"
        q2 = "SELECT dat, debLiq, debLiqTR, debOil, debOilTR, water, waterTR, Pzab, Pplast, dynLevel from history where well =?"
        self.cursor.execute(q, (well,))
        df = pd.DataFrame(self.cursor.fetchall(), columns = cols)
        df['Дата'] = pd.to_datetime(df['Дата'], format="%Y/%m/%d")
        df.set_index('Дата')

        self.cursor.execute(q2, (well,))
        df2_ = pd.DataFrame(self.cursor.fetchall(), columns=cols2)
        df2 = pd.merge(left=df_dat, right=df2_, how='left', on="Дата")
        df2 = df2.fillna(0)

        df2['Дата'] = pd.to_datetime(df2['Дата'], format="%Y/%m/%d")
        df2.set_index('Дата')

        if 'НЕФ' in well:
            s = 'НЕФ'
        else:
            s = 'НАГ'

        df_evt = self.getEventfromBD(S(well), form, s)
        df_evt['Дата'] = pd.to_datetime(df_evt['Дата'], format="%Y/%m/%d")
        df_evt.set_index('Дата')
        df2 = pd.merge(left=df2, right=df_evt, how='left', on="Дата")




        return df, df2


        # Выгрузна данных для ЧЕНА 2

    def getChen2FromBD(self,  form, well):
        nn = '%' + '|НЕФ|' + form
        cols = ['№ скважины', 'Дата',
                'Дебит нефти (ТР), т/сут',
                'Дебит жидкости за последний месяц, т/сут',
                'Добыча жидкости за посл.месяц, т',
                'Добыча нефти за посл.месяц, т',
                'Время работы, часы',
                'Обводненность (ТР), % (объём)',
                'Обводненность за посл.месяц, % (вес)']
        q = "SELECT substr(well,1,length(well)-length(?)+1) as N, dat, debOilTR, debLiq,  " \
            "debTime/24*debLiq as debLiqMonth, debTime/24*debOil as debOilMonth, debTime, waterTR, water from history where well = ?"

        self.cursor.execute(q, (nn,well))
        df_chen = pd.DataFrame(self.cursor.fetchall(), columns=cols)

        return df_chen


       # Выгрузна данных для НО

    def getNOfromBD(self,  form, well):
        nn = '%' + '|НЕФ|' + form
        cols = ['№ скважины', 'Дата',
                'Дебит жидкости за последний месяц, т/сут',
                'Дебит нефти за последний месяц, т/сут',
                'Обводненность за посл.месяц, % (вес)',
                'Время работы в добыче, часы']
        q = "SELECT substr(well,1,length(well)-length(?)+1) as N, dat, debLiq, debOil, water, debTime/24 from history where well = ?"

        self.cursor.execute(q, (nn,well))
        df_no = pd.DataFrame(self.cursor.fetchall(), columns=cols)
        df_no['Дата'] = pd.to_datetime(df_no['Дата'], format="%Y/%m/%d")

        l = df_no['Дата'].tolist()
        l2 = []
        ll = l[0]
        while ll != l[-1]:
            l2.append(ll)
            ll = ll + relativedelta(months=+1)
        l2.append(l[-1])

        df_tmp_dat = pd.DataFrame(l2, columns=['Дата'])
        df_no = pd.merge(left=df_tmp_dat, right=df_no, how='left', on="Дата")
        df_no = df_no.fillna(0)

        return df_no



    # Выгрузна имен всех пластов по месторождению
    def  getNamesForm(self, place):
        q = "SELECT ID from form where place = '" + place + "'"
        self.cursor.execute(q)
        F = self.cursor.fetchall()
        l=[]

        for i in range(len(F)):

            s= F[i][0]

            l.append(S(s))

        return l

    # Выгрузна данных для изменения параметров скважин
    def getWellFromBDtoChange(self, Wid):
        q = "SELECT H, Re from well where ID =?"
        self.cursor.execute(q, (Wid,))
        F = self.cursor.fetchone()
        return F[0], F[1]


    # Выгрузна данных для изменения параметров скважин с историей
    def getWellHistoryFromBDtoChange(self, Wid):

        q = """SELECT name, type, XX, YY, X, Y, H, Re from well where ID = '""" + Wid + """'"""
        self.cursor.execute(q)
        F = self.cursor.fetchone()
        q = """SELECT dat, debLiq, debOil, debLiqTR, debOilTR, inject, water, waterTR, dynLevel, debTime, zakTime, Pzab, Pplast, priem, priemTR, Diam  from history where well = '""" + Wid + """'"""
        self.cursor.execute(q)

        cols = ['Дата',
                'Дебит жидкости за последний месяц, т/сут',
                'Дебит нефти за последний месяц, т/сут',
                'Дебит жидкости (ТР), м3/сут',
                'Дебит нефти (ТР), т/сут',
                'Закачка за посл.месяц, м3',
                'Обводненность за посл.месяц, % (вес)',
                'Обводненность (ТР), % (объём)',
                'Динамический уровень (ТР), м',
                'Время работы в добыче, часы',
                'Время работы под закачкой, часы',
                'Забойное давление (ТР), атм',
                'Пластовое давление (ТР), атм',
                'Приемистость за последний месяц, м3/сут',
                'Приемистость (ТР), м3/сут',
                'Диаметр штуцера, мм']

        df = pd.DataFrame(self.cursor.fetchall(), columns=cols)
        df['№ скважины'] = F[0]
        df['Характер работы'] = F[1]
        df['Координата забоя Х'] = F[2]
        df['Координата забоя Y'] = F[3]
        df['Координата X'] = F[4]
        df['Координата Y'] = F[5]
        df['Нефтенасыщенная толщина, м'] = F[6]

        df['Дата'] = pd.to_datetime(df['Дата'], format="%Y/%m/%d")

        return df, F[7]



    # Выгрузна данных по пласту для расчета фронтов (и изменения параметров пласта)
    def  getFormFromBD(self, Fid):
        q = "SELECT bo, Ro, m, So, So_min,bw, kw, mu, P from form where ID =?"
        self.cursor.execute(q, (Fid,))
        F = self.cursor.fetchone()
        return F[0], F[1], F[2], F[3], F[4],F[5], F[6], F[7], F[8]


    #  Выгрузка из базы накопленной добычи и закачки
    def getAccumFromBD(self, Lid, Ltype):
        tmp = []
        acc = []
        q1 = "SELECT sum(inject) from history where well = ?"
        q2 = "SELECT sum(debTime/24*debOil) from history where well = ?"
        #print(Lid)
        #print(Ltype)
        for i in range(len(Lid)):
            if Ltype[i] == 'НАГ':
                self.cursor.execute(q1, (Lid[i],))
            elif Ltype[i] == 'НЕФ':
                self.cursor.execute(q2, (Lid[i],))
            else:
                pass

            L = self.cursor.fetchone()

            tmp.append(L)
        for j in range(len(tmp)):
            acc.append(tmp[j][0])

        return acc


    # Проверка существует ли пласт и получение данных по нему
    def tryGetDataPlast(self,id):

        q = "SELECT  bw, mu, kw, m, bo, So, So_min, Ro,P from form where ID =?"
        self.cursor.execute(q, (id,))
        tmp = self.cursor.fetchall()
        if len(tmp)>0:
            rezlt = list(tmp[0])
        else:
            rezlt = []
        return rezlt


    def moveToNewForm(self, id, wells, formName):

        q = "SELECT  * from form where ID =?"
        self.cursor.execute(q, (id,))
        tmp = self.cursor.fetchall()

        form_tuple = []

        for i, itm in enumerate(tmp[0]):
            if i == 0:
                a = str(itm)
                for m in range(len(a)):
                    if a[m] == '|':
                        a = formName + a[m:]
                        break
                form_tuple.append(a)
            elif i == 1:
                a = formName
                form_tuple.append(a)

            else:
                form_tuple.append(itm)
        form_tuple = tuple(form_tuple)


        sql_ins_form = """INSERT OR IGNORE INTO form VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
        self.cursor.execute(sql_ins_form, form_tuple)
        self.sqlite_conn.commit()

        self.cursor.execute("PRAGMA foreign_keys=OFF")

        for i, itm in enumerate(wells):

            a = itm.replace(S(id), formName)



            q = "update history set well = '" + a + "' where well = '" + itm + "'"
            self.cursor.execute(q)
            self.sqlite_conn.commit()

            b =  id.replace(S(id), formName)

            q = "update well set ID = '" + a + "', formFK  = '" + b +  "' where ID = '" + itm + "'"
            self.cursor.execute(q)
            self.sqlite_conn.commit()

        self.cursor.execute("PRAGMA foreign_keys=ON")





    #  ВЫГРУЗКА ИЗ  БАЗЫ ДАННЫХ ДЛЯ КАРТЫ
    def getWellFromBD(self,l):
        namee = []
        typee = []
        XX =[]
        YY =[]
        X =[]
        Y= []
        id =[]
        h = []
        Ffk = []
        re = []
        #t = tuple(l)
        q = "SELECT DISTINCT name, type, XX,YY,X,Y,ID,H, formFK, Re from well where ID =?"
        for i in range(len(l)):
            self.cursor.execute(q, (l[i],))
            wellsForMap = self.cursor.fetchall()
            namee.append(wellsForMap[0][0])
            typee.append(wellsForMap[0][1])
            XX.append(wellsForMap[0][2])
            YY.append(wellsForMap[0][3])
            X.append(wellsForMap[0][4])
            Y.append(wellsForMap[0][5])
            id.append(wellsForMap[0][6])
            h.append(wellsForMap[0][7])
            Ffk.append(wellsForMap[0][8])
            re.append(wellsForMap[0][9])

        return namee, typee,XX,YY,X,Y,id,h,Ffk, re



    #  ВЫГРУЗКА ИЗ  БАЗЫ ДАННЫХ ДЛЯ ДЕРЕВА
    def  getALLfromBD(self):

        #now = datetime.now()
        #print("Текущая секунда: %d" % now.second)

        dictTree = {}

        self.cursor.execute("SELECT DISTINCT place from form ORDER BY place")
        mesto = self.cursor.fetchall()
        #print(mesto[1][0])
        #print(mesto)

        if len(mesto) > 0:
            for i in range(len(mesto)):
                self.cursor.execute("SELECT DISTINCT name from form where place = ? ORDER BY place", (mesto[i][0],))
                forms = self.cursor.fetchall()
                #print(forms[0][0])
                #print(forms)


                dictTree2 = {}
                for j in range(len(forms)):
                    l = []
                    p = forms[j][0]+'|'+mesto[i][0]+'|'
                    self.cursor.execute("SELECT  name, type from well where formFK= ? ORDER BY name", (p,))
                    wells = self.cursor.fetchall()
                    for m in range(len(wells)):
                        l.append(wells[m][0]+'-'+wells[m][1])
                    #print(l)
                    dictTree2[forms[j][0]] = l
                   # print(dictTree2)


                dictTree[mesto[i][0]] = dictTree2
                #print(dictTree)

        #now = datetime.now()
        #print("Текущая секунда: %d" % now.second)

        return  dictTree



    def insPlastBD(self, form_tuple, skv_list_tuple, param_list_tuple):

        self.cursor.execute("PRAGMA foreign_keys=OFF")

        sql_ins_form= """INSERT OR REPLACE INTO form VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
        self.cursor.execute(sql_ins_form, form_tuple)
        self.sqlite_conn.commit()

        sql_ins_form = """INSERT OR REPLACE INTO well VALUES (?,?,?,?,?,?,?,?,?,?)"""
        self.cursor.executemany(sql_ins_form, skv_list_tuple)
        self.sqlite_conn.commit()

        sql_ins_form = """INSERT OR REPLACE INTO history VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        self.cursor.executemany(sql_ins_form, param_list_tuple)
        self.sqlite_conn.commit()

        self.cursor.execute("PRAGMA foreign_keys=ON")




    def getExcelForSql(self, path_exl):

        try:

            df_main = pd.DataFrame(pd.read_excel(path_exl))

            err = 0

            if type(df_main['Дата'].tolist()[0]) == str:
                df_main['Дата'] = pd.to_datetime(df_main['Дата'], format="%d.%m.%Y")

            err = 1
            df_main = df_main.dropna(subset=['Объекты работы'])
            err = 2
            df_main = df_main.astype({"Объекты работы": str})
            df_main = df_main.astype({"№ скважины": str})
            err = 3
            df_main['Координата забоя Х'].fillna(0, inplace=True)
            err = 4
            df_main['Координата забоя Y'].fillna(0, inplace=True)
            err = 5
            df_main['Закачка за посл.месяц, м3'].fillna('', inplace=True)
            err = 6
            df_main['Забойное давление (ТР), атм'].fillna('', inplace=True)
            err = 7
            df_main['Пластовое давление (ТР), атм'].fillna('', inplace=True)
            err = 8
            df_main['Время работы под закачкой, часы'].fillna(0, inplace=True)
            err = 9
            df_main['Время работы в добыче, часы'].fillna(0, inplace=True)
            err = 10
            df_main['Диаметр штуцера, мм'].fillna('0', inplace=True)
            self.err = 11
            df_main['Приемистость (ТР), м3/сут'].fillna(0, inplace=True)
            err = 12
            df_main['Приемистость за последний месяц, м3/сут'].fillna('', inplace=True)
            err = 13
            df_main['Обводненность за посл.месяц, % (вес)'].fillna('', inplace=True)
            err = 14
            df_main['Обводненность (ТР), % (объём)'].fillna(0, inplace=True)
            err = 15
            df_main['Дебит нефти за последний месяц, т/сут'].fillna('', inplace=True)
            err = 16
            df_main['Дебит жидкости за последний месяц, т/сут'].fillna('', inplace=True)
            err = 17
            df_main['Динамический уровень (ТР), м'].fillna('0', inplace=True)
            err = 18
            df_main['Нефтенасыщенная толщина, м'].fillna('', inplace=True)
            err = 19
            df_main['Дебит нефти (ТР), т/сут'].fillna(0, inplace=True)
            err = 20
            df_main['Дебит жидкости (ТР), м3/сут'].fillna(0, inplace=True)

        except:
            return err

        try:

            df_main.loc[(df_main['Закачка за посл.месяц, м3'] == 0) | (df_main['Закачка за посл.месяц, м3'] == '') , 'Время работы под закачкой, часы'] = 0
            df_main.loc[(df_main['Дебит жидкости за последний месяц, т/сут'] == 0) | (df_main['Дебит жидкости за последний месяц, т/сут'] == ''), 'Время работы в добыче, часы'] = 0


            df_nag = df_main.loc[df_main["Время работы под закачкой, часы"] > 0]  # 240
            df_nag.loc[(df_nag['Характер работы'] == 'НЕФ'), 'Характер работы'] = 'НАГ'
            df_nef = df_main.loc[df_main["Время работы в добыче, часы"] > 0]  # 10
            df_nef.loc[(df_nef['Характер работы'] == 'НАГ'), 'Характер работы'] = 'НЕФ'
            df_skv = pd.concat([df_nag, df_nef], ignore_index=True)  # все скважины

            return df_skv

        except Exception as e:
            return str(e)



    #  Все скважины на выбранном пласте
    def getSkvForSql(self, plast):

        p = str(plast)

        tmp = self.df_skv['Объекты работы'].str.contains(p, regex=False)

        df_skvInPlast0 = self.df_skv.loc[self.df_skv[tmp].index]

        df_skvInPlast = df_skvInPlast0.drop_duplicates(['№ скважины','Характер работы'], keep='last')

        #self.df_nag.to_excel('nag.xlsx')
        Lskv = []
        L_dat = []
        L_debLiq = []
        L_debOil = []
        L_water = []
        L_debLiqTR = []
        L_debOilTR = []
        L_waterTR = []
        L_dynLevel = []
        L_Pzab = []
        L_PriemTR = []
        L_Diam = []
        L_inject = []
        L_Pplast = []
        L_priem = []
        L_debTime = []
        L_zakTime = []
        
        l1 = df_skvInPlast['№ скважины'].tolist()
        Lskv.append(l1)
        l2 = df_skvInPlast['Характер работы'].tolist()
        Lskv.append(l2)
        l = df_skvInPlast['Координата забоя Х'].tolist()
        Lskv.append(l)
        l = df_skvInPlast['Координата забоя Y'].tolist()
        Lskv.append(l)
        l = df_skvInPlast['Координата X'].tolist()
        Lskv.append(l)
        l = df_skvInPlast['Координата Y'].tolist()
        Lskv.append(l)
        l = df_skvInPlast['Нефтенасыщенная толщина, м'].tolist()
        Lskv.append(l)

        #return Lskv

        for i in range(len(l1)):
            tmp_df = df_skvInPlast0.loc[df_skvInPlast0["№ скважины"] == l1[i]]
            tmp_df = tmp_df.loc[tmp_df["Характер работы"] == l2[i]]

            
            l = tmp_df['Дата'].tolist() 
            L_dat.append(l)
            l = tmp_df['Дебит жидкости за последний месяц, т/сут'].tolist()
            L_debLiq.append(l)
            l = tmp_df['Дебит нефти за последний месяц, т/сут'].tolist() 
            L_debOil.append(l)
            l = tmp_df['Обводненность за посл.месяц, % (вес)'].tolist() 
            L_water.append(l)
            l = tmp_df['Дебит жидкости (ТР), м3/сут'].tolist() 
            L_debLiqTR.append(l)
            l = tmp_df['Дебит нефти (ТР), т/сут'].tolist() 
            L_debOilTR.append(l)
            l = tmp_df['Обводненность (ТР), % (объём)'].tolist() 
            L_waterTR.append(l)
            l = tmp_df['Динамический уровень (ТР), м'].tolist() 
            L_dynLevel.append(l)
            l = tmp_df['Забойное давление (ТР), атм'].tolist() 
            L_Pzab.append(l)
            l = tmp_df['Приемистость (ТР), м3/сут'].tolist() 
            L_PriemTR.append(l)
            l = tmp_df['Диаметр штуцера, мм'].tolist() 
            L_Diam.append(l)
            l = tmp_df['Закачка за посл.месяц, м3'].tolist() 
            L_inject.append(l)
            l = tmp_df['Пластовое давление (ТР), атм'].tolist() 
            L_Pplast.append(l)
            l = tmp_df['Приемистость за последний месяц, м3/сут'].tolist() 
            L_priem.append(l)
            l = tmp_df['Время работы в добыче, часы'].tolist()
            L_debTime.append(l)
            l = tmp_df['Время работы под закачкой, часы'].tolist()
            L_zakTime.append(l)


            
        return Lskv, L_debLiq, L_debOil, L_water, L_debLiqTR, L_debOilTR, L_waterTR, L_dynLevel, L_Pzab, L_PriemTR,\
               L_Diam, L_inject, L_Pplast, L_priem, L_dat, L_debTime, L_zakTime



    # Мероприятия из файла Excel
    def getExcel_evt(self, path_exl):

        if path_exl != '':


            df_evt = pd.DataFrame(
                pd.read_excel(path_exl, skiprows=[0], usecols=['Unnamed: 0', 'Месторождение', 'Скважина', 'Тип', 'Объект разработки до ГТМ', 'Объект разработки после ГТМ', 'ВНР.1'] ))
            #pd.read_excel(path_exl, skiprows=[0], usecols="A,B,C,E,G,H,AI"))
            df_evt.fillna('0', inplace=True)
            df_evt.rename(columns={'Unnamed: 0': 'type', 'Месторождение': 'field', 'Скважина': 'well', 'Куст': 'cluster',
                                   'Тип': 'event', 'Объект разработки до ГТМ': 'form1', 'Объект разработки после ГТМ': 'form2', 'ВНР.1': 'D1'}, inplace=True)


            df_evt.loc[(df_evt.type == 'Добывающая'), 'type'] = 'НЕФ'
            df_evt.loc[(df_evt.type == 'Нагнетательная'), 'type'] = 'НАГ'


            return df_evt




    # ГРП  из  файла Excel
    def getExcel_grp(self, path_exl):

        if path_exl!='':

            try:

                df_grp = pd.DataFrame(
                    pd.read_excel(path_exl, skiprows=1, usecols=['Месторождение', 'Дата', 'Номер скважины', 'Пласт']))
                df_grp = df_grp.astype({"Дата": str})
                df_grp['Дата'] = df_grp.apply(lambda x: x['Дата'][:-3], axis=1)
                df_grp['Дата'] = pd.to_datetime(df_grp['Дата'], format='%Y-%m')

                skv = df_grp['Номер скважины'].tolist()
                N = 0
                for i in range(len(skv)):
                    if skv[i] != skv[i]:
                        skv[i] = N
                    else:
                        N = skv[i]
                df_grp.drop(columns=['Номер скважины'], axis=1)
                df_grp['Номер скважины'] = skv
                df_grp = df_grp.drop_duplicates()

                return df_grp, 2

            except:
                return 0, 0

        else:
            return 0, 1


    def  insGRPtoBD(self, grp_list_tuple):

        q = """INSERT OR REPLACE  INTO grp VALUES (?,?,?)"""
        self.cursor.executemany(q, grp_list_tuple)
        self.sqlite_conn.commit()



    def insEVTtoBD(self, list_tuple):
        q = """INSERT OR REPLACE  INTO event VALUES (?,?,?,?,?,?)"""
        self.cursor.executemany(q, list_tuple)
        self.sqlite_conn.commit()

    def getEVTfromBD2(self):

        q = """SELECT * from event order by well"""
        self.cursor.execute(q)
        results = self.cursor.fetchall()
        return results


    def getEVTfromBDforChen(self, well, form):

        q = """SELECT well, event, dat, dat from event where type = 'НЕФ' and form1 = '""" + form + """'  and well = '""" + well + """' order by well"""
        self.cursor.execute(q)
        df = pd.DataFrame(self.cursor.fetchall(), columns=['Скважина', 'ГТМ', 'начало', 'окончание'])

        return df

    # ГТМ без повторяющихся дат
    def getEVTfromBDforAll(self, well, form, type):

        q = """SELECT well,  GROUP_CONCAT(event) as event, dat, dat FROM event WHERE well = '""" + well + """' and type = '""" +type+ """' and form1 = '""" + form + """' GROUP BY dat"""
        self.cursor.execute(q)
        df = pd.DataFrame(self.cursor.fetchall(), columns=['Скважина', 'ГТМ', 'начало', 'окончание'])

        return df


    def delEVT(self, evt):
        q = "DELETE from event where dat =? and well =? and type =? and form1 =? and event =?"
        self.cursor.execute(q, evt)
        self.sqlite_conn.commit()
    def delEVT_All(self):
        q = "DELETE from event"
        self.cursor.execute(q)
        self.sqlite_conn.commit()







    #  История выбранной скважины
    def getHistForSql(self, skv, typ):
        Lhist = []
        if typ == 'НАГ':         
            df = self.df_nag.loc[self.df_nag["№ скважины"] == skv]
            l = df['Дата'].tolist()    
            Lhist.append(l)
            l = df['Закачка за посл.месяц, м3'].tolist()    
            Lhist.append(l)
            l = df['Забойное давление (ТР), атм'].tolist()    
            Lhist.append(l)
            l = df['Пластовое давление (ТР), атм'].tolist()    
            Lhist.append(l)
        if typ == 'НЕФ':         
            df = self.df_nef.loc[self.df_nef["№ скважины"] == skv]
            l = df['Дата'].tolist()    
            Lhist.append(l)
            l = df['Обводненность за посл.месяц, % (вес)'].tolist()    
            Lhist.append(l)
            l = df['Обводненность (ТР), % (объём)'].tolist()    
            Lhist.append(l)
            l = df['Дебит нефти за последний месяц, т/сут'].tolist()    
            Lhist.append(l)

        #print(Lhist)
        return Lhist





    def  getForReportNAG(self, nag):

        form = F(nag)

        q = """SELECT max(dat) from history WHERE  well like '%""" + form + """'"""
        self.cursor.execute(q)
        rez = self.cursor.fetchone()
        maxDat = rez[0]

        q = """SELECT max(dat) from history WHERE  well = '""" + nag + """'"""
        self.cursor.execute(q)
        rez = self.cursor.fetchone()
        maxDatWell = rez[0]

        # Состояние
        if maxDat > maxDatWell:
            sost = 'ОСТ'
        else:
            sost = 'РАБ'

        #  Накопленная закачка, тыс.м3
        q = """ SELECT sum(inject)/1000 FROM history where well = '""" + nag + """'"""
        self.cursor.execute(q)
        rez = self.cursor.fetchone()
        nakzak = round(rez[0],1)

        # Приемистость, Забойное давление (ТР), атм, Диаметр штуцера, мм
        q = """ SELECT priem, Pzab, Diam FROM history where well = '""" + nag + """'"""  + """ and dat = (SELECT max(dat) from history WHERE  well = '""" + nag + """')"""
        self.cursor.execute(q)
        rez = self.cursor.fetchone()
        priem = round(rez[0],1)
        Pzab = round(rez[1])
        Diam = round(rez[2])

        return [S(nag), S(form), sost, nakzak, priem, Pzab, Diam]



        #print(sost + '   '+ nakzak + '   '+  priem+ '    '+ zab+ '   '+ diam + '  ')




    def  getForReportNEF(self, nef):

        form = F(nef)

        q = """SELECT max(dat) from history WHERE  well like '%""" + form + """'"""
        self.cursor.execute(q)
        rez = self.cursor.fetchone()
        maxDat = rez[0]

        q = """SELECT max(dat) from history WHERE  well = '""" + nef + """'"""
        self.cursor.execute(q)
        rez = self.cursor.fetchone()
        maxDatWell = rez[0]

        # Состояние
        if maxDat > maxDatWell:
            sost = 'ОСТ'
        else:
            sost = 'РАБ'

        #  Накопленная закачка, тыс.м3
        q = """ SELECT sum(debOil) FROM history where well = '""" + nef + """'"""
        self.cursor.execute(q)
        rez = self.cursor.fetchone()
        nakdob = str(round(rez[0],1))


        q = """ SELECT debOil,  debLiq, water, Pzab, Pplast FROM history where well = '""" + nef + """'"""  + """ and dat = (SELECT max(dat) from history WHERE  well = '""" + nef + """')"""
        self.cursor.execute(q)
        rez = self.cursor.fetchone()
        debOil = round(rez[0],1)
        debLiq = round(rez[1],1)
        water = round(rez[2])
        Pzab = round(rez[3])
        Pplast = round(rez[4])

        return [S(nef), S(form), sost, nakdob, debOil, debLiq, water, Pzab, Pplast]

        #print(nef+ '      '+ form+ '     '+sost + '   '+ nakdob + '   '+  debOil+ '    '+ debLiq+ '   '+ water + '  '+Pzab+'    '+Pplast)