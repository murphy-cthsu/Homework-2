
pools = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}
tokens = ["tokenA", "tokenB", "tokenC", "tokenD", "tokenE"]
path=[]




def get_amounts_out(pools, amount_in, path):
    if len(path) < 2:
        raise ValueError('Invalid path: Path should contain at least two tokens')

    amounts = [0] * len(path)
    amounts[0] = amount_in

    for i in range(len(path) - 1):
        reserve_in, reserve_out = get_reserves_from_pool(pools, path[i], path[i + 1])
        amounts[i + 1] = calculate_output_amount(amounts[i], reserve_in, reserve_out)

    return amounts

def get_reserves_from_pool(pools, token_in, token_out):
    if (token_in, token_out) in pools:
        reserve_in, reserve_out = pools[(token_in, token_out)]
    else:
        reserve_out, reserve_in = pools[(token_out, token_in)]  # Swap reserves
    
    return reserve_in, reserve_out

def calculate_output_amount(amount_in, reserve_in, reserve_out):
    # Example implementation, replace with actual logic to calculate output amount
    amount_in_with_fee = amount_in * 997  # Applying fee
    numerator = amount_in_with_fee * reserve_out
    denominator = reserve_in * 1000 + amount_in_with_fee  # Adding fee to reserve_in
    amount_out = numerator / denominator
    return amount_out

def find_cycles_with_token_B(pools,tokens):
    cycles = []
    for token in tokens:
        if token == "tokenB":
            path = ["tokenB"]
            find_cycles_recursive(pools,token, path, cycles)
    return cycles

def find_cycles_recursive(pools,current_token, path, cycles):
    if len(path) > 2:
        pathB=path+["tokenB"]
        amount_in = 5
        amounts_out = get_amounts_out(pools, amount_in, pathB)
        final_amount = amounts_out[-1]
        if final_amount > 20:
            cycles.append((pathB, final_amount))

    for token in tokens:
        if token not in path and ((current_token, token) in pools or (token, current_token) in pools):
            new_path = path + [token]
            find_cycles_recursive( pools,token, new_path, cycles)

cycles = find_cycles_with_token_B(pools, tokens)

max_amount = 0
max_cycle = None
for cycle, final_amount in cycles:
    if final_amount > max_amount:
        max_amount = final_amount
        max_cycle = cycle
max_cycle_str = '->'.join(max_cycle) 
print(f"path: {max_cycle_str}, tokenB balance={max_amount:.10f}")

amounts_out = get_amounts_out(pools,5, max_cycle)
print(amounts_out)





