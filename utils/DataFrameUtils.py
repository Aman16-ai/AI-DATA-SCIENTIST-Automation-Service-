import pandas as pd
import json
def parseDataFrameToJson(df:pd.DataFrame):
    dfJson = df.to_json(orient='records')
    return json.loads(dfJson)