
def stringOutput(plans):
    res = []
    for plan in plans:
        temp = ""
        for item in plan:
            item = item[2:-3]
            temp += item
        res.append(temp)
    return res

# Process step by step
def processPlanStep(plan):
    steps = []
    step_string = ""
    for line in plan:
        temp_string = line.replace(" ","")
        
        # New step
        if line.find("->") != -1:
            steps.append(step_string)
            step_string = temp_string
        
        # Same step
        else:
            step_string += temp_string
    # Final append
    steps.append(step_string)
    
    # Ignore Cost
    return steps[1:]

# Process level by level
def processPlanLevel(plan):
    levels = {0: []}
    current_key = 0
    step_string = ""
    for line in plan:
        # print(levels)    
        # print(step_string)
        # print(current_key)
        #if line is start of step
        if line.find("->") != -1:
            
            #check if level already exists
            step_string = step_string.replace(" ","")
            if current_key in levels: 
                levels[current_key].append(step_string)
            else:
                levels[current_key] = [step_string]
            
            #find level for current step
            count = 0
            for char in line:
                if char != "-":
                    count +=1
                else:
                    break
            current_key = count
            step_string = line
        
        #line is not new step
        else:
            step_string += line
        
    # final append
    step_string = step_string.replace(" ","")
    if current_key in levels: 
        levels[current_key].append(step_string)
    else:
        levels[current_key] = [step_string]
    
    #copy dictionary
    new = {}
    level = 0
    for key in levels:
        new[level] = levels[key]
        level +=1
    return new

def processPlanGraph(plan):
    return


# Testing out function

if __name__ == "__main__":
    
    
    print()
    print("________________"+"Step"+"________________")
    with open("C:/Users/hlati/OneDrive/Desktop/k temp files/q1.txt") as f:
        Q1 = f.readlines()
    Q1 = [x.strip() for x in Q1]
    print(stringOutput(Q1))
    # #print(Q1)

    # steps = processPlanStep(Q1)
    # for line in steps:
    #     print(line)
    #     print()
    print()
    print("________________"+"Level"+"________________")
    with open("C:/Users/hlati/OneDrive/Desktop/k temp files/q2.txt") as f:
        Q2 = f.readlines()
    Q2 = [x.strip() for x in Q2]
    #print(Q2)

    levels = processPlanLevel(Q2)
    for key in levels:
        print(key, levels[key])
        print()




