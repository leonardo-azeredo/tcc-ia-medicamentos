import sys
import openai

openai.api_key = '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'

def get_openai_response(id_paciente, enfermidade, medicamento):
    user_input = f"A {medicamento} é boa para {enfermidade}?"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente médico inteligente."},
            {"role": "user", "content": user_input},
        ]
    )
    
    return response['choices'][0]['message']['content']

# Obtém os argumentos passados via linha de comando
id_paciente = sys.argv[1]
enfermidade = sys.argv[2]
medicamento = sys.argv[3]

# Chama a função com os parâmetros fornecidos
result = get_openai_response(id_paciente, enfermidade, medicamento)
print(result)
