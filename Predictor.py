################################ IMPORTS ################################
#########################################################################
import pandas
#########################################################################
#########################################################################

################################ FUNCTIONS ##############################
#########################################################################
# Function to convert a decimal to 32-bit binary string.
def make_binary_32(n):
    n = int(n)
    b = "{0:b}".format(n)
    if len(b) < 32:
        b = "0"*(32 - len(b)) + b
    return(b)
#########################################################################
#########################################################################

################################ READ TRACE FILE ########################
#########################################################################
# Read trace file.
with open('./file0.trace', 'r') as f:
    trace_input = f.read().split('\n')

# trace_address and trace_actual will be used to simulate branch instructions.
# trace_address contains the address of branch instructions in decimal.
# trace_actual contains "T" or "N", indicating if a branch was taken or not.
trace_address = []  # len = 856017
trace_actual = []  # len = 856017

for _ in trace_input:
    l = _.split(' ')
    a = l[0]
    if("T" in _):
        b = "T"
    else:
        b = "N"
    trace_address.append(a)
    trace_actual.append(b)

#########################################################################
#########################################################################
# Function to return count of branches which are taken.
# Count of branches not taken = total branches - count of branches taken.
def AlwaysT(tr_ac):
    c_t = 0
    for i in tr_ac:
        if(i == "T"):
            c_t += 1
    return(c_t)
#########################################################################
#########################################################################
chosen_policy = 0

while(chosen_policy != 1 and chosen_policy != 2 and chosen_policy != 3):
    print()
    print("Choose a prediction policy:\n\t1.) Always Taken Static Predictor\n\t2.) Always Not Taken Static Predictor\n\t3.) Dynamic Prediction\n")
    chosen_policy = int(input("Enter choice number: "))
print()

if(chosen_policy == 1):  # For QUESTION-2(a).
    print("Using an always taken prediction policy:")
    print("Number of branches taken (correct predictions):", AlwaysT(trace_actual))
    print("Misprediction Rate (in percent):", (100)*((len(trace_actual) - AlwaysT(trace_actual))/(len(trace_actual))))

elif(chosen_policy == 2):  # For QUESTION-2(a).
    # Count of branches not taken = total branches - count of branches taken.
    print("Using an always not taken prediction policy:")
    print("Number of branches not taken (correct predictions):", len(trace_actual) - AlwaysT(trace_actual))
    print("Misprediction Rate (in percent):", (100)*((AlwaysT(trace_actual))/(len(trace_actual))))

elif(chosen_policy == 3):  # For QUESTION-2(b).
    print("Using a dynamic prediction policy:")
    predictor_size = 21
    while(predictor_size < 2 or predictor_size > 20):
        predictor_size = int(input("Enter predictor index size (2 to 20): "))  # States would be numbered (0, 3) --> (strongly taken, strongly not taken).
        # Convert instruction address in trace_dict from decimal to binary.
        # Size of predictor table is given by 2**(predictor_size) (2 raised to the power of (predictor_size)).
    ins_binary = {}
    for i in range(2**predictor_size):
        ins_binary[((make_binary_32(i))[-1:-(predictor_size + 1):-1])[-1::-1]] = 0  # Initialised according to question to strongly taken state.
    
    # ins_binary acts as prediction table with unique addresses (LSB index bits).

    # 0 --> 1 ==> taken states, 2 --> 3 ==> not taken states.
    
    # 0 ==> Strongly taken state.
    # 1 ==> Weakly taken state.
    # 2 ==> Weakly not taken state.
    # 3 ==> Strongly not taken state.
    
    correct_predictions = 0
    mid = 2  # states are: 0, 1, 2, 3.

    for i in range(len(trace_address)):
        curr_state = ins_binary[((make_binary_32(trace_address[i]))[-1:-(predictor_size + 1):-1])[-1::-1]]

        if(trace_actual[i] == "T"):   
            if(0 <= curr_state and curr_state < mid):
                correct_predictions += 1
            if(curr_state != 0):
                curr_state -= 1

        else:  # trace_actual[i] == "N"
            if(mid <= curr_state and curr_state <= 3):
                correct_predictions += 1
            if(curr_state != 3):
                curr_state += 1

        ins_binary[((make_binary_32(trace_address[i]))[-1:-(predictor_size + 1):-1])[-1::-1]] = curr_state
    
    print("Number of correct predictions:", correct_predictions)
    print("Misprediction Rate (in percent):", (100)*((len(trace_actual) - correct_predictions)/(len(trace_actual))))
    
########################################################################################################
########################################################################################################
########################################   GRAPHING   ##################################################
###########################  LINE GRAPH  #################################
if(chosen_policy == 3):
    parr = pandas.read_csv("./b.csv")
    ax = parr.plot(x = "Predictor size", y = "Mis-prediction rate", label = "Dynamic Prediction", ylabel = "Mis-prediction rate", xlabel = "Index size")
elif(chosen_policy == 1 or chosen_policy == 2):
    parr = pandas.read_csv("./a.csv")
    parr["Mis-prediction rate"] = [(100)*((AlwaysT(trace_actual))/(len(trace_actual))), (100)*((len(trace_actual) - AlwaysT(trace_actual))/(len(trace_actual)))]
    ax = parr.plot(x = "Policy", y = "Mis-prediction rate", label = "Static Prediction", ylabel = "Mis-prediction rate", xlabel = "Policy")

print()
print(parr)

ax

###########################  BAR GRAPH  #################################
if(chosen_policy == 1 or chosen_policy == 2):
    df = pandas.DataFrame({"Policy": parr["Policy"], "Mis-prediction rate": parr["Mis-prediction rate"]})
    ax = df.plot.bar(x = "Policy", y = "Mis-prediction rate", rot = 0)
elif(chosen_policy == 3):
    df = pandas.DataFrame({"Predictor size": parr["Predictor size"], "Mis-prediction rate": parr["Mis-prediction rate"]})
    ax = df.plot.bar(x = "Predictor size", y = "Mis-prediction rate", rot = 0)

ax
print()
#########################################################################
#########################################################################
