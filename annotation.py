
# formatting/highlighting string
class color:
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   YELLOW = '\033[93m'
   END = '\033[0m'

# utility functions to annotate explanations

def make_bold(string): 
    boldString = color.BOLD + string + color.END
    return string

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def seq_scan_annotate(step):
    bold_operator = make_bold("Sequential Scan")
    
    #obtain relation names
    relation = "relation"
    splitStep = step.split()
    for i in range(len(splitStep)):
        if (splitStep[i] == "on"):
            relation = splitStep[i+1]
    
    return f"{bold_operator} on {relation} is faster due to much lower selectivity of the predicate"

def index_scan_annotate(step):
    bold_operator = make_bold("Index Scan")
    
    #obtain relation names
    relation = "relation"
    splitStep = step.split()
    for i in range(len(splitStep)):
        if (splitStep[i] == "on"):
            relation = splitStep[i+1]
    return f"{bold_operator} on {relation} is faster due to much high selectivity of the predicate"

def hash_join_annotate(step):
    bold_operator = make_bold("Hash Join")
    #obtain relation names
    relation = "relation"
    relation_condition = find_between(step,"Hash Cond: (",")")
    if ( relation_condition != "" ):
        relation = relation_condition
    return f"{bold_operator} on {relation} is efficient for processing large, unsorted and non-indexed \
inputs compared to the other join types. In this query,it has better performance when doing equality join"

def nested_loop_annotate(step):
    bold_operator = make_bold("Nested Loop")
    return f"{bold_operator} join is particularly effective if the outer input is small\
and the inner input is sorted and large"

def merge_join_annotate(step):
    bold_operator = make_bold("Merge Join")
    return f"{bold_operator} is particularly effective when the joined tables are sorted on the join columns."

   
class Annotation():

    dictionary = {
        "Nested Loop": nested_loop_annotate,
        "Seq Scan": seq_scan_annotate,
        "Hash Join": hash_join_annotate,
        "Index Scan": index_scan_annotate,
        "Merge Join": merge_join_annotate,
    }

    def getAnnotatedExplanations(self,queryPlan):
        print("\nANNOTATED EXPLANATIONS\n")
        explanation = ""
        operators = list(self.dictionary.keys())
        queryPlan = queryPlan.split(" -> ")
        for step in queryPlan:
            #operators consist of list of keyword operators we are searching for
            for i in operators:
                if (i in step): #check if i (eg. hash join) exists as as substring in each step
                    print(self.dictionary[i](step))
                    explanation += "\n-> "
                    explanation += self.dictionary[i](step)
                    explanation += "\n"
                    break #since one step an only be made up of one operator, no use to check for the existence of other operators
        print(explanation)
        return explanation