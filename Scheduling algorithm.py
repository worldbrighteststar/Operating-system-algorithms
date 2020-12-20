###########################################################
# 운영체제 project 1
# Implementation Scheduling algorithm
# (polling & deferrable scheduling)

from fractions import gcd
import random
import copy

period_input = True
Ap_task_input = True
periodTask = [] # each task has (T,C) T:주기, C:computation time
ApTask = [] # each teask has (t,C) t:발생time, C:computation time

# defferable server의 주기와 polling service의 주기는 5로 설정
# each way의 capacity는 1로 설정
defferableT = 5 
defferable_capacity = 1
pollingT = 5
polling_capacity = 1

util = 1/5 # defferable server와 polling service 모두 주기:5, capacity:1이므로 미리 추가
hyperperiod = 0



#초기 period task 3개 추가 코드
count = 0

while count != 3:
    # period task의 주기는 10,20,40,80으로 일반화
    r = random.randrange(0,4)
    T = 10 * (2**r)
    # period task의 computation time은 T:10 에 (1~3)을 random으로 갖도록 하며
    # T: z * 10 (z = 2,4,8)의 C는 (1~3)의 범위에 (1/2)*z을 곱한것으로 설정
    # (이는 무난한 초기 설정을 위한 것으로 변형되어도 알고리즘에 문제는 없다.)
    if T == 10:
        C = random.randrange(1,4)
    else:
        C = int((1/2) * (T/10) * random.randrange(1,4))
    temp = [T,C]
    print("random 으로 생성된 period task의 T,C는", temp, "입니다.")
    periodTask.append(temp)
    
    # 추가될 period task를 포함한 utilization이 허용 범위에 있는지 판단
    n = len(periodTask) + 1 # 1은 polling 또는 deferable 이다.
    
    util += C/T
    if util > n*(2**(1/n) - 1):
        periodTask.pop()
        util -= C/T
        print("period task", temp, "는 프로그램에 추가 될 수 없습니다.")
    else:
        count += 1
        if T > hyperperiod:
            hyperperiod = T

# 초기 Aperiod task 3개 추가 코드 
count = 0
while count != 3:
    # Aperiod task의 발생 time이 겹치지 않게 설정
    while True:
        t = random.randrange(1,hyperperiod-10)# Aperiod가 hyperperiod 안에서 끝 날 확률을 높이기 위해 -10.
        if [t,1] in ApTask or [t,2] in ApTask:
            continue
        else:
            break 
    # Aperiod task의 computation time은 1~2로 일반화
    C = random.randrange(1,3)
    temp = [t,C]
    print("random 으로 생성된 Aperiod task의 t(발생 시간),C는", temp, "입니다.")
    ApTask.append(temp)
    count += 1
    
    


# period task 추가 삽입 코드
while period_input == True:
    
    ask = input("period task를 더 추가하시겠습니까? (Y/N) ")
    if ask == 'Y' or ask == 'y':
        # period task의 주기는 10,20,40,80으로 일반화
        r = random.randrange(0,4)
        T = 10 * (2**r)
        # period task의 computation time은 T:10 에 (1~3)을 random으로 갖도록 하며
        # T: z * 10 (z = 2,4,8)의 C는 (1~3)의 범위에 (1/2)*z을 곱한것으로 설정
        if T == 10:
            C = random.randrange(1,4)
        else:
            C = int((1/2) * (T/10) * random.randrange(1,4))
        temp = [T,C]
        periodTask.append(temp)

        # utiliztion 허용범위 판별
        n = len(periodTask) + 1 # 1은 polling 또는 deferable 이다.
        util += C/T
        if util > n*(2**(1/n) - 1):
            periodTask.pop()
            util -= C/T
            print("period task", temp, "는 프로그램에 추가 될 수 없습니다.")
        else:
            print("period task", temp, "가 추가되었습니다.")
            if T > hyperperiod:
                hyperperiod = T
    else:
        period_input = False
        continue
    


# Aperiod task 추가 삽입
while Ap_task_input == True:
    
    ask = input("Aperiod task를 더 추가하시겠습니까? (Y/N) ")
    if ask == 'Y' or ask == 'y':
        # Aperiod task의 발생 time이 겹치지 않게 설정
        while True:
            t = random.randrange(1,hyperperiod-10)
            if [t,1] in ApTask or [t,2] in ApTask:
                continue
            else:
                break 
        # Aperiod task의 computation time은 1~2로 일반화
        C = random.randrange(1,3)
        temp = [t,C]
        print("random 으로 생성된 Aperiod task의 t(발생 시간),C는", temp, "입니다.")
        ApTask.append(temp)

    else:
        Ap_task_input = False
        continue

# period task와 Aperiod task를 우선순위(주기가 짧을수록 우선)대로 정렬
periodTask.sort()
# period task list의 내용 [task number, T, C]로 변경]
for i in range(len(periodTask)):
    periodTask[i].insert(0,i)



ApTask.sort()    
Ap_arrival_list = [] # Aperiod 도착시간 t의 list
for ap in ApTask:
    Ap_arrival_list.append(ap[0])




################################
#생성된 period task 와 Aperiod task 확인
print("생성된 period task List")
for pt in periodTask:
    print(pt[0], ". 주기 :", pt[1], "Computation time :", pt[2])
print("생성된 Aperiod task List")
for i in range (len(ApTask)):
    print(i, ". 도착 시간 :", ApTask[i][0], "Computation time :", ApTask[i][1])


########################################################
# Polling service 
print()
print("polling service Start!")
print("p : period task")
print("Ap : Aperiod task")
print()

#수행중인 task index
nowAP = 0
#polling 주기 이전에 들어온 Aperiod task List
Apstack = []
# 실행되어야 할 period task를 주기마다 추가하는 list
Pstack = []

# Ap task의 waiting time을 저장하는 list
Ap_wait = []
# Aperiod task가 중간에 compute한 시간 => (추후에 average waiting time계산을 정확히 하기 위함)
worktime = 0

reversedPtask = copy.deepcopy(periodTask)
reversedPtask.reverse()
# hyperperiod 단위만큼 반복 - Main program
for i in range(hyperperiod):
    print("t : (",i, "~",i+1, ")", end='  ')


    # period task의 주기가 시작되는 부분이 있으면 Pstack에 삽입
    for pt in reversedPtask:
        if i%pt[1] == 0:
            temp =[pt[0],pt[1],pt[2]]
            Pstack.insert(0, temp)


    # 현재 t에 Aperiod task가 도착했는지 확인 후에 Apstack에 저장
    if i in Ap_arrival_list:
        temp = Ap_arrival_list.index(i)
        print("(Ap", temp, "arrival !)", end='  ')
        t,c = ApTask[temp][0], ApTask[temp][1]
        Apstack.append([t,c])
        
    # polling 주기이고 처리할 Aperiod task가 있다면 처리한다.
    if i%pollingT == 0 and len(Apstack) >= nowAP+1:
        
        print("Ap", nowAP, "execution")
        Apstack[nowAP][1] -= polling_capacity
        if Apstack[nowAP][1] == 0:
            nowAP += 1
            Ap_wait.append(i) # Aperiod task가 끝난 t를 순차적으로 저장해둠 (average waiting time계산을 위해)
        else:
            worktime += 1
        continue

    
    # 처리해야 할 period task가 있는지 확인 후 처리
    if len(Pstack) == 0:
        print("No execution")
        continue 
    print("p", Pstack[0][0], "execution")
    Pstack[0][2] -= 1
    if Pstack[0][2] == 0:
        del Pstack[0]

# polling service 의 Aperiod task average waiting time 계산
for i in range(len(Ap_wait)):
    Ap_wait[i] -= Ap_arrival_list[i]

average_waiting_time_ofpoliing = (sum(Ap_wait)-worktime)/len(Ap_wait)

########################################################
# Deferable server

print()
print("defferable server Start!")
print("p : period task")
print("Ap : Aperiod task")
print()


#수행중인 task index
nowAP = 0
# 실행되어야 할 period task를 주기마다 추가하는 list
Pstack = []
Apstack = []

# Ap task의 waiting time을 저장하는 list
Ap_wait = []
# Aperiod task가 중간에 compute한 시간 => (추후에 average waiting time계산을 정확히 하기 위함)
worktime = 0
# Bandwidth preserve capacity 설정
BP_capacity = defferable_capacity

reversedPtask = copy.deepcopy(periodTask)
reversedPtask.reverse()
# hyperperiod 단위만큼 반복 - Main program
for i in range(hyperperiod):
    print("t : (",i, "~",i+1, ")", end='  ')


    # period task의 주기가 시작되는 부분이 있으면 Pstack에 삽입
    for pt in reversedPtask:
        if i%pt[1] == 0:
            temp =[pt[0],pt[1],pt[2]]
            Pstack.insert(0, temp)


    # 현재 t에 Aperiod task가 도착했는지 확인 후에 처리한다.
    if i in Ap_arrival_list:
        temp = Ap_arrival_list.index(i)
        print("(Ap", temp, "arrival !)", end='  ')
        t,c = ApTask[temp][0], ApTask[temp][1]
        Apstack.append([t,c])
        if BP_capacity > 0:
            print("Ap", nowAP, "execution")
            if Apstack[nowAP][1] > BP_capacity:
                Apstack[nowAP][1] -= BP_capacity
                BP_capacity = 0
                worktime += 1
            else:
                BP_capacity -= Apstack[nowAP][1]
                nowAP += 1
                Ap_wait.append(i)
            continue

    # BP 주기마다 capacity를 1로 초기화 시켜준다.
    if i%defferableT == 0:
        BP_capacity = 1
        if len(Apstack) >= nowAP+1:# Ap task가 쌓여있는 경우 바로 처리해준다.
            print("Ap", nowAP, "execution")
            if Apstack[nowAP][1] > BP_capacity:
                Apstack[nowAP][1] -= BP_capacity
                BP_capacity = 0
                worktime += 1
            else:
                BP_capacity -= Apstack[nowAP][1]
                nowAP += 1
                Ap_wait.append(i)
            continue


    # 처리해야 할 period task가 있는지 확인 후 처리
    if len(Pstack) == 0:
        print("No execution")
        continue 
    print("p", Pstack[0][0], "execution")
    Pstack[0][2] -= 1
    if Pstack[0][2] == 0:
        del Pstack[0]

# Bandwidth preserve 의 Aperiod task average waiting time 계산
for i in range(len(Ap_wait)):
    Ap_wait[i] -= Ap_arrival_list[i]
average_waiting_time_ofBP = (sum(Ap_wait) - worktime)/len(Ap_wait)

print()
print("=======================================================")
print("polling service의 Aperiod average waiting time is", average_waiting_time_ofpoliing)
print("Bandwidth preserve의 Aperiod average waiting time is", average_waiting_time_ofBP)
print("=======================================================")
