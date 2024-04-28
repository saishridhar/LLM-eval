import pandas as pd
import streamlit as st

# Load the DataFrame (assuming it's already created or loaded)
filename = "results/original.json"
llms = ['Mistral-7B-Instruct-v0.2','Mixtral-8x7B-Instruct-v0.1','Llama-2-7b-chat-hf','Llama-2-13b-chat-hf','Llama-2-70b-chat-hf','gpt-4-0125-preview','gpt-3.5-turbo-0125']
df = pd.read_json(filename, orient='records', lines=True)
# Assuming your DataFrame is named 'df'
df2 = df[['answer', 'question', 'llm_context']]


# Initialize an empty list to store user responses
user_responses = []

# Streamlit app
def main():
    st.title('Question Answering')

    # Create a sidebar
    st.sidebar.title('Sidebar')

    # Add a dropdown list to the sidebar
    filename = st.sidebar.selectbox('Select Mg:', llms)
    df1 = pd.read_json(f'results/{filename}.json', orient='records', lines=True)
    df2['predictions'] = df1[f'{filename}_pred']

    # Create a form
    with st.form(key='question_form'):
        i=1
        # Iterate over each row in the DataFrame
        for _, row in df2.iterrows():
            question = row['question']
            answer = row['answer']
            prediction = row['predictions']
            context = row['llm_context']

            st.subheader(f"Question {i}")
            i += 1
            st.write(context)
            st.write('Given the above context answer the following question:')
            st.write(question)
            st.write("Prediction:")
            st.write(prediction)
            st.write("Ground truth:")
            st.write(answer)

            # Display "Yes" and "No" radio buttons
            user_response = st.radio(
                'Does the prediction and ground truth match?',
                ('Yes', 'No'),
                key=f'response_{question}'
            )

            # Append the user response to the list
            user_responses.append(user_response)

        # Submit button for the form
        submit_button = st.form_submit_button(label='Submit')

    # Display the list of user responses when the form is submitted
    if submit_button:
        print(user_responses)
        df1['human_eval'] = user_responses
        df1.to_json(f'final/{filename}_results.json', orient='records', lines=True)
        #st.header('User Responses')
        #for i, response in enumerate(user_responses):
        #    st.write(f'Question {i+1}: {response}')
        st.write("DONE!")

if __name__ == '__main__':
    main()