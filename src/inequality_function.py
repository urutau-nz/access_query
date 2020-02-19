'''
Inputs:
    a = distribution of data, type=list
    weight (optional) = list of len(a)
    kappa (optional) = int < 0
    beta (optional, default = -0.5) = int < 0
    epsilon (optional, default = 0.5) = int > 0
Output:
    Kolm-Pollak EDE & Index (kappa)
    Atkinson Adjusted EDE & Index (beta)
    Atkinson EDE & Index (epsilon)
    Gini Index
'''

import numpy as np
from scipy.integrate import simps

def kolm_pollak_ede(a, beta = None, kappa = None, weight = None):
    '''returns the Kolm-Pollak EDE'''
    a = np.asanyarray(a)

    if kappa is None:
        if beta is None:
            raise TypeError("you must provide either a beta or kappa aversion parameter")
        kappa = calc_kappa(a, beta, weight)

    if weight is None:
        ede_sum = np.exp(a*-kappa).sum()
        N = len(a)
    else:
        ede_sum = np.multiply(np.exp(a*-kappa), weight).sum()
        N = sum(weight) # for a weighted average

    ede = (-1 / kappa) * np.log(ede_sum / N)
    return(ede)


def kolm_pollak_index(a, beta = -0.5, kappa = None, weight = None):
    if not kappa: # if kappa is not defined
        kappa = calc_kappa(a, beta, weight)
    else:
        kappa = kappa

    if not weight:
        N = len(a)
    else:
        N = sum(weight) #sum of data

    x_mean = np.average(a, weights = weight)
    index_sum = 0
    count = 0 # used to index weightings
    for x_n in a: # compue the sum of the ede eqn
        if not weight:
            index_sum += np.exp(-kappa * (x_n - x_mean))
        else:
            index_sum += np.exp(-kappa * (x_n - x_mean)) * weight[count]
        count += 1

    index = (-1 / kappa) * np.log(index_sum / N)
    return(index)

def atkinson_adjusted_ede(a, beta = -0.5, weight = None):
    '''returns adjusted atkinson index'''
    ede_sum = 0 # init sum
    if not weight:
        N = len(a)
    else:
        N = sum(weight) #sum of data
    x_mean = np.average(a, weights = weight)
    count = 0

    for i in a:
        if not weight:
            ede_sum += (i**(1-beta))
        else:
            ede_sum += (i**(1-beta)) * weight[count]
        count += 1

    ede = (ede_sum / N)**(1 / (1 - beta))
    return(ede)

def atkinson_adjusted_index(a, beta = -0.5, weight = None):
    ede_sum = 0 # init sum
    if not weight:
        N = len(a)
    else:
        N = sum(weight) #sum of data
    x_mean = np.average(a, weights = weight)
    count = 0

    for i in a:
        if not weight:
            ede_sum += (i**(1-beta))
        else:
            ede_sum += (i**(1-beta)) * weight[count]
        count += 1

    ede = (ede_sum / N)**(1 / (1 - beta))

    index = (ede / x_mean) - 1
    return(index)

def atkinson_ede(a, epsilon = -0.5, weight = None):
    '''returns the normal atkinson ede,
    NOTE: this is meant for distributions where high values are better'''
    at_sum = 0
    if not weight:
        N = len(a)
    else:
        N = sum(weight) #sum of data
    x_mean = np.average(a, weights = weight)
    count = 0
    for i in a:
        if not weight:
            at_sum += i**(1 - epsilon)
        else:
            at_sum += (i**(1 - epsilon)) * weight[count]
        count += 1

    ede = (at_sum / N)**(1 / (1 - epsilon))
    return(ede)

def atkinson_index(a, epsilon = -0.5, weight = None):
    ede_sum = 0 # init sum
    if not weight:
        N = len(a)
    else:
        N = sum(weight) #sum of data
    x_mean = np.average(a, weights = weight)
    count = 0

    for i in a:
        if not weight:
            ede_sum += (i**(1-epsilon))
        else:
            ede_sum += (i**(1-epsilon)) * weight[count]
        count += 1

    ede = (ede_sum / N)**(1 / (1 - epsilon))

    index = 1 - (ede / x_mean)
    return(index)

def gini_index(a, beta = -0.5, weight = None):
    area_total = simps(np.arange(0,101,1), dx=1) #Calculates the area under the x=y curve
    if not weight:
        N = len(a)
    else:
        N = sum(weight) #sum of data
    a = list(np.sort(a))
    a_percent = []
    weight_perc = []
    w_perc_sum = 0
    perc_sum = 0
    if not weight:
        for i in a:
            perc_sum += i/data_tot*100
            a_percent.append(perc_sum)
            #w_perc_sum += 1/100
            #weight_perc.append(w_perc_sum)
        area_real = simps(a_percent)#, weight_perc)
        area_diff = area_total - area_real
        gini = round((area_diff / area_total), 3)
    else:
        weight_tot = sum(weight)
        data_tot = sum(a)
        for i in a:
            perc_sum += i/data_tot*100
            a_percent.append(perc_sum)

        for i in weight:
            w_perc_sum += i/weight_tot*100
            weight_perc.append(w_perc_sum)

        area_real = simps(a_percent, weight_perc)
        area_diff = area_total - area_real
        gini = round((area_diff / area_total), 3)
    return(gini)

def calc_kappa(a, beta, weight = None):
    '''calculates kappa by minimising the sum of squares'''
    if weight != None:
        kappa_data = [] # init list
        count = 0 # used for indexing weights
        for i in a:
            for weighting in range(int(weight[count])):
                kappa_data.append(i)
    else:
        kappa_data = a

    x_sum = 0 # init sum
    x_sq_sum = 0 # init x squared sum
    for x in kappa_data:
        x_sum += x
        x_sq_sum += x**2
    kappa = beta * (x_sum / x_sq_sum)

    return(kappa)
