import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from rdp import rdp
from sklearn.metrics import r2_score


def NO(df_initial, value_rdp, month_min, min_determination, max_stay, water_min, form, ID):



    """Параметры для расчета"""
    data_file = "Эксплуатационные показатели Пограничное.xlsx" # Файл для расчета
    cum_production_oil = "Накопленная добыча нефти, т"

    # Параметры для ручной настройки
    '''value_rdp = 1  # параметр для разбиения интервала на подинтервалы в алгоритме rdp
    month_min = 8  # минимальное количество месяцев в базовом интервале
    min_determination = 0.4  # оценка разброса точек
    max_stay = 6
    water_min = 50'''

    # Название столбцов в таблице
    date = "Дата"
    well_number = "№ скважины"
    work_marker = "Характер работы"
    well_status = "Состояние"
    rate_liq = "Дебит жидкости за последний месяц, т/сут"
    rate_oil = "Дебит нефти за последний месяц, т/сут"
    water_cut = "Обводненность за посл.месяц, % (вес)"
    time_prod = "Время работы в добыче, часы"
    prod = "НЕФ" # маркер для добывающей скважины
    object_name = "Объекты работы"

    #df_initial = pd.read_excel(os.path.join(os.path.dirname(__file__), data_file)) # Открытие экселя
    #print(df_initial)
    #df_initial = df_initial.fillna(0)  # Заполнение пустых ячеек нулями
    df_initial[date] = pd.to_datetime(df_initial[date], format="%Y/%m/%d")
    list_columns = [date, rate_liq, rate_oil, time_prod]

    df_history, df_result, df_breakthrough, df1_emp, df2_emp = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame() # создание пустых таблиц

    # Начало расчета для каждой скважины

    #list_objects = slice_prod[object_name].unique()

    slice_object = df_initial


    #slice_object[time_prod] = slice_object[time_prod] / 24  # перевод часов в дни



    #print(slice_object)

    WOR, cumulative_production_oil = log_WOR_for_well(slice_object, list_columns)
    slice_object["WOR"] = list(WOR)
    slice_object["Накопленная добыча нефти, тыс.т"] = list(cumulative_production_oil)

    slice_object["ln(WOR)"] = np.log(np.array(list(WOR)))
    slice_object = slice_object.replace([np.inf, -np.inf], np.nan).fillna(0).reset_index() # замена всех бесконечно и минус бесконечно больших чисел на NAN и потом NAN на нули. А потом сброс индексов - чтобы снова было 0 1 2 3 4
    slice_object_notnull = slice_object[slice_object[time_prod] != 0] # оставили только месяцы, когда скважина работала


    Result_well, Result_break, x_interval, y_interval, x_trend, line_trend, x_oil_interval, line_trend_oil = log_WOR_analysis(slice_object, slice_object.loc[0,well_number], form, value_rdp, min_determination, month_min, max_stay, date)
    df_history = df_history.append(slice_object, ignore_index=True)
    df_result = df_result.append(Result_well, ignore_index=True)
    df_breakthrough = df_breakthrough.append(Result_break, ignore_index=True)



    if df_result.empty:
        name_columns = ["Скважина", "Объект работы", "Подинтервал: начало", "Подинтервал: конец", "Добыча: начало",
                       "Добыча: конец", "Средняя обводненность", "Наклон WOR", "R2", "Заключение"]
        df_result = pd.DataFrame(columns=name_columns)

    if df_breakthrough.empty:
        name_columns = ["Скважина", "Объект работы", "qн до роста ВНФ, т/сут", "qж до роста ВНФ, т/сут", "% воды до роста ВНФ",
                       "Дата начала роста ВНФ", "qн текущий, т/сут", "qж текущий, т/сут", "% воды текущий", "qн прогноз, т/сут",
                       "qж прогноз, т/сут", "% воды прогноз", "Изменение обводненности, %", "Сокращение дебита воды (прогноз qн), т/сут",
                    "Текущий НО воды (прогноз qн), т", "Сокращение дебита воды (текущий qн), т/сут", "Текущий НО воды (текущий qн), т", "R2 нефти", "Примечание"]
        df_breakthrough = pd.DataFrame(columns=name_columns)


    if len(x_interval) != 0:
        x_int_list = list(
            np.concatenate(x_interval).flat)  # создание одного списка из нескольких списков - график отрезков rdp
        y_int_list = list(
            np.concatenate(y_interval).flat)  # создание одного списка из нескольких списков - график отрезков rdp
    else:
        x_int_list = [0]
        y_int_list = [0]


    return df_result, df_breakthrough, slice_object_notnull, [x_int_list, y_int_list], line_trend, x_trend, x_oil_interval, line_trend_oil





def log_WOR_for_well(df, list_columns):
    """Расчет зависимости lnВНФ от накопленной добычи"""
    date, rate_liq, rate_oil, time_prod = list_columns
    production_oil = np.array(df[rate_oil] * df[time_prod])
    production_liquid = np.array(df[rate_liq] * df[time_prod])
    production_water = production_liquid - production_oil
    cumulative_production_oil = production_oil.cumsum()/1000
    WOR = np.array(production_water / production_oil)
    WOR = pd.Series(WOR)

    '''for i in WOR:
        print(i)
        try:
            i+0
        except:
            i=0'''

    return WOR, cumulative_production_oil



def log_WOR_analysis(df, prod_well, reservoir, value_rdp, min_determination, month_min, max_stay, date):
    """Функция поиска базового интервала ln(WOR) и формирования заключения"""
    df_result = pd.DataFrame()
    result_breakthrough = pd.DataFrame()
    df = df.reset_index()
    df_notnull = df[df["Время работы в добыче, часы"] != 0].reset_index(drop=True)
    delta_interval_year = 5  # количество лет между первым месяцем последнего интервала и последним месяцем базового интервала
    month_last = 24  # количество месяцев продолжительного последнего интервала
    intervals_X_all = []
    intervals_Y_WOR_all = []
    conclusion = ''  # заключение
    flag = 0
    list_interval_start, list_interval_end, list_tg_WOR, list_tg_WOR0, list_R2, list_cum_oil_start, list_cum_oil_end, list_water, x_trend, list_line_trend, x_oil_interval, line_trend_oil = [], [], [], [], [], [], [], [], [], [], [], []
    df_analytics = pd.DataFrame(columns=["Скважина", "Объект работы", "Подинтервал: начало", "Подинтервал: конец", "Добыча: начало",
                 "Добыча: конец", "Средняя обводненность", "Наклон WOR", "R2", "Заключение"])

    sum_month_history = 0
    intervals_stay = intervals_x(df, max_stay)

    for i in range(len(intervals_stay) - 1, -1, -1):
        sum_month_history += (intervals_stay[i][1] - intervals_stay[i][0])

    if sum_month_history < 24:

        conclusion = "Короткая история работы"
        flag = 1



    for i in range(len(intervals_stay)-1, -1, -1):
        if flag == 1:  # проверка, сформировался ли вывод
            break
        count = df["index"].iloc[intervals_stay[i][0]:intervals_stay[i][1] + 1].shape[0]
        intervals_Series = []
        slice_interval = df.iloc[intervals_stay[i][0]:intervals_stay[i][1] + 1]
        slice_interval_null = slice_interval.copy()
        slice_interval = slice_interval[(slice_interval["Время работы в добыче, часы"] != 0) & (slice_interval["Дебит нефти за последний месяц, т/сут"] != 0.00)]
        del slice_interval["level_0"]
        slice_interval = slice_interval.reset_index()
        X = np.array(list(slice_interval["Накопленная добыча нефти, тыс.т"]))
        Y_WOR = np.array(list(slice_interval["ln(WOR)"]))


        while flag == 0: # нужно выделить два интервала (базовый - для прогноза, последний - для формирования вывода)

            intervals_X = rdp(np.c_[X, Y_WOR], epsilon = value_rdp)[:,0]
            points = slice_interval.loc[slice_interval["Накопленная добыча нефти, тыс.т"].isin(intervals_X)]
            index_points = list(points['level_0'])

            # проверка выделился ли уже какой-то интервал

            intervals_X_all.insert(0, intervals_X)
            intervals_Y_WOR = np.array(slice_interval.loc[slice_interval["Накопленная добыча нефти, тыс.т"].isin(intervals_X), "ln(WOR)"])
            intervals_Y_WOR_all.insert(0, intervals_Y_WOR)


            # последний выделенный интервал
            if i == len(intervals_stay) - 1:
                start_last = int(np.where(slice_interval["level_0"] == index_points[-2])[0])
                end_last = int(np.where(slice_interval["level_0"] == index_points[-1])[0])
                # Нужно, чтобы в последнем интервале было больше двух точек
                if (end_last - start_last) == 2:

                    conclusion = f'Измените параметры расчета (value rdp).'
                    flag = 1
                    break
                date_start_last = df[date][int(index_points[-2])]
                x_last = X[start_last:end_last + 1]
                y_WOR_last = Y_WOR[start_last:end_last + 1]
                water_mean_last = slice_interval["Обводненность за посл.месяц, % (вес)"][start_last:end_last + 1].mean()

                # Проводим прямую через выбранный подучасток для определения угла наклона
                trend_last = np.polyfit(x_last, y_WOR_last,
                                        1)  # линия тренда, степень полинома 1, список коэффициентов из уравнения прямой
                line_trend_last = np.poly1d(trend_last)
                coefficient_of_determination_last = r2_score(y_WOR_last, np.poly1d(trend_last)(x_last))
                tg_WOR_last = trend_last[0]
                degrees_last = math.degrees(math.atan(tg_WOR_last))
                x_trend.append(x_last)
                list_line_trend.append(line_trend_last)
                list_water.append(round(water_mean_last, 1))
                list_R2.append(round(coefficient_of_determination_last, 2))
                list_tg_WOR.append(math.degrees(math.atan(tg_WOR_last)))
                list_interval_start.append(df[date][int(index_points[-2])])
                list_interval_end.append(df[date][int(index_points[-1])])
                list_cum_oil_start.append(df["Накопленная добыча нефти, тыс.т"][int(index_points[-2])])
                list_cum_oil_end.append(df["Накопленная добыча нефти, тыс.т"][int(index_points[-1])])

                # Проверка угла наклона последнего интервала
                if tg_WOR_last < 0:

                    conclusion = 'Обводненность сокращается'
                    flag = 1
                    break

                if tg_WOR_last == 0:

                    conclusion = "Нулевая обводненность"
                    flag = 1
                    break

                # проверка последнего интервала, если он продолжительный
                if len(x_last) > month_last and coefficient_of_determination_last >= min_determination:

                    conclusion = f'Нормальная выработка последние {month_last} мес.'
                    flag = 1
                    break

                # в случае низкой достоверности, предлагается изменить параметр поиска звеньев
                elif len(x_last) > month_last and coefficient_of_determination_last < min_determination:

                    conclusion = f'Измените параметры расчета (value rdp).'
                    flag = 1
                    break

                # выделение подотрезков больше month_min
                for j in range(len(index_points) - 2):
                    if index_points[j + 1] - index_points[j] > month_min:
                        intervals_Series.append(index_points[j])
                        intervals_Series.append(index_points[j + 1])

                # если скважина работала без длительных остановок, но при этом не выделился ни один интервал с характерным падением/ростом > month_min
                if len(intervals_Series) == 0 and len(intervals_stay) == 1:

                    conclusion = "Нестабильная работа"
                    flag = 1
                    break
                elif len(intervals_Series) == 0 and len(intervals_stay) > 1:  # если в последнем отрезке (intervals_stay) выделился только последний интервал, то переходим к следующем отрезку (intervals_stay)
                    break

            # поиск базового интервала по lnВНФ
            # проверка, как давно скважина работала (>month_min) от последнего интервала
            else:
                check_start_last = intervals_stay[len(intervals_stay) - 1][0]
                check_end_base = intervals_stay[len(intervals_stay) - 2][1]
                check_delta = check_start_last - check_end_base
                if check_delta > 12:  # длительная остановка больше 1 года

                    conclusion = f'Скважина после длительной остановки {check_delta} мес.'
                    flag = 1
                    break

                # разбиение отрезка на подотрезки больше month_min
                for j in range(len(index_points) - 1):
                    if index_points[j + 1] - index_points[j] > month_min:
                        intervals_Series.append(index_points[j])
                        intervals_Series.append(index_points[j + 1])

                if len(intervals_Series) == 0:  # если отрезки больше month_min не выделены

                    conclusion = "Нестабильная работа"
                    flag = 1
                    break



            list_delta_interval = []  # список временных расстояний от предполагаемого базового интервала до последнего
            j = len(intervals_Series) - 1
            # перебор подотрезков и поиск подходящего
            while j > 0:
                start = int(np.where(slice_interval["level_0"] == intervals_Series[j - 1])[0])
                end = int(np.where(slice_interval["level_0"] == intervals_Series[j])[0])
                date_end_base = slice_interval[date][end]
                #-----------------------------print(date_start_last)
                #-----------------------------print(date_end_base)
                #-----------------------------print(np.timedelta64(1, 'Y'))
                delta_interval = (date_start_last - date_end_base) / np.timedelta64(1, 'Y')
                list_delta_interval.append(delta_interval)

                if delta_interval <= delta_interval_year:  # как далеко предполагаемый базовый интервал
                    x = X[start:end + 1]
                    y_WOR = Y_WOR[start:end + 1]
                    water_mean = slice_interval["Обводненность за посл.месяц, % (вес)"][start:end + 1].mean()  # средняя обводненность подотрезка

                    # Проводим прямую через выбранный подучасток для определения угла наклона
                    trend = np.polyfit(x, y_WOR,1)  # линия тренда, степень полинома 1, список коэффициентов из уравнения прямой
                    coefficient_of_determination = r2_score(y_WOR,np.poly1d(trend)(x))  # poly1d - одномерный класс полиномов
                    tg_WOR = trend[0]  # коэффициент a из уравнения прямой - тангенс
                    if tg_WOR < 0:  # для базового интервала нужен подотрезок с положительным углом наклона
                        j -= 2
                        continue
                    else:
                        if water_mean > 40 and water_mean_last > 40:  # проверка на обводненность, при низкой обводненности метод не работает и нет необходимости в ГТМ
                            if coefficient_of_determination >= min_determination:  # проверка на качество линии тренда (степень достоверности)
                                len_base = len(x)

                                # Проверка верно ли выделен базовый интервал
                                if check_base_WOR(df, trend):

                                    conclusion = "Базовый интервал неопределен"
                                    flag = 1
                                    break

                                list_R2.append(round(coefficient_of_determination, 2))
                                line_trend = np.poly1d(trend)
                                list_line_trend.insert(0, line_trend)
                                x_trend.insert(0, x)
                                list_water.append(round(water_mean, 1))
                                list_tg_WOR.append(math.degrees(math.atan(tg_WOR)))
                                list_interval_start.append(df[date][int(intervals_Series[j - 1])])
                                list_interval_end.append(df[date][int(intervals_Series[j])])
                                list_cum_oil_start.append(df["Накопленная добыча нефти, тыс.т"][
                                                              int(intervals_Series[j - 1] - index_points[0])])
                                list_cum_oil_end.append(df["Накопленная добыча нефти, тыс.т"][int(intervals_Series[j] - index_points[0])])

                                # проверка на прорыв/нормальную выработку
                                if list_tg_WOR[0] - list_tg_WOR[1] > 10 and water_mean_last > water_mean + 1 and \
                                        list_tg_WOR[0] > 10:  # в т.ч. учет обводненности в диагностике прорыва
                                    conclusion = "Прорыв"

                                    flag = 1
                                    result_breakthrough, x_oil_interval, line_trend_oil = breakthrough(df, prod_well,
                                                                                                       reservoir, x,
                                                                                                       x_last, trend,
                                                                                                       len_base,
                                                                                                       value_rdp,
                                                                                                       min_determination)
                                else:
                                    conclusion = "Нормальная выработка"

                                    flag = 1
                                break


                            # если достоверность меньше необходимой
                            else:
                                if j > 1:  # переходим к следующему подотрезку
                                    j -= 2
                                else:

                                    conclusion = "Нестабильная работа"
                                    flag = 1
                                    break


                        else:

                            conclusion = "Низкая обводненность - метод не работает"
                            flag = 1
                            break

                # за последние delta_interval_year не выделился стабильный базовый интервал
                else:

                    conclusion = 'Нестабильная работа'
                    flag = 1
                    break

            if i == 0 and j < 0:

                conclusion = 'Базовый интервал неопределен'
                flag = 1

            break

    df_analytics["Подинтервал: начало"] = list_interval_start
    df_analytics["Подинтервал: конец"] = list_interval_end
    df_analytics["Добыча: начало"] = list_cum_oil_start
    df_analytics["Добыча: конец"] = list_cum_oil_end
    df_analytics["Средняя обводненность"] = list_water
    df_analytics["Наклон WOR"] = list_tg_WOR
    df_analytics["R2"] = list_R2
    df_analytics["Скважина"] = prod_well
    df_analytics["Объект работы"] = reservoir
    df_analytics["Заключение"] = conclusion


    df_result = df_result.append(df_analytics, ignore_index=True)

    return df_result, result_breakthrough, intervals_X_all, intervals_Y_WOR_all, x_trend, list_line_trend, x_oil_interval, line_trend_oil




def check_base_WOR(df, trend):
    """Функция проверки выбранного базового интервала на величину ВНФ.
    Прогнозный ВНФ на последнюю рабочую дату по выбранному базовому интервалу не должен превышать фактический ВНФ на последнюю рабочую дату."""
    # df_notnull = df[df["Время работы в добыче, часы"] != 0].reset_index(drop=True)
    df_notnull = df[(df["Время работы в добыче, часы"] != 0) & (df["Дебит нефти за последний месяц, т/сут"] != 0.00)].reset_index(drop=True)

    cum_oil_current = df["Накопленная добыча нефти, тыс.т"].iloc[int(df_notnull["level_0"].iloc[[-1]])]
    WOR_current = df_notnull["ln(WOR)"].iloc[int(np.where(df_notnull["Накопленная добыча нефти, тыс.т"] == cum_oil_current)[0])]
    WOR_predict = trend[0] * cum_oil_current + trend[1]
    if WOR_predict > WOR_current:
        return True
    return False




def intervals_x(df, max_stay):
    """Функция для разбиения массива на интервалы с учетом удаления длительных остановок"""
    intervals_Series = []
    df_notnull = df[df["Время работы в добыче, часы"] != 0]
    del df_notnull["level_0"]
    df_notnull['diff_index'] = np.append(np.diff(np.array(df_notnull.index))-1, 0)  # определяем остановки скважины
    delta_for_check = df_notnull.reset_index()
    delta_for_check = list(delta_for_check[delta_for_check['diff_index'] > 0].index) # индексы - моменты остановок в истории скважины
    if not delta_for_check:
        intervals_Series.append(df_notnull.index[0])
        intervals_Series.append(df_notnull.index[-1])
    else:
        intervals_Series.append(df_notnull.index[0])
        for i in delta_for_check:
            if df_notnull["diff_index"].iloc[i]-df_notnull["diff_index"].iloc[i+1] \
                    > max_stay:
                intervals_Series.append(df_notnull.index[i])
                intervals_Series.append(df_notnull.index[i+1])
        if intervals_Series[-1] != df_notnull.index[-1]:
            intervals_Series.append(df_notnull.index[-1])
        else:
            intervals_Series.pop()
        intervals_Series.append(df_notnull.index[-1])
    intervals_Series = list(zip(*[iter(intervals_Series)] * 2))
    return intervals_Series

def breakthrough(df, prod_well, reservoir, x, x_last, trend, len_base, value_rdp, min_determination):
    """Функция поиска отрезка на графике дебита нефти и прогноз параметров в случае ликвидации прорыва воды"""
    df_notnull = df[df["Время работы в добыче, часы"] != 0].reset_index(drop=True)
    value_rdp_oil = value_rdp
    if min_determination > 0.1:
        min_determination_oil = min_determination - 0.1
    else:
        min_determination_oil = min_determination
    coefficient_of_determination_oil, line_trend_oil = [], []
    min_month_oil = len_base*0.75
    name_columns = ["Скважина", "Объект работы", "qн до роста ВНФ, т/сут", "qж до роста ВНФ, т/сут", "% воды до роста ВНФ", "Дата начала роста ВНФ",
                "qн текущий, т/сут", "qж текущий, т/сут", "% воды текущий", "qн прогноз, т/сут", "qж прогноз, т/сут", "% воды прогноз",
                "Изменение обводненности, %", "Сокращение дебита воды (прогноз qн), т/сут", "Текущий НО воды (прогноз qн), т",
                "Сокращение дебита воды (текущий qн), т/сут", "Текущий НО воды (текущий qн), т", "R2 нефти", "Примечание"]
    df_break_result = pd.DataFrame(columns=name_columns)
    start_oil = int(np.where(df["Накопленная добыча нефти, тыс.т"] == x[0])[0][0])
    if int((np.where(df["Накопленная добыча нефти, тыс.т"] == x_last[0])[0]) - (np.where(df["Накопленная добыча нефти, тыс.т"] == x[-1])[0][0])) > 12:
        end_oil = int(np.where(df["Накопленная добыча нефти, тыс.т"] == x[-1])[0][0] + 12)
    else:
        end_oil = int(np.where(df["Накопленная добыча нефти, тыс.т"] == x_last[0])[0])
    slice_oil = df[start_oil:end_oil]
    slice_oil = slice_oil[slice_oil["Время работы в добыче, часы"] != 0].reset_index(drop=True)
    X_oil = np.array(list(slice_oil["Накопленная добыча нефти, тыс.т"]))
    Y_oil = np.array(list(slice_oil["Дебит нефти за последний месяц, т/сут"]))
    x_oil_interval = []
    # поиск подинтервала на графике дебита нефти с количеством точек >= min_month_oil
    while len(x_oil_interval) == 0:

        intervals_X_oil = rdp(np.c_[X_oil, Y_oil], epsilon=value_rdp_oil)[:, 0]
        points_oil = slice_oil.loc[slice_oil["Накопленная добыча нефти, тыс.т"].isin(intervals_X_oil)]
        index_points_oil = list(points_oil['level_0'])
        delta_oil = np.array(index_points_oil[1:len(index_points_oil)+1]) - np.array(index_points_oil[0:len(index_points_oil)-1])
        check_for_oil = list(delta_oil[np.where(delta_oil >= min_month_oil)])
        if len(check_for_oil) == 0:
            value_rdp_oil += 0.5
        else:
            index_check_oil = int(np.where(delta_oil == check_for_oil[-1])[0])
            start_oil_interval = index_points_oil[index_check_oil] - start_oil
            end_oil_interval = index_points_oil[index_check_oil+1] - start_oil
            x_oil_interval = X_oil[start_oil_interval:end_oil_interval + 1]
            y_oil_interval = Y_oil[start_oil_interval:end_oil_interval + 1]
            trend_oil = np.polyfit(x_oil_interval, y_oil_interval, 1)
            coefficient_of_determination_oil = r2_score(y_oil_interval, np.poly1d(trend_oil)(x_oil_interval))
            tg_WOR_oil = trend_oil[0]
            line_trend_oil = np.poly1d(trend_oil)

            # параметры до прорыва
            cum_oil_before = df["Накопленная добыча нефти, тыс.т"].iloc[int(df_notnull["level_0"].iloc[[-1]]-(len(x_last)))]
            date_break = df["Дата"].iloc[int(df_notnull["level_0"].iloc[[-1]] - len(x_last) + 1)]
            rate_oil_before = df_notnull["Дебит нефти за последний месяц, т/сут"].iloc[int(np.where(df_notnull["Накопленная добыча нефти, тыс.т"] == cum_oil_before)[0])]
            rate_liq_before = df_notnull["Дебит жидкости за последний месяц, т/сут"].iloc[int(np.where(df_notnull["Накопленная добыча нефти, тыс.т"] == cum_oil_before)[0])]
            rate_water_before = rate_liq_before - rate_oil_before
            wc_before = df_notnull["Обводненность за посл.месяц, % (вес)"].iloc[int(np.where(df_notnull["Накопленная добыча нефти, тыс.т"] == cum_oil_before)[0])]
            WOR_before = df_notnull["ln(WOR)"].iloc[int(np.where(df_notnull["Накопленная добыча нефти, тыс.т"] == cum_oil_before)[0])]

            # параметры после прорыва
            cum_oil_current = df["Накопленная добыча нефти, тыс.т"].iloc[int(df_notnull["level_0"].iloc[[-1]])]
            rate_oil_current = df_notnull["Дебит нефти за последний месяц, т/сут"].iloc[int(np.where(df_notnull["Накопленная добыча нефти, тыс.т"] == cum_oil_current)[0])]
            rate_liq_current = df_notnull["Дебит жидкости за последний месяц, т/сут"].iloc[int(np.where(df_notnull["Накопленная добыча нефти, тыс.т"] == cum_oil_current)[0])]
            rate_water_current = rate_liq_current - rate_oil_current
            wc_current = df_notnull["Обводненность за посл.месяц, % (вес)"].iloc[int(np.where(df_notnull["Накопленная добыча нефти, тыс.т"] == cum_oil_current)[0])]
            WOR_current = df_notnull["ln(WOR)"].iloc[int(np.where(df_notnull["Накопленная добыча нефти, тыс.т"] == cum_oil_current)[0])]

            # прогнозные параметры
            WOR_predict = trend[0]*cum_oil_current + trend[1]
            wc_predict = 1/(math.exp(-WOR_predict) + 1)*100

            if coefficient_of_determination_oil >= min_determination_oil and tg_WOR_oil < 0:
                rate_oil_predict = trend_oil[0]*cum_oil_current + trend_oil[1]
                if rate_oil_predict > 0:
                    note = 'Прогнозный дебит нефти'
                else:
                    rate_oil_predict = (rate_oil_before + rate_oil_current) / 2
                    note = 'Средний прогнозный дебит нефти'
            else:
                rate_oil_predict = (rate_oil_before + rate_oil_current) / 2
                note = 'Средний прогнозный дебит нефти'

            rate_water_predict = (wc_predict/100)*rate_oil_predict/(1 - wc_predict/100)
            rate_liq_predict = rate_water_predict + rate_oil_predict

            # сокращение воды
            rate_unprod_water = rate_water_current - rate_water_predict
            rate_unprod_water_current_oil = rate_water_current - (wc_predict/100)*rate_oil_current/(1-wc_predict/100)
            unprod_water_current_oil = rate_unprod_water_current_oil*30
            unprod_volume = rate_unprod_water*30
            change_wc = wc_current - wc_predict

    list_full = pd.Series([prod_well, reservoir, round(rate_oil_before, 2), round(rate_liq_before, 2), round(wc_before, 2),
                           date_break, round(rate_oil_current, 2), round(rate_liq_current, 2),
                        round(wc_current, 2), round(rate_oil_predict, 2), round(rate_liq_predict, 2), round(wc_predict, 2),
                           round(change_wc, 2), round(rate_unprod_water, 2), round(unprod_volume, 2), round(rate_unprod_water_current_oil, 2),
                           round(unprod_water_current_oil, 2), round(coefficient_of_determination_oil, 2), note], index=name_columns)



    df_break_result = df_break_result.append(list_full, ignore_index=True)
    return df_break_result, x_oil_interval, line_trend_oil



