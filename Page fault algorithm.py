###########################################################
# 운영체제 project 
# Virtual Memory : page fault
# FIFO, LRU, OPTIMAL 방식으로 구현 
#
# program =====================================
# frame size : 사용자지정
# reference : frame size * 5
# a range of number used for the reference : frame size * 3 
# =============================================

import random
import copy

# Initializing
sizeofFrame = int(input("frame size is (10~199) :"))
sizeofReference = sizeofFrame * 5
reference = ""

for i in range(sizeofReference):
    num = random.randrange(0, sizeofFrame * 2)
    num = str(num) + ' '
    reference += num

print("REFERENCE is",reference)

# change evert element in reference to integer form
reference = reference.split()
for i in range(len(reference)):
    reference[i] = int(reference[i])
    

page_fault = [] # the number of page_fault in each case of algorithms[FIFO, LRU, OPTIMAL]


###################    
# FIFO
print("<< FIFO >>")
frame = [] # abstracted frame
fifo_list = [] # for checking what page have to be expired
count = 0 # count for page_fault
for i in range(len(reference)):
    page = reference[i]
    fifo_list.append(page)
    s = str(i+1).ljust(3) + ": " + "PAGE " + str(page).ljust(3) + "requires allocation" 
    print(s, end=' ')
    # frame에 현재 required page가 없을 경우
    if page not in frame:
        
        # needs page fault : frame is full 이므로,
        if len(frame) == sizeofFrame:
            pf = fifo_list[0]
            print("=> PAGE-FAULT :", pf, end='')
            minus = 0 # list 요소 삭제시 index순서를 맞추기 위한 변수
            # fifo_list에서 First out이 되야 할 page를 모두 삭제
            for j in range(len(fifo_list)):
                if fifo_list[j-minus] == pf:
                    del fifo_list[j-minus]
                    minus += 1
            count += 1 # increase page-fault count(s)
            
            # page-fault된 page를 frame에서 제거
            index = 0
            for j in frame:
                if j == pf:
                    break
                index += 1
            del frame[index]

            # frame에 page 할당
            frame.append(page)
    
        # frame에 바로 할당 가능.
        else:
            frame.append(page)
    print()
page_fault.append(count)

print("==========================================================")
###################    
# LRU
print("<< LRU >>")
frame = []
lru_list = [] # for checking what page have to be expired
count = 0 # count for page_fault
for i in range(len(reference)):
    page = reference[i]
    # 만약 current page가 frame에 있다면 이전 사용 기록을 최신으로 갱신
    if page in lru_list:
        for j in range(len(lru_list)):
            if page == lru_list[j]:
                del lru_list[j]
                break
    lru_list.append(page)
    s = str(i+1).ljust(3) + ": " + "PAGE " + str(page).ljust(3) + "requires allocation" 
    print(s, end=' ')
    # frame에 현재 required page가 없을 경우
    if page not in frame:
        
        # needs page fault : frame is full 이므로,
        if len(frame) == sizeofFrame:
            pf = lru_list[0]
            print("=> PAGE-FAULT :", pf, end='')
            
            # lru_list에서 out 이 되야 할 page를 삭제
            del lru_list[0]
            count += 1 # increase page-fault count(s)
            
            # page-fault된 page를 frame에서 제거
            index = 0
            for j in frame:
                if j == pf:
                    break
                index += 1
            del frame[index]

            # frame에 page 할당
            frame.append(page)
    
        # frame에 바로 할당 가능.
        else:
            frame.append(page)
    print()
page_fault.append(count)
print("==========================================================")

###################    
# OPTIMAL
print("<< OPTIMAL >>")
frame = []
opimal_list = copy.deepcopy(reference) # for checking what page have to be expired
count = 0 # count for page_fault
for i in range(len(reference)):
    page = reference[i]
    del opimal_list[0]

    s = str(i+1).ljust(3) + ": " + "PAGE " + str(page).ljust(3) + "requires allocation" 
    print(s, end=' ')
    # frame에 현재 required page가 없을 경우
    if page not in frame:
        
        # needs page fault : frame is full 이므로,
        if len(frame) == sizeofFrame:
            findpf = copy.deepcopy(frame)
            # 앞으로 나올 page들을 검사하며 frame에 속한 page는 page-fault 대상에서 제외
            for j in opimal_list:
                if len(findpf) == 1: # page-fault 대상이 하나만 남았다면 page-fault 대상이 확정
                    break
                if j in findpf:
                    findpf.remove(j)
            pf = findpf[0] 
            print("=> PAGE-FAULT :", pf, end='')
            count += 1 # increase page-fault count(s)
            
            # page-fault된 page를 frame에서 제거
            frame.remove(pf)
            # frame에 page 할당
            frame.append(page)
    
        # frame에 바로 할당 가능.
        else:
            frame.append(page)
    print()
page_fault.append(count)

print("==========================================================")
# each count of the number of page-faults in case of three ways
print()
print("FIFO's PAGE-FAULT :", page_fault[0])
print("LRU's PAGE-FAULT :", page_fault[1])
print("OPTIMAL's PAGE-FAULT :", page_fault[2])

