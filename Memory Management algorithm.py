###########################################################
# 운영체제 project 
# Memory Management
# allocates in the best fit with coalescing and compaction(priority and binding) 
#
# program =====================================
# process 할당 요청 : 사용자 지정 
# =============================================

# memory size 는 256k 
sizeofMemory = 256
# File content for an order, process는 12개가 사용됨.
input_order = "1 8 2 8 3 16 4 32 5 16 6 16 7 32 8 64 9 32 10 32 1 0 2 0 4 0 6 0 11 64 5 0 7 0 9 0 12 64"

orderlist = input_order.split()

order = [] # order를 [process number, size] 형태의 이중 list로 저장.
for i in range(0, len(orderlist), 2):
    temp = [int(orderlist[i]), int(orderlist[i+1])]
    order.append(temp)

# ====Initializing====
# abstracted memory 
memory = [[0, sizeofMemory]] # ex. [[1, x], [0, y], [2, z]] = [p1 has xk, 0(free block) has yk, p2 has zk]
# the number of blocks
n_block = 1
# free memory
remain = sizeofMemory
# average size of blocks
average = sizeofMemory

# memory managing start!
print("============================================================")
print("TOTAL MEMORY SIZE :", sizeofMemory)

for i in order:
    ###############################
    print("============================================================")
    coalescing = False # coalescing 이 발생했는지 판단
    priority_compaction = False # priority compaction에 부합하여 시행 됬는지 판단
    binding = False # binding compaction이 시행됬는지 판단

    if i[1] != 0: # requests memory
        print("REQUEST", i[0], ":", i[1])
        temp = [i[0], i[1]] # requested block that will be allocated in memory
        # best fit 찾기
        minimum = sizeofMemory+1 # request된 memory size보다 크거나 같은 blocks중 가장 작은 size of block
        bestfit = 0 # best fit's block index in memory
        index = 0
        for j in memory:
            if j[0] == 0:
                if i[1] <= j[1] and j[1] < minimum:
                    minimum = j[1]
                    bestfit = index
            index += 1
        
        # ====compaction====
        if minimum == sizeofMemory+1: # needs compaction for allocation
            first_free = -1
            last_free = -1
            # 모든 free block이 포함되며, 가장 작은 memory 공간 slice를 찾음. 
            for j in range(len(memory)):
                if memory[j][0] == 0 and first_free == -1:
                    first_free = j
                elif memory[j][0] == 0:
                    last_free = j + 1
            needmove = 0
            needmoveindexlist = []# compaction을 위해 이동해야 하는 process를 저장.
            # priority 가능한지 판별
            for j in range(first_free, last_free):
                if memory[j][0] != 0:
                    needmoveindexlist.append(j)
                    needmove += 1
            
            
            if needmove == 2: 
                # priority compaction
                if memory[needmoveindexlist[0]][1] == memory[last_free-1][1]:
                    memory[last_free-1],memory[needmoveindexlist[0]] = memory[needmoveindexlist[0]],memory[last_free-1]
                    
                    priority_compaction = True
                    
                    minus = 0 # list index 삭제시 요소 댕겨짐 방지 변수
                    # compaction 후 coalescing 
                    for j in range(first_free, last_free-1):
                        if memory[j-minus][0] == 0:
                            del memory[j-minus]
                            minus += 1
                    memory.insert(first_free, [0, remain])

                elif memory[needmoveindexlist[1]][1] == memory[first_free][1]:
                    memory[first_free],memory[needmoveindexlist[1]] = memory[needmoveindexlist[1]],memory[first_free]
                    
                    priority_compaction = True
                    
                    minus = 0 # list index 삭제시 요소 댕겨짐 방지 변수
                    # compaction 후 coalescing 
                    for j in range(first_free, last_free-1):
                        if memory[j-minus][0] == 0:
                            del memory[j-minus]
                            minus += 1
                    memory.insert(first_free, [0, remain])

            # 무작위 binding
            if priority_compaction == False: # priority compaction이 불가능하므로 무작위 binding으로 compaction
                memory.insert(first_free, [0, remain])# total size of free block을 하나로 만들고 알맞은 index에 삽입
                minus = 0
                for j in range(first_free+1, last_free+1):# free blocks(생성된 free block을 제외한) 제거 
                    if memory[j-minus][0] == 0:
                        del memory[j-minus]
                        minus += 1
                binding = True

            # 다시 best fit 찾기
            minimum = sizeofMemory+1 # request된 memory size보다 크거나 같은 blocks중 가장 작은 size of block
            bestfit = 0 # best fit's block index in memory
            index = 0
            for j in memory:
                if j[0] == 0:
                    if i[1] <= j[1] and j[1] < minimum:
                        minimum = j[1]
                        bestfit = index
                index += 1
            
        # ==================

        address = 0 # Address of the best fit
        for j in range(bestfit):
            address += memory[j][1]

        print("Best Fit: Allocated at address", address)
        
        # allocates in memory
        if memory[bestfit][1] > i[1]:
            memory[bestfit][1] -= i[1]
            memory.insert(bestfit, temp)
        else:
            memory[bestfit] = temp
        # free memory 
        remain -= i[1]

    ############################
    if i[1] == 0: # free request
        
        index = 0
        for j in memory:
            if j[0] == i[0]:
                j[0] = 0
                print("FREE REQUEST", i[0], ":", j[1])
                # free memory 
                remain += j[1]

                # for coalescing, check right and left sides if each is free block.
                n = 0 # free request한 process의 양쪽에 있는 free block의 개수
                if index != 0: # free request한 process가 memory의 첫번째 index가 아니면,
                    if memory[index-1][0] == 0:
                        n += 1
                elif index != len(memory) - 1: # free request한 process가 memory의 마지막 index가 아니면,
                    if memory[index+1][0] == 0:
                        n += 1
                break
            index += 1
        
        address = 0 # Address of the best fit
        for j in range(index):
            address += memory[j][1]

        print("Best Fit: Allocated at address", address)

        # coalescing
        if n == 1:
            if memory[index-1][0] == 0:
                memory[index][1] += memory[index-1][1]
                del memory[index-1]
            else:
                memory[index][1] += memory[index+1][1]
                del memory[index+1]
            coalescing = True

        elif n == 2:
            memory[index][1] += memory[index-1][1]
            memory[index][1] += memory[index+1][1]
            del memory[index-1]
            del memory[index]
            coalescing = True
        
        

    # average size of block and the number of blocks
    sum = 0
    n = 0
    for j in memory:
        if j[0] == 0:
            sum += j[1]
            n += 1
    if n == 0:
        average = 0
    else:
        average = sum/n

    print(remain, "free,", n, "block(s),", "average size =", round(average,2),'K')
    if coalescing == True:
        print()
        print("<< COALESCING >>")
    if priority_compaction == True:
        print()
        print("<< PRIORITY COMPACTION >>")
    elif binding == True:
        print()
        print("<< BINDING COMPACTION>> ")

    print()
    print("┌───MEMORY───┐")
    index = 0
    for j in memory:
        if j[0] == 0:
            s = str(j[1]) + "K FREE"
            print('│' + s.center(18) + '│')
            if index == len(memory)-1:
                break
            print("├─────────┤")
        else:
            s = "PROCESS " + str(j[0]) + ' : ' + str(j[1]) +'K'
            print('│' + s.ljust(18) + '│')
            if index == len(memory)-1:
                break
            print("├─────────┤")
        index += 1
    print("└─────────┘")
    print("============================================================")




#### free request best fit 출력하기

