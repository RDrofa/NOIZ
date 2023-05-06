import NO
from mat import getSkvNfromText as wellNumb

class NOwell():

    def __init__(self, df_initial, form, nameNef, value_rdp, month_min, min_determination, max_stay, water_min):
        self.NefID = nameNef
        self.df_initial = df_initial
        self.form = form
        self.value_rdp = value_rdp
        self.month_min = month_min
        self.min_determination = min_determination
        self.max_stay = max_stay
        self.water_min = water_min
        self.NefNumb = wellNumb(self.NefID)

        self.qo_curr = self.df_initial.loc[self.df_initial.shape[0] - 1, "Дебит нефти за последний месяц, т/сут"]
        self.ql_curr = self.df_initial.loc[self.df_initial.shape[0] - 1, "Дебит жидкости за последний месяц, т/сут"]
        self.w_curr = self.df_initial.loc[self.df_initial.shape[0] - 1, "Обводненность за посл.месяц, % (вес)"]

        #self.source_df['D'] = pd.to_datetime(self.source_df['D'], format="%Y/%m/%d")
        self.doCalc()


    def doCalc(self):

        self.df_result, self.df_breakthrough, self.slice, self.rdp, self.line_trend, self.x_trend , self.x_oil_interval, self.line_trend_oil= NO.NO(self.df_initial, float(self.value_rdp), int(self.month_min),
                                                        float(self.min_determination), int(self.max_stay), float(self.water_min), self.form, self.NefID)

        self.setPlot()


    def setPlot(self):

        min_plot = self.slice["Накопленная добыча нефти, тыс.т"][self.slice["ln(WOR)"] <= 0]
        max_plot = self.slice["Накопленная добыча нефти, тыс.т"].max()
        if min_plot.empty:
            min_plot = 0
        else:
            min_plot = min_plot.iloc[-1] // 10 * 10
        if max_plot!=max_plot:
            pass
        else:
            max_plot = self.slice["Накопленная добыча нефти, тыс.т"].max() // 10 * 10 + (
                        (self.slice["Накопленная добыча нефти, тыс.т"].max() % 10) // 2 + 2) * 2

        self.min_plot = min_plot
        self.max_plot = max_plot





