import scipy.stats as ss
from graphviz import Graph
from itertools import groupby
from string import ascii_lowercase as alc


def stringOutput(plans):
    res = []
    for plan in plans:
        temp = ""
        for item in plan:
            item = item[2:-3]
            temp += item
        res.append(temp)
    return res


def draw(choice, q1_dict, q2_dict):
    q1_edges = []
    q2_edges = []

    # Instantiate a new Graph object
    q1_dot = Graph('QEP', format='png')
    for i in range(len(q1_dict)):
        old_key = next(iter(q1_dict[i]))
        new_key = alc[i]

        print(alc[i], old_key)
        q1_dot.node(str(alc[i]), str(old_key))

        # update dict with the letters
        q1_dict[i][new_key] = q1_dict[i][old_key]
        del q1_dict[i][old_key]

    print(q1_dict)
    
    for i in range(1, len(q1_dict)):
        # visited.append(next(iter(q1_dict[i-1])))
        pair_str = None
        if q1_dict[i-1][next(iter(q1_dict[i-1]))] < q1_dict[i][next(iter(q1_dict[i]))]:
            
            # print(q1_ops_by_level[i-1][next(iter(q1_ops_by_level[i]))])
            pair_str = next(iter(q1_dict[i-1])) + next((iter(q1_dict[i])))
            print(pair_str)
        else:
            curr_val = q1_dict[i][next(iter(q1_dict[i]))]

            for j in range(i-1,-1,-1):
                if curr_val > q1_dict[j][next(iter(q1_dict[j]))]:
                    pair_str = next(iter(q1_dict[j])) + next(iter(q1_dict[i]))
                    print(pair_str)
                    break
        q1_edges.append(pair_str)

    # Instantiate a new Graph object
    q2_dot = Graph('AQP', format='png')
    for i in range(len(q2_dict)):
        old_key = next(iter(q2_dict[i]))
        new_key = alc[i]

        print(alc[i], old_key)
        q2_dot.node(str(alc[i]), str(old_key))

        # update dict with the letters
        q2_dict[i][new_key] = q2_dict[i][old_key]
        del q2_dict[i][old_key]

    print(q2_dict)
    edges = []
    for i in range(1, len(q2_dict)):
        # visited.append(next(iter(q1_dict[i-1])))
        pair_str = None
        if q2_dict[i-1][next(iter(q2_dict[i-1]))] < q2_dict[i][next(iter(q2_dict[i]))]:
            
            # print(q1_ops_by_level[i-1][next(iter(q1_ops_by_level[i]))])
            pair_str = next(iter(q2_dict[i-1])) + next((iter(q2_dict[i])))
            print(pair_str)
        else:
            curr_val = q2_dict[i][next(iter(q2_dict[i]))]

            for j in range(i-1,-1,-1):
                if curr_val > q2_dict[j][next(iter(q2_dict[j]))]:
                    pair_str = next(iter(q2_dict[j])) + next(iter(q2_dict[i]))
                    print(pair_str)
                    break
        q2_edges.append(pair_str)

    if choice == 0:
        q1_dot.edges(q1_edges)
        q1_dot.view('query1testqep')
    elif choice == 1:
        q2_dot.edges(q2_edges)
        q2_dot.view('query1testaqp')
    else:
        raise(ValueError("Choice of graph is invalid."))
                

def txt2list(input_path="./query_output.txt"):
    lines = []
    with open(input_path, 'r') as f:
        lines = f.readlines()
    
    return lines


def get_ops_in_order(psql_out):
    break_conditions = ["  (", " on", " us"]
    q1_ops = []
    q2_ops = []

    queries = [list(group) for k, group in groupby(psql_out.copy(), lambda x: x == "For Query Number 2\n") if not k]
    q1 = queries[0]
    q2 = queries[1]

    for line in q1:
        if "cost" in line:
            for i in range(0, len(line)):
                if (line[i]+line[i+1]+line[i+2]) in break_conditions:
                    q1_ops.append(line[0:i+1])
                    break
            print(q1_ops)
    for line in q2:
        if "cost" in line:
            for i in range(0, len(line)):
                if (line[i]+line[i+1]+line[i+2]) in break_conditions:
                    q2_ops.append(line[0:i+1])
                    break
            print(q2_ops)

    assert not (q1 == [] or q1 == [])

    return q1_ops, q2_ops


def find_levels(q1_ops, q2_ops):
    q1_levels_dict_list = []
    q1_spaces_count = []
    q2_levels_dict_list = []
    q2_spaces_count = []

    for op in q1_ops:
        try:
            hyphen_idx = op.index("-")
            op_name_idx = op.index(">")+3
        except ValueError:
            hyphen_idx = 1
            op_name_idx = 2
        q1_spaces_count.append(hyphen_idx)
        q1_levels_dict_list.append({op[op_name_idx:-1] : hyphen_idx})
    ranks = list(ss.rankdata(q1_spaces_count, method='dense'))

    # for elem in q1_levels_dict_list:
    #     elem[next(iter(elem))] = 0

    for i in range(len(q1_levels_dict_list)):
        q1_levels_dict_list[i][next(iter(q1_levels_dict_list[i]))] = ranks[i]
    print(q1_levels_dict_list)

    for op in q2_ops:
        try:
            hyphen_idx = op.index("-")
            op_name_idx = op.index(">")+3
        except ValueError:
            hyphen_idx = 1
            op_name_idx = 2
        q2_spaces_count.append(hyphen_idx)
        q2_levels_dict_list.append({op[op_name_idx:-1] : hyphen_idx})
    ranks = list(ss.rankdata(q2_spaces_count, method='dense'))

    for i in range(len(q2_levels_dict_list)):
        q2_levels_dict_list[i][next(iter(q2_levels_dict_list[i]))] = ranks[i]
    print(q2_levels_dict_list)

    return q1_levels_dict_list, q2_levels_dict_list


def create_graph(choice, psql_out):
    q1_ops, q2_ops = get_ops_in_order(psql_out)
    q1_ops_by_level, q2_ops_by_level = find_levels(q1_ops, q2_ops)
    draw(choice, q1_ops_by_level, q2_ops_by_level)


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




