import subprocess
import sys

grade = 0

# input matrices
a = []
b = []
c = []
d = []
# check done
j_check = []
l_check = []
r_check = []
cur_r_check = []
# result matrix
result = []
cur_result = []
# dimensions
n = -1
m = -1
k = -1
# threads
t = -1
cur_t = -1
# time range
firstTime = -1
lastTime = -1
cur_firstTime = -1
cur_lastTime = -1
# error flags
flag_count = [0 , 0 , 0 , 0]
flag_thread_count = False
flag_thread_order = False
flag_time_limit = False
flag_unmatch_result = False
flag_overall_time = False


def clearAll():
    global t, firstTime, lastTime
    global flag_count
    global result, cur_result, j_check, l_check, r_check, cur_r_check
    global a, b, c, d

    firstTime = -1
    lastTime = -1
    t = -1

    for i in range(len(flag_count)):
        flag_count[i] = 0
    
    a = []
    b = []
    c = []
    d = []
    cur_result = []
    result = []
    j_check = []
    l_check = []
    r_check = []
    cur_r_check = []

def clearCache():
    global cur_t, cur_firstTime, cur_lastTime
    global cur_result, j_check, l_check, r_check, cur_r_check
    global flag_thread_count, flag_thread_order, flag_time_limit, flag_unmatch_result, flag_overall_time

    flag_thread_count = False
    flag_thread_order = False
    flag_time_limit = False
    flag_unmatch_result = False
    flag_overall_time = False

    cur_firstTime = -1
    cur_lastTime = -1
    cur_t = -1

    cur_result = []

    cur_r_check = []
    for i in range(n):
        cur_r_check.append([])
        for j in range(k):
            cur_r_check[i].append(0)

    j_check = []
    for i in range(n):
        j_check.append([])
        for j in range(m):
            j_check[i].append(0)
    
    l_check = []
    for i in range(m):
        l_check.append([])
        for j in range(k):
            l_check[i].append(0)


# get input matrices a, b, c, and d from input-index-.txt
def assertInput(inputLines):
    global n,m,k
    global j_check, l_check
    n, m = [int(x) for x in inputLines[0].split()]
    for i in range(n):
        values = [int(x) for x in inputLines[i+1].split()]
        a.append(values)
    #print(a)
    
    for i in range(n):
        values = [int(x) for x in inputLines[i+n+2].split()]
        b.append(values)
    #print(b)
    
    for i in range(m):
        values = [int(x) for x in inputLines[i+2*n+3].split()]
        c.append(values)
    #print(c)
    
    for i in range(m):
        values = [int(x) for x in inputLines[i+2*n+m+4].split()]
        d.append(values)
    #print(d)
    k = len(d[0])
    
    for i in range(n):
        j_check.append([])
        for j in range(m):
            j_check[i].append(0)
    
    for i in range(m):
        l_check.append([])
        for j in range(k):
            l_check[i].append(0)
    
    for i in range(n):
        r_check.append([])
        for j in range(k):
            r_check[i].append(0)
    for i in range(n):
        cur_r_check.append([])
        for j in range(k):
            cur_r_check[i].append(0)

# get firstTime, lastTime, and result matrix from output-index-.txt
def assertOutput(outputLines):
    global t, firstTime, lastTime
    global r_check
    t = 0
    i = 0
    firstTime = int(outputLines[t].split()[1])
    while(outputLines[i][0] == 't'):
        if(outputLines[i].split()[4][-1] == '2'):
            idx = [int(x) for x in outputLines[i].split()[5].split(':')[0][1:-1].split(',')]
            r_check[idx[0] - 1][idx[1] - 1] = int(outputLines[i].split()[1])

        i += 1
    lastTime = int(outputLines[i-1].split()[1])
    t = i - 1

    for j in range(i, i + n):
        values = [int(x) for x in outputLines[j].split()]
        result.append(values)


# check thread count :: thread order :: threadTime from user's output
def threadCheck(output):
    global cur_t, cur_firstTime, cur_lastTime, lastTime, firstTime
    global flag_thread_order , flag_thread_count, flag_time_limit, flag_overall_time, flag_unmatch_result
    global m, n, k
    cur_t = 0
    i = 0
    cur_firstTime = int(output[cur_t].split()[1])
    while(output[i][0] == 't'):
        idx = [int(x) for x in output[i].split()[5].split(':')[0][1:-1].split(',')]
        if(output[i].split()[4][-1] == '0'):
            j_check[idx[0] - 1][idx[1] - 1] = int(output[i].split()[1])
        elif(output[i].split()[4][-1] == '1'):
            l_check[idx[0] - 1][idx[1] - 1] = int(output[i].split()[1])
        else:
            cur_r_check[idx[0] - 1][idx[1] - 1] = int(output[i].split()[1])        
            for ji in range(m):
                if(j_check[idx[0] - 1][ji] == 0):
                    flag_thread_order = True
                    print(f"IDX: {idx}  ,   ji: {ji}")
                    flag_count[1] += 1
            if(not flag_thread_order):
                for li in range(m):
                    if(l_check[li][idx[1] - 1] == 0):
                        flag_thread_order = True
                        print(f"IDX: {idx}  ,   li: {li}")
                        flag_count[1] += 1
        i += 1
    
    cur_lastTime = int(output[i-1].split()[1])
    cur_t = i - 1

    if(cur_t != t):
        flag_thread_count = True
        flag_count[0] += 1
    
    for ii in range(n):
        for j in range(k):
            t0 = 0
            t1 = 0
            for tt in range(m):
                t0 = max(t0, j_check[ii][tt])
                t1 = max(t1, l_check[tt][j])
            t2 = cur_r_check[ii][j] - max(t0, t1)
            if(t2 > 2*(r_check[ii][j] - firstTime)):
                flag_time_limit = True
                flag_count[2] += 1
            
    if((not flag_time_limit) and ((cur_lastTime - cur_firstTime) > 3*(lastTime - firstTime))):
        flag_overall_time = True

    # check result matrices
    for ri in range(n):
        values = [int(x) for x in output[i+ri].split()]
        cur_result.append(values)
    
    for ri in range(n):
        for rj in range(k):
            # print(f"{len(cur_result)} , {len(cur_result[0])}")
            # print(f"{len(result)} , {len(result[0])}")
            if(cur_result[ri][rj] != result[ri][rj]):
                flag_unmatch_result = True
                flag_count[3] += 1

def printTester(testIdx, rep):
    flag_check = True
    global grade
    print("*****************************************************************************")
    print(f"CASE: {testIdx} :: SIMULATED {rep} TIMES")
    if(flag_count[0] != 0):
        flag_check = False 
        print("=> ERROR :: THREAD COUNT")
        print(f"    UNMATCHING NUMBER OF THREADS OCCURED {flag_count[0]} TIMES")
        print("_________________________________________________________________________")

    if(flag_count[1] != 0):
        flag_check = False 
        print("=> ERROR :: THREAD ORDER")
        print(f"     THREADS DID NOT WORKED ON CORRECT ORDER FOR {flag_count[1]} TIMES")
        print("     POSSIBLE ERROR WITH CONDITIONAL VARIABLE") 
        print("_________________________________________________________________________")   

    if(flag_count[2] != 0):
        flag_check = False
        print("=> ERROR :: TIME LIMIT")
        print(f"     TIME LIMIT EXCEEDED {abs(flag_count[2])} TIMES")
        print("     POSSIBLE ERROR WITH WAIT AND SIGNAL")
        if(flag_overall_time):
            print(f"     !!!WAITS TOO MUCH!!!")
        print("_________________________________________________________________________")    

    if(flag_count[3] != 0):
        flag_check = False
        print("=> ERROR :: NON-MATCHING RESULT")
        print(f"     NON-MATCHING RESULT {flag_count[3]} TIMES")
        print("     POSSIBLE ERROR WITH MUTEX OR CONDITIONAL VARIABLE")
        print("_________________________________________________________________________") 

    if(flag_check):
        grade += rep
        print(f"{rep}/{rep} :: CONGRATS, EVERYTHING WORKS FINE!")
    else:
        i = 0
        for c in flag_count:
            if(c == 0):
                i += 1
        print(f"{i}/4 :: CHECK YOUR CODE")
    print("=============================================================================")


if __name__ == '__main__':
    args = [""]  
    if(len(sys.argv) > 1):
        args = sys.argv[1:]
        if(args[0] == '-c'):
            testCases = [int(args[1])]
            testRepeat = int(args[2])

        elif(args[0] == '-l'):
            testCases = []
            for i in range(len(args)-2):
                testCases.append(int(args[i+1]))
            testRepeat = int(args[-1])

        elif(int(args[0]) > 0 and int(args[1]) > 0):
            testCases = [x for x in range (1, int(args[0]) + 1)]
            testRepeat = int(args[1])     
    else:
        testCases = [x for x in range(1,31)]
        testRepeat = 5

    for i in testCases:
        # Open the file for reading
        with open(f"inputs/input{i}.txt", 'r') as file:
            # Initialize an empty list to store the lines
            input_lines = []
            # Loop through each line in the file
            for line in file:
                # Remove the trailing newline character and append the line to the list
                input_lines.append(line.strip())
        assertInput(input_lines)

        with open(f"outputs/output{i}.txt", 'r') as file:
            # Initialize an empty list to store the lines
            output_lines = []
            # Loop through each line in the file
            for line in file:
                # Remove the trailing newline character and append the line to the list
                output_lines.append(line.strip())
        assertOutput(output_lines)

        for j in range(testRepeat):
            # Run the C executable and capture its output
            p = subprocess.Popen(f"./hw2 < inputs/input{i}.txt", stdout=subprocess.PIPE, shell=True)
            output = []
            # Read the output line by line
            for line in p.stdout:
                # Decode the output as a string and remove trailing newline
                line_str = line.decode("utf-8").rstrip()
                output.append(line_str)
            
            threadCheck(output)
            clearCache()
        printTester(i, testRepeat)
        clearAll()
    
    if(args[0] == '-c'):
        elem = testRepeat
    else:
        elem = len(testCases) * testRepeat
    print(f"YOUR FINAL GRADE: {round(grade*100/elem,2)}/100.00")