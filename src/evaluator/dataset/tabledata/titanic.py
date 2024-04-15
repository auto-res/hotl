import pandas as pd
import seaborn as sns


def titanic_data():
    """Returns the encoded Titanic dataset.

    Returns:
        df_encoded (pandas.DataFrame): The encoded Titanic dataset with dropped NaN values and categorical columns converted to numerical using one-hot encoding.
        None: There is no additional information returned.
    """    
    df = sns.load_dataset("titanic")
    df.dropna(inplace=True)

    categorical_columns = [
        "sex",
        "class",
        "embarked",
        "who",
        "deck",
        "embark_town",
        "alive",
        "alone",
    ]
    df_encoded = pd.get_dummies(df, columns=categorical_columns)
    df_encoded = df_encoded.rename(columns={"survived": "target"})
    df_encoded = df_encoded.astype(float)

    return df_encoded, None
