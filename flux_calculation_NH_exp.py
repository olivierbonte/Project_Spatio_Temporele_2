import numpy as np
import matplotlib.pyplot as plt

def OutfluxNH(NH_h, NH_d, Acell, deltat, deltax, correction, n, vmax_CFL): #voeg vmax_CFL toe later
    '''
    Berkent de flux naar elk van de naburige cellen.
    Geeft deze terug in een array van lengte 4 (want 4 cellen).
    Volgorde van de outputs: F1, F2, F4, F5 (zie conventie p. 679)
    Benodigde inputs (altijd vologrode 1-> 5 voor buren)
    -NH_h: de hoogtes van de DEM van de NH
    -NH_d: de waterdieptes van de NH
    -Acell: constante oppervlakte van 1 grid cell
    -deltat
    -deltax
    -correction voor de hele flux correctie
    -n = manningscoefficient
    '''
    watersurface_elv = NH_h + NH_d #sommeer de twee
    indices_sorted = np.argsort(watersurface_elv)
    watersurface_elv_sorted = np.sort(watersurface_elv)
    NH_d_sorted = NH_d[indices_sorted]
    DWLs = np.zeros(len(NH_d_sorted)-1)
    for i in range(len(DWLs)):
        DWLs[i] = watersurface_elv_sorted[i+1]-watersurface_elv_sorted[i]

    dc = NH_d[2] #we definiëren centrale cell altijd als 3e input!, = d0
    V0 = dc*Acell
    rc = np.where(indices_sorted == 2)[0]   #rank of the central cell

    #oude paper (flood_analysis_bis) maakt gebruik van andere definitie van DWLS
    DWLsold = np.zeros(len(NH_d_sorted)-1)
    for i in range(len(DWLs)):
        DWLsold[i] = -1*watersurface_elv_sorted[i] + watersurface_elv_sorted[rc]

    DeltaVis = np.zeros(5)
    for i in np.arange(0,int(rc)):
        term1 = V0 - np.sum(DeltaVis) #wat kan gegeven worden
        term2 = (i+1)/(i+2)*(Acell*DWLsold[i]-np.sum(DeltaVis))    #aanpassen omdat onze i één waarde lager
        term3 = (i+1)*Acell*DWLs[i] #hier gebruik van formule uit onze paper, deze is equivalent
        #met formule uit oude paper aangezien DWLs bij ons gedefinieerd als verschil tussen 2 lagen (terwijl in oude paper)
        #als verschil met centrale lage. Idee term3: wat beschikbaar is
        DeltaVis[i] = np.min([term1,term2,term3])
    Fluxes = np.zeros(5)
    for i in np.arange(0,int(rc)):
            for j in np.arange(i, int(rc)):
                Fluxes[i] = Fluxes[i] + DeltaVis[j]/(j+1) 
    #Asssign Fluxes to the proper cell
    F1 = Fluxes[indices_sorted == 0]
    F2 = Fluxes[indices_sorted == 1]
    F4 = Fluxes[indices_sorted == 3]
    F5 = Fluxes[indices_sorted == 4]

    Fout = np.hstack([F1,F2,F4,F5])
    #vstars = np.zeros(len(Fout)) #the interfacial velocities
    WLC = watersurface_elv[2] #of the central cell
    zC = NH_h[2] #height of the centrall cell
    if correction == True:
        d = dc #depth of the central cell
        for i in range(len(Fout)):
            if i <= 1: #so for 1 and 2 (indices 0 and 1 in Fout)
                WLN = watersurface_elv[i]
                zN = NH_h[i]
                dstar = np.max([WLC,WLN])-np.max([zN,zC])
                if not(dstar == 0):
                    vstar = Fout[i]/(deltax*deltat*dstar)
                else:
                    vstar = 0
                S = np.abs(watersurface_elv[2]-watersurface_elv[i])/deltax #delen door deltax want een helling! 
            elif i > 1: #so for NH 4 and 5 (indices 2 and 3  in Fout)
                WLN = watersurface_elv[i+1]
                zN = NH_h[i+1]
                dstar = np.max([WLC,WLN])-np.max([zN,zC])
                if not(dstar == 0):
                    vstar = Fout[i]/(deltax*deltat*dstar)
                else:
                    vstar = 0
                S = np.abs(watersurface_elv[2]-watersurface_elv[i+1])/deltax
            R = d
            vmin1 = 1/n*R**(2/3)*S**(1/2)
            vmin2 = 9.81*d
            vmax  = np.min([vmin1,vmin2])
            if vmax > vmax_CFL:
                #raise Warning('Pas op: CFL conditie niet meer voldaan')
                deltat_test = deltax/vmax
                if deltat_test < deltat:
                    deltat = deltat_test
            if vstar > vmax:
                Fout[i] = vmax*deltax*deltat*dstar
    return Fout, deltat

