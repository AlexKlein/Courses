import pandas as pd


def prepare_data_set():
    data_set = pd.read_json(
        'recipes.json',
        lines=True
    )
    data_set['ingredients'].replace(
        ['Chile', 'Chiles', 'Chili'],
        ['Chilies', 'Chilies', 'Chilies'],
        inplace=True
    )
    for column in [col for col in data_set.columns]:
        data_set[column] = data_set[column].replace(
            '[^a-zA-Z0-9]',
            ' ',
            regex=True
        )

    return data_set


def choose_difficulty(data_set):
    for i in range(len(data_set)):
        prep = data_set['prepTime'].iloc[i]
        if prep == 'PT':
            prep = 0
        else:
            prep = int(
                    str(
                    prep
                ).replace(
                    'PT',
                    ''
                ).replace(
                    'M',
                    ''
                ).replace(
                    'H',
                    '00'
                )
            )
        cook = data_set['cookTime'].iloc[i]
        if cook == 'PT':
            cook = 0
        else:
            cook = int(
                str(
                    cook
                ).replace(
                    'PT',
                    ''
                ).replace(
                    'M',
                    ''
                ).replace(
                    'H',
                    '00'
                )
            )
        if prep + cook == 0:
            'Unknown'
        elif prep + cook > 60:
            data_set['difficulty'].iloc[i] = 'Hard'
        elif 30 <= prep + cook <= 60:
            data_set['difficulty'].iloc[i] = 'Medium'
        elif prep + cook < 30:
            data_set['difficulty'].iloc[i] = 'Easy'

    return data_set


if __name__ == '__main__':
    data_set = prepare_data_set()
    data_set = data_set[data_set['ingredients'].str.contains('Chilies')]
    data_set['difficulty'] = pd.Series(str())
    data_set = choose_difficulty(data_set)
    data_set.to_csv(
        'recipes.csv',
        index=False
    )
