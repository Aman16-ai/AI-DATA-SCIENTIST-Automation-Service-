

def init(file):
    return f"""
import numpy as np
import pandas as pd
import sklearn
df = pd.read_excel("{file}")
"""