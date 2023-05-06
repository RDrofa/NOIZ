import xlsxwriter
from mat import spearDecodeK as SD
import subprocess


def setExcelReportNO(data):
    workbook = xlsxwriter.Workbook('Отчеты\Отчет_НО.xlsx')
    worksheet = workbook.add_worksheet()

    title_format = workbook.add_format(
        {'align': 'center', 'valign': 'vcenter', 'fg_color': '#58747E', 'font_color': 'white', 'bold': True,
         'text_wrap': True, 'border': True, 'border_color': 'white'})
    cell_format1 = workbook.add_format(
        {'align': 'left', 'valign': 'vcenter', 'fg_color': '#C3D4DF',
         'text_wrap': True, 'border': True, 'border_color': '#5C99C1'})
    cell_format2 = workbook.add_format(
        {'align': 'left', 'valign': 'vcenter', 'fg_color': 'white',
         'text_wrap': True, 'border': True, 'border_color': '#5C99C1'})

    worksheet.set_column('A:A', 13)
    worksheet.set_column('B:B', 16)
    worksheet.set_column('C:C', 9)
    worksheet.set_column('D:D', 9)
    worksheet.set_column('E:E', 9)
    worksheet.set_column('F:F', 9)
    worksheet.set_column('G:G', 9)
    worksheet.set_column('H:H', 9)
    worksheet.set_column('I:I', 9)
    worksheet.set_column('J:J', 9)
    worksheet.set_column('K:K', 9)
    worksheet.set_column('L:L', 21)
    worksheet.set_column('M:M', 21)
    worksheet.set_column('N:N', 21)
    worksheet.set_column('O:O', 21)
    worksheet.set_column('P:P', 40)
    worksheet.set_row(0, 80)

    worksheet.merge_range('A1:A2', 'Скважина', title_format)
    worksheet.merge_range('B1:B2', 'Дата начала роста ВНФ', title_format)
    worksheet.merge_range('C1:E1', 'Параметры до роста ФНВ', title_format)
    worksheet.write('C2', 'qн, т/сут', title_format)
    worksheet.write('D2', 'qж, т/сут', title_format)
    worksheet.write('E2', '% воды', title_format)

    worksheet.merge_range('F1:H1', 'Параметры за последний месяц', title_format)
    worksheet.write('F2', 'qн, т/сут', title_format)
    worksheet.write('G2', 'qж, т/сут', title_format)
    worksheet.write('H2', '% воды', title_format)

    worksheet.merge_range('I1:K1', 'Прогнозные параметры', title_format)
    worksheet.write('I2', 'qн, т/сут', title_format)
    worksheet.write('J2', 'qж, т/сут', title_format)
    worksheet.write('K2', '% воды', title_format)

    worksheet.merge_range('L1:L2', 'Сокращение дебита воды (прогноз qн), т/сут', title_format)
    worksheet.merge_range('M1:M2', 'Объем непроизводительной добычи воды (прогноз qн), т', title_format)
    worksheet.merge_range('N1:N2', 'Сокращение дебита воды (текущий qн), т/сут', title_format)
    worksheet.merge_range('O1:O2', 'Объем непроизводительной добычи воды (текущий qн), т/сут', title_format)
    worksheet.merge_range('P1:P2', 'Заключение', title_format)

    #print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    #print(data)

    y = False
    for i in range(len(data)):
        y = not (y)
        if y:
            f = cell_format1
        else:
            f = cell_format2
        for j in range(len(data[i])):
            worksheet.write(i + 2, j, data[i][j], f)

    worksheet.freeze_panes(1, 0)

    workbook.close()
    subprocess.Popen("Отчеты\Отчет_НО.xlsx", shell=True)







def setExcelReportChen(data):

    workbook = xlsxwriter.Workbook('Отчеты\Отчет_Чен.xlsx')
    worksheet = workbook.add_worksheet()

    title_format = workbook.add_format(
        {'align': 'center', 'valign': 'vcenter', 'fg_color': '#58747E', 'font_color': 'white', 'bold': True,
         'text_wrap': True, 'border': True, 'border_color': 'white'})
    cell_format1 = workbook.add_format(
        {'align': 'left', 'valign': 'vcenter', 'fg_color': '#C3D4DF',
         'text_wrap': True, 'border': True, 'border_color': '#5C99C1'})
    cell_format2 = workbook.add_format(
        {'align': 'left', 'valign': 'vcenter', 'fg_color': 'white',
         'text_wrap': True, 'border': True, 'border_color': '#5C99C1'})

    worksheet.write('A1', 'Добывающая скважина', title_format)
    worksheet.write('B1', 'Объект', title_format)
    worksheet.write('C1', 'Состояние', title_format)
    worksheet.write('D1', 'Накопленная добыча нефти, т', title_format)
    worksheet.write('E1', 'Дебит нефти за последний месяц, т/сут', title_format)
    worksheet.write('F1', 'Дебит жидкости за последний месяц, т/сут', title_format)
    worksheet.write('G1', 'Обводненность за посл.месяц, % (вес)', title_format)
    worksheet.write('H1', 'Забойное давление (ТР), атм', title_format)
    worksheet.write('I1', 'Пластовое давление (ТР), атм', title_format)
    worksheet.write('J1', 'Источник обводнения', title_format)

    y = False
    for i in range(len(data)):
        y = not (y)
        if y:
            f = cell_format1
        else:
            f = cell_format2
        for j in range(len(data[i])):
            worksheet.write(i + 1, j, data[i][j], f)

    worksheet.set_column('A:A', 13)
    worksheet.set_column('B:B', 10)
    worksheet.set_column('C:C', 10)
    worksheet.set_column('D:D', 13)
    worksheet.set_column('E:E', 13)
    worksheet.set_column('F:F', 15)
    worksheet.set_column('G:G', 13)
    worksheet.set_column('H:H', 10)
    worksheet.set_column('I:I', 10)
    worksheet.set_column('J:J', 35)

    worksheet.autofilter('A1:J1')

    worksheet.freeze_panes(1, 0)

    workbook.close()
    subprocess.Popen("Отчеты\Отчет_Чен.xlsx", shell=True)







def setExcelReportSpear(data):


    workbook = xlsxwriter.Workbook('Отчеты\Отчет_Спирмен.xlsx')
    worksheet = workbook.add_worksheet()

    title_format = workbook.add_format(
        {'align': 'center', 'valign': 'vcenter', 'fg_color': '#58747E', 'font_color': 'white', 'bold': True,
         'text_wrap': True, 'border': True, 'border_color': 'white'})

    cell_format1 = workbook.add_format(
        {'align': 'left', 'valign': 'vcenter', 'fg_color': '#C3D4DF',
         'text_wrap': True, 'border': True, 'border_color': '#5C99C1'})
    cell_format2 = workbook.add_format(
        {'align': 'left', 'valign': 'vcenter', 'fg_color': 'white',
         'text_wrap': True, 'border': True, 'border_color': '#5C99C1'})

    worksheet.write('A1', 'Нагнетательная скважина', title_format)
    worksheet.write('B1', 'Добывающая скважина', title_format)
    worksheet.write('C1', 'Начало периода', title_format)
    worksheet.write('D1', 'Конец периода', title_format)
    worksheet.write('E1', 'Временной лаг, мес.', title_format)
    worksheet.write('F1', 'Коэф. Спирмена жидкость', title_format)
    worksheet.write('G1', 'Коэф. Спирмена нефть', title_format)
    worksheet.write('H1', 'Коэф. Спирмена Обводненность', title_format)
    worksheet.write('I1', 'Коэф. Спирмена Синтетика', title_format)
    worksheet.write('J1', 'Временной лаг Рзаб, мес.', title_format)
    worksheet.write('K1', 'Коэф. Спирмена Рзаб', title_format)
    worksheet.write('L1', 'Степень связи', title_format)

    y = False
    skv = data[0][0]
    for i in range(len(data)):
        if data[i][0]!=skv:
            skv = data[i][0]
            y = not (y)
        if y:
            f = cell_format1
        else:
            f = cell_format2

        try:

            worksheet.write(i + 1, 0, data[i][0], f)
            worksheet.write(i + 1, 1, data[i][7], f)
            worksheet.write(i + 1, 2, str(data[i][26])[:7], f)
            worksheet.write(i + 1, 3, str(data[i][27])[:7], f)
            worksheet.write(i + 1, 4, data[i][18], f) #lag
            worksheet.write(i + 1, 5, data[i][19], f)
            worksheet.write(i + 1, 6, data[i][20], f)
            worksheet.write(i + 1, 7, data[i][21], f)
            worksheet.write(i + 1, 8, data[i][22], f)
            worksheet.write(i + 1, 9, data[i][23], f)
            worksheet.write(i + 1, 10, data[i][24], f)
            ff = workbook.add_format(
                {'align': 'left', 'valign': 'vcenter', 'fg_color': data[i][28],
                 'text_wrap': True, 'border': True, 'border_color': '#5C99C1'})
            worksheet.write(i + 1, 11, data[i][25], ff)

        except:

            pass


    worksheet.set_column('A:A', 16)
    worksheet.set_column('B:B', 16)

    worksheet.set_column('C:C', 11)
    worksheet.set_column('D:D', 11)
    worksheet.set_column('E:E', 13)
    worksheet.set_column('F:F', 12)
    worksheet.set_column('G:G', 12)
    worksheet.set_column('H:H', 15)
    worksheet.set_column('I:I', 16)
    worksheet.set_column('J:J', 12)
    worksheet.set_column('K:K', 11)
    worksheet.set_column('L:L', 52)

    worksheet.autofilter('A1:L1')
    worksheet.freeze_panes(1, 0)

    workbook.close()
    subprocess.Popen("Отчеты\Отчет_Спирмен.xlsx", shell=True)






def setExcelReportAll(data, no):

    workbook = xlsxwriter.Workbook('Отчеты\Общий_отчет.xlsx')
    worksheet = workbook.add_worksheet()

    title_format = workbook.add_format(
        {'align': 'center', 'valign': 'vcenter', 'fg_color': '#58747E', 'font_color': 'white', 'bold': True, 'text_wrap': True, 'border': True, 'border_color':'white'})
    cell_format1 = workbook.add_format(
        {'align': 'left', 'valign': 'vcenter', 'fg_color': '#C3D4DF',
         'text_wrap': True, 'border': True, 'border_color': '#5C99C1'})
    cell_format2 = workbook.add_format(
        {'align': 'left', 'valign': 'vcenter', 'fg_color': 'white',
         'text_wrap': True, 'border': True, 'border_color': '#5C99C1'})
    #title_format = workbook.add_format(
       # {'align': 'center', 'text_wrap': True, })

    worksheet.write('A1', 'Нагнетательная скважина', title_format)
    worksheet.write('B1', 'Объект', title_format)
    worksheet.write('C1', 'Состояние', title_format)
    worksheet.write('D1', 'ФНВ', title_format)
    worksheet.write('E1', 'Накопленная закачка, тыс.м3', title_format)
    worksheet.write('F1', 'Приемистость за последний месяц, м3/сут', title_format)
    worksheet.write('G1', 'Забойное давление (ТР), атм', title_format)
    worksheet.write('H1', 'Диаметр штуцера, мм', title_format)
    worksheet.write('I1', 'Добывающая скважина', title_format)
    worksheet.write('J1', 'Объект', title_format)
    worksheet.write('K1', 'Состояние', title_format)
    worksheet.write('L1', 'КП', title_format)
    worksheet.write('M1', 'Накопленная добыча нефти, т', title_format)
    worksheet.write('N1', 'Дебит нефти за последний месяц, т/сут', title_format)
    worksheet.write('O1', 'Дебит жидкости за последний месяц, т/сут', title_format)
    worksheet.write('P1', 'Обводненность за посл.месяц, % (вес)', title_format)
    worksheet.write('Q1', 'Забойное давление (ТР), атм', title_format)
    worksheet.write('R1', 'Пластовое давление (ТР), атм', title_format)
    worksheet.write('S1', 'Источник обводнения', title_format)
    if no == 0:
        worksheet.write('T1', 'Расстояние между скважинами, м', title_format)
        worksheet.write('U1', 'Временной лаг, мес.', title_format)
        worksheet.write('V1', 'Коэф. Спирмена жидкость', title_format)
        worksheet.write('W1', 'Коэф. Спирмена нефть', title_format)
        worksheet.write('X1', 'Коэф. Спирмена Обводненность', title_format)
        worksheet.write('Y1', 'Коэф. Спирмена Синтетика', title_format)
        worksheet.write('Z1', 'Временной лаг Рзаб, мес.', title_format)
        worksheet.write('AA1', 'Коэф. Спирмена Рзаб', title_format)
        worksheet.write('AB1', 'Степень связи', title_format)
    else:
        worksheet.write('T1', 'Прогнозный дебит нефти, т/сут', title_format)
        worksheet.write('U1', 'Прогнозный дебит жидкости, т/сут', title_format)
        worksheet.write('V1', 'Прогнозная обводненность, %', title_format)
        worksheet.write('W1', 'Объем непроизводительной добычи воды (прогноз qн), т', title_format)
        worksheet.write('X1', 'Объем непроизводительной добычи воды (текущий qн), т/сут', title_format)
        worksheet.write('Y1', 'Расстояние между скважинами, м', title_format)
        worksheet.write('Z1', 'Временной лаг, мес.', title_format)
        worksheet.write('AA1', 'Коэф. Спирмена жидкость', title_format)
        worksheet.write('AB1', 'Коэф. Спирмена нефть', title_format)
        worksheet.write('AC1', 'Коэф. Спирмена Обводненность', title_format)
        worksheet.write('AD1', 'Коэф. Спирмена Синтетика', title_format)
        worksheet.write('AE1', 'Временной лаг Рзаб, мес.', title_format)
        worksheet.write('AF1', 'Коэф. Спирмена Рзаб', title_format)
        worksheet.write('AG1', 'Степень связи', title_format)



    skv = data[0][0]
    y = False
    for i in range(len(data)):
        if data[i][0] != skv:
            skv = data[i][0]
            y = not(y)
        if y:
            f = cell_format1
        else:
            f = cell_format2
        for j in range(len(data[i])-3):
            worksheet.write(i+1,j, data[i][j], f)

    worksheet.set_column('A:A', 15)
    worksheet.set_column('B:B', 10)
    worksheet.set_column('C:C', 10)
    worksheet.set_column('D:D', 7)
    worksheet.set_column('E:E', 10)
    worksheet.set_column('F:F', 13)
    worksheet.set_column('G:G', 10)
    worksheet.set_column('H:H', 9)
    worksheet.set_column('I:I', 13)
    worksheet.set_column('J:J', 10)
    worksheet.set_column('K:K', 10)
    worksheet.set_column('L:L', 7)
    worksheet.set_column('M:M', 13)
    worksheet.set_column('N:N', 13)
    worksheet.set_column('O:O', 15)
    worksheet.set_column('P:P', 13)
    worksheet.set_column('Q:Q', 10)
    worksheet.set_column('R:R', 10)
    worksheet.set_column('S:S', 30)
    if no == 0:
        worksheet.set_column('T:T', 13)
        worksheet.set_column('U:U', 11)
        worksheet.set_column('V:V', 11)
        worksheet.set_column('W:W', 10)
        worksheet.set_column('X:X', 10)
        worksheet.set_column('Y:Y', 10)
        worksheet.set_column('Z:Z', 11)
        worksheet.set_column('AA:AA', 10)
        worksheet.set_column('AB:AB', 45)
        worksheet.autofilter('A1:AB1')
    else:
        worksheet.set_column('T:T', 12)
        worksheet.set_column('U:U', 12)
        worksheet.set_column('V:V', 12)
        worksheet.set_column('W:W', 21)
        worksheet.set_column('X:X', 21)
        worksheet.set_column('Y:Y', 13)
        worksheet.set_column('Z:Z', 11)
        worksheet.set_column('AA:AA', 11)
        worksheet.set_column('AB:AB', 10)
        worksheet.set_column('AC:AC', 10)
        worksheet.set_column('AD:AD', 10)
        worksheet.set_column('AE:AE', 11)
        worksheet.set_column('AF:AF', 10)
        worksheet.set_column('AG:AG', 45)

        worksheet.autofilter('A1:AG1')



    '''worksheet.add_table(0, 0, len(data) , 24, {'data': data,
                         'columns': [{'header': 'Нагнетательная скважина'},
                                     {'header': 'Объект'},
                                     {'header': 'Состояние'},
                                     {'header': 'Накопленная закачка, тыс.м3'},
                                     {'header': 'Приемистость за последний месяц, м3/сут'},
                                     {'header': 'Забойное давление (ТР), атм'},
                                     {'header': 'Диаметр штуцера, мм'},
                                     {'header': 'Добывающая скважина'},
                                     {'header': 'Объект '},
                                     {'header': 'Состояние '},
                                     {'header': 'Накопленная добыча нефти, т'},
                                     {'header': 'Дебит нефти за последний месяц, т/сут'},
                                     {'header': 'Дебит жидкости за последний месяц, т/сут'},
                                     {'header': 'Обводненность за посл.месяц, % (вес)'},
                                     {'header': 'Забойное давление (ТР), атм '},
                                     {'header': 'Пластовое давление (ТР), атм'},
                                     {'header': 'Источник обводнения'},
                                     {'header': 'Расстояние между скважинами, м'},
                                     {'header': 'Временной лаг, мес.'},
                                     {'header': 'Коэф. Спирмена жидкость'},
                                     {'header': 'Коэф. Спирмена нефть'},
                                     {'header': 'Коэф. Спирмена Обводненность'},
                                     {'header': 'Коэф. Спирмена Синтетика'},
                                     {'header': 'Временной лаг Рзаб, мес.'},
                                     {'header': 'Коэф. Спирмена Рзаб'},
                                     {'header': 'Степень связи'}

                                     ], 'banded_rows': False,
                         'banded_columns': True})

    worksheet.conditional_format(0, 0, len(data) , 40, {'type': 'cell',
                                                      'criteria': '!=',
                                                      'value': '____',
                                                      'format': title_format})'''
    worksheet.freeze_panes(1, 0)
    workbook.close()

    subprocess.Popen("Отчеты\Общий_отчет.xlsx", shell=True)





def setExcelReport(L, nag, cols, D1, D2, K, oneLag):

    try:

        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook('Отчеты\Spearman_'+str(nag)+'.xlsx')
        worksheet = workbook.add_worksheet()

        worksheet.set_column('C:C', 11)
        worksheet.set_column('D:D', 11)
        worksheet.set_column('E:E', 5)
        worksheet.set_column('F:F', 9)
        worksheet.set_column('G:G', 9)
        worksheet.set_column('H:H', 9)
        worksheet.set_column('I:I', 40)

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})

        # Write some simple text.
        merge_format = workbook.add_format({'align': 'center','fg_color': '#00008B', 'font_color':'white', 'bold': True, })
        worksheet.merge_range('A2:B2', 'Пара скважин',merge_format)
        worksheet.merge_range('C2:D2', 'Период расчета',merge_format)
        #worksheet.merge_range('E2:E3', 'ета', merge_format)
        worksheet.write('E2', 'Лаг',merge_format)
        worksheet.write('F2', 'Жидкость',merge_format)
        worksheet.write('G2', 'Нефть',merge_format)
        worksheet.write('H2', 'Давление',merge_format)
        worksheet.write('I2', 'Комментарий', merge_format)
        worksheet.write('A1', 'Коэффициент Спирмена в зависимости от временного лага', bold)

        #worksheet.merge_range('E2:E3', 'vvvv', merge_format)

        '''worksheet.write('A3', 'НАГ')
        worksheet.write('B3', 'НЕФ')
        worksheet.write('C3', 'НАЧАЛО')
        worksheet.write('D3', 'КОНЕЦ')
    
        for i in range(len(cols)):
            for j in range(7):
                worksheet.write(j+i*7+3,4, str(j))'''



        data = []
        for i in range(len(cols)):
            for j in range(oneLag[0]):
                tmp = []
                tmp.append(str(nag))
                tmp.append(str(cols[i]))
                tmp.append(D1[i][:7])
                tmp.append(D2[i][:7])
                if oneLag[1]==-1:
                    tmp.append(j)
                else:
                    tmp.append(oneLag[1])
                tmp.append(L[i * 3][j])
                tmp.append(L[i * 3 + 1][j])
                tmp.append(L[i * 3 + 2][j])
                s, clr = SD(K[j+7*i])
                tmp.append(s)
                data.append(tmp)

        worksheet.add_table(2,0,2+len(cols)*oneLag[0],8, {'data': data,
                                  'columns': [{'header': 'НАГ'},
                                              {'header': 'НЕФ'},
                                              {'header': 'НАЧАЛО'},
                                              {'header': 'КОНЕЦ'},
                                              {'header': 'Л'},
                                              {'header': 'Qж'},
                                              {'header': 'Qн'},
                                              {'header': 'Pзаб'},
                                              {'header': '   '}
                                              ], 'banded_rows': False, 'banded_columns': True})

        #worksheet.merge_range(3,0,len(cols)*7+3,0, 'Период расчета', merge_format)

        if oneLag[0]==1:
            while True:
                try:
                    K.remove(0)
                except:
                    break

        for i in range(0,len(K)):

            s, clr = SD(K[i])
            format1 = workbook.add_format({'bg_color': clr,
                                       })
            worksheet.conditional_format(3 + i, 4, 3 + i, 7, {'type': 'cell',
                                                 'criteria': '<',
                                                 'value': 1000,
                                                 'format': format1})
            worksheet.conditional_format(3 + i, 8, 3 + i, 8, {'type': 'text',
                                                              'criteria': 'containing',
                                                              'value': 'свя',
                                                              'format': format1})
        #worksheet.insert_image('B5', 'logo.png')  'font_color': '#9C0006'



        workbook.close()

    except:
        pass


