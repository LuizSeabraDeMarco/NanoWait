# Nano-Wait Vision Module

Nano-Wait agora inclui um módulo de **Visão Inteligente**, capaz de ler números diretamente da tela e tomar decisões automáticas em aplicativos ou vídeos.

## Funcionalidades principais

- **Múltiplas regiões**: capture números de várias áreas da tela ao mesmo tempo.
- **Marcação interativa**: selecione regiões da tela facilmente usando o mouse com `mark_region()`.
- **Modos inteligentes**:
  - `observe`: apenas lê e exibe números.
  - `decision`: lê números e executa ações automáticas com base em valores.
  - `learn`: registra padrões visuais para uso futuro.
- **Ações automatizadas**: clique duplo, pular itens, etc.
- Compatível com macOS, Windows e Linux.

## Instalação

```bash
pip install -e .
# Dependências para o módulo de visão
pip install pyautogui pytesseract pynput opencv-python-headless
# macOS: instale o Tesseract OCR
brew install tesseract
