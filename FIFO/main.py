import numpy as np
import json

def generate(n, arrive_t, page_range):
    pages = np.empty((n,2), dtype=int)

    pages[:,0] = np.random.randint(1, arrive_t+1, (n)) #Arrival time
    pages[:,1] = np.random.randint(1, page_range, (n)) #Page ID
    #print(pages) Arrival Time | Page ID
    return pages

def f_queue(f_pages, time_unit):
    f_queue = np.empty((0, 2), dtype=int)

    for i in range(f_pages.shape[0]):
        if f_pages[i, 0] == time_unit:
            f_queue = np.append(f_queue, [f_pages[i]], axis=0)

    return f_queue

with open("config.json", "r") as config:
    data = json.load(config)

hit_rate = open("hit_rate.txt", 'w')
access_time = open("access_time.txt", 'w')

nof = data['number_of_frames']
nop = data['number_of_pages']
arrival = data['arrival_time']
r_page = data['range_of_pages']
t_unit=0 #starting time unit

pages = generate(nop, arrival, r_page)

frames = np.full((nof, 2), [-1])

temp_queue = np.empty((0, 2), dtype=int)
queue = np.empty((0, 2), dtype=int)

#print(frames)
print(pages)

temp_queue = f_queue(pages, t_unit)
queue = np.append(queue, temp_queue, axis=0)

while t_unit <= nop:

    if queue.size > 0:
        t_unit += 1
        temp_queue = f_queue(pages, t_unit)
        queue = np.append(queue, temp_queue, axis=0) #updating queue for current t_unit
        if np.all(frames[:, 0] != queue[0, 1]): #is first queue page already in memory
            oldest_frame_index = np.argmin(frames[:,1]) #find the oldest frame
            frames[oldest_frame_index,0] = queue[0,1] #assign page to frame
            frames[oldest_frame_index,1] = 0 #clear frame age
            hit_rate.write(str(1) + '\n')
            access_time.write(str(t_unit-queue[0,0])+ '\n')
        else:
            hit_rate.write(str(0) + '\n')
        queue = np.delete(queue, 0, axis=0) #deletes replacing or existing page from queue
        print(f'frames | age \n{frames} \n####')
        #print(f'queue \n{queue} \n####')
        frames[:,1] -=1 #increasing age of page in frame

    else:
         #print("waiting for process")
         t_unit += 1
         temp_queue = f_queue(pages, t_unit)
         queue = np.append(queue, temp_queue, axis=0)

hit_rate.close()
access_time.close()