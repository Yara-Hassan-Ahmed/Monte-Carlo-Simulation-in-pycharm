import numpy #to generate random numbers
import simpy #simulation library

#variables
#makes sure to run the simulation correctly(around 2 batches)
NumberOfBatches = 0

#Gear jobs arrive in batches of 10 units and their interarrival times are uniformly distributed between 400 and 600 minutes
maxTime = 600
minTime = 400

Gear1Arrival = 0
Gear2Arrival = 0
Gear3Arrival = 0

Gear1Exit = 0
Gear2Exit = 0
Gear3Exit = 0

ArriveAtMillingG1 = 0
ArriveAtMillingG2 = 0
ArriveAtMillingG3 = 0

BeginMillingG1 = 0
BeginMillingG2 = 0
BeginMillingG3 = 0

waitingMG1 = 0
waitingMG2 = 0
waitingMG3 = 0

ArriveAtDrillingG1 = 0
ArriveAtDrillingG2 = 0
ArriveAtDrillingG3 = 0

BeginDrillingG1 = 0
BeginDrillingG2 = 0
BeginDrillingG3 = 0

waitingDG1 = 0
waitingDG2 = 0
waitingDG3 = 0

ArriveAtPaintingG1 = 0
ArriveAtPaintingG2 = 0
ArriveAtPaintingG3 = 0

BeginPaintingG1 = 0
BeginPaintingG2 = 0
BeginPaintingG3 = 0

waitingPG1 = 0
waitingPG2 = 0
waitingPG3 = 0

ArriveAtPolishingG1 = 0
ArriveAtPolishingG2 = 0
ArriveAtPolishingG3 = 0

BeginPolishingG1 = 0
BeginPolishingG2 = 0
BeginPolishingG3 = 0

# time waited in buffers of each station
waitingPoG1 = 0
waitingPoG2 = 0
waitingPoG3 = 0


# Flow Calculation
counterMi = []
counterDr = []
counterPa = []
counterPo = []

# Small counters are for waiting time of each gear for delays
COUNTER1 = []
COUNTER2 = []
COUNTER3 = []


#7aga gowa el object b capacity mo3ayana,7aga bensha8al 3aliha el project 2akenaha space
env = simpy.Environment()

#2 trucks bamashy kol gear
#resources 7ataha gowa el simulation
truck1 = simpy.Resource(env, capacity=1)
truck2 = simpy.Resource(env, capacity=1)
milling = simpy.Resource(env, capacity=4)
drilling = simpy.Resource(env, capacity=3)
painting = simpy.Resource(env, capacity=2)
polishing = simpy.Resource(env, capacity=1)


#variable, the time program run
Running = 0

def checkIfOutputEqualsZero(num):
    if num == 0:
        return 1
    else:
        return num

###################################### GEAR ONE PROCESS #################################################
def G1(env, Running, truck1, truck2, milling, drilling, painting, polishing):
    ######first thing we see if there is any truck is available to take the gear##########
    # ba3raf delwa2ty el wa2t 2ad eh
    Gear1Arrival = env.now

    #makes gear1 available throughout the whole running time
    # the time it takes pause l7ad el gear t arrive
    yield env.timeout(Running)
    print('\nG1 arrived at: %7.4f ' % (env.now))

################################### Milling Process ################################################
    #asks for both trucks first,if one came, the other is released
    # zay farkret lama banady 3al garcon
    with truck1.request() as req1, truck2.request() as req2:

    # The resource’s request() method generates an event that lets you wait until the resource becomes available again.
        results = yield req1 | req2

    # If you are resumed, you “own” the resource until you release it.
    #law gali req1 2no fady yeb2a 7afkis l req2 2li howa truck2
        if req1 in results:
            truck2.release(req2)
        else:
            truck1.release(req1)

    #time taken by truck to attend to milling station, it takes 1min
        yield env.timeout(1)

    ###### Milling process ######
    #3ashan 2a3arf el wa2t 2li gear arrived fih
        ArriveAtMillingG1 = env.now
        print('\nG1 Arrived at the Milling at: %5.4f' % (env.now))
    #call wa7da men el milling 3ashan ye3mel el process beta3to, we initialized the request reqi
        with milling.request() as reqi:
            #wait until milling buffer becomes available
            # el wa7da fiha 4
            yield reqi #gebt men el milling makan fa keda ana na2ast meno (4-1=3)
            BeginMillingG1 = env.now #7ayebda2 el milling
            print('G1 Started  Milling: %5.4f' % (env.now))
            yield env.timeout(35) #by3mel el process fi 35min
            print('G1 Finished  Milling: %5.4f' % (env.now)) #arrival time + service time

        #### witing time operation for the gear to start milling ####
        waitingMG1 = BeginMillingG1 - ArriveAtMillingG1

        #counterMI is used to calculate the delay
    #ma3 kol gear ba5od el wa2t beta3 el wait time w ba7oto fel array
        counterMi.append(waitingMG1)

################################### Drilling Process ################################################
    with truck1.request() as req1, truck2.request() as req2:
        results = yield req1 | req2
        if req1 in results:
            truck2.release(req1)
        else:
            truck1.release(req2)
        yield env.timeout(3)

        ArriveAtDrillingG1 = env.now
        print('\nG1 Arrived at the Drilling at: %5.4f' % (env.now))

        with drilling.request() as reqi:
            yield reqi
            BeginDrillingG1 = env.now
            print('G1 Started  Drilling: %5.4f' % (env.now))
            yield env.timeout(20)
            print('G1 Finished  Drilling: %5.4f' % (env.now))

        waitingDG1 = BeginDrillingG1 - ArriveAtDrillingG1
        #for delay calculation
        counterDr.append(waitingDG1)

################################### Painting Process ################################################
    with truck1.request() as req1, truck2.request() as req2:
        results = yield req1 | req2
        if req1 in results:
            truck2.release(req2)
        else:
            truck1.release(req1)
        yield env.timeout(1.5)

        ArriveAtpaintingG1 = env.now
        print('\nG1 Arrived at the Painting at: %5.4f' % (env.now))
        with painting.request() as reqi:
            yield reqi
            BeginPaintingG1 = env.now
            print('G1 Started  Painting: %5.4f' % (env.now))
            yield env.timeout(55)

            print('G1 Finished  Painting: %5.4f' % (env.now))

        waitingPG1 = BeginPaintingG1 - ArriveAtpaintingG1
        counterPa.append(waitingPG1)

################################### Polishing Process ################################################
    with truck1.request() as req1, truck2.request() as req2:
        results = yield req1 | req2
        if req1 in results:
            truck2.release(req2)
        else:
            truck1.release(req1)
        yield env.timeout(3)

        ArriveAtPolishingG1 = env.now
        print('\nG1 Arrived at the Polishing at: %5.4f' % (env.now))
        with polishing.request() as reqi:
            #asks if it's avaialbe so the gear can come into service
            yield reqi
            BeginPolishingG1 = env.now
            print('G1 Started  polishing: %5.4f' % (env.now))
            yield env.timeout(15)
            print('G1 Finished  polishing: %5.4f' % (env.now))

        waitingPoG1 = BeginPolishingG1 - ArriveAtPolishingG1
        counterPo.append(waitingPoG1)

################################### Caculating Delays in Gear 1 ################################################
    #counter1 calculates the delay of gear 1 in all stations passed
    counter1 = waitingPoG1 + waitingPG1 + waitingDG1 + waitingMG1
    print("\nGEAR1 Delay = ", counter1) #el delay 2li 2a5ado kolo fi process gear 1
    yield env.timeout(0)
    print('G1 finished: %5.4f' % (env.now))
    Gear1Exit = env.now
    #system time of gear1
    AvgSys1 = (Gear1Exit - Gear1Arrival) #2a5ad wa2t 2ad eh
    print("GEAR1 FLOW = ", AvgSys1)
    #total time spent by gear1 in each station
    COUNTER1.append(AvgSys1)
################################# GEAR ONE PROCESS DONE ###########################

###################################### GEAR TWO PROCESS #################################################
def G2(env, Running, truck1, truck2, milling, drilling, painting, polishing):
    Gear2Arrival = env.now
    yield env.timeout(Running)
    print('\nG2 arrived at: %7.4f ' % (Running))

################################### Milling Process ################################################
    with truck1.request() as req1, truck2.request() as req2:
        results = yield req1 | req2
        if req1 in results:
            truck2.release(req2)
        else:
            truck1.release(req1)
        yield env.timeout(1)

        ArriveAtMillingG2 = env.now
        print('\nG2 Arrived at the Milling at: %5.4f' % (env.now))
        with milling.request() as reqi:
            yield reqi
            BeginMillingG2 = env.now
            print('G2 Started  Milling: %5.4f' % (env.now))
            yield env.timeout(25)
            print('G2 Finished  Milling: %5.4f' % (env.now))

        waitingMG2 = BeginMillingG2 - ArriveAtMillingG2
        counterMi.append(waitingMG2)

################################### Painting Process ################################################
    with truck1.request() as req1, truck2.request() as req2:
        results = yield req1 | req2
        if req1 in results:
            truck2.release(req2)
        else:
            truck1.release(req1)
        yield env.timeout(4)

        ArriveAtpaintingG2 = env.now
        print('\nG2 Arrived at the Painting at: %5.4f' % (env.now))
        with painting.request() as reqi:
            yield reqi
            BeginPaintingG2 = env.now
            print('G2 Started  Painting: %5.4f' % (env.now))
            yield env.timeout(35)
            print('G2 Finished  Painting: %5.4f' % (env.now))

        waitingPG2 = BeginPaintingG2 - ArriveAtpaintingG2
        counterPa.append(waitingPG2)

################################### Polishing Process ################################################
    with truck1.request() as req1, truck2.request() as req2:
        results = yield req1 | req2
        if req1 in results:
            truck2.release(req2)
        else:
            truck1.release(req1)
        yield env.timeout(3)

        ArriveAtPolishingG2 = env.now
        print('\nG2 Arrived at the Polishing at: %5.4f' % (env.now))
        with polishing.request() as reqi:
            yield reqi
            BeginPolishingG2 = env.now
            print('G2 Started  Polishing: %5.4f' % (env.now))
            yield env.timeout(15)
            print('G2 Finished  Polishing: %5.4f' % (env.now))

        waitingPoG2 = BeginPolishingG2 - ArriveAtPolishingG2
        counterPo.append(waitingPoG2)

################################### Caculating Delays in Gear 2 ################################################
    counter2 = waitingPoG2 + waitingPG2 + waitingDG2 + waitingMG2
    print("\nGEAR2 Delay = ", counter2)
    yield env.timeout(0)
    print('G2 finished: %7.4f' % (env.now))
    Gear2Exit = env.now
    AvgSys2 = Gear2Exit - Gear2Arrival
    print("GEAR2 FLOW = ", AvgSys2)
    COUNTER2.append(AvgSys2)
################################# GEAR TWO PROCESS DONE ###########################

################################# GEAR THREE PROCESS ###########################
def G3(env, Running, truck1, truck2, milling, drilling, painting, polishing):
    Gear3Arrival = env.now
    yield env.timeout(Running)
    print('\nG3 arrived at: %7.4f ' % (Running))

################################### Drilling Process ################################################
    with truck1.request() as req1, truck2.request() as req2:
        results = yield req1 | req2
        if req1 in results:
            truck2.release(req2)
        else:
            truck1.release(req1)
        yield env.timeout(1)

        ArriveAtDrillingG3 = env.now
        print('\nG3 Arrived at the Driling at: %7.4f' % (env.now))
        with drilling.request() as reqi:
            yield reqi
            BeginDrillingG3 = env.now
            print('G3 Started  Drilling: %7.4f' % (env.now))
            yield env.timeout(18)
            print('G3 Finished  Drilling: %7.4f' % (env.now))

        waitingDG3 = BeginDrillingG3 - ArriveAtDrillingG3
        counterDr.append(waitingDG3)

################################### Painting Process ################################################
    with truck1.request() as req1, truck2.request() as req2:
        results = yield req1 | req2
        if req1 in results:
            truck2.release(req2)
        else:
            truck1.release(req1)
        yield env.timeout(1.5)

        ArriveAtpaintingG3 = env.now
        print('\nG3 Arrived at the Painting at: %7.4f' % (env.now))
        with painting.request() as reqi:
            yield reqi
            BeginPaintingG3 = env.now
            print('G3 Started  Painting: %7.4f' % (env.now))
            yield env.timeout(35)
            EndpaintingG3 = env.now
            print('G3 Finished  Painting: %7.4f' % (env.now))

        waitingPG3 = BeginPaintingG3 - ArriveAtpaintingG3
        counterPa.append(waitingPG3)

################################### Polishing Process ################################################
    with truck1.request() as req1, truck2.request() as req2:
        results = yield req1 | req2
        if req1 in results:
            truck2.release(req2)
        else:
            truck1.release(req1)
        yield env.timeout(3)

        ArriveAtPolishingG3 = env.now
        print('\nG3 Arrived at the polishing at: %7.4f' % (env.now))
        with polishing.request() as reqi:
            yield reqi
            BeginPolishingG3 = env.now
            print('G3 Started  Polishing: %7.4f' % (env.now))
            yield env.timeout(15)
            print('G3 Finished  Polishing: %7.4f' % (env.now))

        waitingPoG3 = BeginPolishingG3 - ArriveAtPolishingG3
        counterPo.append(waitingPoG3)

################################### Caculating Delays in Gear 3 ################################################
    counter3 = waitingPoG3 + waitingDG3 + waitingPG3 + waitingMG3
    print("\nGEAR3 Delay = ", counter3)
    yield env.timeout(0)
    print('G3 finished: %7.4f' % (env.now))
    Gear3Exit = env.now
    AvgSys3 = Gear3Exit - Gear3Arrival
    print("GEAR3 FLOW = ", AvgSys3)
    COUNTER3.append(AvgSys3)
################################# GEAR THREE PROCESS DONE ###########################

gear1Batch = 0
gear2Batch = 0
gear3Batch = 0
total_number_gears1 = 0
total_number_gears2 = 0
total_number_gears3 = 0
#toul ma howa b run fi 480 w byigili batch men 400-600
while Running <= (8*60) and NumberOfBatches < 1:
    #ma3ana array b size 10 w bn generate random num men 1 l 100
    x = numpy.random.randint(1, 101, 10)
    #print(x)

    for i in x:
#arriving batches, 50% are of type G1
        if i >= 0 and i <= 50:
            env.process(G1(env, Running, truck1, truck2, milling, drilling, painting, polishing))
            #calculates total gear 1 in this batch
            gear1Batch = gear1Batch + 1

#arriving batches, 30% are of type G2
        elif i > 50 and i <= 80:
            env.process(G2(env, Running, truck1, truck2, milling, drilling, painting, polishing))
            #calculates total gear 2 in this batch
            gear2Batch = gear2Batch + 1

#arriving batches, 20% are of type G3
        elif i > 80 and i <= 100:
            env.process(G3(env, Running, truck1, truck2, milling, drilling, painting, polishing))
            #calculates total gear 3 in this batch
            gear3Batch = gear3Batch + 1

    #print(z)
    #print(y)
    #print(t)

    # total_number_gears1 signifies total gears in all
    total_number_gears1 += gear1Batch
    total_number_gears2 += gear2Batch
    total_number_gears3 += gear3Batch
    #print(total_number_gears1, total_number_gears2, total_number_gears3)

#interval of time between batches el wa2t el batches bt arrive fiha
    Running = numpy.random.uniform(minTime, maxTime)

    #Return_correct_interval(Running)
    #bagib 3adad l batches
    NumberOfBatches += 1
    #print(Running)
    #by rest el batches 3ashan ne3mel el batches 2li ba3daha
    gear1Batch=0
    gear2Batch=0
    gear3Batch=0

env.run(until=480)

print("________________________________________________")
print("GEARS FLOW")
print("________________________________________________")
sum1 = 0
#COUNTER1
for i in COUNTER1:
    sum1 = sum1 + i
print("Gear 1 TotalFlow: ", sum1 / checkIfOutputEqualsZero(total_number_gears1))

sum2 = 0
for i in COUNTER2:
    sum2 = sum2 + i
print("Gear 2 TotalFlow: ", sum2 / checkIfOutputEqualsZero(total_number_gears2))

sum3 = 0
for i in COUNTER3:
    sum3 = sum3 + i
print("Gear 3 TotalFlow: ", sum3 / checkIfOutputEqualsZero(total_number_gears3))

print("________________________________________________")
print("GEARS DELAY")
print("________________________________________________")

sumM = 0
for i in counterMi:
    sumM = sumM + i

#How much time the gears have wasted time in each station
delayMi = sumM / checkIfOutputEqualsZero((total_number_gears1 + total_number_gears2))
print("Milling total delay: ", delayMi)

sum2 = 0
for i in counterDr:
    sum2 = sum2 + i
delayDr = sum2 / checkIfOutputEqualsZero((total_number_gears1 + total_number_gears3))

print("Drilling total delay: ", delayDr)

sum3 = 0
for i in counterPa:
    sum3 = sum3 + i
delayPa = sum3/checkIfOutputEqualsZero((total_number_gears1 + total_number_gears2 + total_number_gears3))

print("Painting total delay: ", delayPa)

sum4 = 0
for i in counterPo:
    sum4 = sum4 + i
delayPo = sum4 / checkIfOutputEqualsZero((total_number_gears1 + total_number_gears2 + total_number_gears3))

print("Polishing total delay: ", delayPo)

print("________________________________________________")
print("GEARS Utilization")
print("________________________________________________")
#dah el wa2t 2li process 2eshta8lit fih men el wa2t heya 1 - (delay beta3aha / 480)
#-- 1 dah 100% 2no 2eshta8al bashil meno el delay beta3o 2li ma2soum 3ala 480
print("Utilizations for milling: ", 1 - (delayMi / 480))

print("Utilizations for drilling: ", 1 - (delayDr / 480))

print("Utilizations for painting: ", 1 - (delayPa / 480))

print("Utilizations for polishing: ", 1 - (delayPo / 480))