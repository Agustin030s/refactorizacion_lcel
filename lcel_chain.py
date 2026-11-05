import asyncio
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic


load_dotenv()


modelo = ChatAnthropic(model="claude-sonnet-5-5", max_tokens=1024)

# ---------------------------------------------------------------------------
# Prompt con roles System y Human.
#    {pregunta} es una variable: su nombre debe coincidir EXACTAMENTE con la
#    llave del diccionario que se pasa a ainvoke().
# ---------------------------------------------------------------------------
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Eres un profesor que explica conceptos en español, de forma breve y clara."),
        ("human", "{pregunta}"),
    ]
)

# ---------------------------------------------------------------------------
# Parser: convierte el AIMessage que devuelve el modelo en texto plano.
# ---------------------------------------------------------------------------
parser = StrOutputParser()

# ---------------------------------------------------------------------------
# La cadena LCEL: cada | pasa la salida de un paso como entrada del siguiente.
#    dict  →  prompt (mensajes)  →  modelo (AIMessage)  →  parser (str)
# ---------------------------------------------------------------------------
chain = prompt | modelo | parser


async def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Falta ANTHROPIC_API_KEY en el archivo .env")
        return

    try:
        respuesta = await chain.ainvoke({"pregunta": "¿Qué es la arquitectura de software?"})

        print(f"Respuesta:\n{respuesta}")
    except Exception as error:
        print(f"⚠️ Error al llamar al modelo: {type(error).__name__}: {error}")


if __name__ == "__main__":
    asyncio.run(main())