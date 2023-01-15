import numpy as np
import json

#generates 'n' processes with random arrival/burst time from arrival/burst_t range
def generate(n, arrive_t, burst_t):
    processes = np.empty((n,2), dtype=int)
    processes[:,0] = np.random.randint(1, arrive_t+1, (n))
    processes[:,1] = np.random.randint(1, burst_t+1, (n))

    return processes

#manages queue depending on symulation time
def f_queue(list_of_processes, time_unit):
    f_queue = np.empty((0, 2), dtype=int)
    for i in range(list_of_processes.shape[0]):
        if list_of_processes[i, 0] == time_unit:
            f_queue = np.append(f_queue, [list_of_processes[i]], axis=0)
    return f_queue

#data preparation
with open("config.json", "r") as config:
    data = json.load(config)

results = open("results.txt", 'w')

nop = data['number_of_processes']
arrival = data['arrival_time']
burst = data['burst_time']
t_unit=0 #global time unit
processes = generate(nop, arrival, burst)



##execution
temp_queue = np.empty((0, 2), dtype=int)
queue = np.empty((0, 2), dtype=int)
#temp_burst = 0
print(f'{processes}, \n#####')

burst_sum = sum(processes[:,1])
while t_unit <= nop*4:
    #execution
    print(f'{queue}, \n#####')
    if queue.size > 0:
        temp_burst = queue[0, 1] #burst time of first in queue
        temp_arrival = queue[0,0] #arrival time of first in queue
        for i in range(temp_burst): #executing process for (burst time)[units]
            t_unit += 1
            temp_queue = f_queue(processes, t_unit) #each time t_unit itterates, queue is updated
            queue = np.append(queue, temp_queue, axis=0)
        print(f'process has finished at: {t_unit}. process was alive for: {t_unit-temp_arrival}, it was waiting {t_unit-temp_burst-temp_arrival} for execution')
        results.write(str(t_unit-temp_burst-temp_arrival) + '\n')
        queue = np.delete(queue, 0, axis=0)  #deleting process from queue after its finished

    #waiting for process if queue is empty
    else:
        print("waiting for process")
        t_unit += 1
        temp_queue = f_queue(processes, t_unit)
        queue = np.append(queue, temp_queue, axis=0)

results.close()
