import os
import pandas as pd
from pydantic_ai import Agent, Tool
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider
from schemas import Pergunta, Resposta
from dotenv import load_dotenv
from preprocessing import unzip

# Carregar variáveis .env
load_dotenv()
api_key = os.getenv("API_KEY")
model = os.getenv("MODEL")

# Carrega os CSVs
unzip()
cabecalho_df = pd.read_csv("data/202401_NFs_Cabecalho.csv")
itens_df = pd.read_csv("data/202401_NFs_Itens.csv")
cabecalho_df_preview = cabecalho_df.head(2).to_markdown(index=False)
itens_df_preview = itens_df.head(2).to_markdown(index=False)

# Set up Groq provider and model
provider = GroqProvider(api_key=api_key)
model = GroqModel(model, provider=provider)

@Tool
def query_data(query: str) -> str:
    """
    Executes a Python query to answer questions.
    """
    try:
        # The 'global' scope makes the dataframes available to eval()
        result = eval(query, globals())
        
        # Se o resultado for um DataFrame, retorne um resumo em vez do objeto inteiro
        if isinstance(result, pd.DataFrame):
            return f"A consulta retornou uma tabela com {len(result)} linhas. Aqui estão as 5 primeiras: {result.head().to_string()}"
        # Se for uma série (uma coluna), também resuma
        elif isinstance(result, pd.Series):
             return f"A consulta retornou uma série com {len(result)} itens. Aqui estão os 5 primeiros: {result.head().to_string()}"
        
        return str(result)
    except Exception as e:
        return f"Error executing query: {e}"

# Create the agent
agent = Agent(
    model=model,
    system_prompt=f"""
Você é um assistente de análise de dados especializado em notas fiscais.
Sua tarefa é responder a perguntas usando DataFrames do pandas.

Você tem acesso a dois DataFrames: 'cabecalho_df' e 'itens_df'.

Para responder à pergunta do usuário, você DEVE seguir estes passos:
1.  Primeiro, gere o código Python necessário para a ferramenta `query_data` para encontrar a resposta nos DataFrames.
2.  A ferramenta executará o código e retornará o resultado (por exemplo, um número, uma lista ou uma tabela).
3.  Com base nesse resultado, formule uma resposta final para o usuário em linguagem natural. A resposta deve ser concisa, direta e NUNCA conter código Python.

Exemplo de consulta: Para encontrar o valor total de todas as notas, o código seria `cabecalho_df['VALOR NOTA FISCAL'].sum()`. Se o resultado for `15000.50`, sua resposta final deve ser algo como: "O valor total de todas as notas fiscais é R$ 15.000,50."

### Visualização dos dados disponíveis. Foque nas colunas e nos tipos de dados para interpretar as perguntas e fazer as operações corretamente!

#### 📄 `cabecalho_df` (Notas fiscais selecionadas aleatoriamente do arquivo de notas fiscais do mês de janeiro/2024, disponibilizado pelo Tribunal de Contas da União):
{cabecalho_df_preview}

#### 📄 `itens_df` (Os itens correspondentes das notas fiscais selecionadas):
{itens_df_preview}

⚠️ As colunas de data (como 'DATA EMISSÃO') estão no formato:
**AAAA-MM-DD HH:MM:SS**
Onde:
- AAAA = ano (ex: 2024)
- MM = mês (ex: 01)
- DD = dia (ex: 10)
- HH = hora (ex: 09)
- MM = minuto (ex: 45)
- SS = segundo (ex: 00)
""",
    tools=[query_data]
)
