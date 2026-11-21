
import json

from services.llm import chamar_llm, MODEL, TEMPERATURE
from services.prompt_engine import montar_prompt
from services.storage import buscar_cache, salvar_execucao, HISTORY_PATH
from prompts.formats import FORMATS


TIPOS = {
    "1": "diagnosis",
    "2": "resolution",
    "3": "clarification",
    "4": "flowchart"
}


def carregar_historico():
    with open(HISTORY_PATH, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def selecionar_cliente():
    with open("data/customers.json", encoding="utf-8") as arquivo:
        clientes = json.load(arquivo)

    print("\n=== CLIENTES ===")

    for i, cliente in enumerate(clientes, 1):
        print(f"{i}. {cliente['name']} - {cliente['technical_level']}")

    while True:
        opcao = input("Selecione o cliente: ")

        if opcao.isdigit() and 1 <= int(opcao) <= len(clientes):
            return clientes[int(opcao) - 1]

        print("Cliente inválido.")


def selecionar_tipo():
    print("\n=== TIPO DE CONTEÚDO ===")
    print("1. Diagnóstico")
    print("2. Resolução")
    print("3. Perguntas de esclarecimento")
    print("4. Fluxograma")

    while True:
        opcao = input("Selecione o tipo: ")

        if opcao in TIPOS:
            return TIPOS[opcao]

        print("Opção inválida.")


def selecionar_versao():
    while True:
        versao = input("Versão do prompt (v1/v2): ").strip().lower()

        if versao in ("v1", "v2"):
            return versao

        print("Versão inválida.")


def validar_resposta(output, tipo):
    schema = FORMATS[tipo]
    if (
        not isinstance(output, dict)
        or set(output) != set(schema)
        or any(
            not isinstance(output[campo], type(valor))
            for campo, valor in schema.items()
        )
    ):
        raise ValueError("Estrutura JSON inválida.")

    for campo, valor in output.items():
        if isinstance(valor, list) and any(not isinstance(item, str) for item in valor):
            raise ValueError(f"O campo {campo} deve conter somente textos.")
        textos = valor if isinstance(valor, list) else [valor]
        if not textos or any(not texto.strip() for texto in textos):
            raise ValueError(f"O campo obrigatório {campo} está vazio.")

    if tipo == "flowchart":
        if output["format"] != "decision_tree":
            raise ValueError("O formato do fluxo deve ser decision_tree.")
        if "\\n" in output["flow"]:
            raise ValueError("O fluxo contém escapes de linha duplicados (\\n literal).")


def gerar_resposta(cliente, ticket, tipo, versao):
    mensagens = montar_prompt(cliente, ticket, tipo, versao)

    output = buscar_cache(mensagens, MODEL, TEMPERATURE)
    resposta_nova = output is None

    if resposta_nova:
        resposta = chamar_llm(mensagens)
        try:
            output = json.loads(resposta)
        except (json.JSONDecodeError, TypeError) as erro:
            raise ValueError("A LLM não retornou um JSON válido.") from erro

    validar_resposta(output, tipo)

    if resposta_nova:
        salvar_execucao(
            cliente, ticket, tipo, versao,
            output, MODEL, TEMPERATURE, mensagens
        )

        print("\nNova resposta gerada e salva!")
    else:
        print("\nResposta recuperada do cache!")

    print(json.dumps(output, indent=4, ensure_ascii=False))

    if tipo == "flowchart":
        print("\nFluxo:")
        print(output["flow"])

    return output


def gerar_conteudo(comparar=False):
    cliente = selecionar_cliente()
    ticket = input("\nDescreva o problema: ").strip()

    if not ticket:
        print("O ticket não pode estar vazio.")
        return

    tipo = selecionar_tipo()

    if comparar:
        versoes = ["v1", "v2"]
    else:
        versoes = [selecionar_versao()]

    for versao in versoes:
        print(f"\n========== RESULTADO {versao.upper()} ==========")
        gerar_resposta(cliente, ticket, tipo, versao)


def selecionar_registro(historico):
    if not historico:
        print("\nHistórico vazio.")
        return None

    registros = list(reversed(historico[-10:]))

    print("\n=== ÚLTIMAS EXECUÇÕES ===")

    for i, registro in enumerate(registros, 1):
        print(
            f"{i}. {registro['customer_id']} | "
            f"{registro['content_type']} | "
            f"{registro['prompt_version']} | "
            f"{registro['ticket'][:45]}"
        )

    while True:
        opcao = input("\nNúmero do registro (0 para voltar): ")

        if opcao == "0":
            return None

        if opcao.isdigit() and 1 <= int(opcao) <= len(registros):
            return registros[int(opcao) - 1]

        print("Opção inválida.")


def consultar_historico():
    historico = carregar_historico()
    registro = selecionar_registro(historico)

    if registro is not None:
        print(json.dumps(registro, indent=4, ensure_ascii=False))


def avaliar_resposta():
    historico = carregar_historico()
    registro = selecionar_registro(historico)

    if registro is None:
        return

    print("\n=== RESPOSTA A SER AVALIADA ===")
    print(json.dumps(registro["output"], indent=4, ensure_ascii=False))

    criterios = {
        "clarity": "Clareza",
        "customer_fit": "Adequação ao cliente",
        "actionability": "Acionabilidade"
    }

    avaliacao = {}

    for campo, nome in criterios.items():
        print(f"\nCritério: {nome}")

        while True:
            nota = input("Nota (1 a 5): ")

            if nota.isdigit() and 1 <= int(nota) <= 5:
                break

            print("A nota deve estar entre 1 e 5.")

        justificativa = input("Justificativa: ").strip()

        while not justificativa:
            justificativa = input("Informe uma justificativa: ").strip()

        avaliacao[campo] = {
            "score": int(nota),
            "justification": justificativa
        }

    registro["evaluation"] = avaliacao

    with open(HISTORY_PATH, "w", encoding="utf-8") as arquivo:
        json.dump(historico, arquivo, indent=4, ensure_ascii=False)

    print("\nAvaliação salva com sucesso!")


def main():
    while True:
        print("\n========== ASSISTENTE DE SUPORTE TÉCNICO ==========")
        print("1. Gerar conteúdo")
        print("2. Comparar prompts V1 e V2")
        print("3. Consultar histórico")
        print("4. Avaliar resposta")
        print("5. Sair")

        opcao = input("\nEscolha uma opção: ")

        try:
            if opcao == "1":
                gerar_conteudo()

            elif opcao == "2":
                gerar_conteudo(comparar=True)

            elif opcao == "3":
                consultar_historico()

            elif opcao == "4":
                avaliar_resposta()

            elif opcao == "5":
                print("Encerrando...")
                break

            else:
                print("Opção inválida.")

        except Exception as erro:
            print(f"\nErro: {erro}")


if __name__ == "__main__":
    main()
