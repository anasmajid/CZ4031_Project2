

def make_bold(string):
    boldString = FontFormat.BOLD_START + string + FontFormat.BOLD_END
    return boldString


# def append_annotation(query_plan, comparison):

# def func_scan_annotation(query_plan, comparison):
   
# def limit_annotation(query_plan, comparison):
   
# def subquery_scan_annotation(query_plan, comparison):
  
# def value_scan_annotation(query_plan, comparison):
  

# def materialize_annotation(query_plan, comparison):
   
def nl_join_annotation(operand1,operand2):
    return f"Nested loop join between {operand1} and {operand2} is ideal when one join input is smaller and the other join input is large and indexed on its join columns."
   

# def unique_annotation(query_plan, comparison):
  

# def hash_func_annotation(query_plan, comparison):
  
# def gather_merge_annotation(query_plan, comparison):
   

# def aggregate_annotation(query_plan, comparison):


# def cte_scan_annotation(query_plan, comparison):


# def group_annotation(query_plan, comparison):


# def index_scan_annotation(query_plan, comparison):


# def index_only_scan_annotation(query_plan, comparison):


# def merge_join_annotation(query_plan, comparison):


# def set_operation_annotation(query_plan, comparison):


def sequential_scan_annotation(operand1):
    return f"Seq scan on {operand1} is faster due to low selectivity of predicate"


# def sort_annotation(query_plan, comparison):
   

def hash_join_annotation(operand1, operand2):
        return f"Hash join on {operand1,operand2} is efficient for processing large, unsorted and non-indexed inputs compared to other join types. In this query,it has better performance when doing equality join"

 
dictionary = {
    "Aggregate": aggregate_annotation,
    "Append": append_annotation,
    "CTE Scan": cte_scan_annotation,
    "Function Scan": func_scan_annotation,
    "Group": group_annotation,
    "Index Scan": index_scan_annotation,
    "Index Only Scan": index_only_scan_annotation,
    "Limit": limit_annotation,
    "Materialize": materialize_annotation,
    "Unique": unique_annotation,
    "Merge Join": merge_join_annotation,
    "SetOp": set_operation_annotation,
    "Subquery Scan": subquery_scan_annotation,
    "Values Scan": value_scan_annotation,
    "Nested Loop": nl_join_annotation,
    "Seq Scan": sequential_scan_annotation,
    "Sort": sort_annotation,
    "Hash": hash_func_annotation,
    "Hash Join": hash_join_annotation,
    "Gather Merge": gather_merge_annotation,
}

keys = list(dictionary.keys())
strings = ["Nested Loop between customers and table.", "Seq Scan across Orders.", "Hash Join on places and transactions"]
counter = 0
for string_test in strings:
    counter+=1
    for i in keys:
        if str(i) in string_test:
            if (i == "Nested Loop" ):
                result = dictionary[i]("company","orders")
                print(counter,".", result)
            if (i == "Seq Scan" ):
                result = dictionary[i]("Orders")
                print(counter, ".", result)
            if (i == "Hash Join"):
                result = dictionary[i]("places","transactions")
                print(counter, ".", result)
