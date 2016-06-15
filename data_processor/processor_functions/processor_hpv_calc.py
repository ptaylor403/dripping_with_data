def calc_hpv(mh, claims):
    if claims == 0:
        hpv = 0
    else:
        hpv = mh/claims
    return hpv
