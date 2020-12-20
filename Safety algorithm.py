###########################################################
# 운영체제 project 2
# safety algorithm
# for deadlock avoidence
#
# program =====================================
# process 개수(3~99) : 입력 
# resource 개수(2~9) : 입력
# resource마다 instance 개수(1~99) : 랜덤
# MAX, ALLOCATION 설정 : 논리적인 범위 안에서 랜덤 
# =============================================

import random

resource_type = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
# process와 resource type의 개수를 입력받는다 (예외처리는 x)
n_process = int(input("the number of processes(3~99) :"))
n_resource = int(input("the number of resources(2~9) :"))
available = [0] * n_resource # 각 resource들의 available을 저장할 list 

#process들의 allocation, max, need를 저장할 lists
process_max = [[0]*n_resource for i in range(n_process)]
process_need = [[0]*n_resource for i in range(n_process)]
process_alloc = [[0]*n_resource for i in range(n_process)] # contains initialized process allocation
#resource type과 해당 resource가 가지는 instance를 저장할 dinctionary
resource_dic = {} 

# initialize resource info
for i in range(n_resource):
    n = random.randrange(1, 100)# instance 개수
    # resource정보와 available에 random으로 생성된 instance수를 저장
    resource_dic[resource_type[i]] = n
    available[i] = n # process의 allocation 초기화시 minus해줄것.

# initailize process MAX
for i in range(n_process): 
    index = 0
    for j in resource_dic.values():
        # 두개 이상의 process의 max가 resource가 가지고 있는 instance의 수와 비슷해지면
        # deadlock avoidance가 불가능한 경우가 만들어질 가능성이 크기 때문에 max를 process개수에 따라 적절하게 제한함. 
        temp_max = random.randrange(0, int(j/(n_process//10 + 1))+1)
        process_max[i][index] = temp_max
        index += 1

# initialize process allocation

list_index = 0
for i in process_max:
    index = 0
    for j in i:
        # 현재의 available(초기화 도중의)가 해당 process의 max보다 크거나 같은 경우
        if available[index] >= j:
            temp_alloc = random.randrange(0, int(j/3)+1) # deadlock avoidance가 가능할 확률을 증가 시키기 위해 alloc제한
            process_alloc[list_index][index] = temp_alloc
            available[index] -= temp_alloc
        # ... 작은 경우 : max가 아닌 available 값 보다 작게 random한 값을 allocation
        else:
            temp_alloc = random.randrange(0, int(available[index]/3)+1)# deadlock avoidance가 가능할 확률을 증가 시키기 위함 
            process_alloc[list_index][index] = temp_alloc
            available[index] -= temp_alloc
        index += 1
    list_index += 1

# calculate process NEED
for i in range(n_process):
    for j in range(n_resource):
        process_need[i][j] = process_max[i][j] - process_alloc[i][j]


print("RESOURCE info")
print(resource_dic)
print("====MAX====")
for i in range(n_process):
    print("process", i, ':', end = ' ')
    for j in process_max[i]:
        print(j, end = ' ')
    print()
print("====NEED====")
for i in range(n_process):
    print("process", i, ':', end = ' ')
    for j in process_need[i]:
        print(j, end = ' ')
    print()
print("====ALLOCATION====")
for i in range(n_process):
    print("process", i, ':', end = ' ')
    for j in process_alloc[i]:
        print(j, end = ' ')
    print()
print("AVAILABLE")
print(available)

##########
# safety sequence running !!!
#
# 
print("safety sequence CHECK!!")

finish = [False for i in range(n_process)]
work = available

i = 0 # list index
goback = False # while문 처음으로 가기 위한 boolean
deadlock = False # deadlock에 걸렸을 시 다른 작업 없이 while문을 나가기 위한 boolean
while True:
    # index > number of process : safety sequence 
    if i == n_process:
        print("system is in a SAFE state!")
        break
    # If finish[i] is False, process 'i' is still executing
    if finish[i] == False:
        goback = False
        for j in range(n_resource):
            # check if a need is bigger than available, then process 'i' cannot request for the need
            if process_need[i][j] > work[j]:
                i += 1
                # if process 'i' is the last one, no more process cannot request, so it may be unsafe
                if i == n_process:
                    print("system is in an UNSAFE state")
                    deadlock = True
                    break
                goback = True
                continue

        if deadlock == True:
            break
        if goback == True:
            continue
        # process 'i' requests ...
        print("------------------------------------------")
        print("Process", i, "request", process_need[i])
        for j in range(n_resource):
            work[j] += process_alloc[i][j]
        print("current available :", work)
        print("------------------------------------------")
        finish[i] = True
        i = 0
    else:
        i += 1


##########
