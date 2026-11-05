# Refactorización a LCEL Asíncrono

Script que responde una pregunta usando una cadena **LCEL** (LangChain Expression Language), ejecutada de forma asíncrona.

```
{"pregunta": "..."}  →  ChatPromptTemplate  →  ChatOpenAI  →  StrOutputParser  →  texto plano
```

En una sola línea:

```python
chain = prompt | modelo | parser
```

## Requisitos

- Python 3.12+
- Una API key de OpenAI (o de Anthropic, ver más abajo)

## Instalación

1. Crear y activar el entorno virtual:

   ```bash
   # Windows
   py -3.12 -m venv .venv
   .venv\Scripts\Activate.ps1

   # macOS / Linux
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```

2. Instalar las librerías:

   ```bash
   pip install langchain langchain-openai python-dotenv
   ```

3. Crear un archivo `.env` en la misma carpeta con tu key:

   ```
   OPENAI_API_KEY=sk-...
   ```

## Ejecución

```bash
python lcel_chain.py
```

Salida esperada:

```
¿Es texto plano (str)?: True
Respuesta:
La entropía es una medida del desorden...
```

## Cómo funciona

| Paso | Componente | Qué hace |
|------|-----------|----------|
| 1 | `ChatOpenAI` | Reemplaza al cliente manual del SDK (`AsyncOpenAI`). |
| 2 | `ChatPromptTemplate` | Arma los mensajes con roles `system` y `human`. La variable `{pregunta}` se completa con el diccionario de entrada. |
| 3 | `StrOutputParser` | Convierte el `AIMessage` del modelo en texto plano (`str`). |
| 4 | `\|` | Conecta los componentes: la salida de uno es la entrada del siguiente. |
| 5 | `await chain.ainvoke(...)` | Ejecuta la cadena sin bloquear el programa. |

## Usar Anthropic en lugar de OpenAI

1. Instalar: `pip install langchain-anthropic`
2. En el `.env`: `ANTHROPIC_API_KEY=sk-ant-...`
3. En `lcel_chain.py`, cambiar el import y el modelo:

   ```python
   from langchain_anthropic import ChatAnthropic

   modelo = ChatAnthropic(model="claude-sonnet-5-5", max_tokens=1024)
   ```

> Los modelos actuales de Anthropic **no aceptan `temperature`** (responden con error 400), por eso no se pasa ese parámetro.

## Errores comunes

- **Olvidar el `await`:** sin él, `ainvoke` devuelve una corrutina en lugar de la respuesta.
- **Variables que no coinciden:** la llave `{pregunta}` del prompt debe llamarse igual que la llave del diccionario (`{"pregunta": ...}`).
- **Error 404 de modelo:** el nombre del modelo no existe o no está disponible en tu cuenta. Verifícalo en la documentación oficial del proveedor.