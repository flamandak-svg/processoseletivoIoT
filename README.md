#Relatório – Projeto Smart Cooler
## Relatório do Candidato

O arquivo **`README.md` do seu repositório** deve ser utilizado como o  
**relatório final do desafio técnico**.

Preencha todas as seções abaixo de forma **clara, objetiva e técnica**.

> **Dica importante**  
> Não é necessário um relatório extenso.  
> O principal critério é demonstrar **clareza nas decisões técnicas**, organização e entendimento do sistema embarcado desenvolvido.
> Não mantenha os demais conteúdos escritos nesse arquivo README, aqui devem ser concentradas apenas informações referentes ao projeto desenvolvido.

---

### Identificação do Candidato

- **Nome completo: Amanda Kellen Farias Lopes**
- **GitHub: flamandak-svg**

---

## Visão Geral da Solução

Desenvolvi um sistema que monitora duas situações de risco ao mesmo tempo: a porta ficar aberta por muito tempo e uma subida brusca de temperatura. Quando qualquer uma dessas coisas acontece, o sistema imprime um alerta na saída serial; quando tudo volta ao normal, ele também avisa. O sistema funciona sozinho, reagindo direto às leituras do botão (que simula a porta) e do sensor MPU6050 (que simula a temperatura), sem precisar de nenhum comando manual.

---

## Arquitetura do Sistema Embarcado

Ao ligar, o sistema inicializa o sensor via I2C, imprime a mensagem de boot e entra num loop que roda continuamente, checando duas coisas a cada volta:

Porta: guardo o momento em que ela abre. Se passar de 5 segundos (5000ms) aberta, disparo o alerta.
Temperatura: comparo a leitura atual com uma temperatura de referência guardada no início. Se a diferença for de 3°C ou mais, disparo o alerta térmico.
Normalização: só aviso que voltou ao normal quando as duas condições ficam seguras ao mesmo tempo, e espero 600ms de estabilidade antes de avisar (pra evitar disparar cedo demais).

Uso time.ticks_ms() e time.ticks_diff() pra controlar o tempo, nunca time.sleep() dentro do loop principal — assim o programa nunca trava esperando parado, e continua lendo os sensores o tempo todo.

---

## Componentes Utilizados na Simulação

Placa ESP32 DevKit C v4
Sensor MPU6050 (imu1), usado pra simular a leitura de temperatura, ligado via I2C nos pinos 21 e 22
Botão (btn1), simulando o sensor de abertura da porta, com pull-up interno no pino 4
Saída Serial (UART) pra enviar os logs de status e alerta

---

## Decisões Técnicas Relevantes

Usei constantes com nomes claros (LIMITE_TEMPO_X, LIMITE_VARIACAO_Y) ao invés de números soltos no meio do código, pra ficar mais fácil de entender e ajustar depois.
Adicionei uma espera de 600ms antes de avisar que o sistema normalizou — percebi, olhando o log de um teste que falhava no GitHub Actions, que a mensagem estava sendo impressa cedo demais e o teste automático não conseguia "pegar" ela a tempo.
Também ajustei o momento de capturar a temperatura de referência: agora eu espero um pouco no início antes de fixar esse valor, pra dar tempo do cenário de teste configurar o sensor primeiro.

---

## Resultados Obtidos

Os 3 cenários de teste automatizado passam no GitHub Actions: Alarme por Porta Aberta, Alarme por Elevação Térmica e Retorno ao Estado Normal. As mensagens impressas batem exatamente com o texto esperado por cada teste.
---

## Comentários Adicionais (Opcional)

A maior dificuldade foi um erro no diagram.json: eu tinha usado os nomes de pino com a letra "D" na frente (tipo D21, D22), mas o formato certo pra essa placa é sem esse prefixo. Isso impedia o sensor de ser reconhecido (erro ENODEV), e resolvi tirando o "D" dos nomes.
Outra dificuldade foi um problema sutil de tempo na mensagem de normalização — só descobri comparando o log de um teste que passava com o que estava falhando, e resolvi adicionando aquele tempo de confirmação de 600ms antes de imprimir a mensagem.

---

> Este relatório faz parte da avaliação técnica.  
> Clareza, objetividade e organização são tão importantes quanto o funcionamento do código.

---