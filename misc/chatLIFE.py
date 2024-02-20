import os
import PyPDF2
from transformers import pipeline
import csv

from transformers import BertForQuestionAnswering, BertTokenizer, Trainer, TrainingArguments


nlp = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")



def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = [page.extract_text() for page in reader.pages]
    return "\n".join(text)

def answer_questions_from_pdf(pdf_path, questions):
    text = extract_text_from_pdf(pdf_path)
    nlp = pipeline("question-answering")
    answers = {}
    for question in questions:
        answers[question] = nlp(question=question, context=text)['answer']
    return answers

def answer_questions_from_folder(pdf_folder, questions):
    all_answers = {}
    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, filename)
            answers = answer_questions_from_pdf(pdf_path, questions)
            all_answers[filename] = answers
    return all_answers

# Example usage
pdf_folder = "iodosulfuron"
questions = [
    "What is the soil half life used for modelling purposes in soil, groundwater and surface water?",
    "What is the soil half life used for modelling purposes in soil, groundwater and surface water?",
    "What are the key Koc values used for modelling?",
    "What was the key reference GAP used for risk assessment?",
    "What scenarios were modelled in groundwater for each key use?",
    "What scenarios were used for modeling in surface water?",
    "List the key metabolites considered for each compartment and their relative formation fractions?",
    "What were the conclusions of the groundwater assessment?",
    "Prepare a table of the key inputs required for ground and surface water modelling?",
    "What were the key application dates and timings used for each crop?",
    "What was the primary route of exposure in each surface water scenario?",
    "What refinements were considered in the groundwater modelling?",  
    "Were higher tier environmental fate studies provided/required?", 
    "What was the date of peak surface water exposure in the SW modelling?", 
    "Should the sediment dwelling organism risk assessment be based on PECsw or PECsed?",

    # ... other questions
]

# Search the entire folder
folder_answers = answer_questions_from_folder(pdf_folder, questions)

# Display the answers
for filename, answers in folder_answers.items():
    print(f"Answers from {filename}:")
    for question, answer in answers.items():
        print(f"Question: {question}")
        print(f"Answer: {answer}")
    print("\n")

# After extracting answers
with open('answers.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Filename', 'Question', 'Answer'])

    for filename, answers in folder_answers.items():
        for question, answer in answers.items():
            writer.writerow([filename, question, answer])

# # Load a pre-trained model and tokenizer
# model = BertForQuestionAnswering.from_pretrained('bert-base-uncased')
# tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# # Prepare your data: you'll need to format your data into a suitable format for the model
# train_dataset = # your formatted training dataset
# valid_dataset = # your formatted validation dataset

# # Set training arguments
# training_args = TrainingArguments(
#     output_dir='./results',          
#     num_train_epochs=3,              
#     per_device_train_batch_size=16,  
#     per_device_eval_batch_size=64,   
#     warmup_steps=500,                
#     weight_decay=0.01,               
#     logging_dir='./logs',            
#     logging_steps=10,
# )

# # Initialize the Trainer
# trainer = Trainer(
#     model=model,                         
#     args=training_args,                  
#     train_dataset=train_dataset,         
#     eval_dataset=valid_dataset           
# )

# # Train the model
# trainer.train()

# # Validation function
# def validate_model(data):
#     correct = 0
#     for item in data:
#         response = nlp(question=item["question"], context=item["context"])
#         model_answer = response["answer"]
#         if model_answer == item["gold_answer"]:
#             correct += 1
#     accuracy = correct / len(data)
#     return accuracy

# # Validation data

# validation_data = [
#     {
#         "context": extract_text_from_pdf("Iodosulfuron/DAR/Review report inclusion.pdf"),
#         "question": "What is the soil half life used for modelling purposes in soil, groundwater and surface water?",
#         "gold_answer": "6.3 days"
#     },
#     # ... more entries ...
# ]

# # Validate the model
# accuracy = validate_model(validation_data)
# print(f"Model Accuracy: {accuracy * 100:.2f}%")
