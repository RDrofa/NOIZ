from scipy.stats import spearmanr
import pandas as pd

class spearwell():

    def __init__(self, nameNag, nameNef, df, ind1,ind2):
        self.NagID = nameNag
        self.NefID = nameNef
        self.source_df = df
        self.source_df['D'] = pd.to_datetime(self.source_df['D'], format="%Y/%m/%d")
        self.ind1 = ind1
        self.ind2 = ind2

        self.lenWell = 0
        self.FNV = 0
        self.KP = 0

        self.K = 0

        self.K_all = [0,0,0,0,0,0,0]

        self.Kl_lag = 0
        self.Ko_lag = 0
        self.Kp_lag = 0


        self.rangeMax = 42
        self.rangeMin = 12

        self.oneLag = -2

        self.range_all = -2



        self.range_start = 0
        self.range_fin = 0
        self.right_range = False
        self.range_start_D = ''
        self.range_fin_D = ''

        self.df_out = pd.DataFrame({'L': [0, 0, 0, 0, 0, 0, 0], 'O': [0, 0, 0, 0, 0, 0, 0], 'P': [0, 0, 0, 0, 0, 0, 0],
                                    'W': [0, 0, 0, 0, 0, 0, 0], 'S': [0, 0, 0, 0, 0, 0, 0]})



        self.spear_spaces, self.spear_forbidden = self.getEmpty()

        self.setRange()


    def setRange(self):

        dat = self.source_df['D'].tolist()


        def findRange(R):

            s = 0
            spaces = 0
            a = 0
            b = len(dat) - 1
            c = 0

            for j in range(len(dat) - 1, -1, -1):
                if dat[j] in self.spear_forbidden:
                    s = 0
                    b = j - 1
                    #print(str(dat[j-1]) +  '---' + str(dat[j]))
                    spaces = 0
                else:
                    s = s + 1
                if dat[j] in self.spear_spaces:
                    spaces += 1

                if s > R + spaces:
                    c = spaces
                    if dat[j - 1] in self.spear_forbidden:
                        a = j
                        break
                    else:
                        if s >= self.rangeMax + spaces:
                            a = j
                            break
            return [a, b, c]

        Range = findRange(17)
        if Range[1] - Range[0] > 16:
            X = True
        else:
            Range = findRange(16)
            if Range[1] - Range[0] > 15:
                X = True
            else:
                Range = findRange(15)
                if Range[1] - Range[0] > 14:
                    X = True
                else:
                    Range = findRange(14)
                    if Range[1] - Range[0] > 13:
                        X = True
                    else:
                        Range = findRange(13)
                        if Range[1] - Range[0] > 12:
                            X = True
                        else:
                            Range = findRange(12)
                            if Range[1] - Range[0] > 11:
                                X = True
                            else:
                                Range = findRange(11)
                                if Range[1] - Range[0] > 10:
                                    X = True
                                else:
                                    X = False

        if X:
            self.spaces = Range[2]
            self.range_start = Range[0]
            self.range_fin = Range[1]


        else:
            self.range_start = 0
            self.range_fin = len(self.source_df['D'].tolist()) - 1
            self.spaces = 0

        self.range_start_save = self.range_start
        self.range_fin_save = self.range_fin


        self.checkRange()


    def checkRange(self):

        self.range_start_D = self.source_df.loc[self.range_start, 'D']
        self.range_fin_D = self.source_df.loc[self.range_fin, 'D']

        self.right_range = True
        N = self.source_df['D'].tolist()
        N = N[self.range_start: self.range_fin + 1]

        self.spaces = 0
        for itm in N:
            if itm in self.spear_spaces:
                self.spaces +=1

        self.range_all = self.range_fin + 1 - self.range_start - self.spaces


        if self.range_all >= 18:
            lags = 7
        else:
            lags = self.range_all - 11

        fin = len(N) - lags + 1
     
        #N = N[:fin]

        for i in self.spear_forbidden:
            if i in N:
                self.right_range = False
                break

        if self.range_all < self.rangeMin or self.range_all > self.rangeMax:
            self.right_range = False

        if self.oneLag>0:
            if lags<=self.oneLag:
                self.right_range = False



        if self.right_range:
            self.calculateСoeff()
        else:
            self.df_out = pd.DataFrame(
                {'L': [0, 0, 0, 0, 0, 0, 0], 'O': [0, 0, 0, 0, 0, 0, 0], 'P': [0, 0, 0, 0, 0, 0, 0],
                 'W': [0, 0, 0, 0, 0, 0, 0], 'S': [0, 0, 0, 0, 0, 0, 0]})



    def calculateСoeff(self):

        #print(self.spear_spaces)
        #print(self.spear_forbidden)

        self.df_out = pd.DataFrame({'L': [0, 0, 0, 0, 0, 0, 0], 'O': [0, 0, 0, 0, 0, 0, 0], 'P': [0, 0, 0, 0, 0, 0, 0],
                                    'W': [0, 0, 0, 0, 0, 0, 0], 'S': [0, 0, 0, 0, 0, 0, 0]})


        D = self.source_df['D'].tolist()
        priem = self.source_df['priem'].tolist()
        debLiq = self.source_df['debLiq'].tolist()
        debOil = self.source_df['debOil'].tolist()
        Pzab = self.source_df['Pzab'].tolist()
        water = self.source_df['water'].tolist()
        synth = self.source_df['synth'].tolist()

        D = D[self.range_start:self.range_fin + 1]
        priem = priem[self.range_start:self.range_fin + 1]
        debLiq = debLiq[self.range_start:self.range_fin + 1]
        debOil = debOil[self.range_start:self.range_fin + 1]
        Pzab = Pzab[self.range_start:self.range_fin + 1]
        water = water[self.range_start:self.range_fin + 1]
        synth = synth[self.range_start:self.range_fin + 1]

        tmp = []
        for i in range(len(D)):
            if D[i] in self.spear_spaces:
                tmp.append(i)
        for n in sorted(tmp, reverse=True):
            del priem[n]
            del debLiq[n]
            del debOil[n]
            del Pzab[n]
            del water[n]
            del synth[n]

        a = 0
        if self.range_all >= 18:
            lags = 7
        else:
            lags = self.range_all - 11
        if self.oneLag >= 0:
            lags = self.oneLag + 1
            a = self.oneLag

        fin = len(priem) - lags + 1
        for i in range(a,lags):
            corr, _ = spearmanr(priem[0:fin], debLiq[0 + i:fin + i])
            corr = round(corr, 2)
            self.df_out.loc[i, 'L'] = corr
            corr, _ = spearmanr(priem[0:fin], debOil[0 + i:fin + i])
            corr = round(corr, 2)
            self.df_out.loc[i, 'O'] = corr
            if Pzab[0 + i:fin + i].count(max(set(Pzab[0 + i:fin + i]), key=lambda x: Pzab[0 + i:fin + i].count(x))) < 6:
                corr, _ = spearmanr(priem[0:fin], Pzab[0 + i:fin + i])
            else:
                corr = -1
            corr = round(corr, 2)
            self.df_out.loc[i, 'P'] = corr

            if water[0 + i:fin + i].count(max(set(water[0 + i:fin + i]), key=lambda x: water[0 + i:fin + i].count(x))) < 6:
                corr, _ = spearmanr(priem[0:fin], water[0 + i:fin + i])
            else:
                corr = -1
            corr = round(corr, 2)
            self.df_out.loc[i, 'W'] = corr

            corr, _ = spearmanr(priem[0:fin], synth[0 + i:fin + i])
            corr = round(corr, 2)
            self.df_out.loc[i, 'S'] = corr


        self.K_all = []
        for i in range(7):
            if self.df_out.loc[i, 'P'] != -1:
                K = self.spearDecode3(self.df_out.loc[i, 'L'] , self.df_out.loc[i, 'P'], self.df_out.loc[i, 'O'])
            else:
                K = self.spearDecode2(self.df_out.loc[i, 'L'],  self.df_out.loc[i, 'O'])
            self.K_all.append(K)


        L = self.df_out['L'].tolist()

        for i in range(len(L)):
            if L[i] < 0:
                L[i] = 0

        Kl = 0
        Kl_lag = 0
        Kp_lag = 0
        x = -2
        '''for i in range(len(L) - 1):

            if L[i] < x and L[i + 1] < x and x >0.2:
                Kl = x
                Kl_lag = i-1
                break
            else:
                x = L[i]
        if Kl == 0:
            x = 0
            Kl_lag = -1
            for i in range(len(L) - 1):
                if L[i] < x and x>0.2:
                    Kl = x
                    Kl_lag = i-1
                    break
                else:
                    x = L[i]
        if Kl==0:
            Kl = max(L)
            Kl_lag = L.index(Kl)'''
            
        for i in range(len(L) - 1):

            if L[i+1] < L[i]:
                Kl = L[i]
                Kl_lag = i
                break
            else:
                Kl = max(L)
                Kl_lag = L.index(max(L))
            

        L = self.df_out['O'].tolist()
        Ko = L[Kl_lag]
        Ko_lag = Kl_lag

        L = self.df_out['P'].tolist()
        Kp = L[0]
        for i in range(0, Kl_lag+1):
            if L[i]>Kp:
                Kp= L[i]
                Kp_lag = i

        if Kp  != -1:
            self.K = self.spearDecode3(Kl,Kp,Ko)
        else:
            self.K = self.spearDecode2(Kl, Ko)

  
            Kp_lag = ' - '

        self.Kl_lag = Kl_lag
        self.Ko_lag = Ko_lag
        self.Kp_lag = Kp_lag

        self.Kl = Kl
        self.Ko = Ko
        self.Kp = Kp



    def getEmpty(self):
        def chk(zz, dd):
            if zz != zz or zz == 0 or dd != dd or dd == 0:
                return False
            else:
                return True

        N = self.source_df['D'].tolist()
        Z = self.source_df['zakTime'].tolist()
        D = self.source_df['debTime'].tolist()
        spear_spaces = []

        a = []
        for i in range(len(N)):
            if chk(Z[i], D[i]) == False:
                a.append(0)
            else:
                a.append(1)

        spear_forbidden = []
        for i in range(len(a)):
            if a[i] == 0:
                spear_forbidden.append(N[i])

        tmp = []
        for i in range(len(a)):
            if a[i] == 0:
                tmp.append(i)
            else:
                if len(tmp) > 3:
                    tmp.clear()
                else:
                    if len(tmp) > 0:
                        for j in tmp:
                            spear_spaces.append(N[j])
                        tmp.clear()
                    else:
                        pass

        for i in spear_forbidden[:]:
            if i in spear_spaces:
                spear_forbidden.remove(i)

        return spear_spaces, spear_forbidden



    def spearDecode3(self, Qj, Pz, Qn):
        if Qj < 0.1:
            if Pz < 0.1:
                K = 1
            elif 0.4 > Pz >= 0.1:
                K = 2
            else:
                K = 4
        elif 0.2 > Qj >= 0.1:
            if Pz < 0.1:
                K = 3
            elif 0.4 > Pz >= 0.1:
                K = 5
            else:
                K = 6
        elif 0.3 > Qj >= 0.2:
            if Pz < 0.4:
                if Qn < 0.2:
                    K = 5
                else:
                    K = 7
            else:
                if Qn < 0.2:
                    K = 9
                else:
                    K = 9
        elif 0.5 > Qj >= 0.3:
            if Qn < 0.3:
                if Pz < 0.4:
                    K = 7
                else:
                    K = 10
            elif 0.5 > Qn >= 0.3:
                K = 9
            else:
                K = 12
        else:
            if Qn < 0.2:
                if Pz < 0.4:
                    K = 11
                else:
                    K = 13
            elif 0.5 > Qn >= 0.2:
                K = 12
            else:
                K = 14

        return K


    def spearDecode2(self, Qj, Qn):
        if Qj < 0.1:
            K = 1
        elif 0.2 > Qj >= 0.1:
            K = 5
        elif 0.3 > Qj >= 0.2:
            if Qn < 0.2:
                K = 5
            else:
                K = 7
        elif 0.5 > Qj >= 0.3:
            if Qn < 0.3:
                K = 7
            elif 0.5 > Qn >= 0.3:
                K = 9
            else:
                K = 12
        else:
            if Qn < 0.3:
                K = 11
            elif 0.5 > Qn >= 0.3:
                K = 12
            else:
                K = 14
        return K