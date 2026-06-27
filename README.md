# NanoWait v7 — Adaptive Execution Engine for Python

> **Stop waiting blindly. Execute intelligently.**

NanoWait substitui `time.sleep()` por um motor adaptativo que observa CPU e RAM em tempo real e aprende com cada execução.

---

## ⚡ Instalação

```bash
pip install nano-wait
```

Suporte a Wi-Fi (Windows):
```bash
pip install nano-wait[wifi]
```

---

## 🚀 Uso em 30 segundos

```python
from nano_wait import wait

# Espera padrão: nunca entrega menos do que o pedido
# Se o sistema estiver lento, aguarda um pouco mais
wait(2)

# Modo smart: pode reduzir em sistemas ociosos e rápidos
wait(2, smart=True)

# Polling até condição ser True (ou timeout)
wait(lambda: button.is_visible(), timeout=10)

# Condição com erro customizado
from nano_wait import wait_until
wait_until(lambda: page.is_loaded(), timeout=10, msg="Página não carregou")
```

---

## 🧰 API Completa

### `wait(t, **kwargs)` — O coração da lib

| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `t` | `float \| callable \| None` | — | Tempo, condição ou auto |
| `timeout` | `float` | `15.0` | Timeout máximo (modo callable) |
| `speed` | `str \| float` | `"normal"` | Preset ou valor float |
| `smart` | `bool` | `False` | Pode reduzir o tempo em sistemas ociosos |
| `profile` | `str` | `None` | Perfil de execução |
| `verbose` | `bool` | `False` | Logs de diagnóstico |
| `explain` | `bool` | `False` | Retorna `ExplainReport` detalhado |
| `raise_on_timeout` | `bool` | `False` | Lança `WaitTimeoutError` se callable expirar |

**Presets de velocidade:** `"crawl"` | `"slow"` | `"normal"` | `"fast"` | `"ultra"` | `"turbo"`

```python
wait(1, speed="fast")       # espera rápida
wait(1, speed=4.5)          # fator personalizado
wait(1, profile="ci")       # perfil CI/CD (agressivo)
wait(1, explain=True)       # retorna ExplainReport
```

---

### `wait_until(condition, *, timeout, msg, **kwargs)` — Polling semântico

Igual ao `wait(callable)` mas lança `WaitTimeoutError` com mensagem customizável.

```python
from nano_wait import wait_until, WaitTimeoutError

try:
    wait_until(lambda: driver.title == "Home", timeout=15, msg="Home page não carregou")
except WaitTimeoutError as e:
    print(f"Falhou: {e}")
```

---

### `timed_wait(label)` — Context manager de medição

```python
from nano_wait import timed_wait

with timed_wait("login_flow") as info:
    driver.find_element("#user").send_keys("admin")
    driver.find_element("#pass").send_keys("pass")
    driver.find_element("#submit").click()

print(f"Login levou {info['duration']:.3f}s")
```

---

### `execute(fn, **kwargs)` — Execução com retry inteligente

```python
from nano_wait import execute

result = execute(
    lambda: api.get_user(42),
    timeout=10,
    interval=0.3,
    max_attempts=5,
    on_error=lambda e, n: print(f"Tentativa {n}: {e}"),
)

if result.success:
    print(result.result)
else:
    result.raise_if_failed()  # relança a última exceção
```

---

### `wait_async` — Versão assíncrona

```python
import asyncio
from nano_wait import wait_async

async def main():
    await wait_async(1.0, smart=True)
    await wait_async(lambda: check_ready(), timeout=10)

asyncio.run(main())
```

---

### `wait_pool` — Múltiplos waits em paralelo

```python
from nano_wait import wait_pool

# Dispara 3 esperas simultaneamente
results = wait_pool([1.0, 2.0, 0.5], speed="fast")
```

---

## 🎛️ Perfis de Execução

| Perfil | Agr. | Uso ideal |
|---|---|---|
| `ci` | 0.4 | GitHub Actions, GitLab CI, pipelines rápidos |
| `testing` | 0.8 | QA local, testes unitários |
| `default` | 1.0 | Uso geral |
| `rpa` | 2.0 | Automação de sites lentos ou legados |
| `turbo` | 0.25 | Velocidade máxima (quando estabilidade não importa) |
| `safe` | 3.0 | Estabilidade máxima (conexões frágeis, hardware fraco) |

```python
wait(2, profile="turbo")   # o mais rápido possível
wait(2, profile="safe")    # o mais estável possível
```

---

## 🔁 Decorators

```python
from nano_wait import retry, timed, wait_before

# Retry automático até sucesso
@retry(timeout=10, max_attempts=5, smart=True)
def fetch_data():
    return requests.get(url).json()

# Mede tempo de execução
@timed()
def process_image(img):
    ...

# Espera adaptativa antes de cada chamada
@wait_before(0.5, smart=True)
def click_button(driver, selector):
    driver.find_element(selector).click()
```

---

## 🧠 Como o motor pensa

NanoWait tem dois modos de operação:

**Modo padrão (`smart=False`)** — previsível, seguro para testes:
```
WaitTime = BaseTime × (1 + overload_penalty) × ProfileAggressiveness
```
- `overload_penalty` só entra quando o sistema está sobrecarregado (CPU/RAM acima do limiar)
- `wait(2)` nunca devolve menos de 2s — garante que seus testes não ficam flaky

**Modo smart (`smart=True`)** — adaptativo, ideal para automação:
```
WaitTime = (BaseTime / (SystemHealth × SpeedFactor)) × ProfileAggressiveness
```
- Sistema ocioso → espera menor; sistema lento → espera maior
- Ideal quando a espera é uma "cortesia" ao sistema, não um requisito

O motor mantém um arquivo `~/.nano_wait_learning.json` que registra um **bias por perfil** via EMA (*Exponential Moving Average*), calibrando-se com cada execução.

```python
from nano_wait import AdaptiveLearning

al = AdaptiveLearning("default")
print(al.stats())
# {'profile': 'default', 'bias': 0.97, 'samples': 42, 'success_rate': 0.976}

print(AdaptiveLearning.all_profiles_stats())

al.reset()
```

---

## 🌐 Utilitários de Rede

```python
from nano_wait import has_internet

if has_internet():
    wait(2, smart=True)
else:
    wait(5, profile="safe")  # rede instável → mais conservador
```

Wi-Fi awareness (requer `pip install nano-wait[wifi]`):
```python
wait(2, wifi="MeuSSID", smart=True)
```

---

## 🐛 Exceções

```python
from nano_wait import WaitTimeoutError, InvalidProfileError

try:
    wait(lambda: False, timeout=1, raise_on_timeout=True)
except WaitTimeoutError as e:
    print(f"Timeout: {e}")
```

---

## 🆚 NanoWait vs time.sleep()

| | `time.sleep(2)` | `wait(2)` | `wait(2, smart=True)` |
|---|---|---|---|
| PC sobrecarregado (CPU > 80%) | 2.000s | ~2.8s ✅ | ~2.8s ✅ |
| PC normal | 2.000s | 2.000s ✅ | ~1.0s ✅ |
| PC ocioso | 2.000s | 2.000s ✅ | ~0.3s ✅ |
| Aprende com o tempo | ❌ | ✅ | ✅ |
| Polling adaptativo | ❌ | ✅ | ✅ |
| Retry inteligente | ❌ | ✅ | ✅ |
| Previsível para testes | ✅ | ✅ | ⚠️ |

> **`wait(2)`** garante pelo menos 2s — nunca surpreende seus testes com esperas menores.
> **`wait(2, smart=True)`** pode acelerar em sistemas ociosos — use quando a espera é uma cortesia, não um requisito.

---

## 📄 Licença

MIT © NanoWait Team