import pickle
from openai import OpenAI
import pandas as pd


import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
api_key=os.environ.get("OPENAI_KEY"),
)
#openai.api_key = os.getenv("OPENAI_KEY")


def load_data(csv_path):
    return pd.read_csv(csv_path)

#Updated code to use the OpenAI API to generate the response (client.chat.completions.create)

def return_criteria(df, instructions, inclusion_criteria, exclusion_criteria, show_prompt=False):
    """
    Parameters:
        df (pandas dataframe): dataframe with columns 'title', 'abstract', 'author(s)Keywords', 'indexKeywords', 'keywordsPlus', 'year' and 'documentType'
            - 'title' (str): article title
            - 'abstract' (str): article abstract
            - 'author(s)Keywords' (str): author keywords
            - 'indexKeywords' (str): index keywords
            - 'keywordsPlus' (str): additional keywords
            - 'year' (str): year of publication
            - 'documentType' (str): document type
        instructions (str): instructions for screening
        inclusion_criteria (str): screening inclusion criteria
        exclusion_criteria (str): screening exclusion criteria
        show_prompt (bool): whether to print the inclusion/exclusion prompt to the screen [warning: verbose]
    Returns:
        decision (str): 'included' or 'excluded'
    """
    title = df['title']
    abstract = df['abstract']
    authorKeywords = df['author(s)Keywords']
    indexKeywords = df['indexKeywords']
    keywordsPlus = df['keywordsPlus']
    year = df['year']
    documentType = df['documentType']
    prompt = f'{instructions}\n\nTitle: {title}\n\nAbstract:\n{abstract}\n\nKeywords:\n{authorKeywords}, {indexKeywords}, {keywordsPlus}\n\nYear:\n{year}\n\nDocument Type:\n{documentType}\n\nInclusion criteria:\n{inclusion_criteria}\n\nExclusion criteria:\n{exclusion_criteria}\n\nDecision:',    
    if show_prompt:
        print(prompt[0])

    memory = [{"role": "user", "content": prompt[0]}]

    try:
        response = client.chat.completions.create(
            model='gpt-4',
            messages=memory,
            temperature=0,
            top_p=0.5,
        )
    except:
        try:
            print('Context length exceeded, attempting with GPT-4-TURBO.')
            response = client.chat.completions.create(
                model='gpt-4-turbo',
                messages=memory,
                temperature=0,
                top_p=0.5,
            )
            print('Successfully completed with GPT-4-TURBO.')

        except:
            print(f'Invalid character within the row containing the paper: "{title}". Skipping...')
            return ''
    return response.choices[0].message.content.strip('.').lower().capitalize()

def loop_through_df(df, instructions, save_ckpt=True, sample=False, sample_n=3, random_state=42):
    """
    Parameters:
        df (pandas dataframe): dataframe with columns 'Dataset Name', 'Inclusion Criteria', 'Exclusion Criteria'
            - 'Dataset Name' (str): name of dataset
            - 'Inclusion Criteria' (str): screening inclusion criteria
            - 'Exclusion Criteria' (str): screening exclusion criteria
        instructions (str): instructions for screening
        save_ckpt (bool): whether to save a checkpoint of the dataframe after each dataset is screened
        sample (bool): whether to sample the dataset
        sample_n (int): sample size
    Returns:
        dfs (dict): dictionary of dataframes each with columns 'title', 'abstract', 'decision'
    """
    dfs = dict()
    for _, row in df.iterrows():
        print(f'Running: {row["Dataset Name"]}')
        if sample:
            temp_df = pd.read_csv(f"data/{row['Dataset Name']}", encoding='ISO-8859-1').sample(sample_n, random_state=random_state)
        else:
            temp_df = pd.read_csv(f"data/{row['Dataset Name']}", encoding='ISO-8859-1')
        inclusion_criteria = row['Inclusion Criteria']
        exclusion_criteria = row['Exclusion Criteria']
        try:
            temp_df['decision'] = temp_df.apply(lambda x: return_criteria(x, instructions, inclusion_criteria, exclusion_criteria), axis=1)
        #Updated code to handle exceptions and print the error message
        except Exception as e:
            print(f"Error processing file: {e}")
            print(f'Error processing {row["Dataset Name"]}')
            continue
        temp_df['decision'] = temp_df['decision'].apply(
            lambda x: "Included" if "Included" in x else "Excluded" if "Excluded" in x else "Undecided")
        dfs[row['Dataset Name']] = temp_df
        # save checkpoint
        if save_ckpt:
            temp_df.to_csv(f'results/{row["Dataset Name"]}')
            with open(f'checkpoints/{row["Dataset Name"]}.pkl', 'wb') as f:
                pickle.dump(temp_df, f)
    return dfs

def main(csv_path):
    """
    Parameters:
        csv_path (str): path to csv file with columns 'Dataset Name', 'Inclusion Criteria', 'Exclusion Criteria'
            - 'Dataset Name' (str): name of dataset
            - 'Inclusion Criteria' (str): screening inclusion criteria
            - 'Exclusion Criteria' (str): screening exclusion criteria
    Returns:
        dfs (dict): dictionary of dataframes with columns 'title', 'abstract', and 'decision'
    """
    df = load_data(csv_path)
    instructions = 'You are a researcher rigorously screening titles, abstracts, and keywords of scientific papers for inclusion or exclusion in a review paper. Use the criteria below to inform your decision. If any exclusion criteria are met or not all inclusion criteria are met, exclude the article. If all inclusion criteria are met, include the article. Only type "included" or "excluded" to indicate your decision. Do not type anything else.'
    dfs = loop_through_df(df, instructions, save_ckpt=True, sample=False)
    # save all dfs as csv
    if not os.path.exists('results'):
        os.makedirs('results')
    for key, value in dfs.items():
        value.to_csv(f"results/{key.strip('.csv')}.csv", index=False)


if __name__ == '__main__':
    main(input('Enter path to your csv file: '))
