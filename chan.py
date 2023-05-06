import pandas as pd
from dateutil.relativedelta import relativedelta
import numpy as np
from rdp import rdp
from sklearn.metrics import r2_score
import math



name_date = 'Дата'
well_number = '№ скважины'
name_Wc = 'Обводненность за посл.месяц, % (вес)'
name_Qn = 'Добыча нефти за посл.месяц, т'
name_Qz = 'Добыча жидкости за посл.месяц, т'
work_marker = 'Характер работы'
prod = "НЕФ"  # маркер для добывающей скважины
object_name = "Объекты работы"
name_time = "Время работы, часы"
name_list = name_date, well_number, name_Wc, name_Qn, name_Qz, work_marker, prod, object_name, name_time

time='Время работы, часы'


def Chan(df_initial, value_rdp,mounth_start, min_count_1, min_count_2, min_interval,
         min_interval_x, min_subinterval_x, min_dermination, gtj, form):
    """
    Функция для коврового выявления проблем по методиче Чана
    :param data_file: имя файла
    :param df_initial: исходный массив
    :param name_list: Названия столбцов в таблице
    :param value_rdp: параметр для разбиения интервала на подинтервалы в алгоритме rdp
    :param mounth_start: количество первых месяцев, которые не учитываются в анализе
    :param min_count_1: минимальное колличество точек в анализируемом интервале
    :param min_count_2: минимальное колличество точек в анализируемом интервале, если он меньше min_interval_x
    :param min_interval: допустимое время остановки или роста ВНФ лог кривая времени для объединения интервалов
    :param min_interval_x: лог кривая времени (минимальный объединенный интеревал для анализа)
    :param min_subinterval_x: лог кривая времени (минимальный объединенный подинтеревал для анализа)
    :param min_dermination: оценка разброса точек
    :param gtj: выгрузка Новая Стратегия
    :param time: 'Дата' или "Время работы, часы"
                расчет абсциссы графиков на основе оперативного времени работы или дней в месяце
    :return:[df_history - обработанная история скважин, df_result - перечень скважин с проблемами]
    """
    name_date, well_number, name_Wc, name_Qn, name_Qz, work_marker, prod, object_name, name_time = name_list
    df_initial = df_initial.fillna(0)  # Заполнение пустых ячеек нулями

    if not gtj.empty:
        df_geojobs = gtj
        #df_geojobs = gtj.fillna(0)  # Заполнение пустых ячеек нулями
        #df_geojobs = geojobs_clean(df_geojobs)
        pass
    else:
        df_geojobs = pd.DataFrame()

    list_columns = [name_date, name_Wc, name_Qn, name_Qz]
    wells_prod = df_initial[well_number].unique()
    df_history, df_result, df_geojobs_final = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    not_calc = pd.DataFrame(columns=["Скважина", "Причина отсутсвия"])
    for prod_well in wells_prod:
        # Начало расчета для каждой скважины
        #print(prod_well)
        slice_prod = df_initial.loc[df_initial[well_number] == prod_well]
        #slice_prod = slice_prod[(slice_prod[object_name] != 0)]
        # Проверка длины истории, она должна быть не меньше, чем mounth_start
        if slice_prod.shape[0] < mounth_start:
            #print(prod_well, "короткая история")
            not_calc = not_calc.append({'Скважина': prod_well, 'Причина отсутсвия': "короткая история"},
                                       ignore_index=True)
            continue

        slice_prod["ГТМ"] = ""

        slice_object = slice_prod


        # Отметка участков с ГТМ
        if not df_geojobs.empty and str(prod_well) in list(df_geojobs['Скважина'].unique()):
            slice_gtj = df_geojobs.loc[df_geojobs['Скважина'] == str(prod_well)].copy()
            for i in range(slice_gtj.shape[0]):
                problem = slice_gtj.iloc[[i]]['ГТМ'].iloc[0]


                start_date = slice_gtj.iloc[[i]]["начало"].iloc[0]
                end_date = slice_gtj.iloc[[i]]["окончание"].iloc[0]

                if  'Дострел' not in problem:
                    slice_object["ГТМ"] = np.where((slice_object[name_date] >= start_date)
                                                   & (slice_object[name_date] <= end_date),
                                                   slice_object["ГТМ"] + problem, slice_object["ГТМ"])
                    #print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')
                    #print(slice_object["ГТМ"])
                elif start_date != slice_object[name_date].iloc[-1] and start_date != slice_object[name_date].iloc[
                    0]:
                    slice_object["ГТМ"] = np.where(slice_object[name_date] == start_date,
                                                   slice_object["ГТМ"] + " " + problem, slice_object["ГТМ"])
        else:
            slice_object["ГТМ"] = ""
        df_geojobs_final = df_geojobs_final.append(slice_object[slice_object["ГТМ"] != ""], ignore_index=True)


        # Расчет через даты или фактическое время работы
        if time == 'Дата':
            slice_object['delta_time_from_pr_step'] = slice_object[name_date].diff().astype(
                'timedelta64[D]').fillna(0)
            slice_object['delta_days_from_start'] = slice_object['delta_time_from_pr_step'].cumsum()
        elif time == "Время работы, часы":
            slice_object = slice_object[slice_object["Время работы, часы"] != 0]
            slice_object['summ_time_from_start'] = slice_object["Время работы, часы"].fillna(0).cumsum()
            slice_object['delta_days_from_start'] = slice_object['summ_time_from_start'] / 24
            if slice_object.empty:
                continue
        # Кривые Чанна
        WOR, WOR_dir = Chan_for_well(slice_object, list_columns)
        WOR_curr, WOR_dir_curr = Chan_for_well_curr(slice_object, list_columns)  # ------my
        slice_object["WOR"] = list(WOR)
        slice_object["WOR_dir"] = list(WOR_dir)
        slice_object["WOR_curr"] = list(WOR_curr)  # -------my
        slice_object["WOR_dir_curr"] = list(WOR_dir_curr)  # -------my
        slice_object["log10(time)"] = np.log10(np.array(list(slice_object['delta_days_from_start'])))
        slice_object["log10(WOR)"] = np.log10(np.array(list(WOR)))
        slice_object["log10(WOR_dir)"] = np.log10(np.array(list(WOR_dir)))
        slice_object["log10(WOR)_curr"] = np.log10(np.array(list(WOR_curr)))  # ----------my
        slice_object["log10(WOR_dir)_curr"] = np.log10(np.array(list(WOR_dir_curr)))  # ----------my
        slice_object = slice_object.replace([np.inf, -np.inf], np.nan).fillna(0).reset_index()
        intervals = intervals_gtj(slice_object)

        for i in intervals:
            slice_interval = slice_object.loc[i[0]:(i[1] + 1)]
            if slice_interval.shape[0] <= 2:
                #print("короткий интервал")
                continue
            else:
                #print("интервал для анализа")
                pass
            # Анализ кривых Чанна
            Result_well = Chan_analytics_x(slice_interval, prod_well, form, value_rdp, min_interval,
                                           min_interval_x, min_subinterval_x, mounth_start, min_dermination,
                                           min_count_1, min_count_2)
            if not Result_well.empty:
                df_result = df_result.append(Result_well, ignore_index=True)
        df_history = df_history.append(slice_object, ignore_index=True)
        if df_result.empty:
            not_calc = not_calc.append({'Скважина': prod_well, 'Причина отсутсвия': "нет проблемных зон"},
                                       ignore_index=True)
        else:
            if prod_well not in list(df_result['Скважина']):
                not_calc = not_calc.append({'Скважина': prod_well, 'Причина отсутсвия': "нет проблемных зон"},
                                           ignore_index=True)

    if df_history.shape[0] > 0:
        df_history['water'] = round(df_history['Добыча жидкости за посл.месяц, т'] / 100 * df_history[
            'Обводненность за посл.месяц, % (вес)'],1)

    return df_history, df_result, not_calc



def intervals_gtj(df):
    """Функция для разбиения массива на интервалы с учетом ГТМ"""
    intervals_Series = []
    df_notgtj = df[df["ГТМ"] == ""]
    df_notgtj['diff_index'] = np.append(np.diff(np.array(df_notgtj.index))-1, 0)
    delta_for_check = df_notgtj.reset_index()
    delta_for_check = list(delta_for_check[delta_for_check['diff_index'] > 0].index)
    if not delta_for_check:
        intervals_Series.append(df_notgtj.index[0])
        intervals_Series.append(df_notgtj.index[-1])
    else:
        intervals_Series.append(df_notgtj.index[0])
        for i in delta_for_check:
            intervals_Series.append(df_notgtj.index[i])
            intervals_Series.append(df_notgtj.index[i+1])
        intervals_Series.append(df_notgtj.index[-1])
    intervals_Series = list(zip(*[iter(intervals_Series)] * 2))

    return intervals_Series



dict_gtj_Chan = {'Дострел': 'новый объект', 'Кислотная ОПЗ': 3, 'Перестрел': 3, 'Прочие ОПЗ': 3,
                 'РИР': 1, 'ГРП': 6}


def geojobs_clean(df_geojobs, dict = dict_gtj_Chan):

    print(df_geojobs)
    df_geojobs = df_geojobs.loc[df_geojobs[name_gtj].isin(dict.keys())]
    wells_prod = df_geojobs[well_number].unique()
    df_result = pd.DataFrame(columns=['Скважина', 'ГТМ', "начало", "окончание"])
    for prod_well in wells_prod:
        slice = df_geojobs.loc[(df_geojobs[well_number] == prod_well)].copy()
        for i in range(slice.shape[0]):
            problem = slice.iloc[[i]]['Краткое описание мероприятий'].iloc[0]
            start_date = slice.iloc[[i]]['Начало.1'].iloc[0]
            start_date = start_date.replace(day=1, hour=00)
            if problem != 'Дострел':
                if slice.iloc[[i]]['Окончание.1'].iloc[0] != 0:
                    end_date = slice.iloc[[i]]['Окончание.1'].iloc[0] + relativedelta(months=dict[problem])
                    end_date = end_date.replace(day=1, hour=00)
                else:
                    end_date = start_date + relativedelta(months=dict[problem])
            else:
                end_date = 'новый объект'
            df_result = df_result.append({'Скважина':prod_well, 'ГТМ': problem, "начало":start_date,
                                          "окончание":end_date}, ignore_index=True)
    return df_result





def Chan_for_well(df, list_columns, spin=6, method="накопленный ВНФ"):
    """ Расчет кривых Чанна через накопленный/текущий ВНФ (возможны ошибки при расчете через текущий)"""
    name_date, name_Wc, name_Qn, name_Qz = list_columns

    if method == "накопленный ВНФ":
        cumulative_production_oil = df[name_Qn].cumsum()
        cumulative_production_all = df[name_Qz].cumsum()
        cumulative_production_water = cumulative_production_all - cumulative_production_oil
        WOR = np.array(cumulative_production_water / cumulative_production_oil)
        WOR_dir = list(np.diff(np.array(WOR)) / np.diff(np.array(df['delta_days_from_start'])))
    # Обработка WOR_dir
    WOR_dir.append((WOR[-1] - WOR[-2]) / (df['delta_days_from_start'].iloc[-1] - df['delta_days_from_start'].iloc[-2]))
    WOR_dir = pd.Series(WOR_dir)
    WOR = pd.Series(WOR)
    WOR_dir = WOR_dir.where(WOR_dir > 0, 0)
    return WOR, WOR_dir



def Chan_for_well_curr(df, list_columns, spin=6, method="текущий ВНФ"):
    name_date, name_Wc, name_Qn, name_Qz = list_columns
    if method == "текущий ВНФ":
        df["Добыча воды за посл.месяц, т"] = df[name_Qz] - df[name_Qn]
        WOR = np.array(df["Добыча воды за посл.месяц, т"] / df[name_Qn])  # вычисление текущего ВНФ
        WOR_dir = list(np.diff(np.array(WOR)) / np.diff(np.array(df['delta_days_from_start'])))
        # Обработка WOR_dir
        WOR_dir.append(
            (WOR[-1] - WOR[-2]) / (df['delta_days_from_start'].iloc[-1] - df['delta_days_from_start'].iloc[-2]))
        WOR_dir = pd.Series(WOR_dir)
        WOR = pd.Series(WOR)
        WOR_dir = WOR_dir.where(WOR_dir > 0, 0)
        return WOR, WOR_dir


def Chan_analytics_x(df, name_well, reservoir, value_rdp, min_interval, min_interval_x, min_subinterval_x,
                     mounth_start, min_dermination, min_count_1, min_count_2, name_date='Дата'):
    """
    Функция для анализа кривой Чанна: выделение участков с проблемами и их причин
    :param df: DataFrame для анализа
    :param name_well: название добывающей скважины
    :param reservoir: объект работы
    :param value_rdp: параметр для разбиения интервала на подинтервалы в алгоритме rdp
    :param min_interval: допустимое время остановки или роста ВНФ лог кривая времени для объединения интервалов
    :param min_interval_x: минимальный объединенный интеревал для анализа в лог масштабе времени
    :param min_subinterval_x: минимальный объединенный подинтеревал для анализа в лог масштабе времени
    :param mounth_start: количество первых месяцев, которые не учитываются в анализе
    :param min_dermination: оценка разброса точек, коэф. детерминации
    :param min_count_1: минимальное колличество точек в анализируемом интервале
    :param min_count_2: минимальное колличество точек в анализируемом интервале, если он меньше min_interval_x
    :param name_date: название столбца с датами
    :return: DataFrame (содержит все интервалы с проблемами для одной скважины и ее объекста) -
            columns=["Скважина", "Объект работы", "Интервал: начало", "Интервал: конец",
            "Подинтервал: начало", "Подинтервал: конец", "Наклон WOR'", "R2", "Нарушение"]
    """
    df_result = pd.DataFrame()
    if df.shape[0] > mounth_start:
        df = df.iloc[mounth_start:].reset_index()
        del df['level_0']
        df = df.reset_index()
        intervals_WOR_dir = intervals_x(df, min_interval)  # Разбиение на интевралы
        for i in intervals_WOR_dir:
            count = df["log10(time)"].iloc[i[0]:i[1]+1].shape[0]
            delta_x = df["log10(time)"].iloc[i[1]] - df["log10(time)"].iloc[i[0]]
            if delta_x > min_interval_x or (delta_x < min_interval_x and count > min_count_2):
                df_analytics = pd.DataFrame(columns=["Скважина", "Объект работы", "Интервал: начало", "Интервал: конец",
                                                     "Подинтервал: начало", "Подинтервал: конец",  "Наклон WOR",
                                                     "Наклон WOR'", "R2", "Нарушение"])
                list_interval_start, list_interval_end, list_tg_WOR_dir, list_abnormality, list_R2, list_tg_WOR = [], [], [], [], [], []
                slice_interval = df.iloc[i[0]:i[1] + 1]
                slice_interval = slice_interval[slice_interval["log10(WOR_dir)"] != 0]
                # Очистка от выбросов в кривой производной ВНФ
                slice_interval = low_pass_filter_anomaly_detection(df=slice_interval, column_name='log10(WOR_dir)',
                                                                   number_of_stdevs_away_from_mean=1.5, window=3)
                slice_interval = slice_interval[slice_interval['log10(WOR_dir)_Low_Pass_Filter_Anomaly'] == 0]
                # Разбиение участка на подинтервалы
                X = np.array(list(slice_interval["log10(time)"]))
                Y_WOR_dir = np.array(list(slice_interval["log10(WOR_dir)"]))
                Y_WOR = np.array(list(slice_interval["log10(WOR)"]))
                intervals_X = rdp(np.c_[X, Y_WOR_dir], epsilon=value_rdp)[:, 0]
                for j in range(1, len(intervals_X)):
                    start = int(np.where(X == intervals_X[j - 1])[0])
                    end = int(np.where(X == intervals_X[j])[0])
                    x = X[start:end + 1]
                    y_WOR_dir = Y_WOR_dir[start:end + 1]
                    if ((x[-1]-x[0]) > min_subinterval_x and len(y_WOR_dir) > min_count_1) or \
                            ((x[-1]-x[0]) < min_subinterval_x and len(y_WOR_dir) > min_count_2):
                        # Прроводим прямую через выбранный подучасток для определения угла наклона
                        model = np.polyfit(x, y_WOR_dir, 1)
                        coefficient_of_dermination = r2_score(y_WOR_dir, np.poly1d(model)(x))
                        if coefficient_of_dermination >= min_dermination:
                            tg_WOR_dir = model[0]
                            abnormality = check_abnormality(tg_WOR_dir)
                            y_WOR = Y_WOR[start:end + 1]
                            tg_WOR = np.polyfit(x, y_WOR, 1)[0]
                            if abnormality == "НЭК":
                                if 0.1763<=tg_WOR<= np.inf:
                                    abnormality = "НЭК"
                                else:
                                     abnormality = "ФНВ"
                            list_tg_WOR_dir.append(int(math.degrees(math.atan(tg_WOR_dir))))
                            list_tg_WOR.append(int(math.degrees(math.atan(tg_WOR))))
                        else:
                            abnormality = "неанализируемое облако точек"
                            list_tg_WOR_dir.append(0)
                            list_tg_WOR.append(0)
                        list_interval_start.append(df[name_date][int(np.where(df["log10(time)"] == intervals_X[j - 1])[0])])
                        list_interval_end.append(df[name_date][int(np.where(df["log10(time)"] == intervals_X[j])[0])])
                        list_abnormality.append(abnormality)
                        list_R2.append(round(coefficient_of_dermination, 2))
                    else:
                        continue
                df_analytics["Подинтервал: начало"] = list_interval_start
                df_analytics["Подинтервал: конец"] = list_interval_end
                df_analytics["Наклон WOR'"] = list_tg_WOR_dir
                df_analytics["Наклон WOR"] = list_tg_WOR
                df_analytics["Нарушение"] = list_abnormality
                df_analytics["R2"] = list_R2
                df_analytics["Скважина"] = name_well
                df_analytics["Объект работы"] = reservoir
                df_analytics["Интервал: начало"] = list(df[name_date])[i[0]]
                df_analytics["Интервал: конец"] = list(df[name_date])[i[1]]
                df_result = df_result.append(df_analytics, ignore_index=True)


    return df_result








def intervals_x(df, min_interval):
    """Функция для разбиения массива на интервалы с учетом времени остановки или роста ВНФ"""
    intervals_Series = []
    df_notnull = df[df["log10(WOR_dir)"] != 0]
    del df_notnull["level_0"]
    df_notnull['diff_index'] = np.append(np.diff(np.array(df_notnull.index))-1, 0)
    delta_for_check = df_notnull.reset_index()
    delta_for_check = list(delta_for_check[delta_for_check['diff_index'] > 0].index)
    if not delta_for_check:
        intervals_Series.append(df_notnull.index[0])
        intervals_Series.append(df_notnull.index[-1])
    else:
        intervals_Series.append(df_notnull.index[0])
        for i in delta_for_check:
            if df_notnull["log10(time)"].iloc[i+1]-df_notnull["log10(time)"].iloc[i] \
                    > min_interval:
                intervals_Series.append(df_notnull.index[i])
                intervals_Series.append(df_notnull.index[i+1])
        intervals_Series.append(df_notnull.index[-1])
    intervals_Series = list(zip(*[iter(intervals_Series)] * 2))
    return intervals_Series








def check_abnormality(tg_WOR_dir):
    """ Определение проблемы по углу наклона кривой """
    if -0.1763 <= tg_WOR_dir < 0.1763:  # от 10 до 350 | от 190 до 170
        abnormality = "Нормальное вытеснение"
    elif 0.1763 <= tg_WOR_dir <= 0.364 or -0.364 <= tg_WOR_dir <= -0.1763:
        # от 10 до 20 (от 190 до 200) | от 340 до 350 (от 160 до 170)
        abnormality = "Промежуточное положение (ФНВ/нормальное вытеснение/конус)"
    elif 0.364 < tg_WOR_dir <= 5.6713:  # от 10 до 80 | от 190 до 265
        abnormality = "ФНВ"
    elif 5.6713 < tg_WOR_dir <= np.inf:  # от 80 до 89 | от 265 до 269
        abnormality = "НЭК"
    elif -np.inf < tg_WOR_dir < -0.364:  # от 269 до 350 | от 90 до 180
        abnormality = "конус"
    else:
        abnormality = "Неопознанный угол наклона"
    return abnormality


def low_pass_filter_anomaly_detection(df, column_name, number_of_stdevs_away_from_mean, window):
    """
    Implement a low-pass filter to detect anomalies in a time series, and save the filter outputs
    (True/False) to a new column in the dataframe.
    Arguments:
        df: Pandas dataframe
        column_name: string. Name of the column that we want to detect anomalies in
        number_of_stdevs_away_from_mean: float. Number of standard deviations away from
        the mean that we want to flag anomalies at. For example, if
        number_of_stdevs_away_from_mean=2,
        then all data points more than 2 standard deviations away from the mean are flagged as
        anomalies.
    Outputs:
        df: Pandas dataframe. Dataframe containing column for low pass filter anomalies
        (True/False)
    """
    #window rolling average
    df[column_name+'_Rolling_Average']=df[column_name].rolling(window=window, center=True).mean()
    #window standard deviation
    df[column_name+'_Rolling_StDev']=df[column_name].rolling(window=window, center=True).std()
    #Detect anomalies by determining how far away from the mean (in terms of standard deviation)
    #each data point is
    df[column_name+'_Low_Pass_Filter_Anomaly']=(abs(df[column_name]-df[
                                column_name+'_Rolling_Average'])>(
                                number_of_stdevs_away_from_mean*df[
                                column_name+'_Rolling_StDev']))
    return df


