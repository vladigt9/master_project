import numpy as np
import random
import time
from sklearn.utils.extmath import randomized_svd
from sklearn.utils._array_api import get_namespace

def test(X, rows:int, cols:int, n_simulations:int, n_components:int, 
         n_oversamples: int, n_iter: int, normalizer: str, driver:str) -> float:
    
    # Lists created to store test data
    times_rand = []
    sing_values = []
    
    for i in range(n_simulations):
        random.seed(1)
        np.random.seed(1)
        
        st = time.time()
        U, s, Vh = randomized_svd(X, n_components=int(cols*n_components), random_state=1,
                                  n_oversamples=n_oversamples, n_iter=n_iter,
                                  power_iteration_normalizer=normalizer, svd_lapack_driver=driver)
        e = time.time()
        times_rand.append(e-st)
        
        if i == 0:
            sing_values = s
        
    # write a file saving the extracted data from simulations
    with open(f'prem_data_rand/{rows}_{cols}_{n_components}_{n_oversamples}_{n_iter}_{driver}_{normalizer}.txt', 'w') as file:
        file.write(','.join(map(str, ['row', rows, cols, n_components, sum(times_rand)/n_simulations,
                                      n_oversamples, n_iter, normalizer, driver,
                                      '; '.join(map(str, sing_values))])))
    
    return 

def test_svd() -> None:
    
    cols_p = [100, 200, 300]
    # cols_p = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    components = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    n_iter = [0,1,2,3,4,5,6,7,8,9,10]
    # n_oversamples = [0,2,4,6,8,10,12,14,16,18,20]
    n_oversamples = [0, 5, 10, 15, 20]
    normalizer = ['QR', "LU", "none"]
    # driver = ['gesdd', 'gesvd']
    # set the initial number of rows of the matrix
    i = 10000
    
    
    # set the cap for number of columns
    while i <= 15000:
        
        for c in cols_p:
            print(i,c)
            random.seed(1)
            np.random.seed(1)
            X = np.array(np.random.rand(i,c))
            U, Sigma, Vt = np.linalg.svd(X, full_matrices=False)
            n = (([100]*(int(len(Sigma)*2/100)))+([0.01]*(int(len(Sigma)*98/100))))
            X = U@(np.diag(Sigma)*n)@Vt
            xp, _ = get_namespace(X)
            mean_ = xp.mean(X, axis=0)
            X_centered = xp.asarray(X, copy=True)
            X_centered -= mean_
            
            for comp in components:
                print(f'comp {comp}')
                for it in n_iter:
                    print(f'iterations: {it}')
                    for ov in n_oversamples:
                        print(f'oversamples {ov}')
                        for n in normalizer:
                            # for d in driver:
                            test(X=X_centered, rows=i,cols=c,n_simulations=15,
                                    n_components=comp,n_iter=it,
                                    n_oversamples=ov, normalizer=n, driver='gesdd')
        
        i+=10000

    return
