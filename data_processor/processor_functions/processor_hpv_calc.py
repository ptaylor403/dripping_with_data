def calc_hpv(mh, claims):
    """

    :param mh: Integer value - total manhours.
    :param mh: Integer value - total claims.
    :return: Float value - hpv.
    """
    if claims == 0:
        hpv = 0
    else:
        hpv = mh/claims
    return hpv
