import random
import pandas as pd # pandas==1.3.5
import numpy as np
import pprint


def get_dataframe(preferences) -> pd.DataFrame:
    """
    this function converts a dictionary into a Pandas dataframe. the dataframe is easier to work with
    when manipulating data in columns. each preference in the list of alternatives can be thought of as a
    column in a dataframe.

    So a dictionary like this:

        {
            0: [0, 4, 3, 1, 2],
            1: [2, 4, 3, 0, 1],
            2: [4, 1, 3, 2, 0],
            3: [4, 3, 2, 1, 0],
            4: [0, 2, 1, 3, 4],
        }

    is translated into a dataframe like this:

                 pref_0  pref_1  pref_2  pref_3  pref_4
        agent
        0           0       4       3       1       2
        1           2       4       3       0       1
        2           4       1       3       2       0
        3           4       3       2       1       0
        4           0       2       1       3       4
    
    each column can be addressed individually, so it's easy to do things like "give me all pref_0 values"
    """
    df = pd.DataFrame.from_dict(preferences,
                                orient='index',
                                columns=[f'pref_{x}' for x in range(len(preferences[0]))])
    df.index.name='agent'
    return df


def do_tieBreak(column, tieBreak, preferences) -> pd.Series:
    """
    all of the tiebreaking logic is encapsulated into this function. this function sorts
    the dataframe after the voting calculation is performed. tiebreaking can be thought of
    as simply sorting different columns based on different criteria. whichever value comes out
    "on top" after sorting is the winner.
    """
    if column.name == 'alternative':
        if tieBreak == 'min':
            # if tiebreak = "min", we order the alternatives from smallest to largest
            return column.sort_values(ascending=True, ignore_index=True)
        elif tieBreak == 'max':
            # if tiebreak = "max", we order the alternatives from largest to smallest
            return column.sort_values(ascending=False, ignore_index=True)
        elif 'agent' in tieBreak:
            # if tiebreak = "agent i", we rank each value by the position of that value in agent i's preferences
            # first, we extract the value of "i"
            agent_id = int(tieBreak.split(' ')[1])
            # next, we replace each value with the position of that value in the agent's preferences
            new_values = [preferences[agent_id].index(x) for x in column.values]
            return pd.Series(new_values)
        else:
            raise ValueError(f'invalid tieBreak option: {tieBreak}')

    return column


def getWinner(df, tieBreak, preferences):
    """
    every voting function works the same way:
      1) convert the preferences dictionary into a dataframe
      2) perform a series of dataframe operations which transform values in accordance with the voting rule
      3) deliver that dataframe to this function, which sorts the dataframe values using the tiebreaker function
      4) after sorting is complete, the winner of the vote can be found in position [0,0] of the dataframe

    the only exception to this design is the "dictatorship" method, which is trivial.

    the dataframes which are delivered to this function must have 2 fields:
      -- "popularity" is the rank of the alternative, as per the individual voting method. the highest value is the winner.
      -- "alternative" is the ID number of the alternative value.
    """
    df = df.sort_values(by=['popularity', 'alternative'],
                        key=lambda x: do_tieBreak(x, tieBreak, preferences),
                        ascending=[False, True])
    return int(df.iloc[0,0])


def dictatorship(preferenceProfile, agent) -> int:
    """
    this voting method is a simple lookup of the requested agent's preferences.
    """
    if agent not in preferenceProfile:
        raise ValueError(f'agent {agent} not found in preferenceProfile')

    return preferenceProfile[agent][0]


def scoringRule(preferences, scoreVector, tieBreak) -> int:
    """
    this voting method applies a scoreVector to the preference columns
    """
    df = get_dataframe(preferences)

    # first, count the number of times that each alternative appears in each position
    df = df.apply(pd.Series.value_counts)
    """
    for a preference dictionary like this:
        {
            0: [0, 5, 4, 1, 3, 2],
            1: [2, 4, 1, 5, 0, 3],
            2: [3, 5, 2, 4, 1, 0],
            3: [0, 5, 2, 1, 3, 4],
            4: [3, 4, 1, 2, 0, 5]
        }

    a dataframe like this is produced:
            pref_0  pref_1  pref_2  pref_3  pref_4  pref_5
        0     2.0     NaN     NaN     NaN     2.0     1.0
        1     NaN     NaN     2.0     2.0     1.0     NaN
        2     1.0     NaN     2.0     1.0     NaN     1.0
        3     2.0     NaN     NaN     NaN     2.0     1.0
        4     NaN     2.0     1.0     1.0     NaN     1.0
        5     NaN     3.0     NaN     1.0     NaN     1.0

    "2.0" in column "pref_0" for row "0" means that alternative "0" appears 2 times as the first preference.
    """

    # next, we multiply each value count by its position in the scoreVector to produce a final score
    vector_position = 0
    for column in df:
        df[column] = df[column] * scoreVector[vector_position]
        vector_position += 1

    """
    given a scoreVector like this: [0,1,2,4,8,16]

    we produce a dataframe like this:
            pref_0  pref_1  pref_2  pref_3  pref_4  pref_5
        0     0.0     NaN     NaN     NaN    16.0    16.0
        1     NaN     NaN     4.0     8.0     8.0     NaN
        2     0.0     NaN     4.0     4.0     NaN    16.0
        3     0.0     NaN     NaN     NaN    16.0    16.0
        4     NaN     2.0     2.0     4.0     NaN    16.0
        5     NaN     3.0     NaN     4.0     NaN    16.0

    the "losers" are heavily-weighted with a multiplier of 16, while the "winners" are weighted with
    a multiplier of zero.
    """

    # now we sum the score values and reformat the dataframe so that it can be used by getWinner()
    df['popularity'] = df.sum(axis=1)
    df.index.name='alternative'
    df.reset_index(inplace=True)
    """
    this produces a dataframe where sorting by popularity, (highest to lowest), and alternative ID will
    put the winner of the vote into the first row.

    in this case, both alternative 0 and 3 are tied with a popularity score of 32. this means that the
    tiebreaker logic will apply.

    tiebreaker logic of "min" will sort the alternative field from lowest to highest.
    tiebreaker logic of "max" will sort the alternative field from highest to lowest.

            alternative  pref_0  pref_1  pref_2  pref_3  pref_4  pref_5  popularity
        0            0     0.0     NaN     NaN     NaN    16.0    16.0        32.0
        1            1     NaN     NaN     4.0     8.0     8.0     NaN        20.0
        2            2     0.0     NaN     4.0     4.0     NaN    16.0        24.0
        3            3     0.0     NaN     NaN     NaN    16.0    16.0        32.0
        4            4     NaN     2.0     2.0     4.0     NaN    16.0        24.0
        5            5     NaN     3.0     NaN     4.0     NaN    16.0        23.0   
    """

    return getWinner(df, tieBreak, preferences)


def plurality(preferences, tieBreak) -> int:
    df = get_dataframe(preferences)
    
    # this one is easy - we just count the number of times that each alternative appears in the
    # first position. the tiebreaker can then be applied from there:
    df = df.groupby('pref_0').size()
    df = df.reset_index(name='popularity').rename(columns={"pref_0": "alternative"})
    
    """
    for a preference dictionary like this:
        {
            0: [0, 5, 4, 1, 3, 2],
            1: [2, 4, 1, 5, 0, 3],
            2: [3, 5, 2, 4, 1, 0],
            3: [0, 5, 2, 1, 3, 4],
            4: [3, 4, 1, 2, 0, 5]
        }

    a dataframe like this is produced:

                alternative  popularity
        0            0           2
        1            2           1
        2            3           2

    a "2" in popularity for alternative "0" means that "0" appears 2 times as the first preference
    """
    return getWinner(df, tieBreak, preferences)


def veto(preferences, tieBreak) -> int:
    df = get_dataframe(preferences)

    # for this one, we count the number of times that each alternative appears in all positions EXCEPT
    # the last position, (which has been vetoed)

    # first, we simply drop the last column. this has the effect of dropping the last preference from the dataframe
    # and preventing it from being counted.
    df = df.iloc[: , :-1]

    # next, we count the number of times that each alternative appears across all of the remaining columns
    df = df.apply(pd.Series.value_counts)
    df['popularity'] = df.sum(axis=1)
    df.index.name='alternative'
    df.reset_index(inplace=True)

    return getWinner(df, tieBreak, preferences)


def borda(preferences, tieBreak) -> int:
    df = get_dataframe(preferences)

    # for this one, we count the number of times that each alternative appears in each column, and then we 
    # multiply that count by a weighted amount for that column.
    df = df.apply(pd.Series.value_counts)
    
    # the weighted amount starts at the number of columns - 1, and decreases by 1 for each column from left
    # to right.
    multiplier = len(df.columns) - 1
    for column in df:
        df[column] = df[column] * multiplier
        multiplier -= 1

    # then we sum all of the weighted scores. that represents our final ranking.
    df['popularity'] = df.sum(axis=1)
    df.index.name='alternative'
    df.reset_index(inplace=True)

    return getWinner(df, tieBreak, preferences)

def harmonic(preferences, tieBreak) -> int:
    df = get_dataframe(preferences)

    # for this one, we count the number of times that each alternative appears in each column, and then we 
    # divide that count by the harmonic divisor.
    df = df.apply(pd.Series.value_counts)

    # the harmonic divisor starts as 1, and increases by 1 for each column from left to right.
    divisor = 1
    for column in df:
        df[column] = df[column] / divisor
        divisor += 1

    # then we sum all of the weighted scores. that represents our final ranking.
    df['popularity'] = df.sum(axis=1)
    df.index.name='alternative'
    df.reset_index(inplace=True)

    return getWinner(df, tieBreak, preferences)

def STV(preferences, tieBreak) -> int:
    df = get_dataframe(preferences)

    # this is the trickiest one. we will follow this algorithm:
    #   1) count how many times each alternative appears as pref_0
    #   2) find the alternatives which have that minimum count
    #   3) replace all instance of those alternatives with NaN
    #   4) shift the remaining values to the left to fill in the NANs
    #   5) repeat this process until the count of alternative appearences is homogenized

    def squeeze_nan(x):
        # this function is used to shift values in the dataframe to the left, filling in any spaces
        # that were created when alternatives were dropped
        original_columns = x.index.tolist()
        squeezed = x.dropna()
        squeezed.index = [original_columns[n] for n in range(squeezed.count())]
        return squeezed.reindex(original_columns, fill_value=np.nan)

    def apply_STV_rounds(df):
        # this is a recursive function which applies steps 1, 2, and 3 until the count of alternative
        # appearences is homogenized

        # 1) count how many times each alternative appears as pref_0
        freq = df.apply(pd.Series.value_counts).fillna(0.0)
        freq.index.name='alternative'
        freq.reset_index(inplace=True)
        # find the lowest alternative count that appears in pref_0
        pref_0_min = freq['pref_0'].min()
        if pref_0_min < freq['pref_0'].max():
            # 2) find the alternatives which have that minimum count
            drop_list = list(freq.query('pref_0==%s' % pref_0_min)['alternative'])
            # 3) replace all instance of those alternatives with NaN
            df = df.replace(drop_list, np.nan)
            # 4) shift the remaining values to the left to fill in the NANs
            df = df.apply(squeeze_nan, axis=1)
            # do it again...
            return apply_STV_rounds(df)
        else:
            return df

    # apply the STV rounds
    df = apply_STV_rounds(df)
    
    # once the STV rounds are complete, the remaining alternatives in pref_0 are our winners.
    df = df.groupby('pref_0').size()
    df = df.reset_index(name='popularity').rename(columns={"pref_0": "alternative"})

    return getWinner(df, tieBreak, preferences)

############ main execution starts here ############

# set the configuration parameters that are used for generating test data
random_seed = 2
agents = 5
alternatives = 6

# we want to generate random test data, but we want that randomness to be repeatable. this is controlled
# by the seed value. different seed values will produce different sets of random numbers. but the same seed
# value will produce the same set of random numbers.
random.seed(random_seed)

# generate the random test data based on the configuration parameters
preferences = dict()
for i in range(0, agents):
    preferences[i] = random.sample(range(alternatives), k=alternatives)

# print the random agent / alternative preferences data that we generated. it looks something like this:
"""
    {
    0: [0, 5, 4, 1, 3, 2],
    1: [2, 4, 1, 5, 0, 3],
    2: [3, 5, 2, 4, 1, 0],
    3: [0, 5, 2, 1, 3, 4],
    4: [3, 4, 1, 2, 0, 5],
    }
"""
pprint.pprint(preferences)

# test dictatorship
print("dictatorship winner agent 0: %s" % dictatorship(preferences, 0))
print("dictatorship winner agent 1: %s" % dictatorship(preferences, 1))
print("dictatorship winner agent 2: %s" % dictatorship(preferences, 2))

# test scoringRule
print("scoringRule winner min/losers: %s" % scoringRule(preferences, [0,1,2,3,4,5], "min"))
print("scoringRule winner min/winners: %s" % scoringRule(preferences, [5,4,3,2,1,0], "min"))
print("scoringRule winner min/big losers: %s" % scoringRule(preferences, [0,1,2,4,8,16], "min"))
print("scoringRule winner min/big winners: %s" % scoringRule(preferences, [16,8,4,2,1,0], "min"))

# test plurality
print("plurality winner min: %s" % plurality(preferences, "min"))
print("plurality winner max: %s" % plurality(preferences, "max"))
print("plurality winner agent 1: %s" % plurality(preferences, "agent 1"))

# test veto
print("veto winner min: %s" % veto(preferences, "min"))
print("veto winner max: %s" % veto(preferences, "max"))
print("veto winner agent 1: %s" % veto(preferences, "agent 1"))

# test borda
print("borda winner min: %s" % borda(preferences, "min"))
print("borda winner max: %s" % borda(preferences, "max"))
print("borda winner agent 1: %s" % borda(preferences, "agent 1"))

# test harmonic
print("harmonic winner min: %s" % harmonic(preferences, "min"))
print("harmonic winner max: %s" % harmonic(preferences, "max"))
print("harmonic winner agent 1: %s" % harmonic(preferences, "agent 1"))

# test STV
print("STV winner min: %s" % STV(preferences, "min"))
print("STV winner max: %s" % STV(preferences, "max"))
print("STV winner agent 1: %s" % STV(preferences, "agent 1"))
