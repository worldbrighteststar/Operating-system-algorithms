###########################################################
# 운영체제 project 
# Buffer cache 
# buffer cache 구현을 위한 5가지 scenario 구현
# program =====================================
# mode size : 5
# buffer cache size : modesize ** 2
# processes : (0~100) 안에서 random하게 사용  
# =============================================


import random
import time

mode_size = 5 # hash queue mode 종류는 5로 지정
cache_size = mode_size**2

allprocess = []
buffer_cache = [[] for i in range(mode_size)]
busy_bf = [] # 현재 busy 상태인 process list
delayed_bf = [] # 현재 delayed된 process list
writing_bf = [] # 현재 dick로 write하고 있는 process list
free_list = [] 

# initializing
for i in range(cache_size):
    while True:
        num = random.randrange(0, 100)
        if num in allprocess:
            continue
        allprocess.append(num)
        break

# 생성한 process들을 hash queue에 저장
for i in allprocess:
    if i % mode_size == 0:
        buffer_cache[0].append(i)
    elif i % mode_size == 1:
        buffer_cache[1].append(i)
    elif i % mode_size == 2:
        buffer_cache[2].append(i)
    elif i % mode_size == 3:
        buffer_cache[3].append(i)
    else:
        buffer_cache[4].append(i)

allprocess_sorted = []
for i in buffer_cache:
    allprocess_sorted += i
# initializes busy blocks 
for i in range(int(cache_size*(2/3))):
    while True:
        choice = random.randrange(cache_size)
        if allprocess_sorted[choice] in busy_bf:
            continue
        busy_bf.append(allprocess_sorted[choice])
        break

# set free list
for i in allprocess:
    if i not in busy_bf:
        free_list.append(i)

# initialize delayed processes
for i in range(int(mode_size/2)):
    while True:
        choice = random.randrange(cache_size)
        if allprocess_sorted[choice] in free_list and allprocess_sorted[choice] not in delayed_bf:
            delayed_bf.append(allprocess_sorted[choice])
            break

print("BUFFER CACHE")
index = 0
for i in buffer_cache:
    print("Block number", index, "mode", mode_size, ':', end=' ')
    for j in i:
        print(str(j).ljust(2), end=' ')
    index += 1
    print()

print("Busy_buffer", busy_bf)
print("Delayed_ buffer", delayed_bf)
print("Freelist :", end=' ')
index = 0
for i in free_list:
    print(i, end=' ')
    index +=1
    if index < len(free_list):
        print('-', end=' ')
print()

print()
print("========================================================")
while True:
    input_block = input("Input block number in range(0,100) or exit(e or E): ")
    if  input_block == 'e' or input_block == 'E' or int(input_block) not in range(0,100):
        print("exit")
        break
    print()
    input_block = int(input_block)
    if input_block in allprocess: # if block in hash queue
        print(input_block, "is in hash queue.")
        if input_block in busy_bf: # scenario 5
            print("block", input_block, "is busy")
            
            for i in range(random.randrange(10)):
                print("waiting until block", input_block, "is free...")
                time.sleep(1)
            
            busy_bf.remove(input_block)
            free_list.append(input_block)
            print("block", input_block, "can be used from now!")
            
        else: # scenario 1
            free_list.remove(input_block)
            busy_bf.append(input_block)
            print("block", input_block, "is successfully used and becomes busy.")
            
    
    else: # block not on hash queue
        print(input_block, "is not in hash queue.")
        if len(free_list) == 0: # scenario 4 : there are no buffers on free list
            for i in range(random.randrange(10)):
                print("waiting until any bock is free...")
                time.sleep(1)
            # make a busy block becomes free
            willbefree_index = random.randrange(len(busy_bf))
            befreeblk = busy_bf[willbefree_index]
            del busy_bf[willbefree_index]
            free_list.append(befreeblk)
            print("block", befreeblk, "is in free list now!")


        if free_list[0] in delayed_bf: # scenario 3
            # 사용할 수 있는 block 앞에 있는 delayed block을 모두 freelist에서 제거
            for i in free_list:
                if i in delayed_bf:
                    free_list.remove(i)
                    delayed_bf.remove(i)
                    writing_bf.append(i)
                    print("block", i, "is delayed, so it will be written to disk.")

                else:
                    break
    
            releasedblk = free_list[0] # block will be used
            del free_list[0] # free block에서 가장 오래된 block 제거
            print("block", releasedblk,"in free list is released for block", input_block)
            # remove the block from buffer_cache as well
            allprocess.remove(releasedblk)
            blkno = releasedblk % mode_size
            for i in buffer_cache[blkno]:
                if i == releasedblk:
                    buffer_cache[blkno].remove(releasedblk)


            # make a new block for inputed_block with the removed block and make it busy 
            blkno = input_block // mode_size
            allprocess.append(input_block)
            buffer_cache[blkno].append(input_block)
            busy_bf.append(input_block)
            print("block", input_block, "is successfully used and becomes busy.")
            # block(s) writing to disk is finished the work and linked at the head of free list
            for i in writing_bf:
                free_list.insert(0, i)
        else: # scenario 2
            releasedblk = free_list[0] # block will be used
            del free_list[0] # free block에서 가장 오래된 block 제거
            print("block", releasedblk,"in free list is released for block", input_block)
            # remove the block from buffer_cache as well
            allprocess.remove(releasedblk)
            blkno = releasedblk % mode_size
            for i in buffer_cache[blkno]:
                if i == releasedblk:
                    buffer_cache[blkno].remove(releasedblk)

            # make a new block for inputed_block and make it busy 
            blkno = input_block % mode_size
            allprocess.append(input_block)
            buffer_cache[blkno].append(input_block)
            busy_bf.append(input_block)
            print("block", input_block, "is successfully used and becomes busy.")

    print()
    print("BUFFER CACHE")
    index = 0
    for i in buffer_cache:
        print("Block number", index, "mode", mode_size, ':', end=' ')
        for j in i: 
            print(str(j).ljust(2) , end=' ')
        index += 1
        print()

    print("Busy_buffer", busy_bf)
    print("Delayed_ buffer", delayed_bf)
    print("Freelist :", end=' ')
    index = 0
    for i in free_list:
        print(i, end=' ')
        index +=1
        if index < len(free_list):
            print('-', end=' ')
    print()
    print("========================================================")
