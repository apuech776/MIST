import random

from tqdm.auto import tqdm


# seed = 2205

# random.seed(seed)

def all_solution_1():

    all_a = list(range(10))
    all_b = list(range(10))

    all_res = []

    for a in tqdm(all_a):
        for b in all_b:
            
            if a < b:
                continue

            for op in ("+", "-"):
                exp = f"{a} {op} {b}"
                res = eval(exp)

                if res < 10:
                    all_res.append(exp)

    print(all_res)
    

    # random.shuffle(all_res)
    # print(all_res)
    # print(len(all_res))

    with open(f"niveau1_all_solution.txt", mode="w", encoding="utf8") as f:
        for l in all_res:
            f.write(l)
            f.write("\n")

        # f.writelines(all_res)

def all_solution_2():

    all_a = list(range(10))
    all_b = list(range(10))
    all_c = list(range(10))

    all_res = []

    for a in tqdm(all_a):
            for b in tqdm(all_b):
                for c in all_c:

                    for op1 in ("+", "-"):
                        for op2 in ("+", "-"):

                            exp = f"{a} {op1} {b} {op2} {c}"
                            res = eval(exp)

                                    
                            if not (0 <= res <= 9):
                                continue
                                    
                            if isinstance(res, float) and not res.is_integer():
                                continue

                                    
                            all_res.append(exp)
                
    all_res = list(set(all_res))

    print(all_res)

    print(len(all_res))
    

    # random.shuffle(all_res)
    # print(all_res)
    # print(len(all_res))

    with open(f"niveau2_all_solution.txt", mode="w", encoding="utf8") as f:
        for l in all_res:
            f.write(l)
            f.write("\n")


def all_solution_3():

    all_a = list(range(10))
    all_b = list(range(100))
    all_c = list(range(100))

    all_res = []

    for a in tqdm(all_a):
        for b in tqdm(all_b):
            for c in all_c:


                    for op1 in ("+", "-", "*"):
                        for op2 in ("+", "-", "*"):


                            exp = f"{a} {op1} {b} {op2} {c} "
                            res = eval(exp)

                                
                            if not (0 <= res <= 9):
                                continue
                                
                            if isinstance(res, float) and not res.is_integer():
                                continue

                                
                            all_res.append(exp)
            
    all_res = list(set(all_res))

    print(all_res)

    with open(f"niveau3_all_solution.txt", mode="w", encoding="utf8") as f:
        for l in all_res:
            f.write(l)
            f.write("\n")

def all_solution_4():

    all_a = list(range(10))
    all_b = list(range(10))
    all_c = list(range(100))
    all_d = list(range(100))

    all_res = []

    for a in tqdm(all_a):
        for b in tqdm(all_b):
            for c in all_c:
                for d in all_d:

                    
                    # if a < b:
                    #     continue

                    for op1 in ("+", "-", "*"):
                        for op2 in ("+", "-", "*"):
                            for op3 in ("+", "-", "*"):

                                exp = f"{a} {op1} {b} {op2} {c} {op3} {d}"
                                res = eval(exp)

                                
                                if not (0 <= res <= 9):
                                    continue
                                
                                if isinstance(res, float) and not res.is_integer():
                                    continue

                                
                                all_res.append(exp)
            
    all_res = list(set(all_res))

    print(all_res)

    with open(f"niveau4_all_solution.txt", mode="w", encoding="utf8") as f:
        for l in all_res:
            f.write(l)
            f.write("\n")
    


def all_solution_5():

    all_a = list(range(100))
    all_b = list(range(100))
    all_c = list(range(100))
    all_d = list(range(100))

    all_res = []

    for a in tqdm(all_a):
        # for b in tqdm(all_b):
        for b in all_b:
            for c in all_c:
                for d in all_d:

                    
                    # if a < b:
                    #     continue

                    for op1 in ("+", "-", "*", "/"):
                        for op2 in ("+", "-", "*", "/"):
                            for op3 in ("+", "-", "*", "/"):

                                if (op1 == '/' and b == 0) or \
                                (op2 == '/' and c == 0) or \
                                (op3 == '/' and d == 0):
                                    continue

                                exp = f"{a} {op1} {b} {op2} {c} {op3} {d}"
                                res = eval(exp)

                                
                                if not (0 <= res <= 9):
                                    continue
                                
                                if isinstance(res, float) and not res.is_integer():
                                    continue

                                
                                all_res.append(exp)
            
    all_res = list(set(all_res))

    print(len(all_res))
    

    # random.shuffle(all_res)
    # print(all_res)
    # print(len(all_res))

    with open(f"niveau5_all_solution.txt", mode="w", encoding="utf8") as f:
        for l in all_res:
            f.write(l)
            f.write("\n")


if __name__ == "__main__":
    #all_solution_1()

    #all_solution_2()

    # all_solution_3()
    # all_solution_4()
    all_solution_5()
