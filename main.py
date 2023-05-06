import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QRegExp, QEvent
from PyQt5.uic import loadUi
import matplotlib.dates as mdates
from  PyQt5.QtWidgets  import *
import  numpy  as  np
from matplotlib.patches import Circle
from matplotlib.transforms import Affine2D
from matplotlib.patches import FancyBboxPatch
from scipy.stats import spearmanr
import logging
from datetime import datetime
import os
from matplotlib.widgets import Slider
from matplotlib.lines import Line2D
#from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from sql import SQL
from spearman_cls import spearwell
from chen_cls import chenwell
from hall_cls import hallwell
from NO_cls import NOwell
from data_cls import dataform, datawell
import mat
import excl


class Spirman(QtWidgets.QDialog):

    def __init__(self):
        super(Spirman,self).__init__()
        loadUi("Spirman.ui",self)
        #self.Gr_spir.F.tight_layout()
        #self.Gr_spir.F.tight_layout(rect=[-1, 0, 0, 0])
        #self.Gr_spir2 = self.Gr_spir.canvas.axes.twinx()
        # self.cursor = Cursor(self.Gr_spir.canvas.axes, useblit=True, color='red', linewidth=2)
        self.ListOfSpirmanObj = []
        self.Gr_spir_line = self.Gr_spir.canvas.axes.twinx()
        self.Gr_spir_line2 = self.Gr_spir.canvas.axes.twinx()
        self.checkBox_priem.stateChanged.connect(self.changeGr_spir)
        self.checkBox_debLiq.stateChanged.connect(self.changeGr_spir)
        self.checkBox_debOil.stateChanged.connect(self.changeGr_spir)
        self.checkBox_Pzab.stateChanged.connect(self.changeGr_spir)
        self.checkBox_zakTime.stateChanged.connect(self.changeGr_spir)
        self.checkBox_debTime.stateChanged.connect(self.changeGr_spir)
        self.checkBox_water.stateChanged.connect(self.changeGr_spir)
        self.checkBox_sint.stateChanged.connect(self.changeGr_spir)
        self.checkBox_event.stateChanged.connect(self.changeGr_spir)
        self.checkBox_legend.stateChanged.connect(self.changeGr_spir)

        self.Gr_spir_line.yaxis.set_visible(False)
        self.Gr_spir_line2.yaxis.set_visible(False)

        self.combo_lag.addItems(['0', '1', '2', '3', '4', '5', '6'])
        self.currWell = 0
        self.lineCollor = []

        #s_ax = self.Gr_spir.F.add_axes([0.063, 0.07, 0.874, 0.04], facecolor='red')
        #self.slider.valmax = 90
        #self.s_ax = self.Gr_spir.F.add_axes([0.105, 0.01, 0.68, 0.04], facecolor='white')
        #===self.s_ax = self.Gr_spir.F.add_axes([0.105, 0.01, 0.68, 0.04], facecolor='white')

       # self.slider = range_slider.RangeSlider(Qt.Horizontal)
        '''self.slider.setMinimumHeight(30)
        self.slider.setMinimum(1)
        self.slider.setMaximum(60)
        self.slider.setLow(1)
        self.slider.setHigh(60)
        self.slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider.sliderMoved.connect(self.echo)
        self.HLayout.addWidget(self.slider)'''

        '''self.HLayout.addWidget(self.labelLeft)
        self.HLayout.addWidget(self.labelRight)
        self.HlLayout_period.addWidget(self.listWidget)
        self.HlLayout_period.addWidget(self.label_period)
        self.HlLayout_period.addWidget(self.Gr_spir.toolbar)
        self.HlLayout_period.addWidget(self.But_vertlines)
        self.HlLayout_period.addWidget(self.But_vertlines2)'''

        self.HL_tools.addWidget(self.Gr_spir.toolbar)
        self.HL_tools.addWidget(self.label_period)
        self.HL_tools.addWidget(self.comboDat1)
        self.HL_tools.addWidget(self.label_period2)
        self.HL_tools.addWidget(self.comboDat2)


        #self.Gr_spir.canvas.mpl_connect('motion_notify_event', self.getCoords)
        self.cid = self.Gr_spir.canvas.mpl_connect('button_release_event', self.onclick_to_spir)

        self.But_vertlines.setCheckable(True)

        self.But_period.clicked.connect(self.avtoPeriod)
        self.But_period_all.clicked.connect(self.avtoPeriod)
        self.But_refresh.clicked.connect(self.refreshSpirLag)
        self.But_allRange.clicked.connect(self.setNewRangeForAll)
        #self.But_vertlines.setChecked(True)


        self.listWidget.itemClicked.connect(self.listWidgetClick)  # Привязка события клика
        self.listWidget2.itemClicked.connect(self.listWidget2Click)  # Привязка события клика
        self.But_save_spear.clicked.connect(self.saveSpear)
        self.But_open_spear.clicked.connect(self.doRepSpear)



        self.tableSpear.setColumnWidth(0, 50)
        self.tableSpear.setColumnWidth(1, 40)
        self.tableSpear.setColumnWidth(2, 40)
        self.tableSpear.setColumnWidth(3, 40)
        self.tableSpear.setColumnWidth(4, 40)
        self.tableSpear.setColumnWidth(5, 40)
        self.tableSpear.setColumnWidth(6, 300)

        self.L_arrs = []
        self.whatVertLine = 1
        self.currVertLeft = 99999999
        self.currVertRight = -999

        self.tableSpear.setRowCount(7)
        self.letSlide = True

        self.comboDat1.activated[str].connect(self.onChangedComboDat)
        self.comboDat2.activated[str].connect(self.onChangedComboDat)

        self.ListOfSpirmanObj = []
        self.currFormForSpir = ''
        self.lolof = []

    def errorRep(self):
        QtWidgets.QMessageBox.critical(self, "Ошибка", "Ошибка при создании файла")


    def setNewRangeForAll(self):

        for ind in  self.ListOfSpirmanObj:

            ind.range_start = self.comboDat1.currentIndex()
            ind.range_fin = self.comboDat2.currentIndex()
            ind.checkRange()

        for i in range(len(self.NumbersOfSpirObj)):
            item = self.listWidget2.item(i)
            if self.ListOfSpirmanObj[self.NumbersOfSpirObj[i]].right_range == False:
                item.setBackground(QtGui.QColor('darksalmon'))
            else:
                item.setBackground(QtGui.QColor('white'))


        self.changeColor(self.ListOfSpirmanObj[self.N].right_range)





    def onChangedComboDat(self):

        if self.comboDat1.currentIndex() < self.comboDat2.currentIndex():

            self.ListOfSpirmanObj[self.N].range_start = self.comboDat1.currentIndex()
            self.ListOfSpirmanObj[self.N].range_fin = self.comboDat2.currentIndex()
            self.ListOfSpirmanObj[self.N].checkRange()
            self.grVertLines(self.ListOfSpirmanObj[self.N].range_start_D, self.ListOfSpirmanObj[self.N].range_fin_D)
            self.changeColor(self.ListOfSpirmanObj[self.N].right_range)
            self.doSpearText()

        else:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Начальная дата должна быть меньше конечной")


    def doRepSpear(self):

        first_window.listSpearReport = self.ListOfSpirmanObj[:]

        first_window.doReport(1)


    def saveSpear(self):
        #print(self.Gr_spir.toolbar.mode)
        #if self.Gr_spir.toolbar.mode == 'zoom rect':

         #   self.Gr_spir.toolbar.mode = 'pan/zoom

        first_window.listSpearReport = self.ListOfSpirmanObj[:]
        QtWidgets.QMessageBox.information(self, "OK", "Данные записаны в отчет")



    def fillTable(self):





        def isEmp(a):
            if float(a) == 0:
                return QTableWidgetItem('0')
            elif float(a) == -1:
                return QTableWidgetItem(' - ')
            else:
                return QTableWidgetItem(str(a))


        for i in range(7):
            item = QTableWidgetItem(str(i))
            self.tableSpear.setItem(i, 0, item)

            item = isEmp(self.ListOfSpirmanObj[self.N].df_out.loc[i, 'L'])
            self.tableSpear.setItem(i, 1, item)

            item  = isEmp(self.ListOfSpirmanObj[self.N].df_out.loc[i, 'O'])
            self.tableSpear.setItem(i, 2, item)

            item= isEmp(self.ListOfSpirmanObj[self.N].df_out.loc[i, 'P'])
            self.tableSpear.setItem(i, 3, item)

            item = isEmp(self.ListOfSpirmanObj[self.N].df_out.loc[i, 'W'])
            self.tableSpear.setItem(i, 4, item)

            item = isEmp(self.ListOfSpirmanObj[self.N].df_out.loc[i, 'S'])
            self.tableSpear.setItem(i, 5, item)

            K = self.ListOfSpirmanObj[self.N].K_all[i]
            S, clr = mat.spearDecodeK(K)

            if float(self.ListOfSpirmanObj[self.N].df_out.loc[i, 'L'])==0 and float(self.ListOfSpirmanObj[self.N].df_out.loc[i, 'O']) ==0:
                item = QTableWidgetItem('Нет гидродинамической связи')
            else:
                item = QTableWidgetItem(S)
            self.tableSpear.setItem(i, 6, item)

            for j  in range(7):
                self.tableSpear.item(i,j).setBackground(QtGui.QColor(clr))


            if self.ListOfSpirmanObj[self.N].right_range:
                S, clr = mat.spearDecodeK(self.ListOfSpirmanObj[self.N].K)
                self.textRezult.setHtml(
                    mat.setHTMrezult(self.ListOfSpirmanObj[self.N].Kl_lag, self.ListOfSpirmanObj[self.N].Ko_lag,
                                     self.ListOfSpirmanObj[self.N].Kp_lag, S, clr))
            else:
                self.textRezult.setHtml('')


    def avtoPeriod(self):
        try:

            if self.sender().objectName() == 'But_period':

                self.ListOfSpirmanObj[self.N].setRange()

            else:
                for ind in self.ListOfSpirmanObj:
                    ind.range_start = ind.range_start_save
                    ind.range_fin = ind.range_fin_save
                    ind.checkRange()


                for i in range(len(self.NumbersOfSpirObj)):
                    item = self.listWidget2.item(i)
                    if self.ListOfSpirmanObj[self.NumbersOfSpirObj[i]].right_range == False:
                        item.setBackground(QtGui.QColor('darksalmon'))
                    else:
                        item.setBackground(QtGui.QColor('white'))


            self.grVertLines(self.ListOfSpirmanObj[self.N].range_start_D,
                             self.ListOfSpirmanObj[self.N].range_fin_D)

            self.doSpearText()
            self.changeColor(self.ListOfSpirmanObj[self.N].right_range)
            self.comboDat1.setCurrentIndex(self.ListOfSpirmanObj[self.N].range_start)
            self.comboDat2.setCurrentIndex(self.ListOfSpirmanObj[self.N].range_fin)

        except Exception as e:  # Запись  ошибок в лог
            logging.error(str(datetime.now()) + '   ' + str(e) + '   avtoPeriod')




    def refreshSpirLag(self):
        try:
            if self.radio1.isChecked():
                self.ListOfSpirmanObj[self.N].oneLag = -2
            else:
                self.ListOfSpirmanObj[self.N].oneLag = int(self.combo_lag.currentText())
            self.ListOfSpirmanObj[self.N].checkRange()
            self.changeColor(self.ListOfSpirmanObj[self.N].right_range)
            self.doSpearText()
        except Exception as e:  # Запись  ошибок в лог
            logging.error(str(datetime.now()) + '   ' + str(e)+'   refreshSpirLag')


    def onclick_to_spir(self, event):

       # if self.Gr_spir.toolbar.mode== 'pan/zoom' or :


        #try:

        if self.But_vertlines.isChecked():

            if event.button == 1:
                if event.xdata<self.currVertRight:
                    self.currVertLeft = int(event.xdata)
                    D = str(mdates.num2date(self.currVertLeft))[:7]
                    n = mat.getNumOfDate(self.ListOfSpirmanObj[self.N].source_df['D'].tolist(), D)
                    self.ListOfSpirmanObj[self.N].range_start = n
                    self.ListOfSpirmanObj[self.N].checkRange()
                    self.grVertLines(self.ListOfSpirmanObj[self.N].range_start_D, -2)
                    self.changeColor(self.ListOfSpirmanObj[self.N].right_range)
                    self.doSpearText()
                    self.comboDat1.setCurrentIndex(n)

            elif event.button == 3:
                if event.xdata > self.currVertLeft:
                    self.currVertRight = int(event.xdata)
                    D = str(mdates.num2date( self.currVertRight))[:7]
                    n = mat.getNumOfDate(self.ListOfSpirmanObj[self.N].source_df['D'].tolist(), D)
                    self.ListOfSpirmanObj[self.N].range_fin = n
                    self.ListOfSpirmanObj[self.N].checkRange()
                    self.grVertLines(-2, self.ListOfSpirmanObj[self.N].range_fin_D)
                    self.changeColor(self.ListOfSpirmanObj[self.N].right_range)
                    self.doSpearText()
                    self.comboDat2.setCurrentIndex(n)
            else:
                pass

        #except:
        #    print('???????????????????????')



        # Перекраска списка скважин

    def changeItemColor(self):
        itm = self.currNEF
        if self.ListOfSpirmanObj[self.N].right_range == False:
            itm.setBackground(QtGui.QColor('darksalmon'))
        else:
            itm.setBackground(QtGui.QColor('white'))


    def listWidgetClick(self):

        #self.label_period.setText('')
        #self.Gr_spir.canvas.axes.clear()
        #self.Gr_spir.canvas.draw()

        self.But_refresh.setEnabled(False)
        self.comboDat1.setEnabled(False)
        self.comboDat2.setEnabled(False)
        self.NumbersOfSpirObj = []
        self.listWidget2.clear()
        if self.listWidget.currentRow()==-1:
            self.listWidget.setCurrentRow(0)
        self.currNAG = self.listWidget.currentRow()
        for i in range(len(self.ListOfSpirmanObj)):
            a = self.ListOfSpirmanObj[i].ind1
            if a==self.currNAG:
                b = mat.getSkvNfromText(self.ListOfSpirmanObj[i].NefID)
                item = QListWidgetItem(b)
                if self.ListOfSpirmanObj[i].right_range == False:
                    item.setBackground(QtGui.QColor('darksalmon'))
                else:
                    item.setBackground(QtGui.QColor('white'))
                self.listWidget2.addItem(item)
                self.NumbersOfSpirObj.append(i)



    def listWidget2Click(self):
        if self.listWidget2.currentRow()==-1:
            self.listWidget2.setCurrentRow(0)
        self.currNEF = self.listWidget2.currentRow()
        self.N = self.NumbersOfSpirObj[self.currNEF]

        dat_len = len(self.ListOfSpirmanObj[self.N].source_df['D'].tolist())
        a = self.ListOfSpirmanObj[self.N].range_start+1
        b = self.ListOfSpirmanObj[self.N].range_fin+1

        #===self.s_ax.remove()

        #====self.s_ax = self.Gr_spir.F.add_axes([0.104, 0.01, 0.681, 0.04], facecolor='white')
        #====self.slider = RangeSlider(self.s_ax, label=' ', dragging=True,
                                  #valmin=1, valmax=dat_len, valinit=(a, b), valstep=1)

        #===self.slider.on_changed(self.update)

        self.But_refresh.setEnabled(True)
        self.comboDat1.setEnabled(True)
        self.comboDat2.setEnabled(True)

        self.comboDat1.setCurrentIndex(self.ListOfSpirmanObj[self.N].range_start)
        self.comboDat2.setCurrentIndex(self.ListOfSpirmanObj[self.N].range_fin)

        self.doSpearText()
        self.doGrGpear()



    def changeColor(self, u):
        if u == False:
            self.Gr_spir.F.patch.set_facecolor('darksalmon')
            self.Gr_spir_Ev.tick_params(axis='y', colors='darksalmon')
        else:
            self.Gr_spir.F.patch.set_facecolor('white')
            self.Gr_spir_Ev.tick_params(axis='y', colors='white')
        self.Gr_spir.canvas.draw()

        itm = self.listWidget2.currentItem()


        if u == False:
            itm.setBackground(QtGui.QColor('darksalmon'))
            self.fillTable()
        else:
            itm.setBackground(QtGui.QColor('white'))

    def setListForSpear(self):
        itm = QListWidgetItem(self.cols[0])
        self.listWidget.clear()
        for i in range(len(self.cols)):
            item = QListWidgetItem('  '+self.cols[i]+'  ')

            # Выбор цвета ячеек

            if self.checkRange(self.range1[i],self.range2[i],i) == False:
                item.setBackground(QtGui.QColor('darksalmon'))
            else:
                item.setBackground(QtGui.QColor('white'))

            if i==self.currWell:
                itm = item
            self.listWidget.addItem (item)
        self.listWidget.setCurrentItem(itm)

        #for i in range(len(self.cols)):
            #self.radio = QRadioButton(self.cols[i])
            #if i==0:
            #    self.radio.setChecked(True)
            #else:
            #    self.radio.setChecked(False)
            #self.HLayout_radio.addWidget(self.radio)
            #self.radio.toggled.connect(self.onClicked)
            #self.radio.setObjectName('R' + self.cols[i])


    def grVertLines(self, l,h):   # l,h  - даты



        self.letSlide = False

        if l != -2:

            self.Gr_spir_line.clear()
            self.Gr_spir_line.axvline(x=l, color='red', linewidth=3)

            self.currVertLeft = mdates.date2num(l)    #  даты в виде числа (17345)

            a = self.ListOfSpirmanObj[self.N].range_start + 1
            #===self.slider.set_val((a, self.slider.val[1]))


        if h != -2:
            self.Gr_spir_line2.clear()
            self.Gr_spir_line2.axvline(x=h, color='indigo', linewidth=3)

            self.currVertRight = mdates.date2num(h)

            b = self.ListOfSpirmanObj[self.N].range_fin + 1
            #===self.slider.set_val((self.slider.val[0], b ))

        # print(self.Slider1.value())
        self.Gr_spir.canvas.draw()

        self.letSlide = True


    def update(self, val):

        if self.letSlide:
            L = self.ListOfSpirmanObj[self.N].source_df['D'].tolist()

            a = L[val[0]-1]
            b = L[val[1]-1]

            self.grVertLines(a,b)



    def echo(self, low_value, high_value):

        self.setLabels(low_value, high_value)
        self.changeColor(self.checkRange(low_value, high_value, self.currWell))
        self.grVertLines(low_value, high_value)
        self.range1[self.currWell] = low_value
        self.range2[self.currWell] = high_value

        # Перекраска списка скважин
        itm = self.listWidget.currentItem()
        if self.checkRange(self.range1[self.currWell], self.range2[self.currWell], self.currWell) == False:
            itm.setBackground(QtGui.QColor('darksalmon'))
        else:
            itm.setBackground(QtGui.QColor('white'))

        self.setRightWell()

    #   ВЫЧИСЛЕНИЕ КОЭФФИЦИЕНТОВ СПИРМЕНА----------------------------------------------
    def doSpearCalc(self):

        #try:

            df_result = sql.doEmptyDataframe()
            L_result = []
            dat1= []
            dat2= []
            allNef = []
            K = []

            #self.df_list[cw].columns[2]
            for i in range(len(self.df_list)):

                l = self.df_list[i]['D'].tolist()
                dat1.append( l[self.range1[i]-1] )
                dat2.append( l[self.range2[i] - 1])

                if self.radio1.isChecked():
                    a = 0
                    b = self.checkedRanges[i]
                    v = 0
                    oneLag = [7,-1, 1]
                else:
                    a = int(self.combo_lag.currentText())
                    b = a + 1
                    v = a
                    oneLag = [1,a, 7]


                if self.checkedRanges[i]>0:

                    allNef.append(self.cols[i])
                    nag = self.df_list[i].columns[2]
                    priem = self.df_list[i][nag].tolist()
                    priem = mat.doRangeForSpear(priem,self.range1[i],self.range2[i]-b+1)




                    tmp = []
                    for j in range(a, b):
                        liq = self.df_list[i]['debLiq'].tolist()
                        liq = mat.doRangeForSpear(liq, self.range1[i]+j, self.range2[i]+j-b+1)

                        corr, p_value = spearmanr(priem, liq)
                        corr = round(corr, 2)
                        tmp.append(corr)
                    while len(tmp)<7:
                        tmp.append('')
                    df_result[nag+' - '+self.cols[i]+' Жидкость'] = tmp
                    L_result.append(tmp)

                    tmp = []
                    for j in range(a, b):
                        oil = self.df_list[i]['debOil'].tolist()
                        oil = mat.doRangeForSpear(oil, self.range1[i]+j, self.range2[i]+j-b+1)
                        corr, p_value = spearmanr(priem, oil)
                        corr = round(corr, 2)
                        tmp.append(corr)
                    while len(tmp)<7:
                        tmp.append('')
                    df_result[nag+' - '+self.cols[i]+' Нефть'] = tmp
                    L_result.append(tmp)

                    tmp = []
                    for j in range(a, b):
                        zab = self.df_list[i]['Pzab'].tolist()
                        zab = mat.doRangeForSpear(zab, self.range1[i]+j, self.range2[i]+j-b+1)

                        if mat.pzabRepeat(zab)>=70:
                            tmp.append('')
                        else:
                            corr, p_value = spearmanr(priem, zab)
                            corr = round(corr,2)
                            tmp.append(corr)
                    while len(tmp)<7:
                        tmp.append('')
                    df_result[nag+' - '+self.cols[i]+' Давление'] = tmp
                    L_result.append(tmp)



                    '''oil = self.df_list[i]['debOilTR'].tolist()
                    oil = mat.doRangeForSpear(oil, self.range1[i], self.range2[i])
                    zab = self.df_list[i]['Pzab'].tolist()
                    zab = mat.doRangeForSpear(zab, self.range1[i], self.range2[i])'''



            for i in range(0, len(L_result), 3):
                for j in range(len(L_result[i])):
                    if L_result[i][j]!='' and L_result[i+1][j]!='' and L_result[i+2][j]!='':
                        K.append(mat.spearDecode3(L_result[i][j], L_result[i+2][j], L_result[i+1][j]))
                    elif L_result[i][j]!='' and L_result[i+1][j]!='':
                        K.append(mat.spearDecode2(L_result[i][j], L_result[i + 1][j]))
                    else:
                        K.append(0)


            self.lineCollor = []
            self.tableSpear.setRowCount(len(allNef))


            for j in range(len(allNef)):
                item = QTableWidgetItem(str(allNef[j]))
                self.tableSpear.setItem(j, 0, item)
                item = QTableWidgetItem(str(dat1[j][:7]))
                self.tableSpear.setItem(j, 1, item)
                item = QTableWidgetItem(str(dat2[j][:7]))
                self.tableSpear.setItem(j, 2, item)

                if oneLag[0]==7:
                    tmp = K[j * 7:7 * (j + 1)]
                    T = tmp.index(max(tmp))
                    item = QTableWidgetItem(str(T))
                    self.tableSpear.setItem(j, 3, item)

                    U, clr = mat.spearDecodeK(tmp[T])
                    item = QTableWidgetItem(str(U))
                    self.tableSpear.setItem(j, 4, item)

                else:

                    tmp = K[j * 7:7 * (j + 1)]
                    T = 0
                    item = QTableWidgetItem(self.combo_lag.currentText())
                    self.tableSpear.setItem(j, 3, item)

                    U, clr = mat.spearDecodeK(tmp[T])
                    item = QTableWidgetItem(str(U))
                    self.tableSpear.setItem(j, 4, item)

                self.tableSpear.item(j, 0).setBackground(QtGui.QColor(clr))
                self.tableSpear.item(j, 0).setBackground(QtGui.QColor(clr))
                self.tableSpear.item(j, 1).setBackground(QtGui.QColor(clr))
                self.tableSpear.item(j, 2).setBackground(QtGui.QColor(clr))
                self.tableSpear.item(j, 3).setBackground(QtGui.QColor(clr))
                self.tableSpear.item(j, 4).setBackground(QtGui.QColor(clr))

                self.lineCollor.append(clr)



            excl.setExcelReport(L_result, nag, allNef, dat1, dat2, K, oneLag)






            HTM = ''


            for i in range(len(self.cols)):

                self.lineCollor.append('N')

                if self.checkedRanges[i] >0:



                    wells = 'Скважины:   '+nag+' - '+self.cols[i]
                    wells = "<font color='black' size='5'><red>"+wells+"</font><br>"
                    HTM = HTM + wells

                    p = df_result[nag+' - '+self.cols[i]+' Жидкость'].tolist()
                    while True:
                        try:
                            p.remove('')
                        except:
                            break
                    HTM = HTM + "<font color='blue' size='5'><red>Жидкость</font><br>"
                    for j in range(len(p)):
                        if p[j]>0.4:
                            clr = 'green'
                        else:
                            clr = 'red'
                        textt = 'Лаг ' + str(j+v) + ' мес.  ->  Rs = ' + str(round(p[j], 2))
                        texxt = "<font color='"+clr+"' size='4'><"+clr+">"+textt+"</font><br>"
                        HTM = HTM + texxt

                    m1 =  max(p)

                    p = df_result[nag+' - '+self.cols[i]+' Нефть'].tolist()
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
                        textt = 'Лаг ' + str(j+v) + ' мес.  ->  Rs = ' + str(round(p[j], 2))
                        texxt = "<font color='" + clr + "' size='4'><" + clr + ">" + textt + "</font><br>"
                        HTM = HTM + texxt

                    if max(p)>m1:
                        m1 = max(p)

                    p = df_result[nag+' - '+self.cols[i]+' Давление'].tolist()
                    while True:
                        try:
                            p.remove('')
                        except:
                            break

                    if len(p)>0:
                        HTM = HTM + "<font color='blue' size='5'><red>Забойное давление</font><br>"
                        for j in range(len(p)):
                            if p[j] > 0.4:
                                clr = 'green'
                            else:
                                clr = 'red'
                            textt = 'Лаг ' + str(j+v) + ' мес.  ->  Rs = ' + str(round(p[j], 2))
                            texxt = "<font color='" + clr + "' size='4'><" + clr + ">" + textt + "</font><br>"
                            HTM = HTM + texxt

                        if max(p)>m1:
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

            self.textRezult.setHtml(HTM)

            self.drawSpearmanLines()

        #except Exception as e:  # Запись  ошибок в лог
          #  logging.error(str(datetime.now()) + '   ' + str(e)+'   doSpearCalc')


    def drawSpearmanLines___(self):

        if  len( self.L_arrs)>0:
            for i in self.L_arrs:
                i.remove()
            self.L_arrs = []

        E = -1

        for i in range(len(self.cols)):

            if self.checkedRanges[i] >0:
                E = E+1
                c = self.lineCollor[E]
                x1 = first_window.currentNagCoord[0]
                y1 = first_window.currentNagCoord[1]
                #x2 = first_window.currentNefCoords[i*2]
                #y2  = first_window.currentNefCoords[i*2+1]
                x2 = first_window.nefCoords[i*2]
                y2 = first_window.nefCoords[i*2+1]

                x11 = (x1 + 0.9 * x2) / (1 + 0.9)
                y11 = (y1 + 0.9 * y2) / (1 + 0.9)
                x22 = (x2 + 0.1 * x1) / (1 + 0.1)
                y22 = (y2 + 0.1 * y1) / (1 + 0.1)
                '''grX.append(first_window.currentNagCoord[0])
                grX.append(first_window.currentNefCoords[i*2])
                grY.append(first_window.currentNagCoord[1])
                grY.append(first_window.currentNefCoords[i*2+1])'''
                arrowprops=dict(arrowstyle='->', color=c, linewidth=2, mutation_scale=10)

                # !!! Добавление аннотации
                arr = first_window.Gr_map.canvas.axes.annotate('',
                             xy=(x22, y22),
                             xytext=(x11, y11),
                             arrowprops=arrowprops)
                self.L_arrs.append(arr)

                #first_window.Gr_map.canvas.axes.arrow(x1, x2, y1, y2, width = 10,  color=c)
                #first_window.Gr_map.canvas.axes.plot(grX,grY, color=c)
                first_window.Gr_map.canvas.draw()


    def doWinSpear(self, ListOfNag, ListOfListOfNef, wels_len, fnv, kp):

        if first_window.formFK[0] != self.currFormForSpir or ListOfListOfNef != self.lolof:
            self.currFormForSpir = first_window.formFK[0]
            self.lolof = ListOfListOfNef

            self.ListOfSpirmanObj = []

            # Сосзание списка с объектами класса СПИРМАН
            try:

                if len(ListOfNag)>0:

                    for k in ListOfListOfNef:
                        if len(k)>0:
                            self.show()            # Открыть окно Спирман
                            break

                    #now = datetime.now()

                    form0 = ''
                    for i in range(len(ListOfNag)):
                        form1 = mat.getFormName(ListOfNag[i])
                        well1 = ListOfNag[i]

                        if form1!=form0:
                            form0 = form1
                            sql.doTableAllDates(form1)

                        for j in range(len(ListOfListOfNef[i])):

                            form2 = mat.getFormName(ListOfListOfNef[i][j])
                            well2 = ListOfListOfNef[i][j]
                            df = sql.getDataSpearwell(form1, form2, well1, well2)
                            a = spearwell(ListOfNag[i], ListOfListOfNef[i][j], df, i,j)
                            a.lenWell = wels_len[i][j]
                            a.FNV = fnv[i]
                            a.KP = kp[i][j]
                            self.ListOfSpirmanObj.append(a)

                    #print(datetime.now() - now)


                     # Создание интерфейса

                    self.listWidget.clear()
                    self.listWidget2.clear()

                    for i in range(len(ListOfNag)):
                        a = mat.getSkvNfromText(ListOfNag[i])
                        item = QListWidgetItem(a)
                        self.listWidget.addItem(item)

                    self.comboDat1.clear()
                    self.comboDat2.clear()
                    for i in self.ListOfSpirmanObj[0].source_df['D'].tolist():
                        self.comboDat1.addItem(str(i)[:7])
                        self.comboDat2.addItem(str(i)[:7])

                    self.listWidgetClick()
                    self.listWidget2Click()
                    self.listWidget2Click()



            except Exception as e:  # Запись  ошибок в лог
                logging.error(str(datetime.now()) + '   ' + str(e) + '   doWinSpear')
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Нет данных")

        else:

            self.show()


    # NEW
    def changePositionAxes(self):

        self.Gr_spir_P.spines['right'].set_position(('axes', 5))
        self.Gr_spir_T.spines['right'].set_position(('axes', 5))
        self.Gr_spir_W.spines['right'].set_position(('axes', 5))
        self.Gr_spir_S.spines['right'].set_position(('axes', 5))
        T = False
        W = False
        S = False
        a = 1.05
        if self.Gr_Pzab.get_visible():
            self.Gr_spir_P.spines['right'].set_position(('axes', a))
            a = 1.1
        else:
            if self.Gr_zakTime.get_visible() or self.Gr_debTime.get_visible():
                self.Gr_spir_T.spines['right'].set_position(('axes', a))
                a = 1.1
                T = True
            else:
                if self.Gr_water.get_visible():
                    self.Gr_spir_W.spines['right'].set_position(('axes', a))
                    a = 1.1
                    W = True
                else:
                    if self.Gr_sint.get_visible():
                        self.Gr_spir_S.spines['right'].set_position(('axes', a))
                        S = True

        if (self.Gr_zakTime.get_visible() or self.Gr_debTime.get_visible()) and T == False:
            self.Gr_spir_T.spines['right'].set_position(('axes', a))
            a = 1.15
        else:
            if self.Gr_water.get_visible() and W == False:
                self.Gr_spir_W.spines['right'].set_position(('axes', a))
                a = 1.15
                W = True
            else:
                if self.Gr_sint.get_visible() and S == False:
                    self.Gr_spir_S.spines['right'].set_position(('axes', a))
                    S = True

        if self.Gr_water.get_visible() and W == False:
            self.Gr_spir_W.spines['right'].set_position(('axes', a))
            a = 1.2
        else:
            if self.Gr_sint.get_visible() and S == False:
                self.Gr_spir_S.spines['right'].set_position(('axes', a))
                a = 1.2
                S = True
        if self.Gr_sint.get_visible() and S == False:
            self.Gr_spir_S.spines['right'].set_position(('axes', a))

    # NEW
    def changeGr_spir(self):


        if self.sender().objectName() == 'checkBox_priem':
            self.Gr_priem.set_visible(not self.Gr_priem.get_visible())
            self.Gr_priem2.set_visible(not self.Gr_priem2.get_visible())
        if self.sender().objectName() == 'checkBox_debLiq':
            self.Gr_debLiq.set_visible(not self.Gr_debLiq.get_visible())
        if self.sender().objectName() == 'checkBox_debOil':
            self.Gr_debOil.set_visible(not self.Gr_debOil.get_visible())
        if self.sender().objectName() == 'checkBox_Pzab':
            self.Gr_Pzab.set_visible(not self.Gr_Pzab.get_visible())

        if self.sender().objectName() == 'checkBox_zakTime':
            self.Gr_zakTime.set_visible(not self.Gr_zakTime.get_visible())
        if self.sender().objectName() == 'checkBox_debTime':
            self.Gr_debTime.set_visible(not self.Gr_debTime.get_visible())
        if self.sender().objectName() == 'checkBox_water':
            self.Gr_water.set_visible(not self.Gr_water.get_visible())
        if self.sender().objectName() == 'checkBox_sint':
            self.Gr_sint.set_visible(not self.Gr_sint.get_visible())

        '''if self.sender().objectName() == 'checkBox_event':
            self.Gr_grpnag.set_visible(not self.Gr_grpnag.get_visible())
            self.Gr_optnag.set_visible(not self.Gr_optnag.get_visible())
            self.Gr_opznag.set_visible(not self.Gr_opznag.get_visible())
            self.Gr_pvlgnag.set_visible(not self.Gr_pvlgnag.get_visible())
            self.Gr_grpnef.set_visible(not self.Gr_grpnef.get_visible())
            self.Gr_optnef.set_visible(not self.Gr_optnef.get_visible())
            self.Gr_opznef.set_visible(not self.Gr_opznef.get_visible())
            self.Gr_pvlgnef.set_visible(not self.Gr_pvlgnef.get_visible())'''

        if self.sender().objectName() == 'checkBox_event':
            self.doGrEVT()

        if self.checkBox_legend.isChecked():

            y = -0.13
        else:

            y = -10

        c = 'azure'
        f = 1

        self.Gr_spir.canvas.axes.legend(('Приемистость', ''), loc=(0,y), shadow=True, framealpha=f, facecolor=c,
                                        edgecolor='black')
        self.Gr_spir_L_O.legend(('Жидкость', 'Нефть'), loc=(0.12, y), framealpha=f, facecolor=c, edgecolor='black')
        self.Gr_spir_T.legend(('Время работы наг.', 'Время работы доб.'), loc=(0.22, y), framealpha=f, facecolor=c,
                              edgecolor='black')
        self.Gr_spir_P.legend(('Давление', ''), loc=(0.36, y), framealpha=f, facecolor=c, edgecolor='black')
        self.Gr_spir_W.legend(('Обводненность', ''), loc=(0.46, y), framealpha=f, facecolor=c, edgecolor='black')
        self.Gr_spir_S.legend(('Синтетика', ''), loc=(0.59, y), framealpha=f, facecolor=c, edgecolor='black')

        self.changePositionAxes()

        self.Gr_spir.canvas.draw()


    def doSpearText(self):

        self.fillTable()


        self.label_period.setText('Выбранный период:  ' + str(self.ListOfSpirmanObj[self.N].range_all) + ' мес.' +
                                  ' ( +'+str(self.ListOfSpirmanObj[self.N].spaces)+' мес. искл.)     '+
                                  'Начало периода: ' )


    def upd(self, val):
        self.Gr_spir_L_O.set_ylim(top=self.slid.val, bottom=0)
        # fig.canvas.draw_idle()
        # --слайдер---------------------------------------------------------


    def doGrGpear(self):

        self.Gr_spir.F.clear()
        self.Gr_spir.reCreate()
        self.Gr_spir.F.subplots_adjust(left=0.07, right=0.82, top=0.94, bottom=0.12)
        self.Gr_spir_L_O = self.Gr_spir.canvas.axes.twinx()
        self.Gr_spir_P = self.Gr_spir.canvas.axes.twinx()
        self.Gr_spir_T = self.Gr_spir.canvas.axes.twinx()
        self.Gr_spir_W = self.Gr_spir.canvas.axes.twinx()
        self.Gr_spir_S = self.Gr_spir.canvas.axes.twinx()
        self.Gr_spir_Ev = self.Gr_spir.canvas.axes.twinx()
        self.Gr_spir_line = self.Gr_spir.canvas.axes.twinx()
        self.Gr_spir_line2 = self.Gr_spir.canvas.axes.twinx()
        self.Gr_spir.canvas.axes.margins(0.02)
        self.Gr_spir_line.yaxis.set_visible(False)
        self.Gr_spir_line2.yaxis.set_visible(False)


        self.changeColor(self.ListOfSpirmanObj[self.N].right_range)

        #  Цвета    прием               жид       нефть   давл        закВремя   добВремя   обв         синт
        color = ['cornflowerblue', '#0070C0', '#745F2A', '#C00000',  'black',   'grey',   '#00CCFF', '#ED3CCA' ]


        self.Gr_spir.canvas.axes.tick_params(axis='y', colors=color[4])

        self.Gr_spir.canvas.axes.set_title(
            'Эксплуатационные показатели' + '  скважины ' + self.listWidget.currentItem().text() + ' и скважины ' + self.listWidget2.currentItem().text(), fontsize=10)

        self.Gr_priem, = self.Gr_spir.canvas.axes.plot(self.ListOfSpirmanObj[self.N].source_df['D'],self.ListOfSpirmanObj[self.N].source_df['priem'], color=color[0])
        self.Gr_priem2 = self.Gr_spir.canvas.axes.fill_between(self.ListOfSpirmanObj[self.N].source_df['D'],self.ListOfSpirmanObj[self.N].source_df['priem'], color=color[0])

        self.Gr_debLiq, = self.Gr_spir_L_O.plot(self.ListOfSpirmanObj[self.N].source_df['D'], self.ListOfSpirmanObj[self.N].source_df['debLiq'], '-', color=color[1])

        self.Gr_debOil, = self.Gr_spir_L_O.plot(self.ListOfSpirmanObj[self.N].source_df['D'], self.ListOfSpirmanObj[self.N].source_df['debOil'], '-', markersize=6,
                                      color=color[2])
        self.Gr_Pzab, = self.Gr_spir_P.plot(self.ListOfSpirmanObj[self.N].source_df['D'], self.ListOfSpirmanObj[self.N].source_df['Pzab'], '-', markersize=4,
                                      color=color[3])

        self.Gr_zakTime, = self.Gr_spir_T.plot(self.ListOfSpirmanObj[self.N].source_df['D'], self.ListOfSpirmanObj[self.N].source_df['zakTime'], 'x', markersize=3,
                                      color=color[4])
        self.Gr_debTime, = self.Gr_spir_T.plot(self.ListOfSpirmanObj[self.N].source_df['D'], self.ListOfSpirmanObj[self.N].source_df['debTime'], 'o', markersize=2,
                                      color=color[5])

        self.Gr_water, = self.Gr_spir_W.plot(self.ListOfSpirmanObj[self.N].source_df['D'], self.ListOfSpirmanObj[self.N].source_df['water'], '-', lw=2,
                                                         color=color[6])
        self.Gr_sint, = self.Gr_spir_S.plot(self.ListOfSpirmanObj[self.N].source_df['D'], self.ListOfSpirmanObj[self.N].source_df['synth'], '-', lw=2,
                                                       color=color[7])


        self.Gr_priem.set_visible(self.checkBox_priem.isChecked())
        self.Gr_priem2.set_visible(self.checkBox_priem.isChecked())
        self.Gr_debLiq.set_visible(self.checkBox_debLiq.isChecked())
        self.Gr_debOil.set_visible(self.checkBox_debOil.isChecked())
        self.Gr_Pzab.set_visible(self.checkBox_Pzab.isChecked())

        self.Gr_zakTime.set_visible(self.checkBox_zakTime.isChecked())
        self.Gr_debTime.set_visible(self.checkBox_debTime.isChecked())
        self.Gr_water.set_visible(self.checkBox_water.isChecked())
        self.Gr_sint.set_visible(self.checkBox_sint.isChecked())


        # Слайдер для изменения предела оси У дебета------------------------------
        y = self.Gr_spir_L_O.get_ylim()[1]
        try:
            self.ax.remove()
        except:
            pass
        self.ax = self.Gr_spir.F.add_axes([0.815, 0.116, 0.01, 0.825])

        self.slid = Slider(
            ax=self.ax,
            label="",
            valmin=0,
            valmax=y,
            valinit=y,
            orientation="vertical")

        self.slid.on_changed(self.upd)
       #------------------------------------------------------------------------


        if self.checkBox_legend.isChecked():

            c = 'azure'
            f = 1
            y = -0.13

            self.Gr_spir.canvas.axes.legend(('Приемистость', ''), loc=(0, y), shadow=True, framealpha=f, facecolor=c,
                                            edgecolor='black')
            self.Gr_spir_L_O.legend(('Жидкость', 'Нефть'), loc=(0.12, y), framealpha=f, facecolor=c, edgecolor='black')
            self.Gr_spir_T.legend(('Время работы наг.', 'Время работы доб.'), loc=(0.22, y), framealpha=f, facecolor=c,
                                  edgecolor='black')
            self.Gr_spir_P.legend(('Давление', ''), loc=(0.36, y), framealpha=f, facecolor=c, edgecolor='black')
            self.Gr_spir_W.legend(('Обводненность', ''), loc=(0.46, y), framealpha=f, facecolor=c, edgecolor='black')
            self.Gr_spir_S.legend(('Синтетика', ''), loc=(0.59, y), framealpha=f, facecolor=c, edgecolor='black')

        self.Gr_spir.canvas.axes.tick_params(axis='y', colors=color[0])
        self.Gr_spir_L_O.tick_params(axis='y', colors=color[1])
        self.Gr_spir_P.tick_params(axis='y', colors=color[3])
        self.Gr_spir_T.tick_params(axis='y', colors=color[4])
        self.Gr_spir_W.tick_params(axis='y', colors=color[6])
        self.Gr_spir_S.tick_params(axis='y', colors=color[7])

        self.Gr_spir.canvas.axes.set_ylabel("Приемистость, м3/сут", color=color[0])
        self.Gr_spir_L_O.set_ylabel("Дебит (жидкость, нефть), т/сут", color=color[1])
        self.Gr_spir_P.set_ylabel("Заб. давление, атм", color=color[3])
        self.Gr_spir_T.set_ylabel("Время работы, часы", color=color[4])
        self.Gr_spir_W.set_ylabel("Обводненность, %", color=color[6])
        self.Gr_spir_S.set_ylabel("Синтетика", color=color[7])

        self.Gr_spir.canvas.draw()


        self.doGrEVT()


        self.changePositionAxes()

        self.Gr_spir.canvas.axes.grid()
        self.Gr_spir.canvas.draw()

        self.grVertLines(self.ListOfSpirmanObj[self.N].range_start_D, self.ListOfSpirmanObj[self.N].range_fin_D)



    def doGrEVT(self):  # events

        self.Gr_spir_Ev.set_yticklabels([])
        self.Gr_spir_Ev.set_ylim([0, 500])
        self.Gr_spir_Ev.tick_params(axis='y', colors='white')

        if self.checkBox_event.isChecked():


            d = self.ListOfSpirmanObj[self.N].source_df['D'].tolist()
            g1 = self.ListOfSpirmanObj[self.N].source_df['nagEVT'].tolist()
            g2 = self.ListOfSpirmanObj[self.N].source_df['nefEVT'].tolist()

            Y = 40

            for i in range(len(d)):

                if g1[i] != 0:

                    if Y == 40:
                        Y = 25
                    else:
                        Y = 40

                    self.Gr_spir_Ev.text(d[i], Y, mat.gtm_names(g1[i]), fontsize=6,
                                          color='aqua', weight='bold', bbox={"facecolor": "black",
                                                                               "boxstyle": "round",
                                                                               "edgecolor": "black",
                                                                               "alpha": 0.9})
                    Y2 = [0, Y]
                    d2 = [d[i], d[i]]
                    self.Gr_spir_Ev.plot(d2, Y2, color='black', linewidth=1)

                if g2[i] != 0:

                    if Y == 40:
                        Y = 25
                    else:
                        Y = 40

                    self.Gr_spir_Ev.text(d[i], Y, mat.gtm_names(g2[i]), fontsize=6,
                                          color='darkorange', weight='bold', bbox={"facecolor": "black",
                                                                               "boxstyle": "round",
                                                                               "edgecolor": "black",
                                                                               "alpha": 0.9})
                    Y2 = [0, Y]
                    d2 = [d[i], d[i]]
                    self.Gr_spir_Ev.plot(d2, Y2, color='black', linewidth=1)

        else:
            self.Gr_spir_Ev.clear()

            d = self.ListOfSpirmanObj[self.N].source_df['D'].tolist()
            self.Gr_spir_Ev.text(d[0], 0, '', fontsize=1)
            self.Gr_spir_Ev.plot(d[0], 0, color='black', linewidth=1)


class BD(QtWidgets.QDialog):
    def __init__(self):
        super(BD, self).__init__()
        loadUi("bd.ui", self)
        logging.basicConfig(filename="BDlog.txt", level=logging.INFO)

        validator = QtGui.QRegExpValidator(QRegExp("([-]{0,1})([0-9]{0,9})([.]{0,1}[0-9]{0,100})"))
        self.Edit_Bw.setValidator(validator)
        self.Edit_mu.setValidator(validator)
        self.Edit_kw.setValidator(validator)
        self.Edit_m.setValidator(validator)
        self.Edit_Bo.setValidator(validator)
        self.Edit_So.setValidator(validator)
        self.Edit_So_min.setValidator(validator)
        self.Edit_Ro.setValidator(validator)

        self.Edit_Bw.textChanged.connect(self.on_edit_formParam)
        self.Edit_mu.textChanged.connect(self.on_edit_formParam)
        self.Edit_kw.textChanged.connect(self.on_edit_formParam)
        self.Edit_m.textChanged.connect(self.on_edit_formParam)
        self.Edit_Bo.textChanged.connect(self.on_edit_formParam)
        self.Edit_Ro.textChanged.connect(self.on_edit_formParam)
        self.Edit_So.textChanged.connect(self.on_edit_formParam)
        self.Edit_So_min.textChanged.connect(self.on_edit_formParam)
        self.Edit_P.textChanged.connect(self.on_edit_formParam)


        '''path = 'res\w.gif'
        self.gif = QtGui.QMovie(path)  # !!!
        self.label.setMovie(self.gif)'''

        #self.But_Set.setEnabled(False)
        #self.But_Set_average.setEnabled(False)

        self.But_to_BD.setEnabled(True)

        #self.But_Set.clicked.connect(self.clickBtnSet)
        self.But_Set_average.clicked.connect(self.clickBtnAverage)
        self.But_Set_all_average.clicked.connect(self.clickBtnAverage)
        self.But_to_BD.clicked.connect(self.addPlastToBD)

        self.But_Set_Pstart.clicked.connect(self.addPlastStart)


        self.tableBDskv.setRowCount(50)
        self.But_load_excel.clicked.connect(self.fromExlForDB)

        self.tableBDskv.horizontalHeader().setFixedHeight(25)
        self.tableBDskv.horizontalHeader().setStyleSheet("QHeaderView::section{font-weight:bold}")
        self.tableBDskv.setHorizontalHeaderLabels(
            ['Скважина', 'Раб.', 'Заб. Х', 'Заб. Y', 'X', 'Y', 'H', 'Rw',''])
        self.tableBDskv.horizontalHeaderItem(1).setToolTip("Характер работы")
        self.tableBDskv.horizontalHeaderItem(2).setToolTip("Координаты забоя")
        self.tableBDskv.horizontalHeaderItem(3).setToolTip("Координаты забоя")
        self.tableBDskv.horizontalHeaderItem(4).setToolTip("Координаты")
        self.tableBDskv.horizontalHeaderItem(5).setToolTip("Координаты")
        self.tableBDskv.horizontalHeaderItem(6).setToolTip("Нефтенасыщенная толщина, м")
        self.tableBDskv.horizontalHeaderItem(7).setToolTip("Радиус скважины, м")
        self.tableBDskv.horizontalHeaderItem(8).setToolTip("Отмеченные скважины будут записаны в БД")
        self.tableBDskv.setColumnWidth(0, 80)
        self.tableBDskv.setColumnWidth(1, 60)
        self.tableBDskv.setColumnWidth(6, 60)
        self.tableBDskv.setColumnWidth(7, 60)
        self.tableBDskv.setColumnWidth(2, 80)
        self.tableBDskv.setColumnWidth(3, 80)
        self.tableBDskv.setColumnWidth(4, 80)
        self.tableBDskv.setColumnWidth(5, 80)
        self.tableBDskv.setColumnWidth(8, 30)

        #self.tableBDskv.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        #self.tableBDparam.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.VL_tool.addWidget(self.Gr_bd1.toolbar)

        self.tableBDskv.cellChanged.connect(self.on_change_tableBDskv)
        self.tableBDskv.itemSelectionChanged.connect(self.on_selectSkv)
        self.tableBDskv.itemDoubleClicked.connect(self.on_double_click)

        self.tableBDparam.itemDoubleClicked.connect(self.on_double_click)
        self.tableBDparam.cellChanged.connect(self.on_change_table_param)
        self.tableBDparam.cellClicked.connect(self.on_clickTableParamCell)
        self.tableBDparam.horizontalHeader().sectionClicked.connect(self.on_clickTableParam)
        self.tableBDparam.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableBDskv.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableBDparam.customContextMenuRequested.connect(self.conMenuParam)
        self.tableBDskv.customContextMenuRequested.connect(self.conMenuSkv)

        self.clrNo = '#f58258'
        self.clrYes = 'azure'
        self.clrAutoComplete = 'yellow'


        self.dataErrorPar = False
        self.dataErrorForm= False
        self.dataErrorSkv= False

        self.currText = ['','','']

        self.currPlastInTable = ''
        self.currSkvInTable = ''

        self.currPstart = -2

        self.tableBDskv.setToolTip(mat.HTM2)

        #self.tableBDparam.itemSelectionChanged.connect(self.on_selectParam)


        self.a = 9999

        self.errLoad = False
        self.currWell = -1
        self.ListOfDataObj = []
        self.clr = ['lavender', 'red', 'orange', 'dodgerblue','black']



        self.Gr_bd1.F.patch.set_facecolor('lightgray')
        self.Gr_bd1.F.subplots_adjust(top=0.9)

        self.enableLoad()


    def conMenuParam(self, position):
        if self.ListOfDataObj[self.currWell].isRec:
            menu = QtWidgets.QMenu()
            a = QtWidgets.QAction('Обнулить выделенные значения', menu)
            menu.addAction(a)
            a.triggered.connect(self.setZero)
            menu.exec_(self.tableBDparam.viewport().mapToGlobal(position))

    def conMenuSkv(self, position):
        menu = QtWidgets.QMenu()
        a = QtWidgets.QAction('Исключить скважины с неполными данными', menu)
        menu.addAction(a)
        a.triggered.connect(self.excludeWells)
        menu.exec_(self.tableBDskv.viewport().mapToGlobal(position))


    def setZero(self):
        if self.currWell != -1:

            for index in self.tableBDparam.selectedIndexes():
               # item = QTableWidgetItem()
               # item.setText(str(0))
                #self.tableBDparam.setItem(index.row(), index.column(), item)
                self.change_table_param(index.row(), index.column(), 0)

            self.on_change_table_param(-2,-2)


    def excludeWells(self):
        for itm in self.ListOfDataObj:
            if itm.err:
                itm.isRec = False
                #A1.setChecked(False)
                #CH.setObjectName('A' + str(i))
                #CH.setChecked(True)
                itm.checkAll()
        self.doWellTable()
        #self.afterChangeTableParam()
        #self.checkButToBD()



    def addPlastStart(self):

        a = self.currWell

        if self.checkBox_all_Pstart.isChecked():

            for i in range(len(self.ListOfDataObj)):
                self.ListOfDataObj[i].currPstart = self.Edit_P.text()
                self.ListOfDataObj[i].addDataPplast()

        else:

            self.ListOfDataObj[a].currPstart = self.Edit_P.text()
            self.ListOfDataObj[a].addDataPplast()

        if self.ListOfDataObj[a].typ == 'НАГ':
            self.doTableNAG(a, self.clr, True)
        else:
            self.doTableNEF(a, self.clr, True)



    def enableLoad(self):
        self.But_load_excel.setEnabled(not self.errLoad)



    def on_edit_formParam(self):

        obj = self.sender()
        self.errLoad = False

        style_fail = '''background-color: rgb(255, 64, 64)'''
        style_good = '''background-color: rgb(252, 253, 255)'''

        if mat.isZero(obj.text()):
            obj.setStyleSheet(style_fail)
            self.errLoad = True
        else:
            obj.setStyleSheet(style_good)

        if obj.objectName() == 'Edit_So' or obj.objectName() == 'Edit_So_min':
            if mat.toFloat2(self.Edit_So.text(), self.Edit_So_min.text())<=0:
                self.Edit_So.setStyleSheet(style_fail)
                self.Edit_So_min.setStyleSheet(style_fail)
                self.errLoad = True
            else:
                self.Edit_So.setStyleSheet(style_good)
                self.Edit_So_min.setStyleSheet(style_good)

        self.enableLoad()
        self.checkButToBD()



    def on_double_click(self):
        self.wasChange = True

    def empty(self):
        pass



    #  ЗАПИСЬ В БАЗУ ПЛАСТА
    def addPlastToBD(self):

        self.plast_db.Bw = self.Edit_Bw.text()
        self.plast_db.mu = self.Edit_mu.text()
        self.plast_db.kw = self.Edit_kw.text()
        self.plast_db.m = self.Edit_m.text()
        self.plast_db.Bo = self.Edit_Bo.text()
        self.plast_db.So = self.Edit_So.text()
        self.plast_db.So_min = self.Edit_So_min.text()
        self.plast_db.Ro = self.Edit_Ro.text()
        self.plast_db.P = self.Edit_P.text()

        self.plast_db.tupleForBD()

        form_tuple = self.plast_db.form_tuple

        skv_list_tuple = []
        for itm in self.ListOfDataObj:
            if itm.isRec:
                l = []
                l.append(itm.wellName + '|' + itm.typ + '|' + self.plast_db.p1)
                l.append(itm.wellName)
                l.append(itm.typ)
                l.append(itm.XX)
                l.append(itm.YY)
                l.append(itm.X)
                l.append(itm.Y)
                l.append(itm.H)
                l.append(itm.Re)
                l.append(self.plast_db.p1)  # внешний ключ - пласт
                # rec_list.append(self.tableBDskv.item(i, j).text())
                t = tuple(l)
                skv_list_tuple.append(t)

        param_list_tuple = []
        for itm in self.ListOfDataObj:
            if itm.isRec:
                b = itm.wellName + '|' + itm.typ + '|' + self.plast_db.p1

                for j in range(len(itm.L_dat)):
                    l = []
                    l.append(str(itm.L_dat[j]))
                    l.append(b)
                    l.append(itm.L_debLiq[j])
                    l.append(itm.L_debOil[j])
                    l.append(itm.L_debLiqTR[j])
                    l.append(itm.L_debOilTR[j])
                    l.append(itm.L_inject[j])
                    l.append(itm.L_water[j])
                    l.append(itm.L_waterTR[j])
                    l.append(itm.L_dynLevel[j])
                    l.append(itm.L_debTime[j])
                    l.append(itm.L_zakTime[j])
                    l.append(itm.L_Pzab[j])
                    l.append(itm.L_Pplast[j])
                    l.append(itm.L_priem[j])
                    l.append(itm.L_PriemTR[j])
                    l.append(itm.L_Diam[j])

                    t = tuple(l)
                    param_list_tuple.append(t)

        try:
            sql.insPlastBD(form_tuple, skv_list_tuple, param_list_tuple)
            try:
                first_window.unCheckAll()
                first_window.tree_wells.clear()
                first_window.tree_wells.itemChanged[QTreeWidgetItem, int].disconnect(first_window.get_item)
                first_window.all_tree_parent_checked = []
                first_window.addTree(first_window.tree_wells, sql.getALLfromBD())
                first_window.tree_wells.itemChanged[QTreeWidgetItem, int].connect(first_window.get_item)
            except:
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Дерево скважин не может быть построено")
            QtWidgets.QMessageBox.information(self, "OK", "Данные по пласту, скважинах и их истории записаны")

        except Exception as e:  # Запись  ошибок в лог
            logging.error(str(datetime.now()) + '   ' + str(e) + '   insPlastBD')
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Данные не записаны")


    def refreshTable(self,L,x):

        self.tableBDparam.blockSignals(True)
        self.tableBDparam.model().blockSignals(True)
        try:
            self.tableBDparam.cellChanged.disconnect(self.on_change_table_param)
        except:
            pass
        for i in range(len(L)):
            self.tableBDparam.item(i,x).setText(str(L[i]))
        self.tableBDparam.blockSignals(False)
        self.tableBDparam.model().blockSignals(False)
        self.tableBDparam.cellChanged.connect(self.on_change_table_param)


    def  clickBtnAverage(self):

        def setAuto(L,w):
            for i in range(len(w)):
                L[w[i]] = 2

        def setAVG(a, j):

            was_chg = False

            if self.ListOfDataObj[a].typ == 'НАГ':

                if j == 1:
                    self.ListOfDataObj[a].L_inject, W, was_chg = mat.averageForParam(self.ListOfDataObj[a].L_inject, False)
                    if len(W)>0:
                        setAuto(self.ListOfDataObj[a].L_inject_check, W)
                if j == 2:
                    self.ListOfDataObj[a].L_Pzab, W, was_chg = mat.averageForParam(self.ListOfDataObj[a].L_Pzab, True)
                    if len(W)>0:
                        setAuto(self.ListOfDataObj[a].L_Pzab_check, W)
                if j == 3:
                    self.ListOfDataObj[a].L_Pplast, W, was_chg = mat.averageForParam(self.ListOfDataObj[a].L_Pplast, True)
                    if len(W)>0:
                        setAuto(self.ListOfDataObj[a].L_Pplast_check, W)
                if j == 4:
                    self.ListOfDataObj[a].L_priem, W, was_chg = mat.averageForParam(self.ListOfDataObj[a].L_priem, True)
                    if len(W)>0:
                        setAuto(self.ListOfDataObj[a].L_priem_check, W)
                if j == 5:
                    self.ListOfDataObj[a].L_PriemTR, W, was_chg = mat.averageForParam(self.ListOfDataObj[a].L_PriemTR, False)
                    if len(W)>0:
                        setAuto(self.ListOfDataObj[a].L_PriemTR_check, W)
                if j == 6:
                    self.ListOfDataObj[a].L_Diam, W, was_chg = mat.averageForParam(self.ListOfDataObj[a].L_Diam, True)
                    if len(W)>0:
                        setAuto(self.ListOfDataObj[a].L_Diam_check, W)

            else:

                if j == 1:
                    self.ListOfDataObj[a].L_Pzab, W, was_chg = mat.averageForParam(self.ListOfDataObj[a].L_Pzab, True)
                    if len(W)>0:
                        setAuto(self.ListOfDataObj[a].L_Pzab_check, W)
                if j == 2:
                    self.ListOfDataObj[a].L_Pplast, W, was_chg = mat.averageForParam(self.ListOfDataObj[a].L_Pplast, True)
                    if len(W)>0:
                        setAuto(self.ListOfDataObj[a].L_Pplast_check, W)
                if j == 3:
                    self.ListOfDataObj[a].L_debLiq, W, was_chg = mat.averageForParam(self.ListOfDataObj[a].L_debLiq, False)
                    if len(W)>0:
                        setAuto(self.ListOfDataObj[a].L_debLiq_check, W)
                if j == 4:
                    self.ListOfDataObj[a].L_debLiqTR, W, was_chg = mat.averageForParam(self.ListOfDataObj[a].L_debLiqTR, False)
                    if len(W)>0:
                        setAuto(self.ListOfDataObj[a].L_debLiqTR_check, W)
                if j == 5:
                    self.ListOfDataObj[a].L_debOil, W, was_chg = mat.averageForParam(self.ListOfDataObj[a].L_debOil, False)
                    if len(W)>0:
                        setAuto(self.ListOfDataObj[a].L_debOil_check, W)
                if j == 6:
                    self.ListOfDataObj[a].L_debOilTR, W, was_chg = mat.averageForParam(self.ListOfDataObj[a].L_debOilTR, False)
                    if len(W)>0:
                        setAuto(self.ListOfDataObj[a].L_debOilTR_check, W)
                if j == 7:
                    self.ListOfDataObj[a].L_water, W, was_chg = mat.averageForParam(self.ListOfDataObj[a].L_water, False)
                    if len(W)>0:
                        setAuto(self.ListOfDataObj[a].L_water_check, W)
                if j == 8:
                    self.ListOfDataObj[a].L_waterTR, W, was_chg = mat.averageForParam(self.ListOfDataObj[a].L_waterTR, False)
                    if len(W)>0:
                        setAuto(self.ListOfDataObj[a].L_waterTR_check, W)
                if j == 9:
                    self.ListOfDataObj[a].L_dynLevel, W, was_chg = mat.averageForParam(self.ListOfDataObj[a].L_dynLevel, True)
                    if len(W)>0:
                        setAuto(self.ListOfDataObj[a].L_dynLevel_check, W)

            if  was_chg:
                self.ListOfDataObj[a].checkAll()

        a = self.currWell
        j = self.tableBDparam.currentColumn()

        if self.sender().objectName() == 'But_Set_average':
            setAVG(a,j)
        else:

            if self.checkBox_all_avr.isChecked():

                for x in range(len(self.ListOfDataObj)):
                    if self.ListOfDataObj[x].typ == 'НАГ':
                        t = 7
                    else:
                        t = 10
                    for i in range(1, t):
                        setAVG(x, i)

            else:

                if self.ListOfDataObj[a].typ == 'НАГ':
                    t = 7
                else:
                    t = 10
                for i in range(1,t):
                    setAVG(a, i)

        self.checkButToBD()

        if self.ListOfDataObj[a].typ == 'НАГ':
            self.doTableNAG(a, self.clr, True)
        else:
            self.doTableNEF(a, self.clr, True)


    def on_clickTableParamCell(self, i,j):
        #self.tableBDparam.item(i, j).setBackground(QtGui.QColor('blue'))
        self.on_clickTableParam(j)


    def checkTableForm(self):
        self.dataErrorForm = False

    #  Проверка всех параметров всех скважин с отметкой некорректных в таблице скважин
    def checkAllParam(self):

        clr1 = 'red'
        clr2 = 'black'
        self.dataErrorPar = False
        for i in range(len(self.Lskv[0])):
            for n in range(0,8):
                self.tableBDskv.item(i, n).setForeground(QtGui.QBrush(QtGui.QColor(clr2)))
            typeSkv = self.Lskv[1][i]
            if typeSkv == 'НАГ':
                for j in range(len(self.L_inject[i])):
                    if mat.isFloat(self.L_inject[i][j]) or mat.isFloat(self.L_priem[i][j]) or mat.isFloat(
                            self.L_Diam[i][j]):
                        for n in range(0, 8):
                            self.tableBDskv.item(i, n).setForeground(QtGui.QBrush(QtGui.QColor(clr1)))
                            self.dataErrorPar = True
                        break

            if typeSkv == 'НЕФ':
                for j in range(len(self.L_debLiq[i])):
                    if mat.isFloat(self.L_debLiq[i][j]) or mat.isFloat(self.L_debOil[i][j]) or \
                            mat.isFloat(self.L_water[i][j]) or mat.isFloat(self.L_dynLevel[i][j]):
                        for n in range(0, 8):
                            self.tableBDskv.item(i, n).setForeground(QtGui.QBrush(QtGui.QColor(clr1)))
                            self.dataErrorPar = True
                        break

            for j in range(len(self.L_Pzab[i])):
                if mat.isFloat(self.L_Pzab[i][j]) or mat.isFloat(self.L_Pplast[i][j]) or mat.isZero(self.L_Pzab[i][j]) \
                        or mat.isZero(self.L_Pplast[i][j]):
                    for n in range(0, 8):
                        self.tableBDskv.item(i, n).setForeground(QtGui.QBrush(QtGui.QColor(clr1)))
                        self.dataErrorPar = True
                    break

        self.checkButToBD()


    # ПОЛУЧЕНИЕ ДАННЫХ ПО СКВАЖИНЕ ДЛЯ РЕДАКТИРОВАНИЯ ------------------------------------------------------------------

    def  wellToEdit(self, wellID):

        bo, ro, m, so, so_min, bw, kw, mu, pn = sql.getFormFromBD(mat.getFormName(wellID))

        self.currForm = mat.getSkvNfromText(mat.getFormName(wellID))
        mesto = mat.getFormName(wellID)[len(self.currForm)+1 : -1]

        self.Edit_Bw.setText(str(bw))
        self.Edit_mu.setText(str(mu))
        self.Edit_kw.setText(str(kw))
        self.Edit_m.setText(str(m))
        self.Edit_Bo.setText(str(bo))
        self.Edit_So.setText(str(so))
        self.Edit_So_min.setText(str(so_min))
        self.Edit_Ro.setText(str(ro))
        self.Edit_P.setText(str(pn))

        pars = []
        pars.append(self.Edit_Bw.text())
        pars.append(self.Edit_mu.text())
        pars.append(self.Edit_kw.text())
        pars.append(self.Edit_m.text())
        pars.append(self.Edit_Bo.text())
        pars.append(self.Edit_So.text())
        pars.append(self.Edit_So_min.text())
        pars.append(self.Edit_Ro.text())
        pars.append(self.Edit_P.text())

        self.plast_db = dataform(self.currForm, mesto, pars)

        self.But_load_excel.setEnabled(False)
        self.Edit_P.setEnabled(False)
        self.But_Set_Pstart.setEnabled(False)

        self.ListOfDataObj = []

        df, re = sql.getWellHistoryFromBDtoChange(wellID)

        a = datawell(df, '')
        a.Re = re
        a.Re_check = 0
        self.ListOfDataObj.append(a)

        #self.Gr_bd1.canvas.axes.plot(L_dat[i], float(L_graf[i]), 'ko', markersize=4, color=clr[L_status[i]])


        self.tableBDskv.setRowCount(1)
        self.tableBDparam.clearContents()

        self.show()
        self.doWellTable()
        self.on_selectSkv()

        self.Gr_bd1.canvas.axes.clear()
        self.Gr_bd1.canvas.draw()



    #df = sql.getExcelForSql(a)



    # ПОЛУЧЕНИЕ ДАННЫХ ИЗ EXCEL ----------------------------------------------------------------------------------------

    def  fromExlForDB(self):

        a = QtWidgets.QFileDialog.getOpenFileName()[0]
        if a!='':
            df = sql.getExcelForSql(a)
            if type(df)==int:
                t = mat.error_type(df)
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Файл Excel не корректный - " + t)
                logging.error(str(datetime.now()) + '   '+  t + '   fromExlForDB')
            elif type(df)==str:
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Ошибка обработки файла. Смотрите log.txt")
                logging.error(str(datetime.now()) + '   ' + df + '   fromExlForDB')
            else:

                mesto = df.loc[0, 'Месторождение']
                plast0 = df['Объекты работы'].tolist()

                for i in plast0:
                    if ',' in i:
                        plast = ''
                    else:
                        plast = i
                        break
                if plast == '':
                    plast = mat.getAllForms(plast0)[0]

                df = df[df['Объекты работы'].str.contains(plast, regex=False)]
                df_skvInPlast = df.drop_duplicates(['№ скважины', 'Характер работы'], keep='last')


                formPar = sql.tryGetDataPlast(plast+'|'+mesto+'|')

                if len(formPar) > 0:

                    self.Edit_Bw.setText(str(formPar[0]))
                    self.Edit_mu.setText(str(formPar[1]))
                    self.Edit_kw.setText(str(formPar[2]))
                    self.Edit_m.setText(str(formPar[3]))
                    self.Edit_Bo.setText(str(formPar[4]))
                    self.Edit_So.setText(str(formPar[5]))
                    self.Edit_So_min.setText(str(formPar[6]))
                    self.Edit_Ro.setText(str(formPar[7]))
                    self.Edit_P.setText(str(formPar[8]))


                pars = []
                pars.append(self.Edit_Bw.text())
                pars.append(self.Edit_mu.text())
                pars.append(self.Edit_kw.text())
                pars.append(self.Edit_m.text())
                pars.append(self.Edit_Bo.text())
                pars.append(self.Edit_So.text())
                pars.append(self.Edit_So_min.text())
                pars.append(self.Edit_Ro.text())
                pars.append(self.Edit_P.text())

                self.plast_db = dataform(plast, mesto, pars)               # Экземпляр пласта создание------------------------------------------------------------------
                self.currForm = plast

                l1 = df_skvInPlast['№ скважины'].tolist()            # Экземпляр скважины подготовка------------------------------------------------------------------
                l2 = df_skvInPlast['Характер работы'].tolist()

                self.ListOfDataObj = []

                for i in range(len(l1)):
                    tmp_df = df.loc[df["№ скважины"] == l1[i]]
                    tmp_df = tmp_df.loc[tmp_df["Характер работы"] == l2[i]]

                    a = datawell(tmp_df, pars[8])                              # Экземпляр скважины создание----------------------------------------------------------

                    self.ListOfDataObj.append(a)


                # Нефтенасыщеная толщина
                '''for itm in self.ListOfDataObj:
                    if mat.isZero(itm.H):
                        lenmin = 99999999
                        h = 0
                        x = itm.X
                        y = itm.Y
                        for itm2 in self.ListOfDataObj:
                            if not mat.isZero(itm2.H):
                                lenn =  mat.lenWell(x, y, itm2.X, itm2.Y)
                                if lenn<lenmin:
                                    lenmin = lenn
                                    h = itm2.H
                        itm.H = h
                        itm.H_check = 2
                        itm.checkAll()'''

                for itm in self.ListOfDataObj:
                    if mat.isZero(itm.H):

                        ind1 = 99999999
                        h1 = -1
                        h2 = -1
                        h3 = -1
                        x = itm.X
                        y = itm.Y

                        lenmin = 99999999
                        for itm2 in self.ListOfDataObj:
                            if not mat.isZero(itm2.H):
                                lenn = mat.lenWell(x, y, itm2.X, itm2.Y)
                                if lenn < lenmin:
                                    lenmin = lenn
                                    h1 = itm2.H
                                    ind1 = self.ListOfDataObj.index(itm2)

                        lenmin = 99999999
                        for itm2 in self.ListOfDataObj:
                            if not mat.isZero(itm2.H) and self.ListOfDataObj.index(itm2) != ind1:
                                lenn = mat.lenWell(x, y, itm2.X, itm2.Y)
                                if lenn < lenmin:
                                    lenmin = lenn
                                    h2 = itm2.H
                                    ind2 = self.ListOfDataObj.index(itm2)

                        lenmin = 99999999
                        for itm2 in self.ListOfDataObj:
                            if not mat.isZero(itm2.H) and self.ListOfDataObj.index(itm2) != ind1 and self.ListOfDataObj.index(itm2) != ind2:
                                lenn = mat.lenWell(x, y, itm2.X, itm2.Y)
                                if lenn < lenmin:
                                    lenmin = lenn
                                    h3 = itm2.H

                        if h1<0 and h2<0 and h3<0:
                            itm.H = 0
                        elif h2<0 and h3<0:
                            itm.H = h1
                            itm.H_check = 2
                        elif h3<0:
                            itm.H = round((h1 + h2)/2 , 1)
                            itm.H_check = 2
                        else:
                            itm.H = round((h1 + h2 + h3) / 3, 1)
                            itm.H_check = 2


                        itm.checkAll()




                self.doForm()
                self.doWellTable()


                self.But_Set_average.setEnabled(False)
                self.But_Set_all_average.setEnabled(False)
                self.But_Set_Pstart.setEnabled(False)


    def doForm(self):

        self.Gr_bd1.canvas.axes.clear()
        self.Gr_bd1.canvas.axes.margins(0.05)
        self.Gr_bd1.F.tight_layout()
        self.Gr_bd1.F.subplots_adjust(top=0.9)

        self.Gr_bd1.canvas.draw()
        self.But_Set_average.setEnabled(False)

        self.tableBDparam.clearContents()

        self.label_well.setText('Пласт - ' + self.currForm)


        self.tableBDskv.setRowCount(len(self.ListOfDataObj))


    def doWellTable(self):

        self.tableBDskv.model().blockSignals(True)


        self.tableBDskv.clearContents()

        for i in range(len(self.ListOfDataObj)):

            print(self.ListOfDataObj[i].H_check)

            item = QTableWidgetItem(str(self.ListOfDataObj[i].wellName))
            if self.ListOfDataObj[i].err and self.ListOfDataObj[i].isRec:
                item.setForeground(QtGui.QColor('red'))
            self.tableBDskv.setItem(i, 0, item)
            item = QTableWidgetItem(str(self.ListOfDataObj[i].typ))
            self.tableBDskv.setItem(i, 1, item)
            item = QTableWidgetItem(str(self.ListOfDataObj[i].XX))
            self.tableBDskv.setItem(i, 2, item)
            item = QTableWidgetItem(str(self.ListOfDataObj[i].YY))
            self.tableBDskv.setItem(i, 3, item)
            item = QTableWidgetItem(str(self.ListOfDataObj[i].X))
            self.tableBDskv.setItem(i, 4, item)
            item = QTableWidgetItem(str(self.ListOfDataObj[i].Y))
            self.tableBDskv.setItem(i, 5, item)
            item = QTableWidgetItem(str(self.ListOfDataObj[i].H))
            self.tableBDskv.setItem(i, 6, item)
            if self.ListOfDataObj[i].H_check > 0:
                  self.tableBDskv.item(i, 6).setBackground(QtGui.QColor(self.clr[self.ListOfDataObj[i].H_check]))

            item = QTableWidgetItem(str(self.ListOfDataObj[i].Re))
            self.tableBDskv.setItem(i, 7, item)
            if self.ListOfDataObj[i].Re_check > 0:
                  self.tableBDskv.item(i, 7).setBackground(QtGui.QColor(self.clr[self.ListOfDataObj[i].Re_check]))

            CH = QtWidgets.QCheckBox("", self)
            CH.setObjectName('A' + str(i))
            CH.setChecked(self.ListOfDataObj[i].isRec)
            CH.setStyleSheet("margin-left:6;")

            self.tableBDskv.setCellWidget(i, 8, CH)
            CH.stateChanged.connect(self.isWellsRec)


        self.tableBDskv.model().blockSignals(False)
        self.tableBDskv.update()
        self.checkButToBD()



    def isWellsRec(self):

        num = int(self.sender().objectName()[1:])
        self.ListOfDataObj[num].isRec = self.sender().isChecked()
        self.ListOfDataObj[num].checkAll()
        self.afterChangeTableParam()
        self.checkButToBD()



    #  Изменения в таблице скважин
    def on_change_tableBDskv(self, i, j):

        a = self.tableBDskv.item(i, j).text()

        if j == 6:
            self.ListOfDataObj[i].H = a
            self.ListOfDataObj[i].H_check = 30
        if j == 7:
            self.ListOfDataObj[i].Re = a
            self.ListOfDataObj[i].Re_check = 30

        self.ListOfDataObj[i].checkAll()
        self.doWellTable()

        self.checkButToBD()



    # Клик по скважине (строке) в таблице
    def on_selectSkv(self):

        try:

            a = self.tableBDskv.currentRow()

            if a == -1:
                a = 0

            self.currWell = a


            self.label_well.setText(
                'Пласт - ' + self.currForm + '   ' + 'Скважина:  ' + self.ListOfDataObj[a].wellName)

            self.tableBDparam.setRowCount(len(self.ListOfDataObj[a].L_dat))


            if  self.ListOfDataObj[a].typ == 'НАГ':
                self.tableBDparam.setColumnCount(7)
                self.tableBDparam.setHorizontalHeaderLabels(
                    ['Дата', 'Закачка', 'Р заб.', 'Р пл.', 'Qзак(МЭР)', 'Qзак(ТР)', 'D шт.'])   #,  'Ндин'
                for i in range(1,6):
                    self.tableBDparam.horizontalHeaderItem(i).setToolTip(mat.setName(i))
                self.tableBDparam.horizontalHeaderItem(6).setToolTip(mat.setName(13))
                #self.tableBDparam.horizontalHeaderItem(7).setToolTip(mat.setName(12))

                self.tableBDparam.setColumnWidth(0, 70)
                self.tableBDparam.setColumnWidth(1, 90)
                self.tableBDparam.setColumnWidth(2, 70)
                self.tableBDparam.setColumnWidth(3, 70)

                self.doTableNAG(a, self.clr, False)

            else:

                self.tableBDparam.setColumnCount(10)
                self.tableBDparam.setHorizontalHeaderLabels(
                    ['Дата',  'Р заб.', 'Р пл.', 'Qж(МЭР)', 'Qж(ТР)', 'Qн(МЭР)', 'Qн(ТР)', 'WC(МЭР)', 'WC(ТР)', 'Ндин'])
                for i in range(6, 13):
                    self.tableBDparam.horizontalHeaderItem(i-3).setToolTip(mat.setName(i))
                self.tableBDparam.horizontalHeaderItem(1).setToolTip(mat.setName(2))
                self.tableBDparam.horizontalHeaderItem(2).setToolTip(mat.setName(3))

                self.tableBDparam.setColumnWidth(0, 76)
                self.tableBDparam.setColumnWidth(1, 70)
                self.tableBDparam.setColumnWidth(2, 70)
                self.tableBDparam.setColumnWidth(3, 80)
                self.tableBDparam.setColumnWidth(4, 80)
                self.tableBDparam.setColumnWidth(5, 80)
                self.tableBDparam.setColumnWidth(6, 80)
                self.tableBDparam.setColumnWidth(7, 80)
                self.tableBDparam.setColumnWidth(8, 80)
                self.tableBDparam.setColumnWidth(9, 70)

                self.doTableNEF(a, self.clr, False)


            self.But_Set_average.setEnabled(False)
            self.But_Set_all_average.setEnabled(True)
            if self.Edit_P.isEnabled():
                self.But_Set_Pstart.setEnabled(True)

            self.Gr_bd1.canvas.axes.clear()
            self.Gr_bd1.canvas.axes.set_title('')

        except Exception as e:
            logging.error(str(datetime.now()) + '   ' + str(e) + '   on_selectSkv')


    def afterChangeTableParam(self):

        self.tableBDskv.blockSignals(True)

        for i in range(len(self.ListOfDataObj)):

            #a = self.currWell
            item = QTableWidgetItem(str(self.ListOfDataObj[i].wellName))
            if self.ListOfDataObj[i].err:
                item.setForeground(QtGui.QColor('red'))
            else:
                item.setForeground(QtGui.QColor('black'))
            self.tableBDskv.setItem(i, 0, item)

        self.tableBDskv.blockSignals(False)


    def doTableNAG(self, a, clr, M):

        self.tableBDparam.blockSignals(True)

        #self.ListOfDataObj[a].checkAll()

        self.tableBDparam.horizontalHeaderItem(1).setForeground(QtGui.QColor(clr[self.ListOfDataObj[a].dict_err['L_inject']]))
        self.tableBDparam.horizontalHeaderItem(2).setForeground(QtGui.QColor(clr[self.ListOfDataObj[a].dict_err['L_Pzab']]))
        self.tableBDparam.horizontalHeaderItem(3).setForeground(QtGui.QColor(clr[self.ListOfDataObj[a].dict_err['L_Pplast']]))
        self.tableBDparam.horizontalHeaderItem(4).setForeground(QtGui.QColor(clr[self.ListOfDataObj[a].dict_err['L_priem']]))
        self.tableBDparam.horizontalHeaderItem(5).setForeground(QtGui.QColor(clr[self.ListOfDataObj[a].dict_err['L_PriemTR']]))
        self.tableBDparam.horizontalHeaderItem(6).setForeground(QtGui.QColor(clr[self.ListOfDataObj[a].dict_err['L_Diam']]))

        self.tableBDparam.cellChanged.disconnect(self.on_change_table_param)

        for i in range(len(self.ListOfDataObj[a].L_dat)):


            item = QTableWidgetItem(str(self.ListOfDataObj[a].L_dat[i])[:7])
            item.setBackground(QtGui.QColor(clr[0]))
            self.tableBDparam.setItem(i, 0, item)

            item = QTableWidgetItem(str(self.ListOfDataObj[a].L_inject[i]))
            item.setBackground(QtGui.QColor(clr[self.ListOfDataObj[a].L_inject_check[i]]))
            self.tableBDparam.setItem(i, 1, item)

            item = QTableWidgetItem(str(self.ListOfDataObj[a].L_Pzab[i]))
            item.setBackground(QtGui.QColor(clr[self.ListOfDataObj[a].L_Pzab_check[i]]))
            self.tableBDparam.setItem(i, 2, item)

            item = QTableWidgetItem(str(self.ListOfDataObj[a].L_Pplast[i]))
            item.setBackground(QtGui.QColor(clr[self.ListOfDataObj[a].L_Pplast_check[i]]))
            self.tableBDparam.setItem(i, 3, item)

            item = QTableWidgetItem(str(self.ListOfDataObj[a].L_priem[i]))
            item.setBackground(QtGui.QColor(clr[self.ListOfDataObj[a].L_priem_check[i]]))
            self.tableBDparam.setItem(i, 4, item)

            item = QTableWidgetItem(str(self.ListOfDataObj[a].L_PriemTR[i]))
            item.setBackground(QtGui.QColor(clr[self.ListOfDataObj[a].L_PriemTR_check[i]]))
            self.tableBDparam.setItem(i, 5, item)

            item = QTableWidgetItem(str(self.ListOfDataObj[a].L_Diam[i]))
            item.setBackground(QtGui.QColor(clr[self.ListOfDataObj[a].L_Diam_check[i]]))
            self.tableBDparam.setItem(i, 6, item)


        #self.tableBDparam.update()
        self.tableBDparam.cellChanged.connect(self.on_change_table_param)
        self.tableBDparam.blockSignals(False)

        if M:

            self.afterChangeTableParam()

        if self.tableBDparam.currentColumn()>0:
            self.on_clickTableParam(self.tableBDparam.currentColumn())


    def doTableNEF(self, a, clr, M):

        #self.ListOfDataObj[a].checkAll()


        self.tableBDparam.horizontalHeaderItem(1).setForeground(QtGui.QColor(clr[self.ListOfDataObj[a].dict_err['L_Pzab']]))
        self.tableBDparam.horizontalHeaderItem(2).setForeground(QtGui.QColor(clr[self.ListOfDataObj[a].dict_err['L_Pplast']]))
        self.tableBDparam.horizontalHeaderItem(3).setForeground(QtGui.QColor(clr[self.ListOfDataObj[a].dict_err['L_debLiq']]))
        self.tableBDparam.horizontalHeaderItem(4).setForeground(QtGui.QColor(clr[self.ListOfDataObj[a].dict_err['L_debLiqTR']]))
        self.tableBDparam.horizontalHeaderItem(5).setForeground(QtGui.QColor(clr[self.ListOfDataObj[a].dict_err['L_debOil']]))
        self.tableBDparam.horizontalHeaderItem(6).setForeground(QtGui.QColor(clr[self.ListOfDataObj[a].dict_err['L_debOilTR']]))
        self.tableBDparam.horizontalHeaderItem(7).setForeground(QtGui.QColor(clr[self.ListOfDataObj[a].dict_err['L_water']]))
        self.tableBDparam.horizontalHeaderItem(8).setForeground(QtGui.QColor(clr[self.ListOfDataObj[a].dict_err['L_waterTR']]))
        self.tableBDparam.horizontalHeaderItem(9).setForeground(QtGui.QColor(clr[self.ListOfDataObj[a].dict_err['L_dynLevel']]))


        self.tableBDparam.cellChanged.disconnect(self.on_change_table_param)

        for i in range(len(self.ListOfDataObj[a].L_dat)):
            item = QTableWidgetItem(str(self.ListOfDataObj[a].L_dat[i])[:7])
            item.setBackground(QtGui.QColor(clr[0]))
            self.tableBDparam.setItem(i, 0, item)

            item = QTableWidgetItem(str(self.ListOfDataObj[a].L_Pzab[i]))
            item.setBackground(QtGui.QColor(clr[self.ListOfDataObj[a].L_Pzab_check[i]]))
            self.tableBDparam.setItem(i, 1, item)

            item = QTableWidgetItem(str(self.ListOfDataObj[a].L_Pplast[i]))
            item.setBackground(QtGui.QColor(clr[self.ListOfDataObj[a].L_Pplast_check[i]]))
            self.tableBDparam.setItem(i, 2, item)

            item = QTableWidgetItem(str(self.ListOfDataObj[a].L_debLiq[i]))
            item.setBackground(QtGui.QColor(clr[self.ListOfDataObj[a].L_debLiq_check[i]]))
            self.tableBDparam.setItem(i, 3, item)

            item = QTableWidgetItem(str(self.ListOfDataObj[a].L_debLiqTR[i]))
            item.setBackground(QtGui.QColor(clr[self.ListOfDataObj[a].L_debLiqTR_check[i]]))
            self.tableBDparam.setItem(i, 4, item)

            item = QTableWidgetItem(str(self.ListOfDataObj[a].L_debOil[i]))
            item.setBackground(QtGui.QColor(clr[self.ListOfDataObj[a].L_debOil_check[i]]))
            self.tableBDparam.setItem(i, 5, item)

            item = QTableWidgetItem(str(self.ListOfDataObj[a].L_debOilTR[i]))
            item.setBackground(QtGui.QColor(clr[self.ListOfDataObj[a].L_debOilTR_check[i]]))
            self.tableBDparam.setItem(i, 6, item)

            item = QTableWidgetItem(str(self.ListOfDataObj[a].L_water[i]))
            item.setBackground(QtGui.QColor(clr[self.ListOfDataObj[a].L_water_check[i]]))
            self.tableBDparam.setItem(i, 7, item)

            item = QTableWidgetItem(str(self.ListOfDataObj[a].L_waterTR[i]))
            item.setBackground(QtGui.QColor(clr[self.ListOfDataObj[a].L_waterTR_check[i]]))
            self.tableBDparam.setItem(i, 8, item)

            item = QTableWidgetItem(str(self.ListOfDataObj[a].L_dynLevel[i]))
            item.setBackground(QtGui.QColor(clr[self.ListOfDataObj[a].L_dynLevel_check[i]]))
            self.tableBDparam.setItem(i, 9, item)

        self.tableBDparam.update()
        self.tableBDparam.cellChanged.connect(self.on_change_table_param)

        if M:
            self.afterChangeTableParam()

        if self.tableBDparam.currentColumn() > 0:
            self.on_clickTableParam(self.tableBDparam.currentColumn())


    def change_table_param(self, i,j, s):
        a = self.currWell

        if self.ListOfDataObj[a].typ == 'НАГ':
            if j == 1:
                self.ListOfDataObj[a].L_inject[i] = s
                self.ListOfDataObj[a].L_inject_check[i] = 30
            if j == 2:
                self.ListOfDataObj[a].L_Pzab[i] = s
                self.ListOfDataObj[a].L_Pzab_check[i] = 30

            if j == 3:
                self.ListOfDataObj[a].L_Pplast[i] = s
                self.ListOfDataObj[a].L_Pplast_check[i] = 30
            if j == 4:
                self.ListOfDataObj[a].L_priem[i] = s
                self.ListOfDataObj[a].L_priem_check[i] = 30
            if j == 5:
                self.ListOfDataObj[a].L_PriemTR[i] = s
                self.ListOfDataObj[a].L_PriemTR_check[i] = 30
            if j == 6:
                self.ListOfDataObj[a].L_Diam[i] = s
                self.ListOfDataObj[a].L_Diam_check[i] = 30

        if self.ListOfDataObj[self.currWell].typ == 'НЕФ':
            if j == 1:
                self.ListOfDataObj[a].L_Pzab[i] = s
                self.ListOfDataObj[a].L_Pzab_check[i] = 30
            if j == 2:
                self.ListOfDataObj[a].L_Pplast[i] = s
                self.ListOfDataObj[a].L_Pplast_check[i] = 30
            if j == 3:
                self.ListOfDataObj[a].L_debLiq[i] = s
                self.ListOfDataObj[a].L_debLiq_check[i] = 30
            if j == 4:
                self.ListOfDataObj[a].L_debLiqTR[i] = s
                self.ListOfDataObj[a].L_debLiqTR_check[i] = 30
            if j == 5:
                self.ListOfDataObj[a].L_debOil[i] = s
                self.ListOfDataObj[a].L_debOil_check[i] = 30
            if j == 6:
                self.ListOfDataObj[a].L_debOilTR[i] = s
                self.ListOfDataObj[a].L_debOilTR_check[i] = 30
            if j == 7:
                self.ListOfDataObj[a].L_water[i] = s
                self.ListOfDataObj[a].L_water_check[i] = 30
            if j == 8:
                self.ListOfDataObj[a].L_waterTR[i] = s
                self.ListOfDataObj[a].L_waterTR_check[i] = 30
            if j == 9:
                self.ListOfDataObj[a].L_dynLevel[i] = s
                self.ListOfDataObj[a].L_dynLevel_check[i] = 30

    def on_change_table_param(self,i,j):

        if i != -2:
            s = self.tableBDparam.item(i, j).text()
            self.change_table_param(i,j, s)

        self.ListOfDataObj[self.currWell].checkAll()

        if self.ListOfDataObj[self.currWell].typ == 'НАГ':
            self.doTableNAG(self.currWell, self.clr, True)
        else:
            self.doTableNEF(self.currWell, self.clr, True)

        self.checkButToBD()





        # График  параметра

    def on_clickTableParam(self, j):

        a = self.currWell

        if len(self.ListOfDataObj) > 0:

            try:

                self.But_Set_average.setEnabled(True)

                L_dat = self.ListOfDataObj[a].L_dat

                if self.ListOfDataObj[a].typ == 'НАГ':

                    if j == 1:
                        L_graf = self.ListOfDataObj[a].L_inject
                        L_status = self.ListOfDataObj[a].L_inject_check
                        name_gr = 'Закачка за посл.месяц, м3'
                    if j == 2:
                        L_graf = self.ListOfDataObj[a].L_Pzab
                        L_status = self.ListOfDataObj[a].L_Pzab_check
                        name_gr = 'Забойное давление (ТР), атм'

                    if j == 3:
                        L_graf = self.ListOfDataObj[a].L_Pplast
                        L_status = self.ListOfDataObj[a].L_Pplast_check
                        name_gr = 'Пластовое давление (ТР), атм'

                    if j == 4:
                        L_graf = self.ListOfDataObj[a].L_priem
                        L_status = self.ListOfDataObj[a].L_priem_check
                        name_gr = 'Приемистость за последний месяц, м3/сут'

                    if j == 5:
                        L_graf = self.ListOfDataObj[a].L_PriemTR
                        L_status = self.ListOfDataObj[a].L_PriemTR_check
                        name_gr = 'Приемистость (ТР), м3/сут'

                    if j == 6:
                        L_graf = self.ListOfDataObj[a].L_Diam
                        L_status = self.ListOfDataObj[a].L_Diam_check
                        name_gr = 'Диаметр штуцера, мм'

                else:

                    if j == 1:
                        L_graf = self.ListOfDataObj[a].L_Pzab
                        L_status = self.ListOfDataObj[a].L_Pzab_check
                        name_gr = 'Забойное давление (ТР), атм'

                    if j == 2:
                        L_graf = self.ListOfDataObj[a].L_Pplast
                        L_status = self.ListOfDataObj[a].L_Pplast_check
                        name_gr = 'Пластовое давление (ТР), атм'

                    if j == 3:
                        L_graf = self.ListOfDataObj[a].L_debLiq
                        L_status = self.ListOfDataObj[a].L_debLiq_check
                        name_gr = 'Дебит жидкости за последний месяц, т/сут'

                    if j == 4:
                        L_graf = self.ListOfDataObj[a].L_debLiqTR
                        L_status = self.ListOfDataObj[a].L_debLiqTR_check
                        name_gr = 'Дебит жидкости (ТР), м3/сут'

                    if j == 5:
                        L_graf = self.ListOfDataObj[a].L_debOil
                        L_status = self.ListOfDataObj[a].L_debOil_check
                        name_gr = 'Дебит нефти за последний месяц, т/сут'

                    if j == 6:
                        L_graf = self.ListOfDataObj[a].L_debOilTR
                        L_status = self.ListOfDataObj[a].L_debOilTR_check
                        name_gr = 'Дебит нефти (ТР), т/сут'

                    if j == 7:
                        L_graf = self.ListOfDataObj[a].L_water
                        L_status = self.ListOfDataObj[a].L_water_check
                        name_gr = 'Обводненность за посл.месяц, % (вес)'

                    if j == 8:
                        L_graf = self.ListOfDataObj[a].L_waterTR
                        L_status = self.ListOfDataObj[a].L_waterTR_check
                        name_gr = 'Обводненность (ТР), % (объём)'

                    if j == 9:
                        L_graf = self.ListOfDataObj[a].L_dynLevel
                        L_status = self.ListOfDataObj[a].L_dynLevel_check
                        name_gr = 'Динамический уровень (ТР), м'


                self.doDataGr(L_dat, L_graf, L_status, name_gr)

            except:
                print('?????????????????????')


    def doDataGr(self, L_dat, L_graf, L_status,  name_gr):

        self.Gr_bd1.canvas.axes.clear()
        self.Gr_bd1.canvas.axes.grid()

        self.Gr_bd1.canvas.axes.set_title(name_gr)

        clr = ['green', 'red', 'orange', 'dodgerblue']

        for i in range(len(L_graf)):

            if mat.isFloat(L_graf[i]):
                self.Gr_bd1.canvas.axes.plot(L_dat[i], 0, 'ko', markersize=4, color=clr[L_status[i]])
            else:
                self.Gr_bd1.canvas.axes.plot(L_dat[i], float(L_graf[i]), 'ko', markersize=4, color=clr[L_status[i]])



        self.Gr_bd1.canvas.draw()




    def checkButToBD(self):
        self.But_to_BD.setEnabled(not self.errLoad)

        if len(self.ListOfDataObj) > 0:
            a = 0
            for itm in self.ListOfDataObj:
                if itm.isRec:
                    a = a + 1
                if itm.err and itm.isRec:
                    self.But_to_BD.setEnabled(False)
                    break
            if a == 0:
                self.But_to_BD.setEnabled(False)


class First_window(QMainWindow):

    def __init__(self):
        super(First_window,self).__init__()
        loadUi("FirstWin.ui",self)

        q = QDesktopWidget().availableGeometry()
        if q.width() <= 1920 or q.height() <= 1200:
            self.showMaximized()

        self.listChenReport = []
        self.listSpearReport = []
        self.listNOReport = []

        self.But_exp.setCheckable(True)
        self.But_exp.clicked.connect(self.expTree)
        self.But_rep.clicked.connect(self.doReportAll)
        self.But_home.clicked.connect(self.doGrHome)

        logging.basicConfig(filename="Log.txt", level=logging.INFO)

        self.all_checked = []
        self.all_tree_itm_checked = []
        self.all_tree_parent_checked = []
        self.curr_itm_parent = 'A'
        self.L_circ = []

        self.lineRad.setInputMask('99999')

        self.HL_forMap.addWidget(self.Gr_map.toolbar_map)

        #self.toolbar1 = NavTool(self.Gr_hall1.canvas, self)

        self.Gr_map.canvas.mpl_connect('motion_notify_event', self.getCoords)
        self.Gr_map.canvas.mpl_connect('scroll_event',self.zoom_fun)


        self.action_3.triggered.connect(self.load_bd_win)
        self.action_6.triggered.connect(self.load_spirman)
        self.action_5.triggered.connect(self.load_param)
        #self.action_4.triggered.connect(self.load_grp)
        self.action_8.triggered.connect(self.load_evt)
        self.action_9.triggered.connect(self.load_word)
        self.action_chen.triggered.connect(self.load_chen2)
        self.action_hall.triggered.connect(self.load_hall2)
        self.action_no.triggered.connect(self.load_no)

        self.checkBox_Nag1.stateChanged.connect(self.changeGrNag)
        self.checkBox_Nag2.stateChanged.connect(self.changeGrNag)
        self.checkBox_Nag3.stateChanged.connect(self.changeGrNag)
        self.checkBox_Nag4.stateChanged.connect(self.changeGrNag)
        self.checkBox_Nag5.stateChanged.connect(self.changeGrNag)
        self.checkBox_Nag6.stateChanged.connect(self.changeGrNag)

        self.checkBox_Nef1.stateChanged.connect(self.changeGrNef)
        self.checkBox_Nef2.stateChanged.connect(self.changeGrNef)
        self.checkBox_Nef3.stateChanged.connect(self.changeGrNef)
        self.checkBox_Nef4.stateChanged.connect(self.changeGrNef)
        self.checkBox_Nef5.stateChanged.connect(self.changeGrNef)
        self.checkBox_Nef6.stateChanged.connect(self.changeGrNef)
        self.checkBox_Nef7.stateChanged.connect(self.changeGrNef)
        self.checkBox_Nef8.stateChanged.connect(self.changeGrNef)
        self.checkBox_Nef9.stateChanged.connect(self.changeGrNef)
        self.checkBox_Nef10.stateChanged.connect(self.changeGrNef)

        self.checkBox_front.stateChanged.connect(self.onOffFront)

        self.hLayoutGrNag.addWidget(self.Gr_nag.toolbar)
        self.hLayoutGrNef.addWidget(self.Gr_nef.toolbar)

        self.cid = self.Gr_map.canvas.mpl_connect('button_press_event', self.onclick_to_map)   # клик на скважину на карте

        self.N = 0

        self.Nag = -1
        self.Nef = -1

        self.skvN = []

        self.xyLims = [0, 0, 0, 0]


        self.Gr_nag_dop1 = self.Gr_nag.canvas.axes.twinx()
        self.Gr_nag_dop2 = self.Gr_nag.canvas.axes.twinx()
        self.Gr_nag_dop3 = self.Gr_nag.canvas.axes.twinx()
        self.Gr_nag_dop4 = self.Gr_nag.canvas.axes.twinx()
        self.Gr_nag_dop4.set_yticklabels([])

        self.Gr_nef_dop1 = self.Gr_nef.canvas.axes.twinx()
        self.Gr_nef_dop2 = self.Gr_nef.canvas.axes.twinx()
        self.Gr_nef_dop3 = self.Gr_nef.canvas.axes.twinx()

        self.Gr_nef_dop4 = self.Gr_nef.canvas.axes.twinx()

        self.tree_wells.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_wells.customContextMenuRequested.connect(self.TreeMenu)
        self.TreeItemCurr = ''
        self.canRefreshMap = True   #  для исключения лишних обновлений карты
        self.canRefreshMap2 = True

        #  СОЗДАНИЕ ДЕРЕВА  ОБЪЕКТОВ  В  TREEVIEW

        self.addTree(self.tree_wells, sql.getALLfromBD())
        self.tree_wells.itemChanged[QTreeWidgetItem, int].connect(self.get_item)


    def addTree(self, p, ch):

        for k, v in ch.items():
            item = self.new_item(k)
            if isinstance(p, QTreeWidget):
                p.addTopLevelItem(item)

            else:
                p.addChild(item)

            if isinstance(v, dict):
                self.addTree(item, v)

            elif isinstance(v, list):
                for txt in v:
                    item.setIcon(0, QtGui.QIcon("res\icoForm.png"))
                    self.all_tree_parent_checked.append(item)
                    item.setCheckState(0, Qt.Unchecked)
                    item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    item.addChild(self.new_item(txt))

    def new_item(self, text):
        item = QTreeWidgetItem()
        item.setText(0, text)
        if 'НАГ' in text or 'НЕФ' in text:
            if 'НАГ' in text:
                item.setIcon(0, QtGui.QIcon("res\icoWater.png"))
            if 'НЕФ' in text:
                item.setIcon(0, QtGui.QIcon("res\icoOil.png"))
            item.setCheckState(0, Qt.Unchecked)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        return item

    # Выбор скважины в дереве скважин
    def get_item(self, item, column):

        #now = datetime.now()
        #print("Текущая секунда: %d" % now.second)

        try:

            if item.childCount()==0:

                if item.checkState(column) == Qt.Checked:

                    texts = []
                    itm = item
                    while item is not None:
                        texts.append(item.text(0))
                        item = item.parent()
                    checked = "|".join(texts)
                    checked = checked.replace("-Н", "|Н")
                    checked = checked + '|'
                    self.all_checked.append(checked)
                    #self.TreeItemCurr = checked

                    #  Сброс всех флажков при переходе на другой пласт
                    if itm.parent()!='A' and itm.parent()!=self.curr_itm_parent:
                        #self.unCheckAll()
                        pass


                    # Проверка случая выборcanselALLа одной и тойже скв.  НЕФ  и  НАГ,  сброс флажка
                    o = []
                    for b in range(len(self.all_checked)):
                       o.append(mat.getSkvNfromText(self.all_checked[b]))
                    s = set(o)
                    if len(o) != len(s):
                        itm.setCheckState(0, Qt.Unchecked)
                    else:
                        self.all_tree_itm_checked.append(itm)    #  Добавление скважины в "выбраные"
                        self.curr_itm_parent = itm.parent()


                else:
                    #print(item.text(0))
                    texts = []
                    while item is not None:
                        texts.append(item.text(0))
                        item = item.parent()
                    checked = "|".join(texts)
                    checked = checked.replace("-Н", "|Н")
                    checked = checked + '|'
                    if checked in self.all_checked:
                        indexx = self.all_checked.index(checked)
                        if indexx == self.Nag:
                            self.Nag = -1
                        if indexx == self.Nef:
                            self.Nef = -1
                        self.all_checked.remove(checked)
                    #print(f'{item.text(column)} was unchecked')
                #print(self.all_checked)

            else:

                if item.checkState(column) == Qt.Checked:

                    h = item

                    for b in self.all_tree_parent_checked:
                        if b!=h:
                            b.setCheckState(0, Qt.Unchecked)

                    self.unCheckAll()

                    self.canRefreshMap = False

                    for i in range(item.childCount()):

                        item.child(i).setCheckState(0, Qt.Checked)
                        if i == item.childCount()-1:
                            self.canRefreshMap = True

                else:

                    self.unCheckAll()

            if len(self.all_checked)>0 and self.canRefreshMap and self.canRefreshMap2:

                self.xyLims = [0,0,0,0]

                self.load_data_MAP_sql()

                #print(self.all_checked)

            self.checkForSpirman()

        except Exception as e:  # Запись  ошибок в лог
            logging.error(str(datetime.now()) + '   ' + str(e)+'   get_item')


    def TreeMenu(self,position):
        if self.tree_wells.itemAt(position) is not None:

            texts = []
            itm = self.tree_wells.currentItem()
            while itm is not None:
                texts.append(itm.text(0))
                itm = itm.parent()
            checked = "|".join(texts)
            checked = checked.replace("-Н", "|Н")
            checked = checked + '|'

            self.WhatDel = checked


            if self.WhatDel.count('|')>1:
                menu = QtWidgets.QMenu()
                if  self.WhatDel.count('|')>3:
                    all0 = QtWidgets.QAction('Выбрать скважину на карте', menu)
                    all = QtWidgets.QAction('Удалить  скважину с ее историей', menu)
                    all2 = QtWidgets.QAction('Редактировать параметры скважины', menu)
                    all3 = QtWidgets.QAction('Редактировать параметры скважины и ее историю', menu)
                    all.triggered.connect(self.delObj)
                    all0.triggered.connect(self.selWell)
                    all2.triggered.connect(self.load_edit)
                    all3.triggered.connect(self.load_wellEdit)
                    if self.WhatDel in self.all_checked:
                        menu.addAction(all0)
                    menu.addAction(all2)
                    menu.addAction(all3)

                else:
                    all = QtWidgets.QAction('Удалить пласт со всеми скважинами и их историей', menu)
                    all2 = QtWidgets.QAction('Редактировать параметры пласта', menu)
                    all21 = QtWidgets.QAction('Переместить выбранные скважины', menu)
                    all3 = QtWidgets.QAction('Удалить все скважины пласта c их историей', menu)
                    all4 = QtWidgets.QAction('Удалить только выбранные скважины c их историей', menu)
                    all.triggered.connect(self.delObj)
                    all2.triggered.connect(self.load_edit)
                    all21.triggered.connect(self.prepearMoveWells)
                    all3.triggered.connect(self.delAll)
                    all4.triggered.connect(self.delSomeWells)
                    menu.addAction(all2)
                    menu.addAction(all21)
                    menu.addAction(all3)
                    menu.addAction(all4)
                #all2 = QtWidgets.QAction('description', menu)
                #all2.triggered.connect(self.popUpSetAll)
                menu.addAction(all)


                #menu.addAction(all2)
                menu.exec_(self.tree_wells.viewport().mapToGlobal(position))

    def load_wellEdit(self):

        bd.wellToEdit(self.WhatDel)


    def unCheckAll(self):

        self.Gr_map.setToolTip('')

        if  len(self.all_tree_itm_checked)>0:

            self.canRefreshMap2 = False
            for y in range(len(self.all_tree_itm_checked)):

                self.all_tree_itm_checked[y].setCheckState(0, Qt.Unchecked)
                if y == len(self.all_tree_itm_checked) - 1:

                    self.canRefreshMap2 = True



        self.all_tree_itm_checked = []


        self.Nag = -1
        self.Neg = -1

        self.Gr_nag.canvas.axes.clear()
        self.Gr_nef.canvas.axes.clear()
        self.Gr_map.canvas.axes.clear()
        self.Gr_map.canvas.draw()
        self.Gr_nag.canvas.draw()
        self.Gr_nef.canvas.draw()


    def prepearMoveWells(self):

        edit3.setWindowTitle('Переместить скважины с пласта '+  mat.getSkvNfromText(self.WhatDel) + ' в указанный пласт')

        aa = []
        for itm in self.all_checked:
            if self.WhatDel in itm:
                aa.append(itm)

        if len(aa) > 0:

            a = mat.getPlaceName(self.WhatDel)[1:-1]

            edit3.comboBox.clear()
            edit3.comboBox.addItems(sql.getNamesForm(a))

            edit3.show()

        else:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Не выбранно ни одной скважины")


    def moveWells(self, formForMove):

        a = []
        for itm in self.all_checked:
            if self.WhatDel in itm:
                a.append(itm)

        try:

            sql.moveToNewForm(self.WhatDel, a, formForMove)

            self.unCheckAll()
            self.tree_wells.clear()
            self.tree_wells.itemChanged[QTreeWidgetItem, int].disconnect(self.get_item)
            self.all_tree_parent_checked = []
            self.addTree(self.tree_wells, sql.getALLfromBD())
            self.tree_wells.itemChanged[QTreeWidgetItem, int].connect(self.get_item)

        except Exception as e:  # Запись  ошибок в лог
            logging.error(str(datetime.now()) + '   ' + str(e) + '   moveWells')



    # выбрать скважину на карте
    def selWell(self):
        for i in range(len(self.all_checked)):
            if self.WhatDel == self.all_checked[i]:
                a  = i
                break
        self.N = a

        if self.skvType[a] == 'НАГ':
            self.Nag = a
            self.load_data_MAP_sql()
            self.exe_hall()
            self.drawSpearmanLines()
        else:
            self.Nef = a
            self.load_data_MAP_sql()
            self.exe_chen()



    def delAll(self):


        q = QtWidgets.QMessageBox.question(self, "NOIZ", "Удалить все скважины пласта  " + mat.getSkvNfromText(self.WhatDel) + " ?",
                                           defaultButton=QtWidgets.QMessageBox.No)

        if q == 16384:

            self.unCheckAll()

            sql.delPlast(self.WhatDel, 1)
            self.tree_wells.clear()
            self.tree_wells.itemChanged[QTreeWidgetItem, int].disconnect(self.get_item)
            self.all_tree_parent_checked = []
            self.addTree(self.tree_wells, sql.getALLfromBD())
            self.tree_wells.itemChanged[QTreeWidgetItem, int].connect(self.get_item)

        else:
            pass


    def delSomeWells(self):

        q = QtWidgets.QMessageBox.question(self, "NOIZ", "Удалить выбранные скважины ?",
                                           defaultButton=QtWidgets.QMessageBox.No)

        if q == 16384:

            l = []
            for h in self.all_checked:
                t = []
                t.append(h)
                l.append(tuple(t))

                sql.delWell(h)


            self.unCheckAll()

            self.tree_wells.clear()
            self.tree_wells.itemChanged[QTreeWidgetItem, int].disconnect(self.get_item)
            self.all_tree_parent_checked = []
            self.addTree(self.tree_wells, sql.getALLfromBD())
            self.tree_wells.itemChanged[QTreeWidgetItem, int].connect(self.get_item)
        else:
            pass


    def delObj(self):

        q = QtWidgets.QMessageBox.question(self, "NOIZ", "Удалить объект " + mat.getSkvNfromText(self.WhatDel) + " ?", defaultButton=QtWidgets.QMessageBox.No)

        if q==16384:

            self.unCheckAll()

            if self.WhatDel.count('|')>3:

                sql.delWell(self.WhatDel)
            else:
                sql.delPlast(self.WhatDel, 0)

            self.tree_wells.clear()

            self.tree_wells.itemChanged[QTreeWidgetItem, int].disconnect(self.get_item)
            self.all_tree_parent_checked = []
            self.addTree(self.tree_wells, sql.getALLfromBD())
            self.tree_wells.itemChanged[QTreeWidgetItem, int].connect(self.get_item)

        else:
            pass


    def doGrHome(self):
        self.xyLims = [0, 0, 0, 0]
        self.load_data_MAP_sql()

    #def handler(self, item, column_no):

    #    texts = []
    #    while item is not None:
     #       texts.append(item.text(0))
     #       item = item.parent()
     #   checked = "|".join(texts)
     #   checked = checked.replace("-Н", "|Н")
     #   print(checked)

    #    self.all_checked.append(checked)
        #print(self.all_checked)load_spirman
# ------------------------------------------------------------------------------------------

    def expTree(self):

        if self.But_exp.isChecked():
            self.Gr_map.setMinimumHeight(0)

        else:
            self.Gr_map.setMinimumHeight(600)


    def onOffFront(self):
        try:
            self.load_data_MAP_sql()
        except:
            pass


    def load_param(self):
        param.show()

    def load_evt(self):
        evt.show()
        evt.get_data_evt()



    def load_edit(self):

        if self.WhatDel.count('|') > 3:

            h, re = sql.getWellFromBDtoChange(self.WhatDel)
            edit2.HEdit.setText(str(h))
            edit2.reEdit.setText(str(re))
            edit2.label.setText(mat.getSkvNfromText(self.WhatDel))
            edit2.wellID = self.WhatDel
            edit2.show()

        else:
            bo, ro, m, so, so_min, bw, kw, mu, pn = sql.getFormFromBD(self.WhatDel)
            edit.boEdit.setText(str(bo))
            edit.roEdit.setText(str(ro))
            edit.mEdit.setText(str(m))
            edit.soEdit.setText(str(so))
            edit.so_minEdit.setText(str(so_min))
            edit.bwEdit.setText(str(bw))
            edit.kwEdit.setText(str(kw))
            edit.muEdit.setText(str(mu))
            edit.PEdit.setText(str(pn))
            edit.formID = self.WhatDel
            edit.label.setText(self.WhatDel)
            edit.show()



    def load_spirman(self):

        try:

            r = int(self.lineRad.text())
            self.nefCoords = []
            spirAllnag = []
            spirAllnagN = []
            spirAllnef = []
            wells_len =[]
            FNV = []
            KP = []

            for i in range(len(self.all_checked)):

                if 'НАГ' in self.all_checked[i]:
                    spirAllnag.append(self.all_checked[i])
                    spirAllnagN.append(i)
                    FNV.append(self.R[i])

            for i in spirAllnagN:
                tmp = []
                tmp_len =[]
                tmp_kp = []
                for j in range(len(self.all_checked)):
                    if 'НЕФ' in self.all_checked[j]:
                        if mat.InRadius(self.skvX[i], self.skvY[i], self.skvX[j], self.skvY[j], self.skvXX[j], self.skvYY[j], r):
                            tmp.append(self.all_checked[j])
                            if self.skvXX[j] < 0 and self.skvYY[j] < 0:
                                tmp_len.append(mat.lenWell(self.skvX[i], self.skvY[i], self.skvX[j], self.skvY[j]))

                            else:
                                tmp_len.append(mat.lenWell_gorizon(self.skvX[i], self.skvY[i], self.skvX[j], self.skvY[j], self.skvXX[j], self.skvYY[j]))
                            tmp_kp.append(self.R[j])

                spirAllnef.append(tmp)
                wells_len.append(tmp_len)
                KP.append(tmp_kp)

            spirman.doWinSpear(spirAllnag, spirAllnef, wells_len, FNV, KP)

        except Exception as e:  # Запись  ошибок в лог
            logging.error(str(datetime.now()) + '   ' + str(e) + '   load_spirman')


    def load_bd_win(self):

        bd.show()
        bd.But_load_excel.setEnabled(True)
        bd.Edit_P.setEnabled(True)


    def isNaN(self, num):
        return num != num


    #def focusInEvent(self, event):
     #   self.Edit_rdp.setText('123123123')

    def zoom_fun(self,event):

        base_scale = 1.2

        # get the current x and y limits
        cur_xlim = self.Gr_map.canvas.axes.get_xlim()
        cur_ylim = self.Gr_map.canvas.axes.get_ylim()
        # set the range
        cur_xrange = (cur_xlim[1] - cur_xlim[0]) * .5
        cur_yrange = (cur_ylim[1] - cur_ylim[0]) * .5
        xdata = event.xdata  # get event x location
        ydata = event.ydata  # get event y location
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1 / base_scale
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1

        # set new limits
        self.Gr_map.canvas.axes.set_xlim([xdata - cur_xrange * scale_factor,
                     xdata + cur_xrange * scale_factor])
        self.Gr_map.canvas.axes.set_ylim([ydata - cur_yrange * scale_factor,
                     ydata + cur_yrange * scale_factor])

        self.xyLims[0] = xdata - cur_xrange * scale_factor
        self.xyLims[1] = xdata + cur_xrange * scale_factor
        self.xyLims[2] = ydata - cur_yrange * scale_factor
        self.xyLims[3] = ydata + cur_yrange * scale_factor


        self.Gr_map.canvas.draw_idle()  # force re-draw the next time the GUI refreshes



    def getCoords(self, event):

         try:

            a = 0
            deltaN = 40

            for i in range(len(self.skvN)):

                deltaY = self.M /20
                deltaX = self.M /20

                try:
                    chk1 = event.xdata > self.skvX[i] - deltaN and event.xdata < self.skvX[i] + deltaN
                    chk2 = event.ydata > self.skvY[i] - deltaN and event.ydata < self.skvY[i] +deltaN
                except:
                    chk1 = False
                    chk2 = False

                if chk1 and chk2:
                    a = i
                    break
                else:
                    a = -1
            if a>-1:

                try:
                    if len(self.L_circ) == 0:
                        Gr, = self.Gr_map.canvas.axes.plot(self.skvX[a], self.skvY[a], 'o', markersize=30, color='yellow',
                                                               alpha = 0.4)
                        self.L_circ.append(Gr)
                        self.Gr_map.canvas.draw()


                    self.Gr_map.setCursor(Qt.PointingHandCursor)
                except:
                    pass

            else:
                if len(self.L_circ) > 0:
                    for t in self.L_circ:
                        t.remove()
                    self.L_circ = []
                    self.Gr_map.canvas.draw()

                self.Gr_map.setCursor(Qt.ArrowCursor)

         except:
             pass



   # def event(self, e):
   #     if e.type() == QEvent.WindowUnblocked:
   #         if inputdata.data_got:
   #             self.load_data()
   #     return QtWidgets.QWidget.event(self, e)


    def onclick_to_map(self, event):

        try:
            a =-1
            for i in range(len(self.skvN)):
                deltaY = self.M /20
                deltaX = self.M /20
                deltaN = 40
                #chk1 = abs(self.skvX[i] - event.xdata) <30
                #chk2 = abs(self.skvY[i] - event.ydata) <30
                #chk1 = event.xdata > self.skvX[i] + deltaX and event.xdata < self.skvX[i] + deltaX*3
                #chk2 = event.ydata > self.skvY[i] - deltaY and event.ydata < self.skvY[i]
                chk1 = event.xdata > self.skvX[i] - deltaN and event.xdata < self.skvX[i] + deltaN
                chk2 = event.ydata > self.skvY[i] - deltaN and event.ydata < self.skvY[i] + deltaN
                if chk1 and chk2:
                    a = i
                    break
                else:
                    a = -1

        except Exception as e:  # Запись  ошибок в лог
            logging.error(str(datetime.now()) + '   ' + str(e)+'   onclick_to_map')

        if a>-1:
            #self.Combo_hall.setCurrentIndex(a)
            #self.change_skv(str(self.skvN[a]))
            self.N = a

            if self.skvType[a] == 'НАГ':
                self.Nag = a
                self.load_data_MAP_sql()
                self.exe_hall()
                self.drawSpearmanLines()

            else:

                self.Nef = a
                self.load_data_MAP_sql()
                self.exe_chen()



    def drawSpearmanLines(self):

        if len(spirman.ListOfSpirmanObj)>0:

            self.L_arrs = []

            self.Gr_map.setToolTip(mat.HTM)

            idNag = self.all_checked[self.Nag]
            x1 = self.skvX[self.Nag]
            y1 = self.skvY[self.Nag]


            for itm in spirman.ListOfSpirmanObj:

                if itm.NagID == idNag:
                    for j in range(len(self.all_checked)):
                        #print(itm.NefID + '   ' + self.all_checked[j])
                        if self.all_checked[j] == itm.NefID:
                            x2 = self.skvX[j]
                            y2 = self.skvY[j]
                            x11 = (x1 + 0.9 * x2) / (1 + 0.9)
                            y11 = (y1 + 0.9 * y2) / (1 + 0.9)
                            x22 = (x2 + 0.1 * x1) / (1 + 0.1)
                            y22 = (y2 + 0.1 * y1) / (1 + 0.1)
                            _, clr = mat.spearDecodeK(itm.K)
                            arrowprops = dict(arrowstyle='->', color=clr, linewidth=2, mutation_scale=10)
                            # !!! Добавление аннотации
                            arr = self.Gr_map.canvas.axes.annotate('',
                                                                           xy=(x22, y22),
                                                                           xytext=(x11, y11),
                                                                           arrowprops=arrowprops)
                            self.L_arrs.append(arr)

            self.Gr_map.canvas.draw()


    def checkForSpirman(self):                                  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        a = False
        b = False
        for i in self.all_checked:
            if 'НАГ' in i:
                a=True
            if 'НЕФ' in i:
                b=True
            if a and b:
                break
        if a and b:
            self.action_6.setEnabled(True)
        else:
            self.action_6.setEnabled(False)
        if b:
            self.action_chen.setEnabled(True)
            self.action_no.setEnabled(True)
        else:
            self.action_no.setEnabled(False)
        if a:
            self.action_hall.setEnabled(True)
        else:
            self.action_hall.setEnabled(False)




        '''if self.Nag>-1 and 'НЕФ' in self.skvType:
            self.action_6.setEnabled(True)
        else:
            self.action_6.setEnabled(False)
        if self.Nef>-1 and 'НАГ' in self.skvType:
            self.action_7.setEnabled(False)         # Пока заблокированно
        else:
            self.action_7.setEnabled(False)'''


    def load_data_MAP_sql(self):

        try:

            self.skvN, self.skvType, self.skvXX, self.skvYY, self.skvX, self.skvY, self.id, self.h, self.formFK, self.re = sql.getWellFromBD(self.all_checked)


            self.X1 = self.skvX[:]
            self.Y1 = self.skvY[:]
            self.X2 = self.skvXX[:]
            self.Y2 = self.skvYY[:]


            self.currentNagCoord = []
            self.currentNefCoords = []

            Xmin = min(self.skvX)
            Ymin = min(self.skvY)
            xx_ = [i for i in self.skvXX if i != 0]
            yy_ = [i for i in self.skvYY if i != 0]
            if len(xx_)>0:
                xx = min(xx_)
                if Xmin < xx:
                    pass
                else:
                    Xmin = xx
            if len(yy_)>0:
                yy = min(yy_)
                if Ymin < yy:
                    pass
                else:
                    Ymin = yy


            self.skvX = [i-Xmin  for i in self.skvX]
            self.skvY = [i-Ymin  for i in self.skvY]
            self.skvXX = [i-Xmin  for i in self.skvXX]
            self.skvYY = [i-Ymin  for i in self.skvYY]
            #self.skvXX = list(map(lambda c: c*0 if c<0 else c, self.skvXX))
            #self.skvYY = list(map(lambda c: c*0 if c<0 else c, self.skvYY))


            '''self.Nag = -1
            for i in range(len(self.skvType)):
                if self.skvType[i] == "НАГ":
                    self.Nag = i
                    break
            self.Nef = -1
            for i in range(len(self.skvType)):
                if self.skvType[i] == "НЕФ":
                    self.Nef = i
                    break'''


            self.Gr_map.canvas.axes.clear()

            tempX = []
            tempY = []

            for i in range(len(self.skvN)):

                if self.skvType[i] == 'НАГ':
                    clr = 'blue'
                else:
                    clr = 'brown'

                tempX.clear()
                tempY.clear()
                if self.skvXX[i] < 0:
                    tempX.append(self.skvX[i])
                    tempY.append(self.skvY[i])
                else:
                    tempX.append(self.skvX[i])
                    tempY.append(self.skvY[i])
                    tempX.append(self.skvXX[i])
                    tempY.append(self.skvYY[i])
                self.Gr_map.canvas.axes.plot(tempX, tempY, '-', linewidth=4, color=clr)


            for i in range(len(self.skvN)):
                if self.skvType[i] == 'НАГ':
                    clr = 'blue'
                else:
                    clr = 'brown'
                    self.currentNefCoords.append(self.skvX[i])
                    self.currentNefCoords.append(self.skvY[i])
                self.Gr_map.canvas.axes.plot(self.skvX[i], self.skvY[i],
                                         'ko', markersize=10, color=clr, label="Карта скважин")

        except Exception as e:  # Запись  ошибок в лог
            logging.error(str(datetime.now()) + '   ' + str(e)+'   load_data_MAP_sql')


        # self.tomark(self.skvN[0])  # Подписи к точкам
        self.Gr_map.canvas.axes.margins(0.1)
        self.Gr_map.canvas.axes.grid()
        self.Gr_map.canvas.axes.set_title('Карта скважин пласта ')

        if self.xyLims == [0,0,0,0]:
            M1 = max(self.skvX)
            M2 = max(self.skvY)
            if M1 > M2:
                self.M = M1
            else:
                self.M = M2
            self.xyLims = [-350, self.M + 350, -350, self.M + 350]

        self.Gr_map.canvas.axes.set(xlim=(self.xyLims[0],self.xyLims[1]), ylim=(self.xyLims[2],self.xyLims[3]))

        self.Gr_map.canvas.draw()

        # TOMARK
        # self.Gr_map.ax.annotate(self.skvN[1], (self.skvX[1]+50, self.skvY[1]-50), facecolor='cyan')

        for i in range(len(self.skvN)):

            delta = self.M / 80
            deltaX = self.M / 80


            if sql.getWasGRP(self.skvN[i], self.formFK[i]):
                self.Gr_map.canvas.axes.plot(self.skvX[i], self.skvY[i] + delta+delta/2, marker='v', mec='black', lw=1, mew=1,
                                      ms=6, c='wheat')

            #deltaX = self.M / 20
            #if self.skvType[i] == 'НЕФ':
            #    delta = self.M / 20
            #else:
            #    delta = self.M / 20




            #if i == -100:

            formName = ' - ' + mat.getSkvNfromText(self.formFK[i])

            if i == self.Nef or i == self.Nag:
                if i == self.Nag:                              #  Сохранение координат текущей нагнетательной
                    self.currentNagCoord.append(self.skvX[i])
                    self.currentNagCoord.append(self.skvY[i])

                self.Gr_map.canvas.axes.text(self.skvX[i] + deltaX, self.skvY[i] - delta, self.skvN[i]+formName, fontsize=8,
                                             color='red',  weight='bold', bbox={"facecolor": "yellow",
                                                                               "boxstyle": "round",
                                                                               "edgecolor": "red"})  # bbox=dict(facecolor='red', alpha=0.5)
            else:
                self.Gr_map.canvas.axes.text(self.skvX[i] + deltaX, self.skvY[i] - delta, self.skvN[i], fontsize=8,
                                             color='darkslategrey',  weight='bold', bbox={"facecolor": "white",
                                                                                         "boxstyle": "round",
                                                                                         "edgecolor": "black",
                                                                                          "alpha":0.5,})  # bbox=dict(facecolor='red', alpha=0.5))     +' x= '+str(self.skvX[i])+' y= '+str(self.skvY[i])+' xx= '+str(self.skvXX[i])+' yy= '+str(self.skvYY[i])
        # ПРОРИСВКА ФРОНТОВ

        if self.checkBox_front.isChecked():

            try:
                self.radiuses()          # Вычисление радиусов всех выбраных скважин

            except Exception as e:  # Запись  ошибок в лог
                logging.error(str(datetime.now()) + '   ' + str(e)+'   radiuses')

            for i in range(len(self.skvType)):
                if self.skvType[i]=='НАГ':
                    clr='blue'
                else:
                    clr = 'brown'
                if self.skvXX[i]<0:
                    circle = Circle((self.skvX[i], self.skvY[i]), self.R[i], color=clr, fill=True, alpha=0.2)
                    self.Gr_map.canvas.axes.add_patch(circle)  # добавление на карту фигуры - круг
                else:
                    deg = mat.degWell(self.skvX[i], self.skvY[i], self.skvXX[i],self.skvYY[i])
                    boxStyl = "round,pad="+str(self.R[i])
                    p_fancy = FancyBboxPatch((self.skvX[i], self.skvY[i]), mat.lenWell(self.skvX[i], self.skvY[i], self.skvXX[i],self.skvYY[i]), 0,
                                             alpha=0.2,
                                             boxstyle=boxStyl,
                                             transform=Affine2D().rotate_deg_around(*(self.skvX[i], self.skvY[i]), deg) + self.Gr_map.canvas.axes.transData,
                                             fc=(clr),ec=(clr))
                    self.Gr_map.canvas.axes.add_patch(p_fancy)    # добавление на карту фигуры - прямоугольник со скругленными углами

        self.Gr_map.canvas.draw()


        # Прорисовка радиуса охвата

        try:

            rad = int(self.lineRad.text())
            circle2 = Circle((self.currentNagCoord[0], self.currentNagCoord[1]), rad, color='red', fill=False, alpha=1)
            self.Gr_map.canvas.axes.add_patch(circle2)
            self.Gr_map.canvas.draw()
        except:
            pass


    def  radiuses(self):

        accum = sql.getAccumFromBD(self.id, self.skvType)

        self.R = []

        for i in range(len(self.skvType)):
            bo, ro, m, so, so_min, bw, _, _, _ = sql.getFormFromBD(self.formFK[i])
            if self.skvType[i]=='НАГ':
                R = mat.R_nag(accum[i], bw,  self.h[i], m, so, so_min, self.skvX[i], self.skvY[i], self.skvXX[i],self.skvYY[i])
            else:
                R = mat.R_dob(accum[i], bo, ro, self.h[i], m, so, so_min, self.skvX[i], self.skvY[i], self.skvXX[i],self.skvYY[i])
            self.R.append(round(R, 1))
        #print('-------------------------------------------------------------------------------------------')
        #print('Радиусы')
        #print(self.R)
        #print('Суммы добычи жидкости')
        #print(accum)
        #print('Нефтенасыщеная толщина')
        #print(self.h)


    # Подготовка df2 для графика на главном окне,  df, парметров для расчетов и графиков в окне Холла
    def exe_hall(self):

        _ ,self.df2 = sql.getHallFromBD(self.id[self.Nag], self.formFK[self.Nag], param.Edit_minHall.text())
        self.makeGR_hall()


    def makeGR_hall(self):

        D = self.df2['Дата'].tolist()
        Dmin = D[0]
        Dmax = D[-1]

# --------------------------------НОВЫЕ--ГРАФИКИ----------------------------------
        self.Gr_colors = ['white', '#5B9BD5', '#00CCFF', '#C00000', '#8EDC84', 'gray', 'black', 'orangered']

        self.Gr_nag.F.clear()
        self.Gr_nag.reCreate()
        self.Gr_nag_dop1 = self.Gr_nag.canvas.axes.twinx()
        self.Gr_nag_dop2 = self.Gr_nag.canvas.axes.twinx()
        self.Gr_nag_dop3 = self.Gr_nag.canvas.axes.twinx()
        self.Gr_nag_dop4 = self.Gr_nag.canvas.axes.twinx()
        self.Gr_nag_dop4.set_yticklabels([])

        self.Gr_nag.canvas.axes.clear()
        self.Gr_nag_dop1.clear()  # ось давления
        self.Gr_nag_dop2.clear()  # ось времени работы
        self.Gr_nag_dop3.clear()  # ось диаметра штуцера
        self.Gr_nag_dop4.clear()  # ось ГРП
        # self.Gr_nag_dop5.clear()
        # self.Gr_nag_dop6.clear()

        # self.Gr_nag_dop1.spines['right'].set_position(('axes', 1.05))
        self.Gr_nag_dop2.spines['right'].set_position(('axes', 1.05))
        # self.Gr_nag_dop4.spines['right'].set_position(('axes',1.09))
        self.Gr_nag_dop3.spines['right'].set_position(('axes', 1.1))

        self.Gr_nag.canvas.axes.tick_params(axis='y', colors='blue')
        self.Gr_nag_dop1.tick_params(axis='y', colors=self.Gr_colors[3])
        self.Gr_nag_dop2.tick_params(axis='y', colors=self.Gr_colors[5])
        #self.Gr_nag_dop4.set_yticklabels([])
        self.Gr_nag_dop3.tick_params(axis='y', colors=self.Gr_colors[4])
        self.Gr_nag_dop4.tick_params(axis='y', colors=self.Gr_colors[0])

        self.Gr_nag.canvas.axes.set_title('Основные эксплуатационные показатели   скв. ' + self.skvN[self.Nag])

        self.doGrNag1()
        self.doGrNag2()
        self.doGrNag3()
        self.doGrNag4()
        self.doGrNag5()
        self.doGrNag6()
        # self.doGrNag7()

        self.Gr_nag.canvas.axes.grid()

        self.Gr_nag.canvas.axes.set_ylabel("Приемистость, м3/сут", color=self.Gr_colors[1])
        self.Gr_nag_dop1.set_ylabel("Давление, атм", color=self.Gr_colors[3])
        self.Gr_nag_dop2.set_ylabel("Время работы, часы", color=self.Gr_colors[5])
        self.Gr_nag_dop3.set_ylabel("Диаметр штуцера, мм", color=self.Gr_colors[4])
        # self.Gr_nag_dop4.set_ylabel("Диаметр штуцера", color=self.Gr_colors[6])
        # self.Gr_nag_dop5.set_ylabel("grp", color=self.Gr_colors[7])

        self.Gr_nag.canvas.draw()


    def changeGrNag(self):
        if self.Nag != -1:
            if self.sender().objectName() == 'checkBox_Nag1':
                self.GrNag1.set_visible(not self.GrNag1.get_visible())
                self.GrNag11.set_visible(not self.GrNag11.get_visible())
            if self.sender().objectName() == 'checkBox_Nag2':
                self.GrNag2.set_visible(not self.GrNag2.get_visible())
            if self.sender().objectName() == 'checkBox_Nag3':
                self.GrNag3.set_visible(not self.GrNag3.get_visible())
            if self.sender().objectName() == 'checkBox_Nag4':
                self.GrNag4.set_visible(not self.GrNag4.get_visible())
            if self.sender().objectName() == 'checkBox_Nag5':
                self.GrNag5.set_visible(not self.GrNag5.get_visible())
                self.GrNag55.set_visible(not self.GrNag55.get_visible())
            if self.sender().objectName() == 'checkBox_Nag6':
                self.doGrNag6()

            # if self.sender().objectName() == 'checkBox_Nag7':
            #     self.GrNag7.set_visible(not self.GrNag7.get_visible())
            self.Gr_nag.canvas.draw()


    def doGrNag1(self):  # Прием МЭР


        self.GrNag1, = self.Gr_nag.canvas.axes.plot(self.df2['Дата'],
                                                    self.df2['Приемистость за последний месяц, м3/сут'],
                                                    color=self.Gr_colors[1])
        self.GrNag11 = self.Gr_nag.canvas.axes.fill_between(self.df2['Дата'],
                                                            self.df2['Приемистость за последний месяц, м3/сут'],
                                                            color=self.Gr_colors[1])
        #self.GrNag111 = self.Gr_nag.canvas.axes.plot(self.df2['Дата'],
        #                                                    self.df2['Приемистость за последний месяц, м3/сут'],'o',ms=4,
        #                                                    color=self.Gr_colors[1])
        self.GrNag1.set_visible(self.checkBox_Nag1.isChecked())
        self.GrNag11.set_visible(self.checkBox_Nag1.isChecked())


    def doGrNag2(self):  # Прием ТР

        self.GrNag2, = self.Gr_nag.canvas.axes.plot(self.df2['Дата'], self.df2['Приемистость (ТР), м3/сут'],
                                                    color=self.Gr_colors[2])
        self.GrNag2.set_visible(self.checkBox_Nag2.isChecked())

    def doGrNag3(self):  # Давление

        self.GrNag3, = self.Gr_nag_dop1.plot(self.df2['Дата'], self.df2['Забойное давление (ТР), атм'],
                                             color=self.Gr_colors[3])
        #self.GrNag33, = self.Gr_nag_dop1.plot(self.df2['Дата'], self.df2['Забойное давление (ТР), атм'],'o',ms=2,
        #                                     color=self.Gr_colors[3])
        self.GrNag3.set_visible(self.checkBox_Nag3.isChecked())

    def doGrNag4(self):  # Время работы

        self.GrNag4, = self.Gr_nag_dop2.plot(self.df2['Дата'], self.df2['Время работы под закачкой, часы'], 'x',ms=3,
                                             color=self.Gr_colors[5])
        self.GrNag4.set_visible(self.checkBox_Nag4.isChecked())

    def doGrNag5(self):  # Штуцер

        self.GrNag5, = self.Gr_nag_dop3.plot(self.df2['Дата'], self.df2['Диаметр штуцера, мм'], color=self.Gr_colors[4])
        self.GrNag55, = self.Gr_nag_dop3.plot(self.df2['Дата'], self.df2['Диаметр штуцера, мм'],'o',ms=2, color=self.Gr_colors[4])
        self.GrNag5.set_visible(self.checkBox_Nag5.isChecked())
        self.GrNag55.set_visible(self.checkBox_Nag5.isChecked())

    def doGrNag6(self):  # events

        if self.checkBox_Nag6.isChecked():

            self.Gr_nag_dop4.set_ylim([0, 500])
            self.Gr_nag_dop4.set_yticklabels([])

            d = self.df2['Дата'].tolist()
            g = self.df2['ГТМ'].tolist()
            Y = 60

            for i in range(len(d)):

                if g[i]==g[i]:

                    if Y == 60:
                        Y = 40
                    elif Y ==40:
                        Y = 20
                    else:
                        Y = 60

                    self.Gr_nag_dop4.text(d[i], Y, mat.gtm_names(g[i]), fontsize=6,
                                          color='aqua', weight='bold', bbox={"facecolor": "black",
                                                                             "boxstyle": "round",
                                                                             "edgecolor": "black",
                                                                             "alpha":0.9})
                    Y2 = [0,Y]
                    d2 = [d[i],d[i]]
                    self.Gr_nag_dop4.plot(d2, Y2,  color='black', linewidth=1)

        else:
            self.Gr_nag_dop4.clear()

            d = self.df2['Дата'].tolist()
            self.Gr_nag_dop4.text(d[0], 0, '', fontsize=1)
            self.Gr_nag_dop4.plot(d[0], 0, color='black', linewidth=1)


    def exe_chen(self):

        self.df3, self.df4 = sql.getChenFromBD(self.id[self.Nef], self.formFK[self.Nef])
        self.makeGR_chen()


    def makeGR_chen(self):

        # --------------------------------НОВЫЕ--ГРАФИКИ--ЧЕН-----------------------------
        self.Gr_colors = ['white', '#72A8DA', '#0070C0', '#DCB24C', '#745F2A', '#00CCFF', '#C00000', '#FF0062', 'dodgerblue', 'aqua',
                          'blue', 'peru', 'orangered', 'deepskyblue', 'sienna']

        self.Gr_nef.F.clear()
        self.Gr_nef.reCreate()
        self.Gr_nef_dop1 = self.Gr_nef.canvas.axes.twinx()
        self.Gr_nef_dop2 = self.Gr_nef.canvas.axes.twinx()
        self.Gr_nef_dop3 = self.Gr_nef.canvas.axes.twinx()
        self.Gr_nef_dop4 = self.Gr_nef.canvas.axes.twinx()

        self.Gr_nef.canvas.axes.clear()
        self.Gr_nef_dop1.clear()
        self.Gr_nef_dop2.clear()
        self.Gr_nef_dop3.clear()
        self.Gr_nef_dop4.clear()

        self.Gr_nef_dop2.spines['right'].set_position(('axes', 1.05))
        self.Gr_nef_dop3.spines['right'].set_position(('axes', 1.1))
        # self.Gr_nef_dop3.spines['right'].set_position(('axes', 1.15))

        self.Gr_nef.canvas.axes.tick_params(axis='y', colors='navy')
        self.Gr_nef_dop1.tick_params(axis='y', colors=self.Gr_colors[5])
        self.Gr_nef_dop2.tick_params(axis='y', colors=self.Gr_colors[6])
        self.Gr_nef_dop3.tick_params(axis='y', colors=self.Gr_colors[8])
        self.Gr_nef_dop4.tick_params(axis='y', colors=self.Gr_colors[0])

        self.Gr_nef.canvas.axes.set_title('Основные эксплуатационные показатели   скв. ' + self.skvN[self.Nef])

        #self.Gr_nef.canvas.axes.set_ylim(bottom = 0)
        self.doGrNef1()
        self.doGrNef2()
        self.doGrNef3()
        self.doGrNef4()
        self.doGrNef5()

        self.Gr_nef.canvas.axes.grid()

        self.Gr_nef.canvas.axes.set_ylabel("Дебит, т/сут", color='navy')
        self.Gr_nef_dop1.set_ylabel("Обводненность, %", color=self.Gr_colors[5])
        self.Gr_nef_dop2.set_ylabel("Давление, атм", color=self.Gr_colors[6])
        self.Gr_nef_dop3.set_ylabel("Динамический уровень, м", color=self.Gr_colors[8])
        # self.Gr_nef_dop4.set_ylabel("ГРП", color=self.Gr_colors[11])

        self.Gr_nef.canvas.draw()

    def changeGrNef(self):
        if self.Nef != -1:
            if self.sender().objectName() == 'checkBox_Nef1':
                self.GrNef1.set_visible(not self.GrNef1.get_visible())
            if self.sender().objectName() == 'checkBox_Nef2':
                self.GrNef11.set_visible(not self.GrNef11.get_visible())
            if self.sender().objectName() == 'checkBox_Nef3':
                self.GrNef12.set_visible(not self.GrNef12.get_visible())
            if self.sender().objectName() == 'checkBox_Nef4':
                self.GrNef13.set_visible(not self.GrNef13.get_visible())
            if self.sender().objectName() == 'checkBox_Nef5':
                self.GrNef2.set_visible(not self.GrNef2.get_visible())
            if self.sender().objectName() == 'checkBox_Nef6':
                self.GrNef3.set_visible(not self.GrNef3.get_visible())
            if self.sender().objectName() == 'checkBox_Nef7':
                self.GrNef4.set_visible(not self.GrNef4.get_visible())
            if self.sender().objectName() == 'checkBox_Nef8':
                self.GrNef5.set_visible(not self.GrNef5.get_visible())
            if self.sender().objectName() == 'checkBox_Nef9':
                self.GrNef6.set_visible(not self.GrNef6.get_visible())
            if self.sender().objectName() == 'checkBox_Nef10':
                self.doGrNef5()
            self.Gr_nef.canvas.draw()

    def doGrNef1(self):  # Дебит

        self.GrNef1 = self.Gr_nef.canvas.axes.fill_between(self.df4['Дата'],
                                                           self.df4['Дебит жидкости за последний месяц, т/сут'],
                                                           color=self.Gr_colors[1])
        self.GrNef11, = self.Gr_nef.canvas.axes.plot(self.df4['Дата'], self.df4['Дебит жидкости (ТР), м3/сут'],
                                                     color=self.Gr_colors[2])
        self.GrNef12 = self.Gr_nef.canvas.axes.fill_between(self.df4['Дата'],
                                                            self.df4['Дебит нефти за последний месяц, т/сут'],
                                                            color=self.Gr_colors[3])
        self.GrNef13, = self.Gr_nef.canvas.axes.plot(self.df4['Дата'], self.df4['Дебит нефти (ТР), т/сут'],
                                                     color=self.Gr_colors[4])

        self.GrNef1.set_visible(self.checkBox_Nef1.isChecked())
        self.GrNef11.set_visible(self.checkBox_Nef2.isChecked())
        self.GrNef12.set_visible(self.checkBox_Nef3.isChecked())
        self.GrNef13.set_visible(self.checkBox_Nef4.isChecked())

    # Слайдер для изменения предела оси У дебета------------------------------
        y = self.Gr_nef.canvas.axes.get_ylim()[1]

        try:
            self.ax.remove()
        except:
            pass
        self.ax = self.Gr_nef.F.add_axes([0.05, 0.11, 0.01, 0.77])
        self.Gr_nef.F.subplots_adjust(left=0.055)

        self.slid = Slider(
            ax=self.ax,
            label="",
            valmin=0,
            valmax=y,
            valinit=y,
            orientation="vertical"
        )

        self.slid.on_changed(self.update)

    def update(self, val):
        self.Gr_nef.canvas.axes.set_ylim(top=self.slid.val, bottom = 0)
        #fig.canvas.draw_idle()
    #--слайдер---------------------------------------------------------


    def doGrNef2(self):  # Обводненость

        self.GrNef2, = self.Gr_nef_dop1.plot(self.df4['Дата'], self.df4['Обводненность за посл.месяц, % (вес)'],
                                             color=self.Gr_colors[5])
        self.GrNef2.set_visible(self.checkBox_Nef5.isChecked())

        self.GrNef3, = self.Gr_nef_dop1.plot(self.df4['Дата'], self.df4['Обводненность (ТР), % (объём)'],':',
                                             color=self.Gr_colors[5])
        self.GrNef3.set_visible(self.checkBox_Nef6.isChecked())

    def doGrNef3(self):  # Давление

        self.GrNef4, = self.Gr_nef_dop2.plot(self.df4['Дата'], self.df4['Забойное давление (ТР), атм'],
                                             color=self.Gr_colors[6])
        self.GrNef4.set_visible(self.checkBox_Nef7.isChecked())

        self.GrNef5, = self.Gr_nef_dop2.plot(self.df4['Дата'], self.df4['Пластовое давление (ТР), атм'],
                                             color=self.Gr_colors[7])
        self.GrNef5.set_visible(self.checkBox_Nef8.isChecked())

    def doGrNef4(self):  # Дин. уровень

        self.GrNef6, = self.Gr_nef_dop3.plot(self.df4['Дата'], self.df4['Динамический уровень (ТР), м'],
                                             color=self.Gr_colors[8])
        self.GrNef6.set_visible(self.checkBox_Nef9.isChecked())

    def doGrNef5(self):  # GRP

        if self.checkBox_Nef10.isChecked():

            self.Gr_nef_dop4.set_ylim([0, 500])
            self.Gr_nef_dop4.set_yticklabels([])

            d = self.df4['Дата'].tolist()
            g = self.df4['ГТМ'].tolist()
            Y = 60

            for i in range(len(d)):

                if g[i]==g[i]:

                    if Y == 60:
                        Y = 40
                    elif Y ==40:
                        Y = 20
                    else:
                        Y = 60

                    self.Gr_nef_dop4.text(d[i], Y, mat.gtm_names(g[i]), fontsize=6,
                                          color='darkorange', weight='bold', bbox={"facecolor": "black",
                                                                             "boxstyle": "round",
                                                                             "edgecolor": "black",
                                                                             "alpha":0.9})
                    Y2 = [0,Y]
                    d2 = [d[i],d[i]]
                    self.Gr_nef_dop4.plot(d2, Y2,  color='black', linewidth=2)

        else:
            self.Gr_nef_dop4.clear()

            d = self.df4['Дата'].tolist()
            self.Gr_nef_dop4.text(d[0], 0, '', fontsize=1)
            self.Gr_nef_dop4.plot(d[0], 0, color='black', linewidth=1)

    def load_hall(self):
        if self.Nag != -1:
            hall_window.doGrHall()
            hall_window.show()


    def load_hall2(self):
        l = []
        f = []
        R = []
        h = []
        re = []

        for i in range(len(self.all_checked)):
            if 'НАГ' in self.all_checked[i]:
                l.append(self.all_checked[i])
                f.append(self.formFK[i])
                R.append(self.R[i])
                h.append(self.h[i])
                re.append(self.re[i])
        hall_window.allWell = l
        hall_window.forms = f
        hall_window.R = R
        hall_window.h = h
        hall_window.re = re
        hall_window.minHall = param.Edit_minHall.text()
        hall_window.rdp = param.Edit_rdp.text()
        hall_window.show()
        hall_window.doHall()


    def load_chen2(self):

        l = []
        f = []
        for i in range(len(self.all_checked)):
            if 'НЕФ' in self.all_checked[i]:
                l.append(self.all_checked[i])
                f.append(self.formFK[i])
        chen_window2.allWell = l[:]
        chen_window2.forms = f[:]
        chen_window2.show()
        chen_window2.doChen()

    def load_no(self):

        l = []
        f = []
        for i in range(len(self.all_checked)):
            if 'НЕФ' in self.all_checked[i]:
                l.append(self.all_checked[i])
                f.append(self.formFK[i])
        no.allWell = l[:]
        no.forms = f[:]
        no.doNO()
        no.show()

    def load_word(self):
        os.startfile('Руководство пользователя ПИ Прогноз НОиЗ.docx')

    def doReportAll(self):

        self.doReport(0)

    def doReport(self, type_rep):   # подготовка данных для отчета

        NOtoAllRep = []

        if type_rep == 3:
            if len(self.listNOReport) > 0:
                data = []
                for i in range(len(self.listNOReport)):
                    tmp = []
                    if self.listNOReport[i].df_result.shape[0] > 0:
                        tmp.append(self.listNOReport[i].df_result.loc[0, 'Скважина'])


                        if self.listNOReport[i].df_breakthrough.shape[0] > 0:
                            tmp.append(str(self.listNOReport[i].df_breakthrough.loc[0, 'Дата начала роста ВНФ'])[:7])
                            tmp.append(self.listNOReport[i].df_breakthrough.loc[0, 'qн до роста ВНФ, т/сут'])
                            tmp.append(self.listNOReport[i].df_breakthrough.loc[0, 'qж до роста ВНФ, т/сут'])
                            tmp.append(self.listNOReport[i].df_breakthrough.loc[0, '% воды до роста ВНФ'])

                            tmp.append(self.listNOReport[i].qo_curr)
                            tmp.append(self.listNOReport[i].ql_curr)
                            tmp.append(self.listNOReport[i].w_curr)


                            tmp.append(self.listNOReport[i].df_breakthrough.loc[0, 'qн прогноз, т/сут'])
                            tmp.append(self.listNOReport[i].df_breakthrough.loc[0, 'qж прогноз, т/сут'])
                            tmp.append(self.listNOReport[i].df_breakthrough.loc[0, '% воды прогноз'])

                            tmp.append(self.listNOReport[i].df_breakthrough.loc[0, 'Сокращение дебита воды (прогноз qн), т/сут'])
                            tmp.append(self.listNOReport[i].df_breakthrough.loc[0, 'Текущий НО воды (прогноз qн), т'])
                            tmp.append(self.listNOReport[i].df_breakthrough.loc[0, 'Сокращение дебита воды (текущий qн), т/сут'])
                            tmp.append(self.listNOReport[i].df_breakthrough.loc[0, 'Текущий НО воды (текущий qн), т'])

                        else:
                            for k in range(14):
                                if k==4:
                                    tmp.append(self.listNOReport[i].qo_curr)
                                elif k==5:
                                    tmp.append(self.listNOReport[i].ql_curr)
                                elif k==6:
                                    tmp.append(self.listNOReport[i].w_curr)
                                else:
                                    tmp.append('-')


                        tmp.append(self.listNOReport[i].df_result.loc[0, 'Заключение'])
                        data.append(tmp)

                try:

                    excl.setExcelReportNO(data)
                except Exception as e:
                    no.errorRep()
                    logging.error(str(datetime.now()) + '   ' + str(e) + '   setExcelReportNO')
            else:
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Нет данных для отчета")

    ######################################################################################
        if type_rep == 2:
            if len(self.listChenReport) > 0:
                data = []
                for i in range(len(self.listChenReport)):
                    tmp = []
                    L2 = sql.getForReportNEF(self.listChenReport[i].NefID)
                    if self.listChenReport[i].df_result.shape[0] > 0:
                        water_source = str(self.listChenReport[i].df_result.loc[
                                               self.listChenReport[i].df_result.shape[0] - 1, 'Нарушение'])
                    else:
                        water_source = 'Не выявлено'
                    tmp.extend(L2)
                    tmp.extend([water_source])
                    data.append(tmp)
                try:
                    excl.setExcelReportChen(data)
                except Exception as e:
                    chen_window2.errorRep()
                    logging.error(str(datetime.now()) + '   ' + str(e) + '   setExcelReportChen')
            else:
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Нет данных для отчета")


        if type_rep == 0 or type_rep == 1:
            if len(self.listSpearReport)>0:

                data = []

                for i in range(len(self.listSpearReport)):

                    tmp = []

                    nagID = self.listSpearReport[i].NagID
                    nefID = self.listSpearReport[i].NefID

                    lenWell = self.listSpearReport[i].lenWell

                    dat1 = self.listSpearReport[i].range_start_D
                    dat2 = self.listSpearReport[i].range_fin_D

                    L1 = sql.getForReportNAG(nagID)
                    L2 = sql.getForReportNEF(nefID)

                    if self.listSpearReport[i].right_range:
                        S, clr = mat.spearDecodeK(self.listSpearReport[i].K)
                        lag = self.listSpearReport[i].Kl_lag
                        lag2 = self.listSpearReport[i].Kp_lag
                        Kl = self.listSpearReport[i].Kl
                        Ko = self.listSpearReport[i].Ko
                        Kp = self.listSpearReport[i].Kp
                        if Kp==-1:
                            Kp = ''
                        Kw = self.listSpearReport[i].df_out['W'].tolist()[lag]
                        Ks = self.listSpearReport[i].df_out['S'].tolist()[lag]
                    else:
                        S, clr = 'Нет совместной работы', 'white'
                        lag = '-'
                        lag2 = '-'
                        Kl = '-'
                        Ko = '-'
                        Kp = '-'
                        Kw = '-'
                        Ks = '-'

                    # Добавление в общий отчет информацию из Чена, если есть
                    if len(self.listChenReport) > 0:

                        for v in range(len(self.listChenReport)):
                            if self.listChenReport[v].NefID == nefID:
                                ind = v
                                break
                        if self.listChenReport[ind].df_result.shape[0] > 0:
                            water_source = str(self.listChenReport[ind].df_result.loc[
                                                   self.listChenReport[ind].df_result.shape[0] - 1, 'Нарушение'])
                        else:
                            water_source = ' '
                    else:
                        water_source = ' '

                    # Добавление в общий отчет информацию из НО, если есть

                    if len(self.listNOReport) > 0:

                        NOtoAllRep = ['-', '-', '-', '-', '-']

                        for v in range(len(self.listNOReport)):
                            if self.listNOReport[v].NefID == nefID:
                                ind = v
                                break


                        if  self.listNOReport[ind].df_result.shape[0] > 0:

                            if self.listNOReport[ind].df_breakthrough.shape[0] > 0:

                                NOtoAllRep = []

                                NOtoAllRep.append(self.listNOReport[ind].df_breakthrough.loc[0, 'qн прогноз, т/сут'])
                                NOtoAllRep.append(self.listNOReport[ind].df_breakthrough.loc[0, 'qж прогноз, т/сут'])
                                NOtoAllRep.append(self.listNOReport[ind].df_breakthrough.loc[0, '% воды прогноз'])

                                NOtoAllRep.append(self.listNOReport[ind].df_breakthrough.loc[0, 'Текущий НО воды (прогноз qн), т'])
                                NOtoAllRep.append(self.listNOReport[ind].df_breakthrough.loc[0, 'Сокращение дебита воды (текущий qн), т/сут'])


                    tmp.extend(L1)
                    if type_rep==0:
                        tmp.insert(3, self.listSpearReport[i].FNV)
                    #tmp.extend(['', '', '', ''])
                    tmp.extend(L2)
                    if type_rep == 0:
                        tmp.insert(11, self.listSpearReport[i].KP)
                    tmp.extend([water_source])
                    if len(self.listNOReport) > 0 and type_rep ==0:
                        tmp.extend(NOtoAllRep)
                    #tmp.extend(['', '', '', '', ''])
                    tmp.extend([round(lenWell,0)])
                    tmp.extend([lag, Kl, Ko, Kw, Ks, lag2, Kp, S])
                    tmp.extend([dat1, dat2])
                    tmp.extend([clr])

                    data.append(tmp)

                if type_rep==0:
                    try:

                        excl.setExcelReportAll(data, len(NOtoAllRep))
                    except Exception as e:
                        if '[Errno 2]' in str(e):
                            QtWidgets.QMessageBox.critical(self, "Ошибка", "Отсутствует папка Отчеты в директории программы")
                        QtWidgets.QMessageBox.critical(self, "Ошибка", "Ошибка при создании файла (общий отчет). Возможно файл уже открыт")
                        logging.error(str(datetime.now()) + '   ' + str(e) + '   setExcelReportAll')

                if type_rep==1:
                    try:
                        excl.setExcelReportSpear(data)
                    except Exception as e:
                        if '[Errno 2]' in str(e):
                            QtWidgets.QMessageBox.critical(self, "Ошибка", "Отсутствует папка Отчеты в директории программы")
                        spirman.errorRep()
                        logging.error(str(datetime.now()) + '   ' + str(e) + '   setExcelReportSpear')

            else:

                QtWidgets.QMessageBox.critical(self, "Ошибка", "Нет данных для отчета (Спирмен)")

    ######################################################################################


        '''df_rep = sql.doRepDataframe()



       # if len(self.listChenReport) > 0:
        #    for

        for i in range(len(self.listSpearReport)):

            tmp = []

            nagID = self.listSpearReport[i].NagID
            nefID = self.listSpearReport[i].NefID


            lenWell = self.listSpearReport[i].lenWell

            L1 = sql.getForReportNAG(nagID)
            L2 = sql.getForReportNEF(nefID)



            if self.listSpearReport[i].right_range:
                S, clr = mat.spearDecodeK(self.listSpearReport[i].K)
                lag = self.listSpearReport[i].Kl_lag
                lag2 = self.listSpearReport[i].Kp_lag
                Kl = self.listSpearReport[i].Kl
                Ko = self.listSpearReport[i].Ko
                Kp = self.listSpearReport[i].Kp
                Kw = self.listSpearReport[i].df_out['W'].tolist()[lag]
                Ks = self.listSpearReport[i].df_out['S'].tolist()[lag]
            else:
                S, clr = '  ',  'white'
                lag = ''
                lag2 = ''
                Kl = ''
                Ko = ''
                Kp = ''
                Kw = ''
                Ks = ''




            if len(self.listChenReport) > 0:

                for v in range(len(self.listChenReport)):
                    if self.listChenReport[v].NefID == nefID:
                        ind = v
                        break
                if self.listChenReport[ind].df_result.shape[0] > 0:
                    water_source = str(self.listChenReport[ind].df_result.loc[self.listChenReport[ind].df_result.shape[0] - 1, 'Нарушение'])
                else:
                    water_source = ' '
            else:
                water_source = ' '


            tmp.extend(L1)
            tmp.extend(['','','',''])
            tmp.extend(L2)
            tmp.extend([water_source])
            tmp.extend(['', '', '', '',''])
            tmp.extend([lenWell])
            tmp.extend([lag,Kl,Ko,Kw,Ks,lag2,Kp,S,' '])

            df_rep.loc[len(df_rep.index)] = tmp

        df_rep.to_excel('Отчеты\Общий отчет.xlsx')'''


class Param(QtWidgets.QDialog):
    def __init__(self):
        super(Param, self).__init__()
        loadUi("Param.ui", self)
        self.But_param_ok.clicked.connect(self.clos)
        self.Edit_elektr.setInputMask('999999')
        self.Edit_res.setInputMask('999999')
        self.Edit_KRS.setInputMask('999999')
        self.Edit_RIR.setInputMask('999999')
        self.Edit_forecast.setInputMask('99')

        validator = QtGui.QRegExpValidator(QRegExp("([-]{0,1})([0-9]{0,9})([.]{0,1}[0-9]{0,100})"))
        self.lineEdit_rdp.setValidator(validator)
        self.lineEdit_min_interval.setValidator(validator)
        self.lineEdit_points.setValidator(validator)

        self.lineEdit_rdpNO.setValidator(validator)
        self.lineEdit_pointsNO.setValidator(validator)



    def clos(self):
        self.close()


class Edit3(QtWidgets.QDialog):
    def __init__(self):
        super(Edit3, self).__init__()
        loadUi("Edit3.ui", self)
        self.pushButton.clicked.connect(self.save)


    def save(self):
        a = self.comboBox.currentText()
        self.close()
        first_window.moveWells(a)


class Edit2(QtWidgets.QDialog):
    def __init__(self):
        super(Edit2, self).__init__()
        loadUi("Edit2.ui", self)
        self.pushButton.clicked.connect(self.rec)
        self.wellID = ''

    def rec(self):
        h = edit2.HEdit.text()
        re = edit2.reEdit.text()

        if  mat.toFloat(h)<=0 or mat.toFloat(re)<=0:
            R = True
        else:
            R = False

        if  R:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Данные не корректные " )
        else:
            L = [h, re]
            try:
                sql.updateWell(self.wellID, L)
                QtWidgets.QMessageBox.information(self, "OK", "Данные изменены")
            except:
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Данные не изменены " )


class Edit(QtWidgets.QDialog):
    def __init__(self):
        super(Edit, self).__init__()
        loadUi("Edit.ui", self)
        self.pushButton.clicked.connect(self.rec)
        self.formID = ''


    def rec(self):
        bo = edit.boEdit.text()
        ro = edit.roEdit.text()
        m = edit.mEdit.text()
        so = edit.soEdit.text()
        so_min = edit.so_minEdit.text()
        bw = edit.bwEdit.text()
        kw = edit.kwEdit.text()
        mu = edit.muEdit.text()
        pn = edit.PEdit.text()

        R = mat.isFloat(bo) or mat.isFloat(ro) or mat.isFloat(m) or\
            mat.isFloat(so) or mat.isFloat(so_min) or mat.isFloat(bw) or mat.isFloat(kw) or  mat.isFloat(mu) or  mat.isFloat(pn)

        try:
            if so<=so_min:
                R = True
        except:
            pass


        if  R:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Данные не корректные " )
        else:
            L = [bo,ro,m,so,so_min,bw,kw,mu,pn]
            try:
                sql.updateForm(self.formID, L)
                QtWidgets.QMessageBox.information(self, "OK", "Данные изменены")
            except:
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Данные не изменены " )

    def clos(self):
        self.close()


class EVT(QtWidgets.QDialog):
    def __init__(self):
        super(EVT, self).__init__()
        loadUi("Events.ui", self)
        self.But_load_evt.clicked.connect(self.load_data_evt)
        self.But_del_gtm_all.clicked.connect(self.del_all)
        self.But_evt_to_BD.clicked.connect(self.evt_to_BD)
        self.But_del_gtm.clicked.connect(self.evt_del)
        self.But_gtm_back.clicked.connect(self.evt_back)
        self.tableBDevt.setColumnWidth(0, 80)
        self.tableBDevt.setColumnWidth(1, 110)
        self.tableBDevt.setColumnWidth(2, 70)
        self.tableBDevt.setColumnWidth(3, 70)
        self.tableBDevt.setColumnWidth(4, 110)
        self.tableBDevt.setColumnWidth(5, 110)
        self.tableBDevt.setColumnWidth(6, 300)



        self.a = -1
        self.dict = {}

        self.tableBDevt.itemSelectionChanged.connect(self.on_selectItm)


        self.typesEvent = ['ВПП',
                      'Дострел',
                      'ИДН',
                      'Кислотная ОПЗ',
                      'Механизация',
                      'Оптимизация',
                      'Перестрел',
                      'Подъем Рзак',
                      'Промывка/нормализация',
                      'Прочие ОПЗ',
                      'Ревизия ППД',
                      'РИР',
                      'ГРП',
                      'Приобщение пласта',
                      'Смена ЭЦН',
                      'Прочие ГТМ',
                      'Не учитывать ГТМ']


    def del_all(self):
        q = QtWidgets.QMessageBox.question(self, "NOIZ", "Удалить из базы все ГТМ?",
                                           defaultButton=QtWidgets.QMessageBox.No)

        if q == 16384:
            sql.delEVT_All()
            self.tableBDevt.setRowCount(0)


    def evt_back(self):

        try:
            curr = self.tableBDevt.currentRow()

            for key in self.dict:
                l = self.dict[key]
                if curr in l:
                    l.pop(0)
                    for itm in l:
                        self.event[itm] = key
                    break
            self.tableBDevt.setRowCount(0)
            self.tableBDevt.setRowCount(len(self.D1))
            self.fillTable()
            self.a = -1

        except:
            print('??????????????????????')


    def onChangedCombo(self):


        b =  self.tableBDevt.item(self.a, 6).text()
        c = self.comboTypeEv.currentText()

        if b!=c:


            tmp=[]
            for i in range(len(self.event)):
                if self.event[i] == b:
                    self.event[i] = c
                    tmp.append(i)
            tmp.insert(0,c)
            self.dict[b] = tmp

               #self.GL.addWidget(self.comboTypeEv)
            #self.tableBDevt.clear()
        self.tableBDevt.setRowCount(0)
        self.tableBDevt.setRowCount(len(self.D1))

        self.fillTable()

        self.a = -1

        self.But_gtm_back.setEnabled(False)




    def  on_selectItm(self):

        s = ''
        try:
            s = self.tableBDevt.item(self.tableBDevt.currentRow(), 6).text()
            self.But_gtm_back.setEnabled(True)

        except:
            pass


        if s not in self.typesEvent:


            self.comboTypeEv = QComboBox()

            #item = QtGui.QStandardItem(s)
            #item.setForeground(QtGui.QColor('red'))
            #self.comboTypeEv.addItem(item)

            '''self.combo_box.setStyleSheet("QListView"
                                         "{"
                                         "background-color: lightgreen;"
                                         "}")'''
            self.comboTypeEv.addItem(s)
            self.comboTypeEv.setItemData(0, QtGui.QColor('red'), Qt.BackgroundRole)
            self.comboTypeEv.addItem("ВПП")
            self.comboTypeEv.addItem("Дострел")
            self.comboTypeEv.addItem("ИДН")
            self.comboTypeEv.addItem("Кислотная ОПЗ")
            self.comboTypeEv.addItem("Механизация")
            self.comboTypeEv.addItem("Оптимизация")
            self.comboTypeEv.addItem("Перестрел")
            self.comboTypeEv.addItem("Подъем Рзак")
            self.comboTypeEv.addItem("Промывка/нормализация")
            self.comboTypeEv.addItem("Прочие ОПЗ")
            self.comboTypeEv.addItem("Ревизия ППД")
            self.comboTypeEv.addItem("РИР")
            self.comboTypeEv.addItem("ГРП")
            self.comboTypeEv.addItem("Приобщение пласта")
            self.comboTypeEv.addItem("Смена ЭЦН")
            self.comboTypeEv.addItem("Прочие ГТМ")
            self.comboTypeEv.addItem("Не учитывать ГТМ")


            self.comboTypeEv.activated[str].connect(self.onChangedCombo)

            if self.a == -1:
                self.a = self.tableBDevt.currentRow()
                self.tableBDevt.setCellWidget(self.a, 6, self.comboTypeEv)
                self.But_gtm_back.setEnabled(False)



    def evt_del(self):

        q = QtWidgets.QMessageBox.question(self, "NOIZ", "Удалить выбранный ГТМ?", defaultButton=QtWidgets.QMessageBox.No)

        if q == 16384:

            t=[]
            a = self.tableBDevt.currentRow()
            if a!= -1:

                try:
                    x = self.tableBDevt.item(a, 0).text()+'-01 00:00:00'
                    t.append(x)
                    x = self.tableBDevt.item(a, 2).text()
                    t.append(x)
                    x = self.tableBDevt.item(a, 3).text()
                    t.append(x)
                    x = self.tableBDevt.item(a, 4).text()+'|'+self.tableBDevt.item(a, 1).text()+'|'
                    t.append(x)
                    x = self.tableBDevt.item(a, 6).text()
                    t.append(x)
                    t = tuple(t)
                    sql.delEVT(t)
                    QtWidgets.QMessageBox.information(self, "OK", "Данные по ГТМ удалены")
                    self.get_data_evt()
                except:
                    QtWidgets.QMessageBox.critical(self, "Ошибка", "Данные не удалены")

            else:
                QtWidgets.QMessageBox.information(self, "OK", "Выделите нужный ГТМ")





    def clos(self):
        self.close()

    def load_data_evt__________________(self):


        df_evt, err = sql.getExcel_evt(QtWidgets.QFileDialog.getOpenFileName()[0])
        if err == 2:

            dat = df_evt['D'].tolist()
            opt = df_evt['OPT'].tolist()
            opz = df_evt['OPZ'].tolist()
            pvlg = df_evt['PVLG'].tolist()


            self.tableBDevt.setRowCount(len(dat))

            for j in range(len(dat)):
                item = QTableWidgetItem(str(dat[j])[:7])
                self.tableBDevt.setItem(j, 0, item)
                item = QTableWidgetItem(opt[j])
                self.tableBDevt.setItem(j, 1, item)
                item = QTableWidgetItem(opz[j])
                self.tableBDevt.setItem(j, 2, item)
                item = QTableWidgetItem(pvlg[j])
                self.tableBDevt.setItem(j, 3, item)


        elif err==0:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Файл Excel не корректный")

        else:
            pass


    def get_data_evt(self):

        def mesto(s):
            r = ''
            for a in range(len(s)):
                if s[a]=='|':
                    r = s[a+1:]
                    r = r[:-1]
                    break
            return r
        def form(s):
            r = ''
            for a in range(len(s)):
                if s[a]=='|':
                    r = s[:a]
                    break
            return r




        rezult = sql.getEVTfromBD2()
        if len(rezult)>0:

            self.tableBDevt.setRowCount(len(rezult))

            for i in range(len(rezult)):


                item = QTableWidgetItem(str(rezult[i][0])[:7])
                self.tableBDevt.setItem(i, 0, item)

                item = QTableWidgetItem(mesto(str(rezult[i][3])))
                self.tableBDevt.setItem(i, 1, item)

                item = QTableWidgetItem(str(rezult[i][1]))
                self.tableBDevt.setItem(i, 2, item)

                item = QTableWidgetItem(str(rezult[i][2]))
                self.tableBDevt.setItem(i, 3, item)

                item = QTableWidgetItem(form(str(rezult[i][3])))
                self.tableBDevt.setItem(i, 4, item)

                item = QTableWidgetItem(form(str(rezult[i][4])))
                self.tableBDevt.setItem(i, 5, item)

                item = QTableWidgetItem(str(rezult[i][5]))
                self.tableBDevt.setItem(i, 6, item)

        self.But_del_gtm.setEnabled(True)
        self.But_del_gtm_all.setEnabled(True)




    def checkEvent(self):
        e = False

        for i in range(self.tableBDevt.rowCount()):
            if self.tableBDevt.item(i, 6).text() not in self.typesEvent:
                e = True
                break
        if e:
            self.But_evt_to_BD.setEnabled(False)
        else:
            self.But_evt_to_BD.setEnabled(True)


    def load_data_evt(self):

        try:

            try:
                f = open('gtm.txt', 'r')
                data = f.read()
                f.close()
                mat.dict_gtm = eval(data)
            except:
                pass

            self.dict.clear()

            df_evt = sql.getExcel_evt(QtWidgets.QFileDialog.getOpenFileName()[0])

            self.D1 = df_evt['D1'].tolist()
            self.type = df_evt['type'].tolist()
            self.field = df_evt['field'].tolist()
            self.well = df_evt['well'].tolist()
            self.form1 = df_evt['form1'].tolist()
            self.form2 = df_evt['form2'].tolist()
            self.event = df_evt['event'].tolist()

            for i in range(len(self.event)):               # замена разных ГТМ типовыми (из файла)
                for j in mat.dict_gtm:
                    if self.event[i] in mat.dict_gtm[j]:
                        self.event[i] = j
                        break


            for x in range(len(self.type)):
                self.type[x] =  sql.getTypeWellForGTM(str(self.D1[x])[:7],  self.form1[x],  self.well[x], self.field[x])

            tmp = self.type[:]
            for x in range(len(tmp)-1,-1,-1):
                if self.type[x]=='':
                    self.D1.pop(x)
                    self.type.pop(x)
                    self.field.pop(x)
                    self.well.pop(x)
                    self.form1.pop(x)
                    self.form2.pop(x)
                    self.event.pop(x)


            self.fillTable()

            self.But_del_gtm.setEnabled(False)
            self.But_del_gtm_all.setEnabled(False)








        except Exception as e:

            QtWidgets.QMessageBox.critical(self, "Ошибка", "Файл Excel не корректный")
            logging.error(str(datetime.now()) + '   ' + str(e) + '   load_data_evt')



    def  fillTable(self):

        self.tableBDevt.setRowCount(len(self.D1))

        for j in range(len(self.D1)):
            item = QTableWidgetItem(str(self.D1[j])[:7])
            self.tableBDevt.setItem(j, 0, item)
            item = QTableWidgetItem(self.field[j])
            self.tableBDevt.setItem(j, 1, item)
            item = QTableWidgetItem(str(self.well[j]))
            self.tableBDevt.setItem(j, 2, item)
            item = QTableWidgetItem(self.type[j])
            self.tableBDevt.setItem(j, 3, item)
            item = QTableWidgetItem(self.form1[j])
            self.tableBDevt.setItem(j, 4, item)
            item = QTableWidgetItem(self.form2[j])
            self.tableBDevt.setItem(j, 5, item)
            item = QTableWidgetItem(self.event[j])
            self.tableBDevt.setItem(j, 6, item)
            if self.event[j] not in self.typesEvent:
                self.tableBDevt.item(j, 6).setBackground(QtGui.QColor('red'))
        self.checkEvent()






    def evt_to_BD(self):


        for key in self.dict:
            s = self.dict[key][0]
            if key not in mat.dict_gtm[s]:
                mat.dict_gtm[s].append(key)


        f = open('gtm.txt', 'w')
        f.write(str(mat.dict_gtm))
        f.close()


        def isnone(s):
            if s=='' or s!=s:
                return False
            else:
                return True


        try:

            list_tuple = []


            for i in range(self.tableBDevt.rowCount()):

                if self.tableBDevt.item(i, 6).text() != 'Не учитывать ГТМ':

                    if isnone(self.tableBDevt.item(i, 0).text()) and isnone(self.tableBDevt.item(i, 1).text()) and \
                            isnone(self.tableBDevt.item(i, 2).text()) and isnone(self.tableBDevt.item(i, 3).text()) and \
                            isnone(self.tableBDevt.item(i, 4).text()) and isnone(self.tableBDevt.item(i, 5).text()) and \
                            isnone(self.tableBDevt.item(i, 6).text()):

                        l = []
                        l.append(self.tableBDevt.item(i, 0).text() + '-01 00:00:00')
                        l.append(self.tableBDevt.item(i, 2).text())
                        l.append(self.tableBDevt.item(i, 3).text())
                        l.append(self.tableBDevt.item(i, 4).text()+'|'+self.tableBDevt.item(i, 1).text()+'|')
                        l.append(self.tableBDevt.item(i, 5).text()+'|'+self.tableBDevt.item(i, 1).text()+'|')
                        l.append(self.tableBDevt.item(i, 6).text())
                        t = tuple(l)
                        list_tuple.append(t)


            sql.insEVTtoBD(list_tuple)
            self.But_del_gtm.setEnabled(True)
            self.But_del_gtm_all.setEnabled(True)

            QtWidgets.QMessageBox.information(self, "OK", "Данные по мероприятиям записаны")

        except Exception as e:  # Запись  ошибок в лог
            logging.error(str(datetime.now()) + '   ' + str(e) + '  evt_to_BD')
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Данные не запсаны")


class Hall_window(QtWidgets.QDialog):

    def __init__(self):
        super(Hall_window, self).__init__()
        loadUi("Hall.ui", self)
        self.allWell = []
        self.forms = []
        self.h = []
        self.R = []
        self.re = []
        self.rdp = 3000
        self.minHall = '0'
        self.But_refreshHall.clicked.connect(self.refreshHall)
        self.listWidget.itemClicked.connect(self.listWidgetClick)

        self.checkBox_hall1.stateChanged.connect(self.showOrHide)
        self.checkBox_Pzab1.stateChanged.connect(self.showOrHide)
        self.checkBox_priem1.stateChanged.connect(self.showOrHide)
        self.checkBox_dat1.stateChanged.connect(self.showOrHide)
        self.checkBox_gtm1.stateChanged.connect(self.showOrHide)
        self.checkBox_pgi1.stateChanged.connect(self.showOrHide)
        self.checkBox_hall2.stateChanged.connect(self.showOrHide)
        self.checkBox_Pzab2.stateChanged.connect(self.showOrHide)
        self.checkBox_priem2.stateChanged.connect(self.showOrHide)
        self.checkBox_dat2.stateChanged.connect(self.showOrHide)
        self.checkBox_gtm2.stateChanged.connect(self.showOrHide)
        self.checkBox_pgi2.stateChanged.connect(self.showOrHide)
        self.checkBox_skin.stateChanged.connect(self.showOrHide)
        self.checkBox_diam.stateChanged.connect(self.showOrHide)

        self.Gr_hall1_dop1 = self.Gr_hall1.canvas.axes.twinx()
        self.Gr_hall1_dop2 = self.Gr_hall1.canvas.axes.twinx()
        self.Gr_hall3_dop1 = self.Gr_hall3.canvas.axes.twinx()
        self.Gr_hall3_dop2 = self.Gr_hall3.canvas.axes.twinx()

        self.Gr_hall2_dop1 = self.Gr_hall2.canvas.axes.twinx()

        self.Gr_hall1.F.subplots_adjust(left=0.09, right=0.9)
        self.Gr_hall2.F.subplots_adjust(left=0.09, right=0.9)
        self.Gr_hall3.F.subplots_adjust(left=0.09, right=0.9)

        self.tableHall.setColumnWidth(3, 260)

        self.HL1.addWidget(self.Gr_hall1.toolbar)
        self.HL2.addWidget(self.Gr_hall2.toolbar)
        self.HL3.addWidget(self.Gr_hall3.toolbar)



        '''self.Gr_hall1.canvas.mpl_connect('draw_event', self.on_draw)'''


        #self.Gr_hall1.toolbar.remove_toolitem(self, 'zoom')

    '''def on_draw(self, event):
        n = self.listWidget.currentRow()
        self.ListOfHallObj[n].setLims(self.Gr_hall1.canvas.axes.get_xlim(),  self.Gr_hall1.canvas.axes.get_ylim())'''


    def errorRep(self):
        QtWidgets.QMessageBox.critical(self, "Ошибка", "Ошибка при создании файла")

    def showOrHide(self):

        try:

            sender = self.sender()
            if sender.whatsThis() == '1':
                self.doGrHall1()
            if sender.whatsThis() == '2':
                self.doGrHall2()
            if sender.whatsThis() == '3':
                self.doGrHall3()

        except:
            print('????????????????????????????????????????????????????????????????????????????????????????????????')


    def refreshHall(self):
        n = self.listWidget.currentRow()
        self.ListOfHallObj[n].setPar(self.lineEdit_rdp.text(),  self.lineEdit_minHall.text(),  self.radio1.isChecked())
        self.ListOfHallObj[n].doCalc()
        self.doGrHall1()
        self.doGrHall2()
        self.doGrHall3()


    def doHall(self):

        self.lineEdit_rdp.setText(self.rdp)
        self.lineEdit_minHall.setText(self.minHall)
        self.radio1.setChecked(True)
        self.radio2.setChecked(False)

        self.doHallObj()

        # Интерфейс
        self.listWidget.clear()

        for i in range(len(self.ListOfHallObj)):
            a = mat.getSkvNfromText(self.ListOfHallObj[i].NagID)
            item = QListWidgetItem(a)
            self.listWidget.addItem(item)
        self.listWidget.setCurrentRow(0)

        self.listWidgetClick()



    def listWidgetClick(self):
        n = self.listWidget.currentRow()

        self.lineEdit_rdp.setText(str(self.ListOfHallObj[n].rdp))
        self.lineEdit_minHall.setText(str(self.ListOfHallObj[n].minHall))
        self.radio1.setChecked(self.ListOfHallObj[n].radio)
        self.radio2.setChecked(not self.ListOfHallObj[n].radio)

        self.data_gtm_list = self.ListOfHallObj[n].df_gtm['начало'].tolist()
        self.name_gtm_list = self.ListOfHallObj[n].df_gtm['ГТМ'].tolist()
        self.data_hist = self.ListOfHallObj[n].source_df['Дата'].tolist()
        self.data_hist_TR = self.ListOfHallObj[n].source_df['Дата'].tolist()[self.ListOfHallObj[n].TR_cut:]
        self.gtm_ind = []
        self.gtm_names = []
        self.gtm_ind_TR = []
        self.gtm_names_TR = []

        for i in range(len(self.data_hist)):
            if str(self.data_hist[i])  in self.data_gtm_list:
                indexx =  self.data_gtm_list.index(str(self.data_hist[i]))
                self.gtm_ind.append(i)
                self.gtm_names.append(self.name_gtm_list[indexx])

        for i in range(len(self.data_hist_TR)):
            if str(self.data_hist_TR[i])  in self.data_gtm_list:
                indexx =  self.data_gtm_list.index(str(self.data_hist_TR[i]))
                self.gtm_ind_TR.append(i)
                self.gtm_names_TR.append(self.name_gtm_list[indexx])

        self.doGrHall1()
        self.doGrHall2()
        self.doGrHall3()


    def fillTableHall(self, dates, skin):

        self.tableHall.setRowCount(0)

        self.tableHall.setRowCount(len(dates))

        for i in range(len(dates)):
            item = QTableWidgetItem('     ' + str(dates[i][0])[:7])
            self.tableHall.setItem(i, 0, item)
            item = QTableWidgetItem('     ' + str(dates[i][1])[:7])
            self.tableHall.setItem(i, 1, item)

            item = QTableWidgetItem('     ' + str(round(skin[i][0], 3)))
            self.tableHall.setItem(i, 2, item)



    def doHallObj(self):

        self.ListOfHallObj = []

        for i in range(len(self.allWell)):

            df = sql.getDataforHallObj(self.allWell[i], self.forms[i])

            if df.shape[0] > 9:
                bw, mu, kw = sql.getFormPar(self.forms[i])
                df_gtm = sql.getEVTfromBDforAll(mat.getSkvNfromText(self.allWell[i]), self.forms[i], 'НАГ')

                a = hallwell(df, df_gtm, self.forms[i], self.allWell[i], self.h[i], self.R[i], self.re[i], self.rdp, self.minHall, True,  bw, mu, kw)


                self.ListOfHallObj.append(a)



    def doGrHall1(self):

        self.Gr_hall1.F.clear()
        self.Gr_hall1.reCreate()
        self.Gr_hall1_dop1 = self.Gr_hall1.canvas.axes.twinx()
        self.Gr_hall1_dop2 = self.Gr_hall1.canvas.axes.twinx()


        n = self.listWidget.currentRow()
        N = self.ListOfHallObj[n]

        if len(N.xxx) > 0:

            delta = round(max(N.mass_sum_deltaP_t) / 10, 0)

            Ndat = 0


            for i in range(0, len(N.xxx)):
                self.Gr_hall1.canvas.axes.plot(N.xxx[i], N.yyy[i], linewidth=5)

                # для добавления дат
                if self.checkBox_dat1.isChecked():

                    Ndat = Ndat + len(N.xxx[i])

                    x1 = N.xxx[i][len(N.xxx[i]) - 1]
                    y1 = N.yyy[i][len(N.yyy[i]) - 1]
                    x2 = x1
                    y2 = y1 - y1 / 2
                    try:
                        texxt = N.source_df['Дата'][Ndat - 1]
                    except:
                        texxt ='??????????????'

                        # !!! Добавление аннотации
                    arr = self.Gr_hall1.canvas.axes.annotate(str(texxt)[:7],xy=(x1, y1),xytext=(x2, y2),arrowprops={'arrowstyle': '->'})


            if self.checkBox_hall1.isChecked():
                self.Gr_hall1.canvas.axes.plot(N.sum_W, N.mass_sum_deltaP_t, 'ko', markersize=3, label="график Холла")

            if self.checkBox_Pzab1.isChecked():
                self.Gr_hall1_dop1.plot(N.sum_W, N.source_df['Забойное давление (ТР), атм'], color='red')
                self.Gr_hall1_dop1.spines['right'].set_position(('axes', 1.02))
                self.Gr_hall1_dop1.tick_params(axis='y', colors='red')
            else:
                self.Gr_hall1_dop1.set_yticklabels([])
            if self.checkBox_priem1.isChecked():
                self.Gr_hall1_dop2.plot(N.sum_W, N.source_df['Приемистость за последний месяц, м3/сут'], color='indigo')
                self.Gr_hall1_dop2.spines['right'].set_position(('axes', 1.07))
                self.Gr_hall1_dop2.tick_params(axis='y', colors='indigo')
            else:
                self.Gr_hall1_dop2.set_yticklabels([])

            if self.checkBox_gtm1.isChecked():
                if len(self.gtm_ind) > 0:

                    for ind, val in enumerate(self.gtm_ind):

                        self.Gr_hall1.canvas.axes.plot(N.sum_W[val], N.mass_sum_deltaP_t[val], 'D', markersize=6, color='black', markerfacecolor='red')

                        self.Gr_hall1.canvas.axes.text(N.sum_W[val], N.mass_sum_deltaP_t[val] + delta, mat.gtm_names(self.gtm_names[ind]), fontsize=6,
                                              color='black', weight='bold', bbox={"facecolor": "white", "boxstyle": "round","edgecolor": "black","alpha": 0.9})

                        Y = [N.mass_sum_deltaP_t[val], N.mass_sum_deltaP_t[val] + delta]
                        X = [N.sum_W[val], N.sum_W[val]]
                        self.Gr_hall1.canvas.axes.plot(X, Y, color='black', linewidth=2)

            self.Gr_hall1.canvas.axes.set_title('График Холла, скв ' + mat.getSkvNfromText(N.NagID), fontsize=10)
            self.Gr_hall1.canvas.axes.set_xlabel("Накопленная закачка, м3", fontsize=8)
            self.Gr_hall1.canvas.axes.set_ylabel("SUM(dP*dt),атм*дни")
            self.Gr_hall1.canvas.axes.grid()
            self.Gr_hall1.F.patch.set_facecolor('azure')

            '''if not resetLims:
                self.Gr_hall1.canvas.axes.set_xlim(N.xlim)
                self.Gr_hall1.canvas.axes.set_ylim(N.ylim)'''

            self.Gr_hall1.canvas.draw()

            #self.Gr_hall1.canvas.axes.set_xlim(self.xlim)
            #self.Gr_hall1.canvas.axes.set_ylim(self.ylim)

            #print(self.Gr_hall1.canvas.axes.get_xlim())
            #print(self.Gr_hall1.canvas.axes.get_ylim())
            #self.Gr_hall1.canvas.axes.set_xlim(80000)
            #self.Gr_hall1.canvas.axes.set_ylim(60000)

            #N.xlim = self.Gr_hall1.canvas.axes.get_xlim()
            #N.ylim = self.Gr_hall1.canvas.axes.get_ylim()

        else:
            self.Gr_hall1.canvas.axes.set_title('Мало данных для расчета', fontsize=10)
            self.Gr_hall1.canvas.draw()



    def doGrHall2(self):

        self.Gr_hall2.F.clear()
        self.Gr_hall2.reCreate()
        self.Gr_hall2_dop1 = self.Gr_hall2.canvas.axes.twinx()

        n = self.listWidget.currentRow()
        N = self.ListOfHallObj[n]

        if N.radio:
            N_xx = N.xx
            N_yy = N.yy
            N_arr_skin = N.arr_skin
            N_arr_skin_two_point =  N.arr_skin_two_point
            dates = N.source_df['Дата'].tolist()
            diam = N.source_df['Диаметр штуцера, мм']
            makeGraf = True
        else:
            N_xx = N.TR_xx
            N_yy = N.TR_yy
            N_arr_skin = N.TR_arr_skin
            N_arr_skin_two_point = N.TR_arr_skin_two_point
            if len(N_arr_skin) > 0:
                dates = N.source_df['Дата'].tolist()[N.TR_cut:]
                diam = N.source_df['Диаметр штуцера, мм'][N.TR_cut:]
                makeGraf = True
            else:
                dates = []
                diam = []
                makeGraf = False

        if makeGraf == True:
            # для формирования плато
            xx_ = []
            arr_skin_ = []
            a, b, s = [], [], []
            for i in range(0, len(N_xx) - 1):
                a.append(N_yy[i])
                b.append(N_yy[i + 1])
                s.append(N_arr_skin[i])
                xx_.append(np.ravel(list(zip(a, b))))
                arr_skin_.append(np.ravel(list(zip(s, s))))
                a = []
                b = []
                s = []

            for i in range(0, len(xx_)):
                self.Gr_hall2.canvas.axes.plot(xx_[i], arr_skin_[i], '-', linewidth=2)

            try:
                if self.checkBox_skin.isChecked():
                    self.Gr_hall2.canvas.axes.plot(dates[:-1], N_arr_skin_two_point, 'o', label="Скин-фактор")
            except:
                pass

            if self.checkBox_diam.isChecked():
                self.Gr_hall2_dop1.plot(dates, diam, '-', label="Диаметр штуцера",  color = 'grey', linewidth=2)

            self.Gr_hall2.canvas.axes.set_title('График изменения скин-фактора, скв. ' + mat.getSkvNfromText(N.NagID), fontsize=10)
            self.Gr_hall2.canvas.axes.set_xlabel("Время")
            self.Gr_hall2.canvas.axes.set_ylabel("SKIN")

            self.Gr_hall2.canvas.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

            self.Gr_hall2.canvas.axes.grid()
            self.Gr_hall2.canvas.axes.legend(loc='upper left')

            self.Gr_hall2.F.patch.set_facecolor('azure')
            self.Gr_hall2.canvas.draw()

            self.fillTableHall(xx_, arr_skin_)

        else:
            self.Gr_hall2.canvas.axes.set_title('Мало данных для расчета', fontsize=10)
            self.Gr_hall2.canvas.draw()


    def doGrHall3(self):

        self.Gr_hall3.F.clear()
        self.Gr_hall3.reCreate()
        self.Gr_hall3_dop1 = self.Gr_hall3.canvas.axes.twinx()
        self.Gr_hall3_dop2 = self.Gr_hall3.canvas.axes.twinx()


        n = self.listWidget.currentRow()
        N = self.ListOfHallObj[n]

        if len(N.TR_xxx) > 0:

            dates = N.source_df['Дата'].tolist()[N.TR_cut:]

            delta = round(max(N.TR_mass_sum_deltaP_t) / 10, 0)

            Ndat = 0

            for i in range(0, len(N.TR_xxx)):
                self.Gr_hall3.canvas.axes.plot(N.TR_xxx[i], N.TR_yyy[i], linewidth=5)

                # для добавления дат
                if self.checkBox_dat2.isChecked():

                    Ndat = Ndat + len(N.TR_xxx[i])
                    x1 = N.TR_xxx[i][len(N.TR_xxx[i]) - 1]
                    y1 = N.TR_yyy[i][len(N.TR_yyy[i]) - 1]
                    x2 = x1
                    y2 = y1 - y1 / 2
                    texxt = dates[Ndat - 1]
                   # print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
                   # print(texxt)
                    # !!! Добавление аннотации
                    arr = self.Gr_hall3.canvas.axes.annotate(str(texxt)[:7], xy=(x1, y1), xytext=(x2, y2),
                                                             arrowprops={'arrowstyle': '->'})

            if self.checkBox_hall2.isChecked():
                self.Gr_hall3.canvas.axes.plot(N.TR_sum_W, N.TR_mass_sum_deltaP_t, 'ko', markersize=3,
                                               label="график Холла")

            if self.checkBox_Pzab2.isChecked():
                self.Gr_hall3_dop1.plot(N.TR_sum_W, N.source_df['Забойное давление (ТР), атм'][N.TR_cut:], color='red')
                self.Gr_hall3_dop1.spines['right'].set_position(('axes', 1.02))
                self.Gr_hall3_dop1.tick_params(axis='y', colors='red')
            else:
                self.Gr_hall3_dop1.set_yticklabels([])

            if self.checkBox_priem2.isChecked():
                self.Gr_hall3_dop2.plot(N.TR_sum_W, N.source_df['Приемистость (ТР), м3/сут'][N.TR_cut:],
                                        color='indigo')
                self.Gr_hall3_dop2.spines['right'].set_position(('axes', 1.07))
                self.Gr_hall3_dop2.tick_params(axis='y', colors='indigo')
            else:
                self.Gr_hall3_dop2.set_yticklabels([])

            if self.checkBox_gtm2.isChecked():
                if len(self.gtm_ind_TR) > 0:

                    for ind, val in enumerate(self.gtm_ind_TR):
                        self.Gr_hall3.canvas.axes.plot(N.TR_sum_W[val], N.TR_mass_sum_deltaP_t[val], 'D', markersize=6,
                                                       color='black', markerfacecolor='red')

                        self.Gr_hall3.canvas.axes.text(N.TR_sum_W[val], N.TR_mass_sum_deltaP_t[val] + delta,
                                                       mat.gtm_names(self.gtm_names_TR[ind]), fontsize=6,
                                                       color='black', weight='bold',
                                                       bbox={"facecolor": "white", "boxstyle": "round",
                                                             "edgecolor": "black", "alpha": 0.9})

                        Y = [N.TR_mass_sum_deltaP_t[val], N.TR_mass_sum_deltaP_t[val] + delta]
                        X = [N.TR_sum_W[val], N.TR_sum_W[val]]
                        self.Gr_hall3.canvas.axes.plot(X, Y, color='black', linewidth=2)


            self.Gr_hall3.canvas.axes.set_title('График Холла по тех. режимам, скв ' + mat.getSkvNfromText(N.NagID) , fontsize=10)
            self.Gr_hall3.canvas.axes.set_xlabel("Накопленная закачка, м3", fontsize=8)
            self.Gr_hall3.canvas.axes.set_ylabel("SUM(dP*dt),атм*дни")
            self.Gr_hall3.canvas.axes.grid()
            self.Gr_hall3.F.patch.set_facecolor('azure')
            self.Gr_hall3.canvas.draw()

        else:
            self.Gr_hall3.canvas.axes.set_title('Мало данных для расчета', fontsize=10)
            self.Gr_hall3.canvas.draw()


# Вторая версия Чена
class Chen_window2(QtWidgets.QDialog):
    def __init__(self):
        super(Chen_window2, self).__init__()
        loadUi("Chen.ui", self)
        self.listWidget.itemClicked.connect(self.listWidgetClick)  # Привязка события клика

        '''self.Gr_chen1.canvas.mpl_connect('motion_notify_event', self.getDataOnTrend)
        self.Gr_chen2.canvas.mpl_connect('motion_notify_event', self.getDataOnTrend)
        self.Gr_chen3.canvas.mpl_connect('motion_notify_event', self.getDataOnTrend)'''

        self.Gr_chen1.canvas.mpl_connect('pick_event', self.onpick1)
        self.Gr_chen2.canvas.mpl_connect('pick_event', self.onpick2)
        self.Gr_chen3.canvas.mpl_connect('pick_event', self.onpick3)

        self.rejected.connect(self.recPar)

        self.HL1.addWidget(self.Gr_chen1.toolbar)
        self.HL2.addWidget(self.Gr_chen2.toolbar)
        self.HL3.addWidget(self.Gr_chen3.toolbar)

        self.HL1.addWidget(self.label_dat1)
        self.HL2.addWidget(self.label_dat2)
        self.HL3.addWidget(self.label_dat3)

        self.forms=''

        self.tableChen.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        '''self.tableChen.setColumnWidth(0, 50)
        self.tableChen.setColumnWidth(1, 40)
        self.tableChen.setColumnWidth(2, 40)
        self.tableChen.setColumnWidth(3, 40)
        self.tableChen.setColumnWidth(4, 40)
        self.tableChen.setColumnWidth(5, 40)
        self.tableChen.setColumnWidth(6, 300)
        self.tableChen.setColumnWidth(7, 300)
        self.tableChen.setColumnWidth(8, 300)

        self.HL1.addWidget(self.Gr_chen1.toolbar)
        self.HL1.addWidget(self.lab)
        self.HL1.addWidget(self.Combo_chen)
        self.HL1.addWidget(self.But_refresh)'''

        self.But_refresh.clicked.connect(self.refresh)
        self.But_chenCalc.clicked.connect(self.saveChen2)
        self.But_open_chen.clicked.connect(self.doRepChen)

        #self.Gr_chen1.F.subplots_adjust(left=0.05, right=0.95)

        self.ListOfChenObj = []
        self.allWell = []

        #self.lineEdit_min_count.text(), self.lineEdit_points.text(), self.lineEdit_rdp.text(), self.lineEdit_min_interval.text()

        self.lineEdit_min_count.setText(param.lineEdit_min_count.text())
        self.lineEdit_points.setText(param.lineEdit_points.text())
        self.lineEdit_rdp.setText(param.lineEdit_rdp.text())
        self.lineEdit_min_interval.setText(param.lineEdit_min_interval.text())
        self.lineEdit_months.setText(param.lineEdit_months.text())
        self.radioGTM.setChecked(param.radio1_gtm.isChecked())
        self.radioNotGTM.setChecked(param.radio2_gtm.isChecked())

        self.tableChen.itemSelectionChanged.connect(self.on_selectItm)

        validator = QtGui.QRegExpValidator(QRegExp("([-]{0,1})([0-9]{0,9})([.]{0,1}[0-9]{0,100})"))
        self.lineEdit_rdp.setValidator(validator)
        self.lineEdit_min_interval.setValidator(validator)
        self.lineEdit_points.setValidator(validator)


    def getDataOnTrend(self, event):
        #D = str(mdates.num2date(int(event.xdata)))[:7]
        #I = str(float(event.xdata))
        #print(event.artist)
        pass

    def onpick1(self, event):
        if isinstance(event.artist, Line2D):
            thisline = event.artist
            #xdata = thisline.get_xdata()
            ind = event.ind
            #print('onpick1 line:', xdata[ind])
            s = str(self.ListOfChenObj[self.listWidget.currentRow()].df_history.loc[ind[0], 'Дата'])
            self.label_dat1.setStyleSheet("margin-right:18;background:linen;border-radius:3px;border-style:solid;border-width:1px;font-size: 12px;font-weight: bold;")
            if s in self.data_gtm_list:
                g = '    ГТМ: '+self.name_gtm_list[self.data_gtm_list.index(s)]
            else:
                g = ''
            self.label_dat1.setText(s[:7]+g)
            self.label_dat2.setStyleSheet("")
            self.label_dat3.setStyleSheet("")
            self.label_dat2.setText("")
            self.label_dat3.setText("")
    def onpick2(self, event):
        if isinstance(event.artist, Line2D):
            ind = event.ind
            s = str(self.ListOfChenObj[self.listWidget.currentRow()].df_history.loc[ind[0], 'Дата'])
            self.label_dat2.setStyleSheet(
                "margin-right:18;background:linen;border-radius:3px;border-style:solid;border-width:1px;font-size: 12px;font-weight: bold;")
            if s in self.data_gtm_list:
                g = '    ГТМ: ' + self.name_gtm_list[self.data_gtm_list.index(s)]
            else:
                g = ''
            self.label_dat2.setText(s[:7] + g)
            self.label_dat1.setStyleSheet("")
            self.label_dat3.setStyleSheet("")
            self.label_dat1.setText("")
            self.label_dat3.setText("")
    def onpick3(self, event):
        if isinstance(event.artist, Line2D):
            ind = event.ind
            s = str(self.ListOfChenObj[self.listWidget.currentRow()].df_history.loc[ind[0], 'Дата'])
            self.label_dat3.setStyleSheet(
                "margin-right:18;background:linen;border-radius:3px;border-style:solid;border-width:1px;font-size: 12px;font-weight: bold;")
            if s in self.data_gtm_list:
                g = '    ГТМ: ' + self.name_gtm_list[self.data_gtm_list.index(s)]
            else:
                g = ''
            self.label_dat3.setText(s[:7] + g)
            self.label_dat2.setStyleSheet("")
            self.label_dat1.setStyleSheet("")
            self.label_dat2.setText("")
            self.label_dat1.setText("")


    def errorRep(self):
        QtWidgets.QMessageBox.critical(self, "Ошибка", "Ошибка при создании файла")


    def recPar(self):

        try:

            if len(self.ListOfChenObj) > 0 :

                L = []
                for itm in self.ListOfChenObj:
                    l = []
                    l.append(itm.NefID)
                    l.append(itm.radio_gtm)
                    l.append(itm.param[4])
                    l.append(itm.param[2])
                    l.append(itm.param[0])
                    l.append(itm.param[3])
                    l.append(itm.param[1])
                    t = tuple(l)
                    L.append((t))

                sql.insChenParam(L)

        except Exception as e:  # Запись  ошибок в лог
             logging.error(str(datetime.now()) + '   ' + str(e)+'  recPar')


    def on_selectItm(self):

        if self.tableChen.currentRow() == self.tableChen.rowCount() - 1:

            s = ''
            try:
                s = self.tableChen.item(self.tableChen.currentRow(), 6).text()
            except:
                pass

            self.combo = QComboBox()

            self.combo.addItem(s)
            self.combo.setItemData(0, QtGui.QColor('gray'), Qt.BackgroundRole)
            self.combo.addItem("Нормальное вытеснение")
            self.combo.addItem("ФНВ")
            self.combo.addItem("НЭК")
            self.combo.addItem("конус")
            self.combo.addItem("Неопознанный угол наклона")
            self.combo.addItem("неанализируемое облако точек")

            self.combo.activated[str].connect(self.onChangedCombo)

            self.tableChen.setCellWidget(self.tableChen.currentRow(), 6, self.combo)


    def onChangedCombo(self):

        c = self.combo.currentText()
        n = self.listWidget.currentRow()
        self.ListOfChenObj[n].df_result.loc[self.ListOfChenObj[n].df_result.shape[0] - 1, 'Нарушение'] = c
        self.fillTable()


    def doRepChen(self):

        first_window.listChenReport = self.ListOfChenObj[:]
        first_window.doReport(2)


    def fillTable(self):

        self.tableChen.setRowCount(0)
        n = self.listWidget.currentRow()
        if n == -1:
            n = 0

        a = 0
        for i in range(self.ListOfChenObj[n].df_result.shape[0]):
            a = a + 1
        self.tableChen.setRowCount(a)


        try:

            for i in range(self.ListOfChenObj[n].df_result.shape[0]):

                item = QTableWidgetItem(str(self.ListOfChenObj[n].df_result.loc[i, 'Скважина' ]))
                self.tableChen.setItem(i, 0, item)

                item = QTableWidgetItem(str(self.ListOfChenObj[n].df_result.loc[i, 'Подинтервал: начало'])[:7])
                self.tableChen.setItem(i, 1, item)

                item = QTableWidgetItem(str(self.ListOfChenObj[n].df_result.loc[i, 'Подинтервал: конец'])[:7])
                self.tableChen.setItem(i, 2, item)

                item = QTableWidgetItem(str(self.ListOfChenObj[n].df_result.loc[i, 'Наклон WOR']))
                self.tableChen.setItem(i, 3, item)

                item = QTableWidgetItem(str(self.ListOfChenObj[n].df_result.loc[i, 'Наклон WOR']))
                self.tableChen.setItem(i, 4, item)

                item = QTableWidgetItem(str(self.ListOfChenObj[n].df_result.loc[i, 'R2']))
                self.tableChen.setItem(i, 5, item)

                item = QTableWidgetItem(str(self.ListOfChenObj[n].df_result.loc[i, 'Нарушение']))
                self.tableChen.setItem(i, 6, item)

        except:
            pass




        '''self.tableChen.setRowCount(0)

        a = 0
        for j in range(len(self.ListOfChenObj)):
            for i in range(self.ListOfChenObj[j].df_result.shape[0]):
                a = a + 1
        self.tableChen.setRowCount(a)

        a = -1
        for j in range(len(self.ListOfChenObj)):

            for i in range(self.ListOfChenObj[j].df_result.shape[0]):

                a = a + 1

                item = QTableWidgetItem(str(self.ListOfChenObj[j].df_result.loc[i, 'Скважина' ]))
                self.tableChen.setItem(a, 0, item)

                item = QTableWidgetItem(str(self.ListOfChenObj[j].df_result.loc[i, 'Подинтервал: начало'])[:7])
                self.tableChen.setItem(a, 1, item)

                item = QTableWidgetItem(str(self.ListOfChenObj[j].df_result.loc[i, 'Подинтервал: конец'])[:7])
                self.tableChen.setItem(a, 2, item)

                item = QTableWidgetItem(str(self.ListOfChenObj[j].df_result.loc[i, 'Наклон WOR']))
                self.tableChen.setItem(a, 3, item)

                item = QTableWidgetItem(str(self.ListOfChenObj[j].df_result.loc[i, 'Наклон WOR']))
                self.tableChen.setItem(a, 4, item)

                item = QTableWidgetItem(str(self.ListOfChenObj[j].df_result.loc[i, 'R2']))
                self.tableChen.setItem(a, 5, item)

                item = QTableWidgetItem(str(self.ListOfChenObj[j].df_result.loc[i, 'Нарушение']))
                self.tableChen.setItem(a, 6, item)



                #for j  in range(7):
                #    self.tableSpear.item(i,j).setBackground(QtGui.QColor(clr))'''


    def listWidgetClick(self):

        n = self.listWidget.currentRow()

        self.fillTable()

        self.doGrChen(n)

        self.lineEdit_min_count.setText(str(self.ListOfChenObj[n].param[0]))
        self.lineEdit_points.setText(str(self.ListOfChenObj[n].param[1]))
        self.lineEdit_rdp.setText(str(self.ListOfChenObj[n].param[2]))
        self.lineEdit_min_interval.setText(str(self.ListOfChenObj[n].param[3]))
        self.lineEdit_months.setText(str(self.ListOfChenObj[n].param[4]))
        self.radioGTM.setChecked(self.ListOfChenObj[n].radio_gtm)
        self.radioNotGTM.setChecked(not self.ListOfChenObj[n].radio_gtm)

        self.label_dat1.setText('')
        self.label_dat2.setText('')
        self.label_dat3.setText('')
        self.label_dat1.setStyleSheet("")
        self.label_dat2.setStyleSheet("")
        self.label_dat3.setStyleSheet("")

    def refresh(self):
        n = self.listWidget.currentRow()
        param = [self.lineEdit_min_count.text(), self.lineEdit_points.text(), self.lineEdit_rdp.text(), self.lineEdit_min_interval.text(), self.lineEdit_months.text()]
        self.ListOfChenObj[n].setPar(param, self.radioGTM.isChecked())
        self.ListOfChenObj[n].doCalc()
        self.fillTable()

    def doChenObj(self):

        self.ListOfChenObj = []
        param = [self.lineEdit_min_count.text(), self.lineEdit_points.text(), self.lineEdit_rdp.text(), self.lineEdit_min_interval.text(), self.lineEdit_months.text()]

        for i in range(len(self.allWell)):

            df = sql.getChen2FromBD(self.forms[i], self.allWell[i])
            paramBD, gtm = sql.getChenParam(self.allWell[i])
            if  paramBD != []:
                P = paramBD
                G = gtm
            else:
                P = param
                G = self.radioGTM.isChecked()

            if G:
                df_gtm = sql.getEVTfromBDforAll(mat.getSkvNfromText(self.allWell[i]), self.forms[i], 'НЕФ')
            else:
                df_gtm = sql.doEmptyDataframe()

            a = chenwell(df, self.forms[i], self.allWell[i] , P , df_gtm, G, sql.doEmptyDataframe())

            self.ListOfChenObj.append(a)


    def doChen(self):

        self.lineEdit_rdp.setText(param.lineEdit_rdp.text())
        self.lineEdit_min_count.setText(param.lineEdit_min_count.text())
        self.lineEdit_min_interval.setText(param.lineEdit_min_interval.text())
        self.lineEdit_points.setText(param.lineEdit_points.text())
        self.radioGTM.setChecked(param.radio1_gtm.isChecked())
        self.radioNotGTM.setChecked(param.radio2_gtm.isChecked())

        self.doChenObj()
        # Интерфейс
        self.listWidget.clear()

        for i in range(len(self.ListOfChenObj)):
            a = mat.getSkvNfromText(self.ListOfChenObj[i].NefID)
            item = QListWidgetItem(a)
            self.listWidget.addItem(item)
        self.listWidget.setCurrentRow(0)


        self.listWidgetClick()
        self.fillTable()

        #df = sql.getChen2FromBD(self.currForm, first_window.id[first_window.Nef])
        #self.df_chen = chen2.chen_main(df, self.currForm, self.Combo_chen.currentText())
        #self.doGrChen()

    def doGrChen(self, n):

        a = ''
        for i in self.forms[n]:
            if i != '|':
                a = a + i
            else:
                break
        self.label1.setText('Пласт : ' + a + '   Скважина :  ' + mat.getSkvNfromText(self.ListOfChenObj[n].NefID))

        if self.ListOfChenObj[n].df_history.shape[0]>0:

            self.Gr_chen1.F.clear()
            self.Gr_chen2.F.clear()
            self.Gr_chen3.F.clear()
            self.Gr_chen1.reCreate()
            self.Gr_chen2.reCreate()
            self.Gr_chen3.reCreate()

            # wellN = mat.getSkvNfromText(self.ListOfChenObj[n].NefID)
            # df_gtm = sql.getEVTfromBDforChen2(wellN, self.forms[n])
            self.data_gtm_list = self.ListOfChenObj[self.listWidget.currentRow()].gtj['начало'].tolist()
            self.name_gtm_list = self.ListOfChenObj[self.listWidget.currentRow()].gtj['ГТМ'].tolist()
            self.data_hist = self.ListOfChenObj[self.listWidget.currentRow()].df_history['Дата'].tolist()
            gtm_ind = []
            for i in range(len(self.data_hist)):
                if self.data_hist[i] in self.data_gtm_list:
                    gtm_ind.append(i)


            self.Gr_chen1.canvas.axes.clear()
            self.Gr_chen1.canvas.axes.set_title('График Чена  (Накопленный ВНФ)')
            self.Gr_chen1.canvas.axes.plot(self.ListOfChenObj[n].df_history['delta_days_from_start'], self.ListOfChenObj[n].df_history['WOR'], 'o', markersize=3, picker=True, pickradius=5, label="ВНФ")
            self.Gr_chen1.canvas.axes.plot(self.ListOfChenObj[n].df_history['delta_days_from_start'], self.ListOfChenObj[n].df_history['WOR_dir'], 'o', markersize=3, picker=True, pickradius=5,  label="производная ВНФ")
            for i in gtm_ind:
                self.Gr_chen1.canvas.axes.plot(self.ListOfChenObj[n].df_history['delta_days_from_start'][i],
                                               self.ListOfChenObj[n].df_history['WOR'][i], 'D', markersize=4, color = 'red')

            self.Gr_chen1.canvas.axes.set_ylabel("WOR, WOR'")
            self.Gr_chen1.canvas.axes.legend(loc='upper left')
            self.Gr_chen1.canvas.axes.grid()
            self.Gr_chen1.F.patch.set_facecolor('bisque')
            self.Gr_chen1.canvas.axes.set_xscale('log')
            self.Gr_chen1.canvas.axes.set_yscale('log')
            self.Gr_chen1.canvas.draw()


            self.Gr_chen2.canvas.axes.clear()
            self.Gr_chen2.canvas.axes.set_title('График Чена  (Текущий ВНФ)')
            self.Gr_chen2.canvas.axes.plot(self.ListOfChenObj[n].df_history['delta_days_from_start'], self.ListOfChenObj[n].df_history['WOR_curr'], 'o', markersize=3, picker=True, pickradius=5, label="ВНФ")
            self.Gr_chen2.canvas.axes.plot(self.ListOfChenObj[n].df_history['delta_days_from_start'], self.ListOfChenObj[n].df_history['WOR_dir_curr'], 'o', markersize=3, picker=True, pickradius=5, label="производная ВНФ")
            for i in gtm_ind:
                self.Gr_chen2.canvas.axes.plot(self.ListOfChenObj[n].df_history['delta_days_from_start'][i],
                                               self.ListOfChenObj[n].df_history['WOR_curr'][i], 'D', markersize=4, color = 'red')
            self.Gr_chen2.canvas.axes.set_ylabel("WOR, WOR'")
            self.Gr_chen2.canvas.axes.legend(loc='upper left')
            self.Gr_chen2.canvas.axes.grid()
            self.Gr_chen2.F.patch.set_facecolor('bisque')
            self.Gr_chen2.canvas.axes.set_xscale('log')
            self.Gr_chen2.canvas.axes.set_yscale('log')
            self.Gr_chen2.canvas.draw()

            '''tmp = self.ListOfChenObj[n].df_history['Время работы, часы'].tolist()

            T = []
            q = 0
            for i in tmp:
                q = q + i
                T.append(q)'''

            '''w = self.ListOfChenObj[n].df_history['water'].tolist()
            o = self.ListOfChenObj[n].df_history['Добыча нефти за посл.месяц, т'].tolist()

            with open("Отчеты/t.txt", "w") as file:
                print(*T, file=file, sep="\n")
            with open("Отчеты/w.txt", "w") as file:
                print(*w, file=file, sep="\n")
            with open("Отчеты/o.txt", "w") as file:
                print(*o, file=file, sep="\n")'''

            self.Gr_chen3.canvas.axes.clear()
            self.Gr_chen3.canvas.axes.set_title('График динамики добычи')
            self.Gr_chen3.canvas.axes.plot(self.ListOfChenObj[n].df_history['delta_days_from_start'], self.ListOfChenObj[n].df_history['water'], 'o', markersize=3, picker=True, pickradius=5, label="Вода, т")
            self.Gr_chen3.canvas.axes.plot(self.ListOfChenObj[n].df_history['delta_days_from_start'], self.ListOfChenObj[n].df_history['Добыча нефти за посл.месяц, т'], 'o', markersize=3, picker=True, pickradius=5, label="Нефть, т")
            for i in gtm_ind:
                self.Gr_chen3.canvas.axes.plot(self.ListOfChenObj[n].df_history['delta_days_from_start'][i],
                                               self.ListOfChenObj[n].df_history['water'][i], 'D', markersize=4, color = 'red')
            self.Gr_chen3.canvas.axes.set_ylabel("Вода, нефть")
            self.Gr_chen3.canvas.axes.legend(loc='upper left')
            self.Gr_chen3.canvas.axes.set_xscale('log')
            self.Gr_chen3.canvas.axes.set_yscale('log')
            self.Gr_chen3.canvas.axes.grid()
            self.Gr_chen3.F.patch.set_facecolor('bisque')
            self.Gr_chen3.canvas.draw()

        else:
            self.Gr_chen1.canvas.axes.clear()
            self.Gr_chen2.canvas.axes.clear()
            self.Gr_chen3.canvas.axes.clear()
            self.Gr_chen1.canvas.draw()
            self.Gr_chen2.canvas.draw()
            self.Gr_chen3.canvas.draw()


    def saveChen2(self):

        first_window.listChenReport = self.ListOfChenObj[:]
        QtWidgets.QMessageBox.information(self, "OK", "Данные записаны в отчет")



class NO(QtWidgets.QDialog):

    def __init__(self):
        super(NO, self).__init__()
        loadUi("NO.ui", self)

        self.HL.addWidget(self.Gr_NO.toolbar)
        self.listWidget.itemClicked.connect(self.listWidgetClick)
        self.But_refresh.clicked.connect(self.refresh)

        validator = QtGui.QRegExpValidator(QRegExp("([-]{0,1})([0-9]{0,9})([.]{0,1}[0-9]{0,100})"))
        self.lineEdit_rdpNO.setValidator(validator)
        self.lineEdit_pointsNO.setValidator(validator)

        self.ax_second = self.Gr_NO.canvas.axes.twinx()

        self.ListOfNoObj = []
        self.allWell = []
        self.forms = []

        self.tableNO.setColumnWidth(0, 60)
        self.tableNO.setColumnWidth(1, 100)
        self.tableNO.setColumnWidth(2, 60)

        self.tableNO.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableNO.horizontalHeader().setStyleSheet("QHeaderView { font-size: 9pt; font-weight: bold}")

        self.tableNO.setHorizontalHeaderItem(6, QTableWidgetItem('Сокращение дебита \n воды (прогноз qн), \n т/сут'))
        self.tableNO.setHorizontalHeaderItem(7, QTableWidgetItem('Текущий НО воды \n (прогноз qн), \n т'))
        self.tableNO.setHorizontalHeaderItem(8, QTableWidgetItem('Сокращение дебита \n воды (текущий qн), \n т/сут'))
        self.tableNO.setHorizontalHeaderItem(9, QTableWidgetItem('Текущий НО воды \n (текущий qн), \n т'))

        self.But_NOCalc.clicked.connect(self.saveNO)
        self.But_open_NO.clicked.connect(self.doRepNO)


    def doRepNO(self):

        first_window.listNOReport = self.ListOfNoObj[:]
        first_window.doReport(3)

    def errorRep(self):
        QtWidgets.QMessageBox.critical(self, "Ошибка", "Ошибка при создании файла")


    def saveNO(self):

        first_window.listNOReport = self.ListOfNoObj[:]
        QtWidgets.QMessageBox.information(self, "OK", "Данные записаны в отчет")


    def titleTableNO(self):

        font = QtGui.QFont()
        font.setBold(True)
        self.tableNOtitle.setWordWrap(True)
        item0 = QTableWidgetItem('-')
        item0.setTextAlignment(4)
        item0.setFont(font)
        item0.setBackground(QtGui.QColor('#C5D0E6'))


        #self.tableNO.setCellWidget(0, 0, self.widget)
        self.tableNOtitle.setSpan(0, 0, 2, 1)
        self.tableNOtitle.setColumnWidth(0, 80)
        item = item0.clone()
        item.setText('Скважина')
        self.tableNOtitle.setItem(0, 0, item)

        self.tableNOtitle.setSpan(0, 1, 2, 1)
        self.tableNOtitle.setColumnWidth(1, 60)
        item = item0.clone()
        item.setText('НДН, тыс.т' )
        self.tableNOtitle.setItem(0, 1, item)

        self.tableNOtitle.setSpan(0, 2, 1, 2)
        self.tableNOtitle.setColumnWidth(2, 160)
        item = item0.clone()
        item.setText('Стабильная работа')
        self.tableNOtitle.setItem(0, 2, item)

        self.tableNOtitle.setColumnWidth(2, 70)
        item = item0.clone()
        item.setText('Начало')
        self.tableNOtitle.setItem(1, 2, item)

        self.tableNOtitle.setColumnWidth(3, 70)
        item = item0.clone()
        item.setText('Конец')
        self.tableNOtitle.setItem(1, 3, item)

        self.tableNOtitle.setSpan(0, 4, 1, 3)
        self.tableNOtitle.setColumnWidth(4, 160)
        item = item0.clone()
        item.setText('Параметры до роста ВНФ')
        self.tableNOtitle.setItem(0, 4, item)

        self.tableNOtitle.setColumnWidth(4, 60)
        item = item0.clone()
        item.setText('qн, т/сут')
        self.tableNOtitle.setItem(1, 4, item)
        self.tableNOtitle.setColumnWidth(5, 60)
        item = item0.clone()
        item.setText('qж, т/сут')
        self.tableNOtitle.setItem(1, 5, item)
        self.tableNOtitle.setColumnWidth(6, 60)
        item = item0.clone()
        item.setText('% воды')
        self.tableNOtitle.setItem(1, 6, item)

        self.tableNOtitle.setSpan(0, 7, 2, 1)
        self.tableNOtitle.setColumnWidth(7, 80)
        item = item0.clone()
        item.setText('Дата начала роста ВНФ')
        self.tableNOtitle.setItem(0, 7, item)

        self.tableNOtitle.setSpan(0, 8, 1, 3)
        self.tableNOtitle.setColumnWidth(8, 160)
        item = item0.clone()
        item.setText('Текущие параметры')
        self.tableNOtitle.setItem(0, 8, item)

        self.tableNOtitle.setColumnWidth(8, 60)
        item = item0.clone()
        item.setText('qн, т/сут')
        self.tableNOtitle.setItem(1, 8, item)
        self.tableNOtitle.setColumnWidth(9, 60)
        item = item0.clone()
        item.setText('qж, т/сут')
        self.tableNOtitle.setItem(1, 9, item)
        self.tableNOtitle.setColumnWidth(10, 60)
        item = item0.clone()
        item.setText('% воды')
        self.tableNOtitle.setItem(1, 10, item)

        self.tableNOtitle.setSpan(0, 11, 1, 3)
        self.tableNOtitle.setColumnWidth(11, 160)
        item = item0.clone()
        item.setText('Прогнозные параметры')
        self.tableNOtitle.setItem(0, 11, item)

        self.tableNOtitle.setColumnWidth(11, 60)
        item = item0.clone()
        item.setText('qн, т/сут')
        self.tableNOtitle.setItem(1, 11, item)
        self.tableNOtitle.setColumnWidth(12, 60)
        item = item0.clone()
        item.setText('qж, т/сут')
        self.tableNOtitle.setItem(1, 12, item)
        self.tableNOtitle.setColumnWidth(13, 60)
        item = item0.clone()
        item.setText('% воды')
        self.tableNOtitle.setItem(1, 13, item)

        self.tableNOtitle.setSpan(0, 14, 2, 1)
        self.tableNOtitle.setColumnWidth(14, 90)
        item = item0.clone()
        item.setText('Сокращение дебита воды (прогноз qн), т/сут')
        self.tableNOtitle.setItem(0, 14, item)

        self.tableNOtitle.setSpan(0, 15, 2, 1)
        self.tableNOtitle.setColumnWidth(15, 90)
        item = item0.clone()
        item.setText('Текущий НО воды, (прогноз qн) т')
        self.tableNOtitle.setItem(0, 15, item)

        self.tableNOtitle.setSpan(0, 16, 2, 1)
        self.tableNOtitle.setColumnWidth(16, 90)
        item = item0.clone()
        item.setText('Сокращение дебита воды (текущий qн), т/сут')
        self.tableNOtitle.setItem(0, 16, item)

        self.tableNOtitle.setSpan(0, 17, 2, 1)
        self.tableNOtitle.setColumnWidth(17, 90)
        item = item0.clone()
        item.setText('Текущий НО воды, (текущий qн) т')
        self.tableNOtitle.setItem(0, 17, item)

        self.tableNOtitle.setSpan(0, 18, 2, 1)
        self.tableNOtitle.setColumnWidth(18, 90)
        item = item0.clone()
        item.setText('Время окупаемости РИР, мес')
        self.tableNOtitle.setItem(0, 18, item)

        self.tableNO.setColumnWidth(0, 80)
        self.tableNO.setColumnWidth(1, 60)
        self.tableNO.setColumnWidth(2, 70)
        self.tableNO.setColumnWidth(3, 70)
        self.tableNO.setColumnWidth(4, 60)
        self.tableNO.setColumnWidth(5, 60)
        self.tableNO.setColumnWidth(6, 60)
        self.tableNO.setColumnWidth(7, 80)
        self.tableNO.setColumnWidth(8, 60)
        self.tableNO.setColumnWidth(9, 60)
        self.tableNO.setColumnWidth(10, 60)
        self.tableNO.setColumnWidth(11, 60)
        self.tableNO.setColumnWidth(12, 60)
        self.tableNO.setColumnWidth(13, 60)
        self.tableNO.setColumnWidth(14, 90)
        self.tableNO.setColumnWidth(15, 90)
        self.tableNO.setColumnWidth(16, 90)
        self.tableNO.setColumnWidth(17, 90)
        self.tableNO.setColumnWidth(18, 90)




    def refresh(self):
        n = self.listWidget.currentRow()

        self.ListOfNoObj[n].value_rdp  = self.lineEdit_rdpNO.text()
        self.ListOfNoObj[n].month_min = self.lineEdit_minMonth.text()
        self.ListOfNoObj[n].min_determination = self.lineEdit_pointsNO.text()
        self.ListOfNoObj[n].max_stay = self.lineEdit_maxStop.text()
        self.ListOfNoObj[n].water_min = self.lineEdit_minW.text()

        self.ListOfNoObj[n].doCalc()
        self.fillTable(n)
        self.doGrNO(n)



    def listWidgetClick(self):

        n = self.listWidget.currentRow()

        self.fillTable(n)
        self.doGrNO(n)

        self.lineEdit_rdpNO.setText(self.ListOfNoObj[n].value_rdp)
        self.lineEdit_minMonth.setText(self.ListOfNoObj[n].month_min)
        self.lineEdit_pointsNO.setText(self.ListOfNoObj[n].min_determination)
        self.lineEdit_maxStop.setText(self.ListOfNoObj[n].max_stay)
        self.lineEdit_minW.setText(self.ListOfNoObj[n].water_min)


    def fillTable(self, i):



        def last(R):
            item = QTableWidgetItem(str(self.ListOfNoObj[i].df_result.loc[0, 'Подинтервал: конец'])[:7])
            self.tableNO.setItem(R, 0, item)
            item = QTableWidgetItem(str(self.ListOfNoObj[i].df_result.loc[count - 1, 'R2']))
            self.tableNO.setItem(R, 5, item)
            item = QTableWidgetItem('последний месяц')
            self.tableNO.setItem(R, 1, item)
            item = QTableWidgetItem(str(self.ListOfNoObj[i].df_result.loc[0, 'Заключение']))
            item.setForeground(QtGui.QColor('red'))
            self.tableNO.setItem(2*R, 10, item)

            '''item = QTableWidgetItem(str(self.ListOfNoObj[i].df_breakthrough.loc[0, 'qн текущий, т/сут']))
            self.tableNO.setItem(R, 2, item)
            item = QTableWidgetItem(str(self.ListOfNoObj[i].df_breakthrough.loc[0, 'qж текущий, т/сут']))
            self.tableNO.setItem(R, 3, item)
            item = QTableWidgetItem(str(self.ListOfNoObj[i].df_breakthrough.loc[0, '% воды текущий']))
            self.tableNO.setItem(R, 4, item)'''

            item = QTableWidgetItem(str(self.ListOfNoObj[i].qo_curr))
            self.tableNO.setItem(R, 2, item)
            item = QTableWidgetItem(str(self.ListOfNoObj[i].ql_curr))
            self.tableNO.setItem(R, 3, item)
            item = QTableWidgetItem(str(self.ListOfNoObj[i].w_curr))
            self.tableNO.setItem(R, 4, item)

            '''print(self.ListOfNoObj[i].qo_curr)
            print(self.ListOfNoObj[i].ql_curr)
            print(self.ListOfNoObj[i].w_curr)'''




        self.tableNO.clearContents()

        a = 0

        try:

            count = self.ListOfNoObj[i].df_result.shape[0]

            if count > 0:

                if self.ListOfNoObj[i].df_breakthrough.shape[0] > 0:

                    self.tableNO.setRowCount(3)

                    item = QTableWidgetItem(str(self.ListOfNoObj[i].df_result.loc[count - 1, 'Подинтервал: начало'])[:7])
                    self.tableNO.setItem(0, 0, item)

                    item = QTableWidgetItem('   -   ')
                    self.tableNO.setItem(2, 0, item)

                    item = QTableWidgetItem(str(self.ListOfNoObj[i].df_result.loc[0, 'R2']))
                    self.tableNO.setItem(0, 5, item)

                    item = QTableWidgetItem('   -   ')
                    self.tableNO.setItem(2, 5, item)

                    item = QTableWidgetItem('до роста ВНФ')
                    self.tableNO.setItem(0, 1, item)
                    item = QTableWidgetItem('прогноз')
                    self.tableNO.setItem(2, 1, item)

                    last(1)



                    item = QTableWidgetItem(str(self.ListOfNoObj[i].df_breakthrough.loc[0, 'qн до роста ВНФ, т/сут']))
                    self.tableNO.setItem(0, 2, item)
                    item = QTableWidgetItem(str(self.ListOfNoObj[i].df_breakthrough.loc[0, 'qж до роста ВНФ, т/сут']))
                    self.tableNO.setItem(0, 3, item)
                    item = QTableWidgetItem(str(self.ListOfNoObj[i].df_breakthrough.loc[0, '% воды до роста ВНФ']))
                    self.tableNO.setItem(0, 4, item)

                    item = QTableWidgetItem(str(self.ListOfNoObj[i].df_breakthrough.loc[0, 'qн прогноз, т/сут']))
                    self.tableNO.setItem(2, 2, item)
                    item = QTableWidgetItem(str(self.ListOfNoObj[i].df_breakthrough.loc[0, 'qж прогноз, т/сут']))
                    self.tableNO.setItem(2, 3, item)
                    item = QTableWidgetItem(str(self.ListOfNoObj[i].df_breakthrough.loc[0, '% воды прогноз']))
                    self.tableNO.setItem(2, 4, item)

                    #item = QTableWidgetItem(str(self.ListOfNoObj[i].df_breakthrough.loc[0, 'R2 нефти']))
                    #self.tableNO.setItem(0, 5, item)

                    item = QTableWidgetItem(str(self.ListOfNoObj[i].df_breakthrough.loc[0, 'Сокращение дебита воды (прогноз qн), т/сут']))
                    self.tableNO.setItem(2, 6, item)
                    item = QTableWidgetItem(str(self.ListOfNoObj[i].df_breakthrough.loc[0, 'Текущий НО воды (прогноз qн), т']))
                    self.tableNO.setItem(2, 7, item)
                    item = QTableWidgetItem(str(self.ListOfNoObj[i].df_breakthrough.loc[0, 'Сокращение дебита воды (текущий qн), т/сут']))
                    self.tableNO.setItem(2, 8, item)
                    item = QTableWidgetItem(str(self.ListOfNoObj[i].df_breakthrough.loc[0, 'Текущий НО воды (текущий qн), т']))
                    self.tableNO.setItem(2, 9, item)

                else:
                    self.tableNO.setRowCount(1)
                    last(0)


        except:
            pass


    def doGrNO(self, n):

        '''a = ''
        for i in self.forms[n]:
            if i != '|':
                a = a + i
            else:
                break
        self.label1.setText('Пласт : ' + a)'''


       # if self.ListOfChenObj[n].df_history.shape[0]>0:

        try:

            self.Gr_NO.F.clear()
            self.Gr_NO.reCreate()
            self.ax_second = self.Gr_NO.canvas.axes.twinx()

            self.Gr_NO.canvas.axes.clear()
            self.Gr_NO.canvas.axes.set_title('ln(ВНФ) - '+mat.getSkvNfromText(self.ListOfNoObj[n].NefID), fontsize=12)
            #self.Gr_NO.canvas.axes.set_xlim(self.ListOfNoObj[n].min_plot, self.ListOfNoObj[n].max_plot)
            #self.Gr_NO.canvas.axes.set_xlim(0, self.ListOfNoObj[n].max_plot)
            self.Gr_NO.canvas.axes.plot(self.ListOfNoObj[n].slice["Накопленная добыча нефти, тыс.т"], self.ListOfNoObj[n].slice["ln(WOR)"], color='blue', marker='o', linewidth=1, markersize=3,
                markerfacecolor='deepskyblue', markeredgecolor='mediumblue', markeredgewidth=0.5, label="график Чана")

            #self.Gr_NO.canvas.axes.legend(loc='upper left')

            self.ax_second.clear()

            self.ax_second.grid(False)
           # self.ax_second.set_ylim(0, 100)  # задание пределов дополнительной оси
            self.ax_second.plot(self.ListOfNoObj[n].slice["Накопленная добыча нефти, тыс.т"],
                           self.ListOfNoObj[n].slice["Дебит нефти за последний месяц, т/сут"], color='orange', marker='D',
                           linewidth=1, markersize=3,
                           markerfacecolor='gold', markeredgecolor='darkorange', markeredgewidth=0.5)

            #ax_second.legend(('Дебит нефти', ''), loc=(0.1, 0.95))

            #print(self.ListOfNoObj[n].rdp)

            self.Gr_NO.canvas.axes.plot(self.ListOfNoObj[n].rdp[0], self.ListOfNoObj[n].rdp[1], color='red', linestyle='--', linewidth=1)  # отрезки rdp

           # self.Gr_NO.canvas.axes.legend(('отрезки rdp', ''), loc=(0.2, 0.95))

            for i in range(0, len(self.ListOfNoObj[n].line_trend)):
                self.Gr_NO.canvas.axes.plot(self.ListOfNoObj[n].x_trend[i], self.ListOfNoObj[n].line_trend[i](self.ListOfNoObj[n].x_trend[i]), color='black',
                        linewidth=2)  # линии тренда ln(WOR) выбранных интервалов

            #self.Gr_NO.canvas.axes.legend(('тренд ln(WOR)', ''), loc=(0.3, 0.95))

            if len(self.ListOfNoObj[n].x_oil_interval) != 0 and len(self.ListOfNoObj[n].line_trend_oil) != 0:
                self.ax_second.plot(self.ListOfNoObj[n].x_oil_interval, self.ListOfNoObj[n].line_trend_oil(self.ListOfNoObj[n].x_oil_interval), color='red',
                               linewidth=2)  # линия тренда дебита нефти

            #self.Gr_NO.canvas.axes.legend(('тренд дебита)', ''), loc=(0.4, 0.95))


            '''self.Gr_chen1.canvas.axes.set_ylabel("WOR, WOR'")
            self.Gr_chen1.canvas.axes.legend(loc='upper left')
            self.Gr_chen1.canvas.axes.grid()
            self.Gr_chen1.F.patch.set_facecolor('bisque')
            self.Gr_chen1.canvas.axes.set_xscale('log')
            self.Gr_chen1.canvas.axes.set_yscale('log')'''

            self.Gr_NO.canvas.axes.legend(('lnВНФ', 'отрезки rdp', 'тренд ln(WOR)'), loc=(0, 0.88))
            self.ax_second.legend(('Дебит нефти', 'Тренд дебита'), loc=(0, 0.80))

            self.Gr_NO.canvas.draw()

        except Exception as e:  # Запись  ошибок в лог

            self.Gr_NO.canvas.axes.clear()
            self.Gr_NO.canvas.draw()

            logging.error(str(datetime.now()) + '   ' + str(e) + '   doGrNO (график НО)' )




    def doNO(self):

        self.lineEdit_rdpNO.setText(param.lineEdit_rdpNO.text())
        self.lineEdit_minMonth.setText(param.lineEdit_minMonth.text())
        self.lineEdit_pointsNO.setText(param.lineEdit_pointsNO.text())
        self.lineEdit_maxStop.setText(param.lineEdit_maxStop.text())
        self.lineEdit_minW.setText(param.lineEdit_minW.text())


        self.doNOobj()
        # Интерфейс
        self.listWidget.clear()

        for i in range(len(self.ListOfNoObj)):
            a = mat.getSkvNfromText(self.ListOfNoObj[i].NefID)
            item = QListWidgetItem(a)
            if self.ListOfNoObj[i].df_breakthrough.shape[0] > 0:
                item.setBackground(QtGui.QColor('darksalmon'))
            self.listWidget.addItem(item)
        self.listWidget.setCurrentRow(0)

        self.listWidgetClick()


    def doNOobj(self):

        self.ListOfNoObj = []

        for i in range(len(self.allWell)):

            df = sql.getNOfromBD(self.forms[i], self.allWell[i])

            a = NOwell(df, self.forms[i], self.allWell[i] , self.lineEdit_rdpNO.text(),
                         self.lineEdit_minMonth.text(), self.lineEdit_pointsNO.text(),
                         self.lineEdit_maxStop.text(), self.lineEdit_minW.text())



            self.ListOfNoObj.append(a)





# Handle high resolution displays:
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
app=QApplication(sys.argv)
app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))

#for style_name in QtWidgets.QStyleFactory.keys():
#    print(style_name)

param = Param()
hall_window = Hall_window()
chen_window2 = Chen_window2()
no = NO()
sql = SQL()
edit = Edit()
edit2 = Edit2()
edit3 = Edit3()
first_window=First_window()
evt = EVT()
bd = BD()
spirman = Spirman()
first_window.show()



app.exec_()


