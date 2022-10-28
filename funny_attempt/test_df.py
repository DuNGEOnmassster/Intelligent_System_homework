from collections import defaultdict
import pandas as pd
from random import randint

df = pd.DataFrame({"id":[i for i in range(1,5)], "review_reason_code":[randint(1,6) for i in range(1,5)]})
print(df)

def get_value_counts_table(df, col_name):
    count_dict = defaultdict(int)

    def update_count_dict(r):
        count_dict[r[col_name]] += 1

    df.apply(lambda x: update_count_dict(x), axis=1)
    rows = [[e, count_dict[e]] for e in count_dict]
    return pd.DataFrame(rows, columns=[col_name, "count"])


review_count_table = get_value_counts_table(df, "review_reason_code")

# review_count_table
print(review_count_table)