# ./src/core/debug.py


def debug(file_name: str) -> None:
    print(
        "...\n"
        f"[DEBUG] O script {file_name} está sendo executado em modo de teste.\n"
        "[DEBUG] Isso serve para depurar o módulo, validando suas importações.\n"
        "[DEBUG] Nenhuma operação principal será executada neste processo."
    )


if __name__ == "__main__":
    debug("debug.py")
