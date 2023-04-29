stat_order_list = ["HP", "STR", "DEX", "CON", "INT", "WIS", "CHA"]
stat_order_list_lower = [x.lower() for x in stat_order_list]

SESSION=5
# TODO query session from database metadata

def print_block(info, name=""):
    print("\n\n\n", name, info, "\n\n\n")

    
def to_json(order_list, query_results):
    # print_block(query_results, "query_results")
    try:
        newJson = {}
        if query_results is None or query_results[0] is None:
            print_block("query results is None")
            
            for i in range(len(order_list)):
                newJson[order_list[i]] = 0
        else:
            for i in range(len(order_list)):
                newJson[order_list[i]] = query_results[i]
        return newJson
    except TypeError:
        return False
    

def format_single_stat_status_effect(stat, amount):
    stat_chosen = stat.upper()
    stat_string = ''
    for i in range(len(stat_order_list)):
        if stat_order_list[i] == stat_chosen:
            stat_string += f' {amount}'
            stat_string += " 0"*(len(stat_order_list)-i-1)
            break
        else:
            stat_string += " 0"
    
    return stat_string[1:]