# Nano-Wait

## Automação Inteligente com Espera Adaptativa e Visão Computacional

---

## Visão Geral

Nano-Wait é uma biblioteca Python para automação de interfaces gráficas (GUI) que substitui o uso de time.sleep() por um sistema de Espera Adaptativa Inteligente, ajustando dinamicamente o tempo de espera com base:

- No desempenho do computador (CPU e memória)

- Na qualidade do sinal Wi-Fi (quando disponível)

- No nível de agressividade definido pelo usuário

A partir da versão **3.0**, o Nano-Wait também inclui um Módulo de Visão Computacional (OCR) capaz de ler números diretamente da tela e tomar decisões automatizadas.

## 🚀 Por que não usar time.sleep()?

O time.sleep() é estático e “cego”:
ele ignora se o sistema está sobrecarregado ou se a rede está lenta.

O Nano-Wait resolve isso aplicando um Fator de Ajuste Dinâmico, garantindo que o script:

- Não seja lento demais quando o sistema está rápido

- Nem rápido demais a ponto de quebrar a automação

--- 

## 📦 Instalação
```
pip install nano-wait
```
- Dependências opcionais

- Para funcionamento completo do módulo Vision:

- Tesseract OCR (obrigatório para OCR)

- pytesseract

- Pillow

- pyautogui

- pynput

- psutil

- pywifi (somente no Windows)

## ⚠️ O Nano-Wait não coleta dados de rede.
Ele apenas lê métricas locais de sinal e desempenho do sistema operacional.

## 🧠 Módulo 1 — Espera Adaptativa (Smart Wait)
Função principal: **wait()**

A função wait() é o substituto direto do time.sleep().
```
from nano_wait import wait

wait(5)
```
Assinatura da função
```
wait(
    t: float,
    wifi: str | None = None,
    speed: str | float = "normal",
    verbose: bool = False,
    log: bool = False
) -> float
```

### Parâmetros



| Parâmetro | Valor padrão | Comportamento quando omitido |
|---------|--------------|-------------------------------|
| t | **obrigatório** | Define o tempo máximo de espera. Não pode ser omitido. |
| wifi | `None` | O Nano-Wait ignora métricas de rede e calcula o fator apenas com base no desempenho local (CPU e memória). |
| speed | `"normal"` | Utiliza agressividade balanceada, priorizando estabilidade sem perder desempenho. |
| verbose | `False` | Nenhuma informação de cálculo é exibida no terminal. |
| log| `False` | Nenhum arquivo de log é gerado (`nano_wait.log` não é criado nem atualizado). |


## Exemplo com Wi-Fi
```
wait(
    5,
    wifi="MinhaRede_5G",
    speed="fast",
    verbose=True
)
```
## Exemplo sem Wi-Fi (somente hardware local)
```
wait(2, speed="ultra")
```

## 🔬 Como o tempo de espera é calculado

O Nano-Wait calcula um fator adaptativo com base em:

- Uso de CPU

- Uso de memória

- Intensidade do sinal Wi-Fi (quando disponível)

## Fórmula aplicada
```
wait_time = max(0.05, min(t / factor, t))
```
## Regras de segurança

- Piso: nunca espera menos que 50 ms

- Teto: nunca ultrapassa o tempo t original

- Evita uso excessivo de CPU

## 🧠 Módulo 2 — Vision (OCR e Decisão Visual)

O módulo Vision permite ler números da tela e tomar decisões automáticas.

Classe principal
```
from nano_wait.vision import VisionMode
```
### Modos Disponíveis

| Modo | Descrição |
|------|----------|
| observe | Apenas lê e exibe os dados |
| decision | Lê os dados e executa ações |
| learn | Coleta padrões visuais (experimental) |


## 📸 Captura de Região da Tela

O usuário pode marcar regiões manualmente:
```
region = VisionMode.mark_region()
```

O retorno é uma tupla:
```
(x, y, largura, altura)
```
## 🔍 Exemplo Completo — Leitura e Decisão
```
from nano_wait.vision import VisionMode

vision = VisionMode(mode="decision")
region = VisionMode.mark_region()
vision.run(regions=[region])
```
## Lógica interna (modo decision)

Se número detectado > 1000 → clique duplo

Caso contrário → pular item

Essas ações podem ser facilmente customizadas no código.

## ⚙️ Pipeline Interno do Vision

- Captura da região da tela (ImageGrab)

- Conversão para escala de cinza

- OCR via Tesseract

- Extração numérica com Regex

- Execução de ações automáticas

## 🧪 Modo Learn (Estado Atual)

- O modo learn atualmente:

- Captura dados visuais repetidamente

- Serve como base para futuras versões com persistência

📌 Observação:
O modo learn ainda não salva modelos em disco.
Ele é experimental e focado em coleta de dados.

| Sistema | Wi-Fi | Observação            |
| ------- | ----- | --------------------- |
| Windows | ✅     | Usa pywifi            |
| macOS   | ✅     | Usa comando airport   |
| Linux   | ✅     | Usa nmcli             |
| Outros  | ❌     | Apenas modo sem Wi-Fi |

## 🛠 Casos de Uso Reais

- Bots de automação visual

- Leitura de painéis legados

- Ajuste inteligente de cliques

- Automação baseada em OCR

- RPA leve sem Selenium

## 🤝 Contribuição

- Fork o projeto

- Crie uma branch (feature/minha-melhoria)

- Envie um Pull Request

## 📄 Licença

MIT License

## 👤 Autor

Luiz Seabra De Marco

## 👤 Autor da documentação

Vitor Seabra De Marco
