from hall import for_well
from mat import lenWell

class hallwell():

    def __init__(self, df, df_gtm,  form, nameNag,  h, R, re, rdp, minHall, radio, bw, mu, kw, coord):
        self.NagID = nameNag
        self.source_df_ = df
        self.form = form
        self.df_gtm = df_gtm
        self.h = h
        self.R = R
        self.re = re
        self.rdp = rdp
        self.minHall = minHall
        self.bw = bw
        self.mu = mu
        self.kw = kw
        self.radio = radio
        self.coord = coord

        self.xlim = 0
        self.ylim = 0

        self.TR_cut = 0

        self.xxx = []
        self.yyy = []
        self.sum_W = []
        self.mass_sum_deltaP_t = []
        self.xx = []
        self.yy = []
        self.arr_skin = []
        self.arr_skin_two_point = []

        self.TR_xxx = []
        self.TR_yyy = []
        self.TR_sum_W = []
        self.TR_mass_sum_deltaP_t = []
        self.TR_xx = []
        self.TR_yy = []
        self.TR_arr_skin = []
        self.TR_arr_skin_two_point = []

        #self.source_df['D'] = pd.to_datetime(self.source_df['D'], format="%Y/%m/%d")

        try:
            self.doCalc()
        except:
            pass


    '''def setLims(self, x,y):
        self.xlim = x
        self.ylim = y'''


    def doCalc(self):

        if self.coord[2] !=0 and self.coord[3] != 0:
            L = round(lenWell(self.coord[0],self.coord[1],self.coord[2],self.coord[3]), 2)
        else:
            L = 0


        par = list(map(float, [self.bw, self.mu, self.kw, self.h, self.R, self.re]))

        self.source_df = self.source_df_.loc[self.source_df_["Время работы под закачкой, часы"] > int(self.minHall)]  # 240
        self.source_df.reset_index()

        if self.source_df.shape[0] > 9:

            self.xxx, self.yyy, self.sum_W, self.mass_sum_deltaP_t, self.xx, self.yy, \
            self.arr_skin, self.arr_skin_two_point, self.loss, self.badVal, self.forecast, self.payback, _ \
                = for_well(self.source_df, self.rdp, par, 1,1, 1, 1, 1, False, L)
        else:
            self.xxx = []
            self.yyy = []
            self.sum_W = []
            self.mass_sum_deltaP_t = []
            self.xx = []
            self.yy = []
            self.arr_skin = []
            self.arr_skin_two_point = []


        temp = self.source_df["Закачка ТР"].tolist()
        temp = [x for x in temp if x != 0]

        if len(temp) > 9:


            self.TR_xxx, self.TR_yyy, self.TR_sum_W, self.TR_mass_sum_deltaP_t,   self.TR_xx, self.TR_yy, \
        self.TR_arr_skin, self.TR_arr_skin_two_point,  _,_,_,_, self.TR_cut = for_well(self.source_df, self.rdp, par, 1,1, 1, 1, 1, True, L)

        else:
            self.TR_xxx = []
            self.TR_yyy = []
            self.TR_sum_W = []
            self.TR_mass_sum_deltaP_t = []
            self.TR_xx = []
            self.TR_yy = []
            self.TR_arr_skin = []
            self.TR_arr_skin_two_point = []





    def setPar(self, r, m, rad):

        self.rdp = r
        self.minHall = m
        self.radio = rad
