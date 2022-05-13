import numpy as np
import matplotlib.pyplot as plt

def OutfluxNH(NH_h, NH_d):
    '''
    Berkent de flux naar elk van de naburige cellen.
    Geeft deze terug in een array van lengte 4 (want 4 cellen).
    Volgorde van de outputs: F1, F2, F4, F5 (zie conventie p. 679)
    Benodigde inputs (altijd vologrode 1-> 5 voor buren)
    -NH_h: de hoogtes van de DEM van de NH
    -NH_d: de waterdieptes van de NH
    '''
    watersurface_elv = NH_h + NH_d
    indices_sorted = np.argsort(watersurface_elv)
    