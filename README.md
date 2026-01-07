Com certeza! Analisei a documentação da nova funcionalidade "Explain Mode" e o `README.md` existente. Preparei uma versão atualizada do `README.md` em português, integrando as novidades do "Explain Mode" de forma clara e organizada, seguindo a estrutura e o tom do documento original.

Aqui está a proposta de atualização para o `README.md`:

---

# NanoWait: O Motor de Espera Adaptativo para Python

[![PyPI version](https://img.shields.io/pypi/v/nano_wait.svg)](https://pypi.org/project/nano_wait/)
[![License](https://img.shields.io/pypi/l/nano_wait.svg)](https://github.com/luizfilipe/NanoWait/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/nano_wait.svg)](https://pypi.org/project/nano_wait/)

## 🚀 O que é o NanoWait?

**NanoWait** é um motor de espera de execução, determinístico e adaptativo, projetado para substituir o `time.sleep()` padrão do Python.

Em vez de aguardar um tempo fixo, o NanoWait ajusta dinamicamente a duração da espera com base na **carga do sistema (CPU/RAM)** e, opcionalmente, na **força do sinal Wi-Fi**, garantindo que scripts de automação permaneçam confiáveis mesmo em ambientes lentos ou sobrecarregados.

> **Em resumo:** você solicita um tempo base (ex: `wait(5)`), e o NanoWait garante uma *espera segura e ciente do contexto*, que nunca excede o tempo solicitado e nunca fica abaixo de um piso mínimo de execução.

---

## 🛠️ Instalação

```bash
pip install nano_wait
```

### Módulo Opcional — Vision Mode

A espera visual (detecção de ícones/estados) foi intencionalmente movida para um pacote dedicado para manter o NanoWait leve e determinístico.

```bash
pip install nano-wait-vision
```

Se o Vision Mode não estiver instalado, o NanoWait levantará um erro claro em tempo de execução ao solicitar funcionalidades visuais.

---

## 💡 Guia Rápido

```python
from nano_wait import wait
import time

# Sleep padrão
start = time.time()
time.sleep(5)
print(f"time.sleep(): {time.time() - start:.2f}s")

# Espera adaptativa
start = time.time()
wait(5)
print(f"nano_wait.wait(): {time.time() - start:.2f}s")
```

O NanoWait **nunca espera mais do que o tempo base solicitado** e aplica um atraso interno mínimo de **50 ms** para prevenir o uso excessivo de CPU.

---

## ⚙️ API Principal

```python
wait(
    t: float | None = None,
    *,
    wifi: str | None = None,
    speed: str | float = "normal",
    smart: bool = False,
    explain: bool = False,
    verbose: bool = False,
    log: bool = False
) -> float | dict
```

### Parâmetros

| Parâmetro | Descrição                                                                 |
|-----------|---------------------------------------------------------------------------|
| `t`       | Tempo base em segundos (requerido para espera baseada em tempo).          |
| `wifi`    | SSID da rede Wi-Fi para avaliar a qualidade do sinal (opcional).          |
| `speed`   | Predefinição de velocidade de execução ou valor numérico.                 |
| `smart`   | Ativa o Smart Context Mode (cálculo dinâmico de velocidade).              |
| `explain` | Ativa o Explain Mode, que retorna um relatório detalhado da decisão.      |
| `verbose` | Imprime informações de depuração no `stdout`.                             |
| `log`     | Escreve dados de execução em `nano_wait.log`.                             |

---

## 🔬 Explain Mode (`explain=True`)

O Explain Mode torna o mecanismo de espera do NanoWait determinístico, auditável e explicável. Ele não altera o comportamento da espera, mas **revela como a decisão foi tomada**.

Quando ativado, o `wait()` retorna um dicionário (`Explain Report`) com todos os fatores usados no cálculo, ideal para depuração, auditoria e benchmarks.

### Exemplo de Uso em Código

```python
from nano_wait import wait

report = wait(
    t=1.5,
    speed="fast",
    smart=True,
    explain=True
)

print(report)
```

**Estrutura do Relatório:**

```json
{
    "requested_time": 1.5,
    "final_time": 1.08,
    "speed": "fast",
    "smart": true,
    "cpu_score": 5.8,
    "adaptive_factor": 1.39,
    "min_floor": false,
    "max_cap": false,
    "timestamp": "2026-01-06T23:59:25"
}
```

---

## 🧠 Smart Context Mode (`smart=True`)

Quando ativado, o NanoWait calcula a velocidade de execução automaticamente com base na **pontuação média do contexto do sistema**.

```python
wait(10, smart=True, verbose=True)
```

Exemplo de saída:

```
[NanoWait] speed=3.42 factor=2.05 wait=4.878s
```

### Como a Velocidade Inteligente Funciona

*   **PC Score** → derivado do uso de CPU e memória.
*   **Wi-Fi Score** → derivado do RSSI (se ativado).

A **Velocidade Inteligente** final é:

```
speed = clamp( (pc_score + wifi_score) / 2 , 0.5 , 5.0 )
```

Este valor é usado diretamente como o fator de velocidade de execução.

---

## 🌐 Consciência de Wi-Fi

Se sua automação depende da estabilidade da rede, o NanoWait pode adaptar o comportamento de espera com base na força do sinal Wi-Fi.

```python
wait(5, wifi="MinhaRede_5G")
```

Plataformas suportadas:

*   Windows (`pywifi`)
*   macOS (`airport`)
*   Linux (`nmcli`)

Se os dados do Wi-Fi não puderem ser lidos, o NanoWait recorre a valores neutros de forma segura.

---

## ⚡ Predefinições de Velocidade de Execução

O NanoWait suporta predefinições simbólicas de velocidade, bem como valores numéricos.

| Predefinição | Valor Interno |
|--------------|---------------|
| `slow`       | 0.8           |
| `normal`     | 1.5           |
| `fast`       | 3.0           |
| `ultra`      | 6.0           |

```python
wait(2, speed="fast")
wait(2, speed=2.2)
```

Velocidades mais altas reduzem o tempo de espera nominal de forma mais agressiva.

---

## 🖥️ Interface de Linha de Comando (CLI)

O NanoWait pode ser executado diretamente do terminal:

```bash
nano-wait <time> [options]
```

**Exemplo:**

```bash
nano-wait 5 --smart --verbose
```

**Novo no CLI: `--explain`**

Use a flag `--explain` para obter o relatório de explicação diretamente no terminal.

```bash
python -m nano_wait.cli 1.5 --speed fast --explain
```

**Saída Esperada:**

```
--- NanoWait Explain Report ---
Requested time: 1.5s
Final wait time: 1.079s
Speed input: fast → 3.0
Smart mode: False
CPU score: 5.83
Adaptive factor: 1.39
Minimum floor applied: False
Maximum cap applied: False
Timestamp: 2026-01-06T23:59:25
```

**Flags disponíveis:**

*   `--wifi SSID`
*   `--speed slow|normal|fast|ultra`
*   `--smart`
*   `--explain`
*   `--verbose`
*   `--log`

---

## 👁️ Espera Visual (Opcional)

Funcionalidades de espera visual (ícones, estados de UI) são carregadas sob demanda e requerem:

```bash
pip install nano-wait-vision
```

Se não instalado, o NanoWait levanta um `ImportError` claro explicando como habilitar a funcionalidade.

---

## 🧪 Garantias de Design

*   Comportamento determinístico
*   Sem *busy-waiting* (espera ocupada)
*   Caminhos de fallback seguros
*   Suporte multiplataforma
*   API pronta para produção

---

## 🤝 Contribuição e Licença

O NanoWait é de código aberto e licenciado sob a MIT License.

Issues, discussões e pull requests são bem-vindos.

**Autor:** Luiz Filipe Seabra de Marco
**Licença:** MIT

---
Posso ajudar com mais alguma coisa? Por exemplo, podemos traduzir o restante da documentação ou preparar os comandos para atualizar o pacote no PyPI.