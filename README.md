# NanoWait

**NanoWait** é uma biblioteca Python para automação de tarefas com ajuste dinâmico do tempo de espera com base na qualidade da conexão WiFi e no desempenho do computador. É ideal para situações onde o tempo de espera deve ser ajustado de acordo com a condição da rede e do sistema para garantir que as operações de automação sejam executadas suavemente.

**Requisitos**
Antes de usar o NanoWait, você deve instalar as seguintes bibliotecas:

    pywifi: Para verificar a qualidade do sinal WiFi.
    psutil: Para monitorar o desempenho do sistema.
    pyautogui: Para realizar ações de automação no computador.

**Principais Funções**
wait_wifi: Ela deve ser passada junto com speed e ssid. Ela calcula o tempo de espera considerando o Wifi e o processamento do PC.
wait_n_wifi: Ela deve ser passada junto com speed. Ela calcula o tempo de espera considerando o processamento do PC no momento.
