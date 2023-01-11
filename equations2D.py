import  numpy as np
import matplotlib.pyplot as plt

def mono_dyn(t,N,F):

    f1 = (2/(np.sum(N)**2))*(F[0][0]*N[0]+ F[0][1]*N[1] )
    f2 = (2/(np.sum(N)**2))*(F[1][1]*N[1]+ F[1][0]*N[0] )
    n1 = N[0]*np.exp(-np.multiply( f1,t))
    n2 = N[1]*np.exp(-np.multiply( f2,t))
    return [n1,n2]


def pars(Ntot,F1,vr,ve,v2):
    return ([Ntot/(1+vr),(vr*Ntot)/(1+vr)], [[F1,ve*F1],[ve*F1,v2*F1]])

if __name__ == '__main__':

    vr = 1
    ve = 0
    v2 = 1
    F1 = 1
    Ntot = 500

    N,F = pars(Ntot,F1,vr,ve,v2)


    t = np.linspace(0,2500)
    nm = mono_dyn(t,N,F)
    print(nm)

    plt.plot(t,nm[0])
    plt.plot(t, nm[1])
    print("hello")
    plt.show()
