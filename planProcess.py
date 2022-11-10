
def stringOutput(plans):
    res = []
    for plan in plans:
        temp = ""
        for item in plan:
            item = item[2:-3]
            temp += item
        res.append(temp)
    return res




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




