sampleQueryPlan = """
('Limit  (cost=252890.86..252890.88 rows=10 width=44) (actual time=5038.191..5060.641 rows=10 loops=1)',)
('  ->  Sort  (cost=252890.86..254332.51 rows=576662 width=44) (actual time=5038.185..5060.634 rows=10 loops=1)',)
("        Sort Key: (sum((lineitem.l_extendedprice * ('1'::numeric - lineitem.l_discount)))) DESC, orders.o_orderdate",)
('        Sort Method: top-N heapsort  Memory: 26kB',)
('        ->  Finalize GroupAggregate  (cost=164538.32..240429.40 rows=576662 width=44) (actual time=3861.894..4948.856 rows=145911 loops=1)',)
('              Group Key: lineitem.l_orderkey, orders.o_orderdate, orders.o_shippriority',)
('              ->  Gather Merge  (cost=164538.32..227214.22 rows=480552 width=44) (actual time=3861.880..4510.206 rows=145911 loops=1)',)
('                    Workers Planned: 2',)
('                    Workers Launched: 2',)
('                    ->  Partial GroupAggregate  (cost=163538.29..170746.57 rows=240276 width=44) (actual time=3698.256..4258.666 rows=48637 loops=3)',)
('                          Group Key: lineitem.l_orderkey, orders.o_orderdate, orders.o_shippriority',)
('                          ->  Sort  (cost=163538.29..164138.98 rows=240276 width=24) (actual time=3698.186..3774.811 rows=194856 loops=3)',)
('                                Sort Key: lineitem.l_orderkey, orders.o_orderdate, orders.o_shippriority',)
('                                Sort Method: external merge  Disk: 6784kB',)
('                                Worker 0:  Sort Method: external merge  Disk: 6840kB',)
('                                Worker 1:  Sort Method: external merge  Disk: 6688kB',)
('                                ->  Nested Loop  (cost=4521.94..137136.43 rows=240276 width=24) (actual time=125.542..3335.613 rows=194856 loops=3)',)
('                                      ->  Parallel Hash Join  (cost=4521.51..39222.30 rows=60057 width=12) (actual time=124.124..997.496 rows=48637 loops=3)',)
('                                            Hash Cond: (orders.o_custkey = customer.c_custkey)',)
('                                            ->  Parallel Seq Scan on orders  (cost=0.00..33907.50 rows=302198 width=16) (actual time=0.035..616.770 rows=243690 loops=3)',)
("                                                  Filter: (o_orderdate < '1995-03-21'::date)",)
('                                                  Rows Removed by Filter: 256310',)
('                                            ->  Parallel Hash  (cost=4366.25..4366.25 rows=12421 width=4) (actual time=123.728..123.729 rows=10063 loops=3)',)
('                                                  Buckets: 32768  Batches: 1  Memory Usage: 1504kB',)
('                                                  ->  Parallel Seq Scan on customer  (cost=0.00..4366.25 rows=12421 width=4) (actual time=0.944..110.783 rows=10063 loops=3)',)
("                                                        Filter: (c_mktsegment = 'HOUSEHOLD'::bpchar)",)
('                                                        Rows Removed by Filter: 39937',)
('                                      ->  Index Scan using lineitem_pkey on lineitem  (cost=0.43..1.48 rows=15 width=16) (actual time=0.039..0.044 rows=4 loops=145911)',)
('                                            Index Cond: (l_orderkey = orders.o_orderkey)',)
("                                            Filter: (l_shipdate > '1955-03-21'::date)",)
('Planning Time: 32.344 ms',)
('Execution Time: 5065.467 ms',)
"""

# formatting/highlighting string
class color:
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   YELLOW = '\033[93m'
   END = '\033[0m'

# bolds a string for formatting purposes
def make_bold(string): 
    boldString = color.BOLD + string + color.END
    return boldString

def yellowColor(string):
    return color.YELLOW + string + color.END

def seq_scan_annotate(operand="operand"):
    bold_operator = make_bold("Sequential Scan")
    return f"{bold_operator} on {operand} is faster due to much lower selectivity of the predicate"
   
def index_scan_annotate(operand="operand"):
    bold_operator = make_bold("Index Scan")
    return f"{bold_operator} on {operand} is faster due to much high selectivity of the predicate"

def hash_join_annotate(operand1 ="operand1", operand2 ="operand2"):
    bold_operator = make_bold("Hash Join")
    return f"{bold_operator} on {operand1} and {operand2} is efficient for processing large, unsorted and non-indexed \
inputs compared to other join types. In this query,it has better performance when doing equality join"

def nested_loop_annotate(operand="operand"):
    bold_operator = make_bold("Nested Loop")
    return f"{bold_operator} join is particularly effective if the outer input is small\
and the inner input is sorted and large"

def merge_join_annotate(operand1="operand1", operand2="operand2"):
    bold_operator = make_bold("Merge Join")
    return f"A {bold_operator} is particularly effective when the joined tables are sorted on the join columns."

# dictionary consts of a key(operator) and its respective function to be called
dictionary = {
    "Nested Loop": nested_loop_annotate,
    "Seq Scan": seq_scan_annotate,
    "Hash Join": hash_join_annotate,
    "Index Scan": index_scan_annotate,
    "Merge Join": merge_join_annotate,
}

# operators is a list of keyword operators we are searching for in each step
operators = list(dictionary.keys())

splitSteps = sampleQueryPlan.split(" -> ")

# printing out how the steps look like
print(yellowColor("\nPRINTING OUT ALL THE STEPS IN THE QUERY PLAN"))
for i in splitSteps:
    print(i)
    print("----------------------------------------------------------------------------------------------------------")

print(yellowColor("\nANNOTATED EXPLANATIONS\n"))
for step in splitSteps:
    #operators consist of list of keyword operators we are searching for
    for i in operators:
        if (i in step): #check if i (eg. hash join) exists as as substring in each step
            print(dictionary[i]())
            print()
            break #since one step an only be made up of one operator, no use to check for the existence of other operators