# 🚀 NanoWait — Motor de Execução Adaptativo para Python

**NanoWait não é apenas uma função de espera. É um motor de execução adaptativo.**

> Execute. Retry. Adapt. Learn.

O NanoWait substitui o tradicional e estático `time.sleep()` por um sistema inteligente que observa o contexto do hardware e da rede para calcular o **Custo de Oportunidade de Espera**. Ele garante que suas automações, testes e scripts rodem o mais rápido possível em máquinas potentes, mas com a resiliência necessária em ambientes sob estresse.

---

## 📦 Instalação

A instalação é simples e direta via `pip`. O NanoWait foi projetado para ter o mínimo de dependências externas, garantindo compatibilidade e leveza.

```bash
pip install nano-wait
```

---

## ⚡ Início Rápido

O NanoWait foi desenhado para ser um substituto *drop-in* para funções de espera tradicionais, mas com superpoderes embutidos.

### 1. Espera Inteligente (Smart Wait)

Em vez de travar a thread cegamente, o NanoWait adapta o tempo de espera com base na carga da CPU, pressão de memória e qualidade do sinal Wi-Fi.

```python
from nano_wait import wait

# Adapta-se automaticamente ao seu hardware e rede
wait(2, smart=True)
```

### 2. Espera Condicional (Polling)

Aguarde até que uma condição seja verdadeira, sem sobrecarregar a CPU com loops infinitos. O intervalo de verificação é ajustado dinamicamente.

```python
from nano_wait import wait

# Aguarda até que o botão esteja visível, com timeout de 10 segundos
wait(lambda: button_is_visible(), timeout=10)
```

### 3. Motor de Execução (Execution Engine) 🔥

O núcleo do NanoWait. Ele não apenas espera, mas executa operações com inteligência, retentativas e adaptabilidade.

```python
from nano_wait import execute

def fetch_data():
    # Lógica de requisição ou automação
    return api.get_data()

result = execute(fetch_data, timeout=10)

if result.success:
    print(f"Dados obtidos em {result.duration}s após {result.attempts} tentativas.")
```

### 4. Decorador de Retentativa (Retry)

Uma interface limpa e poderosa para proteger funções propensas a falhas temporárias.

```python
from nano_wait import retry

@retry(timeout=5)
def click_button():
    return driver.click("#submit")
```

---

## 🧠 Base Teórica e Arquitetura

O diferencial do NanoWait reside na sua fundação teórica: a **Observabilidade de Execução**. 

### O Problema do `time.sleep()`

Em automação (RPA, Web Scraping, CI/CD), o uso de `time.sleep(N)` assume que o ambiente de execução é determinístico. No entanto, a latência de rede, a carga da CPU e a disponibilidade de memória variam constantemente. Um `sleep(2)` pode ser muito longo em uma máquina de desenvolvimento rápida (desperdiçando tempo) e muito curto em um servidor de CI sob carga (causando falhas).

### A Solução: Custo de Oportunidade de Espera

O NanoWait calcula o tempo ideal de espera em tempo real. A fórmula base segue uma relação inversamente proporcional à saúde do sistema:

```text
WaitTime = (BaseTime / (SystemHealth * NetworkStability)) * ProfileAggressiveness
```

1. **SystemHealth (Saúde do Sistema):** Calculada a partir do uso de CPU e Memória. Sistemas ociosos recebem pontuações altas, reduzindo o tempo de espera.
2. **NetworkStability (Estabilidade de Rede):** Avaliada através da força do sinal Wi-Fi (RSSI) ou conectividade básica.
3. **ProfileAggressiveness (Agressividade do Perfil):** Um multiplicador definido pelo perfil de execução (`ci`, `testing`, `rpa`).

### Perfis de Execução (Execution Profiles)

O NanoWait permite ajustar o comportamento do motor através de perfis pré-definidos:

| Perfil | Agressividade | Tolerância | Intervalo Base | Uso Recomendado |
| :--- | :--- | :--- | :--- | :--- |
| `ci` | 0.5 (Rápido) | 0.9 (Alta) | 0.05s | Pipelines de Integração Contínua, onde velocidade é crucial. |
| `testing` | 1.0 (Normal) | 0.7 (Média) | 0.10s | Testes automatizados locais. |
| `rpa` | 2.0 (Lento) | 0.5 (Baixa) | 0.20s | Automação de processos robóticos (RPA) em produção, priorizando estabilidade. |

---

## 🔁 Referência da API

A API do NanoWait foi refinada para ser intuitiva, tipada e robusta.

### `wait()`

A função central para pausas e polling adaptativo.

```python
def wait(
    t: float | Callable | None = None,
    *,
    timeout: float = 15.0,
    wifi: str | None = None,
    speed: str | float = "normal",
    smart: bool = False,
    verbose: bool = False,
    log: bool = False,
    explain: bool = False,
    telemetry: bool = False,
    profile: str | None = None
) -> float | bool | ExplainReport
```

**Parâmetros Principais:**
- `t`: Tempo base em segundos (float) ou uma função lambda para polling condicional.
- `smart`: Se `True`, ativa a leitura de sensores de hardware para ajustar o tempo.
- `profile`: Define o perfil de execução (`"ci"`, `"testing"`, `"rpa"`).
- `explain`: Se `True`, retorna um objeto `ExplainReport` detalhando como o tempo foi calculado.

### `execute()` ⭐

O motor de execução para operações que requerem resiliência.

```python
def execute(
    fn: Callable[[], T],
    *,
    timeout: float = 10.0,
    interval: float = 0.2,
    profile: str | None = None,
    verbose: bool = False,
    smart: bool = True
) -> ExecutionResult[T]
```

Retorna um objeto `ExecutionResult` contendo:
- `success`: Booleano indicando se a operação foi bem-sucedida.
- `result`: O valor retornado pela função `fn`.
- `attempts`: Número de tentativas realizadas.
- `duration`: Tempo total gasto na execução.
- `error`: A última exceção capturada (se houver).

---

## 📊 Observabilidade e Telemetria

O NanoWait não é uma "caixa preta". Ele fornece ferramentas para você entender exatamente o que está acontecendo sob o capô.

### Modo Explain (Auditoria)

Ideal para depuração. O modo `explain` revela a matemática por trás da decisão de timing.

```python
report = wait(2, smart=True, explain=True)
print(report.explain())
```

**Saída de Exemplo:**
```text
🚀 NanoWait Explain Mode (v6.0.0)
📅 Timestamp: 2026-04-19T10:00:00.000Z
----------------------------------------
⏱ Tempo solicitado: 2.0s
✅ Tempo final executado: 1.8450s
⚡ Velocidade configurada: normal (valor: 1.5)
🧠 Modo Inteligente (Smart): Ativado
----------------------------------------
🔍 Contexto do Sistema:
  💻 CPU Score: 8.5/10
  🌐 Wi-Fi Score: 9.0/10
  📊 Fator Adaptativo Calculado: 1.5000
----------------------------------------
💡 Decisões Internas:
  - Piso mínimo aplicado: Não
  - Teto máximo aplicado: Não
  - Resultado: Otimizado
----------------------------------------
```

### Telemetria em Tempo Real

Para monitoramento contínuo, o NanoWait pode emitir eventos de telemetria que detalham cada ajuste de intervalo durante operações de polling.

```python
wait(lambda: check_status(), timeout=20, telemetry=True)
```

---

## 🤖 Interface de Linha de Comando (CLI)

O NanoWait inclui uma CLI poderosa para uso em scripts shell e pipelines.

**Espera Básica:**
```bash
nano-wait 2
```

**Espera Inteligente com Perfil:**
```bash
nano-wait 2 --smart --profile testing
```

**Execução de Expressões (Seguro):**
```bash
nano-wait --exec "lambda: check_server_status()" --timeout 10
```

**Modo Agente (Experimental):**
```bash
nano-wait --agent "click login button"
```

---

## 🧩 Casos de Uso Reais

### Automação Web (Selenium / Playwright)

Evite `Explicit Waits` frágeis. Deixe o NanoWait tentar interagir com o elemento de forma adaptativa.

```python
from nano_wait import execute

# Tenta clicar no botão por até 5 segundos, ajustando o polling conforme a CPU
result = execute(
    lambda: driver.find_element(By.ID, "submit-btn").click(),
    timeout=5,
    profile="rpa"
)
```

### Resiliência de API

Proteja chamadas de rede contra instabilidades temporárias.

```python
import requests
from nano_wait import execute

def fetch_user():
    response = requests.get("https://api.exemplo.com/user")
    response.raise_for_status()
    return response.json()

result = execute(fetch_user, timeout=15, profile="testing")
```

---

## 🧠 Motor de Aprendizado (Learning Engine)

O NanoWait possui um sistema de viés adaptativo (Adaptive Bias). Ele aprende com execuções passadas:
- Se as esperas frequentemente resultam em timeouts, ele aumenta sutilmente o tempo base futuro.
- Se as condições são atendidas rapidamente, ele otimiza os intervalos para serem mais agressivos.

Os dados de aprendizado são armazenados localmente em `~/.nano_wait_learning.json`.

---

## 💡 Filosofia

> "Não espere cegamente. Execute com inteligência."

A maioria dos sistemas separa a lógica de espera (`time.sleep`), retentativa (`retry loops`) e polling. O NanoWait unifica esses conceitos em um único motor coeso, tipado e observável.

---

## 🚀 Roadmap

- [x] Refatoração da Arquitetura Core (v6.0.0)
- [x] Tipagem estrita e Genéricos em `ExecutionResult`
- [ ] Integração com LLMs para o Agente Autônomo
- [ ] Circuit Breaker nativo no motor de execução
- [ ] Classificação avançada de erros para retentativas seletivas
