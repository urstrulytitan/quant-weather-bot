def gks(s_slip, s_es, s_ssp, s_fill, w=(0.30,0.30,0.25,0.15)):
    return w[0]*s_slip + w[1]*s_es + w[2]*s_ssp + w[3]*s_fill

def gks_state(g):
    if g < 0.4: return "NORMAL"
    if g < 0.7: return "REDUCE"
    if g < 0.9: return "EXIT_ONLY"
    return "HALT"