# Nano-Wait

Nano-Wait é uma biblioteca Python para **automação inteligente de telas e leitura de dados**, agora com **Módulo de Visão**, permitindo capturar números e textos diretamente da tela e executar ações automatizadas com base nas informações detectadas.

## Funcionalidades Principais

### Espera Inteligente (Wait)

Substitui `time.sleep` por esperas inteligentes, evitando atrasos desnecessários e tornando scripts mais confiáveis.

**Exemplos:**
```python
from nano_wait import wait

# Aguarda até que um botão esteja visível
wait.until_visible(selector="button#start")

# Aguarda até que um valor específico apareça
wait.until_text("Processo concluído")
### Visão Inteligente (Vision)

A partir da versão 3.0, Nano-Wait inclui **OCR** para ler números e textos da tela e tomar decisões automáticas.

**Principais funcionalidades:**
* Marcação de múltiplas regiões: Permite capturar várias áreas da tela simultaneamente.
* **Modos inteligentes:**
    * `observe`: apenas lê e imprime valores detectados.
    * `decision`: lê valores e executa ações automáticas.
    * `learn`: registra padrões visuais para decisões futuras.

**Exemplo de uso:**
```python
from nano_wait.vision import Vision

vision = Vision()
vision.mark_regions()     # Interativo: marque regiões na tela
vision.set_mode("observe") # Modos: observe, decision, learn
vision.run()               # Executa leitura ou ações
### Ações Automatizadas

Execute ações automáticas após detectar padrões ou valores na tela.

**Exemplos de ações:**
* Clique simples ou duplo
* Pular itens
* Executar funções customizadas

```python
def custom_action(value):
    if value > 100:
        print("Valor alto detectado!")
        # clique ou outra ação
        
vision.set_custom_action(custom_action)