import time

class Temporizador:
    def __init__(self):
        # #ifdef _WIN32
        #     start_time = GetTickCount()
        # #else
        #     // Figure out time elapsed since last call to idle function
        #     gettimeofday(&start_time, NULL)
        # #endif
        self.start_time = time.time()
        self.ultimo = time.time()

    # // Retorna o tempo decorrido desde a última chamada desta mesma função
    def getDeltaT(self):
        dt = time.time()-self.ultimo
        self.ultimo = time.time()

        return dt


    #ifdef _WIN32
    #     DWORD end_time
    #     end_time = GetTickCount()
    #     dt = (float) (end_time - start_time) / 1000.0
    # #else
    #     // Figure out time elapsed since last call to idle function
    #     struct timeval end_time
    #     gettimeofday(&end_time, NULL)
    #     dt = (float)(end_time.tv_sec  - start_time.tv_sec) + 1.0e-6*(end_time.tv_usec - start_time.tv_usec)
    # #endif
        self.start_time = end_time
        return dt
