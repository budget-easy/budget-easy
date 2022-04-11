import pandas as pd
import itertools
import pyomo.environ as pyo
from pyomo.opt import SolverFactory

def clicks_max_1(df, budget):
    """
    This function calculates the best combination of keywords by maximizing the clicks.
    It sorts the df by clicks per mo descending, takes the first keyword, 
    then go to the next keyword and take it, if we can afford (total sum of taken keywords not exceeds the budget),
    next keywords as well
    """

    # filter dataframe for keywords with lower costs than budget
    df = df[df['costs_per_mo']<=budget]
    
    # sort value by klicks descending and costs ascending
    df = df.sort_values(['clicks_per_mo', 'costs_per_mo'], ascending=[False, True]).reset_index(drop=True)
    
    # define variables: empty list for the index of the optimal keywords; running sum of costs for optimal keywords
    key_position = []
    costs = 0.0

    # loop through the filtered dataframe
    for idx, row in df.iterrows():
        # take the first row 
        if idx == 0:
            key_position.append(idx)
            costs += row['costs_per_mo']
        # add costs of the additional keyword while running sum of budget is less then budget
        elif costs + row['costs_per_mo'] <= budget:
            key_position.append(idx)
            costs += row['costs_per_mo']

    # return total costs, klicks of best combination of similar keywords
    
    return df.iloc[key_position].reset_index(drop=True)

def clicks_max_2(df, budget):
    """
    This function calculates the best combination of keywords by maximizing the clicks.
    It searchs for the optimal combination of keywords by iterating through all possible combination 
    saving the maximum of clicks at a given budget.
    """
    
    # check if you can take all keywords with the given budget
    if df.costs_per_mo.sum() <= budget:
        return print(f'You need a budget of {round(df.costs_per_mo.sum(),2)} Euro to buy all the keywords!')

    # exclude all keywords that exceed the budget
    df = df[df['costs_per_mo'] <= budget]
    
    # create iterator for all possible combination (True if to choose the keyword, false if not)
    comb = itertools.product([True,False], repeat=len(list(df.keyword)))

    comb_max = []
    clicks = 0

    # loop through all combinations
    for x in comb:
        cl, co = df[list(x)][['clicks_per_mo', 'costs_per_mo']].sum()

        # save the combination if its better than previous saved combination
        if (cl > clicks) and (co <= budget):
            comb_max = list(x)
            clicks = cl

    # return dataframe with the optimal keywords combination
    return df[comb_max].reset_index(drop=True)

def clicks_max_3(df, budget):
    """
    This function calculates the best combination of keywords by maximizing the clicks using a linear solver.
    """
    
    # check if you can take all keywords with the given budget
    if df.costs_per_mo.sum() <= budget:
        return print(f'You need a budget of {round(df.costs_per_mo.sum(),2)} Euro to buy all the keywords!')

    # exclude all keywords that exceed the budget
    df = df[df['costs_per_mo'] <= budget].reset_index(drop=True)
    
    # extracting the indici, clicks and costs from the dataframe
    indici = list(df.index.values)
    clicks = df['clicks_per_mo'].values
    costs = df['costs_per_mo'].values

    # create a concrete model
    model = pyo.ConcreteModel()

    # define the VARIABLES (in the end 0=not selected, 1=selected)
    model.x = pyo.Var(indici, within=pyo.Binary)
    x = model.x

    # define the CONSTRAINT, the total costs should be less than budget
    model.weight_constraint = pyo.Constraint(expr= sum([x[p]*costs[p] for p in indici]) <= budget)

    # define the OBJECTIVE, we want to maximize the value of the selected keywords
    model.objective = pyo.Objective(expr= sum([x[p]*clicks[p] for p in indici]), sense=pyo.maximize)

    # print the complete model
    #model.pprint()

    # call the solver
    opt = SolverFactory('cbc', executable='/Users/damjan/neuefische/capstone-project-tem-2/cbc-osx/cbc') # replace the executable path by your own
    results = opt.solve(model)

    # create a list of 0 (not selected keywords) and 1 (selected keywords)
    solution = [int(pyo.value(model.x[p])) for p in indici]

    # change the 0 and 1 to False and True
    solution = [bool(x) for x in solution]

    # return dataframe with the optimal keywords combination
    return df[solution].reset_index(drop=True)

def clicks_max(clicks, costs, budget):
    """
    This function calculates the best combination of keywords by maximizing the clicks using a linear solver.
    """
    
    # check if you can take all keywords with the given budget
    #if df.costs_per_mo.sum() <= budget:
    #    return print(f'You need a budget of {round(df.costs_per_mo.sum(),2)} Euro to buy all the keywords!')

    # exclude all keywords that exceed the budget
    #df = df[df['costs_per_mo'] <= budget].reset_index(drop=True)
    
    # extracting the indici, clicks and costs from the dataframe
    indici = list(range(len(clicks)))

    # create a concrete model
    model = pyo.ConcreteModel()

    # define the VARIABLES (in the end 0=not selected, 1=selected)
    model.x = pyo.Var(indici, within=pyo.Binary)
    x = model.x

    # define the CONSTRAINT, the total costs should be less than budget
    model.weight_constraint = pyo.Constraint(expr= sum([x[p]*costs[p] for p in indici]) <= float(budget))

    # define the OBJECTIVE, we want to maximize the value of the selected keywords
    model.objective = pyo.Objective(expr= sum([x[p]*clicks[p] for p in indici]), sense=pyo.maximize)

    # print the complete model
    #model.pprint()

    # call the solver
    opt = SolverFactory('cbc', executable='/Users/damjan/neuefische/capstone-project-tem-2/cbc-osx/cbc') # replace the executable path by your own
    results = opt.solve(model)

    # create a list of 0 (not selected keywords) and 1 (selected keywords)
    solution = [int(pyo.value(model.x[p])) for p in indici]

    # change the 0 and 1 to False and True
    #solution = [bool(x) for x in solution]

    # return dataframe with the optimal keywords combination
    #return df[solution].reset_index(drop=True)
    return solution