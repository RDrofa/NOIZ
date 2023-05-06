import chan

class chenwell():

    def __init__(self, df, form, nameNef, par, gtj, radio_gtm, gtj_emp):
        self.NefID = nameNef
        self.source_df = df
        self.form = form
        self.gtj = gtj
        self.gtj_emp = gtj_emp
        self.param = par
        self.radio_gtm = radio_gtm

        #self.source_df['D'] = pd.to_datetime(self.source_df['D'], format="%Y/%m/%d")
        self.doCalc()


    def doCalc(self):

        if self.radio_gtm:
            gtj = self.gtj
        else:
            gtj = self.gtj_emp
        par = self.param

        #self.df_history, self.df_result,  self.not_calc = chen2.chen_main(self.source_df, self.form, par)

        '''df_initial, value_rdp, mounth_start, min_count_1, min_count_2, min_interval,
        min_interval_x, min_subinterval_x, min_dermination, gtj = pd.DataFrame(), time = 'Время работы, часы',
        name_list = name_list'''

        self.df_history, self.df_result, self.not_calc = chan.Chan(self.source_df, float(par[2]), int(par[4]),
                                                        float(par[0]), 20, 0.09, float(par[3]), float(par[3]),
                                                        float(par[1]), gtj, self.form)

    def setPar(self, p,g):

        self.param = p
        self.radio_gtm = g