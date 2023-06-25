import numpy as np
import pandas as pd
from rdp import rdp
import math


def for_well(df, value_rdp, mass_val_par, el, res, KRS, RIR, frcst, TR, L):
    
         
    #mass_val_par = [1.174,0.4,0.8,2.266666667,200,0.09144] 
    global sum_W
    global mass_sum_deltaP_t
    global xx
    global yy
    global xxx
    global yyy
    global global_arr_depress
    global global_arr_days
    global global_arr_w
    global global_arr_real_date
    global tg_two_point
    global arr_skin
    global arr_skin_two_point
    global neproizv_otbor, Q_, flag, delta_Q
    
    global loss
    global badVal
    global forecast
    global payback
    global Len
    Len = L

    sum_W, mass_sum_deltaP_t,xxx,yyy,xx,tg,yy,global_arr_depress,global_arr_days,global_arr_w,global_arr_real_date,tg_two_point, TR_cut = Hallplot(df, value_rdp, TR)



    #df.to_excel('hol0000022222222222' + '.xlsx')
    #print (mass_val_par)

    # скин по аппроксимиоующей примой
    arr_skin = skin(tg,mass_val_par)
    # скин через тангенс по двум точкам
    arr_skin_two_point = skin(tg_two_point,mass_val_par)
        
#Q, Qreal, flag,Q_for_forecast = Class_member.Main_skin(arr_skin,mass_val_par,global_arr_depress,global_arr_days,global_arr_w)
    neproizv_otbor,Q_, flag,delta_Q = Main_skin(arr_skin,mass_val_par,global_arr_depress,global_arr_days,global_arr_w)

    #print (Q_)
    #print (flag)
    #print (delta_Q)
    
    
    
    if flag:
        #денежный результат
        result = el*sum(neproizv_otbor) - res - KRS - RIR 
        #значение непроизводительной закачки
        loss = round(result,2)
#       l14['text'] = round(math.fabs(Qreal - Q),2)
        badVal = str(list(map(round, neproizv_otbor, range(1,100))))
        # ПРОГНОЗ: это произведение дельты последней закачки* стоимость электричества* кол-во месяцев проноза
        sum_,m = discount(int(frcst),delta_Q[-1][-1]*el,RIR,0)
        forecast = round(sum_,2)
        sum1,m1 = discount(1000,delta_Q[-1][-1]*el,RIR,1)
        payback = m1
            
        df_result = pd.DataFrame(columns=['Дата','Дни работы (МЭР)', 'Закачка (МЭР)', 'Скорректированный МЭР','Непроизводительная закачка','Суммарная НЗ за период','Скин','*Месяц, где скажина работала меньше 10 суток, в расчете НЗ не участвует.'])
            
        #print(delta_Q[-1][-1])

        tmp_frame=[]
        tmp_frame1 = []
        tmp_frame2 = []
        tmp_frame3 = []
        tmp_frame4 = []
        tmp_frame5 =[]
        tmp_frame6 = []
        for j in range (1, len(arr_skin)):
            tmp_frame6.append(neproizv_otbor[j-1])
            for i in range (0, len(global_arr_real_date[j])):
                tmp_frame.append(str( pd.Timestamp(global_arr_real_date[j][i])))
                tmp_frame1.append(Q_[j-1][i])
                tmp_frame2.append(delta_Q[j-1][i])
                tmp_frame3.append (global_arr_days[j][i])
                tmp_frame4.append (global_arr_w[j][i])
                tmp_frame5.append(arr_skin[j])
                if i != 0:
                    tmp_frame6.append(int(0))
        #там где скважина работала меньше 10 дней, зануляем НЗ        
        for c in range(0, len(tmp_frame2)):
            if tmp_frame3[c] < 10:
                tmp_frame2[c] = 0
                
        df_result['Дата'] = np.array(tmp_frame).T
        df_result['Скорректированный МЭР'] = np.array(tmp_frame1).T
        df_result['Непроизводительная закачка'] = np.array(tmp_frame2).T
        df_result['Дни работы (МЭР)'] =np.array(tmp_frame3).T
        df_result['Закачка (МЭР)'] =np.array(tmp_frame4).T
        df_result['Скин'] =np.array(tmp_frame5).T
        df_result['Суммарная НЗ за период'] =np.array(tmp_frame6).T

#            df_tmp = pd.merge(df1, df_result, how ='inner', on ='Дата')
            
        #df_result.to_excel('Отчеты\Скв ' + str(NameNag)+'_график Холла.xlsx')
#            df_tmp.to_excel('test.xlsx')

    else:
        loss = "Скин-фактор не уменьшается"
        badVal = '__'
        forecast = '__'
        payback = '__'
       # l4['text']='LOG: попробуйте уменьшить параметр поиска звеньев ломаной '



    return xxx, yyy, sum_W, mass_sum_deltaP_t, xx, yy, arr_skin,arr_skin_two_point, loss, badVal, forecast, payback, TR_cut
        
       
    
    
    
    
    
    
def Hallplot(df,value_rdp, TR):

    TR_cut = 0

    mass_t_for_i = np.array(df["Время работы под закачкой, часы"])  # время под закачкой, (ч)
    mass_pw = np.array(df["Забойное давление (ТР), атм"])  # забойное давление, (атм)
    mass_pp = np.array(df["Пластовое давление (ТР), атм"])  # пластовое давление, (атм)
    mass_date = np.array(df["Дата"])  # дата


    if not TR:
        mass_W = np.array(df["Закачка за посл.месяц, м3"])  # закачка,(м3)
    else:
        mass_W = np.array(df["Закачка ТР"])  # закачка,(м3)
        #mass_W22 = np.array(df["Закачка ТР"])
        #print('-------------------------------')
        #print(nagID)
        #print(mass_W)
        mer = np.array(df["Закачка за посл.месяц, м3"])
        tmp = []
        for i in range(len(mass_W)):
            if mass_W[i] != 0:
                break
            else:
                tmp.append(i)

        if tmp:

            mass_t_for_i = np.delete(mass_t_for_i, tmp)
            mass_pw = np.delete(mass_pw, tmp)
            mass_pp = np.delete(mass_pp, tmp)
            mass_date = np.delete(mass_date, tmp)
            mass_W = np.delete(mass_W, tmp)
            mer = np.delete(mer, tmp)
            TR_cut = len(tmp)

            #mass_W22 = np.delete(mass_W22, tmp)


        for i in range(len(mass_W)):
            if mass_W[i] == 0:
                mass_W[i] = mer[i]

        #print('nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
        #for i in range(len(mass_W)):
         #   print(str(i) + ' - ' +str(mass_W22[i]) + '----'+str(mass_W[i]) + ' - - -   ' + str(mer[i]))


        

    mass_sum_deltaP_t = []
    sum_W = []   # накапливаемая закачка
    depress = [] #депрессия
    delta_work_time = [] #длительность работы под закачкой
        

    mass_sum_deltaP_t.append((mass_pw[0]-mass_pp[0])*mass_t_for_i[0]/24)
    depress.append(mass_pw[0]-mass_pp[0])
    sum_W.append(mass_W[0])
    delta_work_time.append(0)
    
    for j in range(1,len(mass_pw)):
        mass_sum_deltaP_t.append(mass_sum_deltaP_t[j-1] + (mass_pw[j]-mass_pp[j])*mass_t_for_i[j]/24) # переводим в сутки
        sum_W.append(sum_W[j-1] +mass_W[j] )
        depress.append(mass_pw[j]-mass_pp[j])
        delta_work_time.append(mass_t_for_i[j]/24)
            

    xx,yy = [],[] #опорные коорднаты х,y
    tg_two_point = []
    # тангенс прямой через две точки 
    for l in range(0, len(mass_sum_deltaP_t)-1):
        tg_two_point.append((mass_sum_deltaP_t[l+1]-mass_sum_deltaP_t[l])/( sum_W[l+1]-sum_W[l]))
            
        
    X_new = rdp(np.c_[sum_W,mass_sum_deltaP_t],  epsilon = int(value_rdp))
    xx = X_new[0:len(X_new),0]
        
    dicrionary2 = dict(zip(sum_W, mass_date))
    for i in range (0, len(xx)):
        yy.append(dicrionary2.get(xx[i])) 
        

    # массивы точек, которые попадают в разные отрезки аппроксимации
    tmp_x,tmp_y,tmp_depress,tmp_days, tmp_w,tmp_real_data = [],[],[],[],[],[]
        
    global_arr_x = [] # массив массивов координат Х от одной опортной точки до другой
    global_arr_y = [] # массив массивов координат У от одной опортной точки до другой
    global_arr_depress = []
    global_arr_days= []
    global_arr_w = []
    global_arr_real_date = []

    i = 0
    for j in range (1,len(xx)):
        while i < len(sum_W) and sum_W[i] <= xx[j]:
            tmp_x.append(sum_W[i])
            tmp_y.append(mass_sum_deltaP_t[i])
            tmp_depress.append(depress[i])
            tmp_days.append(delta_work_time[i])
            tmp_w.append(mass_W[i])
            tmp_real_data.append(mass_date[i])
            i = i+1
        global_arr_x.append(tmp_x)
        global_arr_y.append(tmp_y)
        global_arr_depress.append(tmp_depress)
        global_arr_days.append(tmp_days)
        global_arr_w.append(tmp_w)
        global_arr_real_date.append(tmp_real_data)
        tmp_x = []
        tmp_y = []
        tmp_depress = []
        tmp_days = []
        tmp_w = []
        tmp_real_data = []

 
    #аппроксимация линией от одной опорной точки до другой
    xxx,yyy,tg=[],[],[] # линейная аппроксимация х,y + тангенс угла как коэфф в kx+b

    for i in range(0, len(global_arr_x)) :

        z = np.poly1d(np.polyfit(global_arr_x[i],global_arr_y[i],1))

        tg.append(z[1])
        yyy.append(z(global_arr_x[i]))
        xxx.append(global_arr_x[i])
            
#        tg = list(set(tg)) # удаление всех дубликотов
        


    return (sum_W, mass_sum_deltaP_t, xxx,yyy,xx,tg,yy,global_arr_depress,global_arr_days,global_arr_w,global_arr_real_date,tg_two_point, TR_cut)
    


def skin(tg,arr_par):

    arr_skin = []

    for i in range(0, len(tg)):
        arr_skin.append(tg[i]*arr_par[-3]*arr_par[-4]/(18.41*arr_par[-6]*arr_par[-5])-math.log(arr_par[-2]/arr_par[-1])) # 18.41 - российские промысловые

    return(arr_skin)  
      
      
#    @classmethod
def Q_from_old_skin(depress,skin,arr_par,time):
        
    q,Q = [],[]
        
    for i in range (0, len(depress)):
        if Len == 0:

            I = (arr_par[2]*arr_par[3]*depress[i])/(18.41*arr_par[1]*arr_par[0]*(math.log(arr_par[-2]/arr_par[-1])+skin))

        else:
            tmp = ((2*arr_par[-2]/Len)**4 + 0.25)**0.5
            tmp = (tmp + 0.5)**0.5
            a = tmp * Len / 2
            tmp = a**2 - (Len/2)**2
            tmp = tmp**0.5 + a
            tmp = math.log(tmp / (Len/2))
            tmp = tmp + arr_par[3] / Len * math.log(arr_par[3] / (2*arr_par[-1])) + skin
            I = (arr_par[2]*arr_par[3]*depress[i])/ (18.41*arr_par[1]*arr_par[0]*tmp)

        q.append(I)
        Q.append(q[i]*time[i])

    return (Q)
    
    
    






def Main_skin(skin,arr_par,global_arr_depress,global_arr_days,global_arr_w):

        
    Q_ = []
    Q_DAY10 =[]
    d = []
        
    t = []
        
    w = []
        
    flag = 0
    d.append([])
    t.append([])
    w.append([])            
    # чистка данных - удаление тех случаев, когда скважина работала меньше 10 дней за месяц
    for k in range (1, len(skin)):
        d.append([])
        t.append([])
        w.append([])
        for j in range(0,len(global_arr_days[k])):
            if global_arr_days[k][j] > 10:
                d[k].append(global_arr_depress[k][j])
                t[k].append(global_arr_days[k][j])
                w[k].append(global_arr_w[k][j])
#                    
#        Q_real = []
#        try:
#            Q_ = MainApp.Q_from_old_skin(self,d,skin[-2],arr_par,t)
#            Q_real= sum(w)
#            flag = 1
#        except IndexError:
#            print("мало скинов")
        
        
        
    neproizv_otbor = []
    arr_tmp,arr_tmp_=[],[]
    arr_tmp_DAY10,arr_tmp_DAY10_=[],[]
    delta_Q=[]
        
    try:
        for i in range (1, len(skin)):
           # условие на скин-фактор - считаем относительно первого предыдущего, который больше текущего
            flag_flag = 0
            if skin[i] > skin[i-1]:
                for l in range(i-1, -1,-1):
                    if skin[l]> skin[i]:
                        # дебит рассчитанный для текущей депрессии, но со старым скин-фактором по формуле Депюи
                        Q_.append(Q_from_old_skin(global_arr_depress[i][:],skin[l],arr_par,global_arr_days[i][:]))
                        Q_DAY10.append(Q_from_old_skin(d[i][:],skin[l],arr_par,t[i][:]))
                        flag_flag = 1
                        break
                if flag_flag == 0:
                        
                    Q_.append([0]*len(global_arr_depress[i][:]))
                    Q_DAY10.append([0]*len(global_arr_depress[i][:]))
                    for m in range(0,len(global_arr_depress[i][:])):                
                        arr_tmp_.append(0)
                        arr_tmp_DAY10_.append(0)
                    neproizv_otbor.append(int(sum(arr_tmp_DAY10_)))
                    delta_Q.append(arr_tmp_)
                    flag = 1
            else:
                # дебит рассчитанный для текущей депрессии, но со старым скин-фактором по формуле Депюи
                Q_.append(Q_from_old_skin(global_arr_depress[i][:],skin[i-1],arr_par,global_arr_days[i][:]))
                Q_DAY10.append(Q_from_old_skin(d[i][:],skin[i-1],arr_par,t[i][:]))
                flag_flag = 1
            # дельта между текущей закачкой и посчитанной через старый скин-фактор
            if flag_flag == 1:
                arr_tmp = [x-y for x,y in zip(global_arr_w[i][:], Q_[i-1])]
                arr_tmp_DAY10 = [x-y for x,y in zip(w[i][:], Q_DAY10[i-1])]
                # непроизводительные отборы
                neproizv_otbor.append(sum(arr_tmp_DAY10))
                delta_Q.append(arr_tmp)
                flag = 1
                
    except IndexError:
        print("мало скинов")              
            
        
                
#        if w != []:
#            delta_Q = w[-1]-Q_[-1]
#        else:
#            delta_Q = 0
#       return (sum(Q_),Q_real, flag,delta_Q )    
    return (neproizv_otbor,Q_, flag,delta_Q )


def discount(month, base_value, rir_value, flag):
    i = 1
    sum_dis_bas_val = []
    sum_dis_bas_val.append(base_value)
    for i in range(1, month):
        coeff_discount = 1 / (1 + 0.14 / 12) ** i
        discount_base_value = coeff_discount * base_value
        tmp = discount_base_value + sum_dis_bas_val[i - 1]
        sum_dis_bas_val.append(tmp)
        if flag and sum_dis_bas_val[i] > rir_value:
            break

    if i == 1:
        return (sum_dis_bas_val[-1], i)
    else:
        return (sum_dis_bas_val[-1], i + 1)