# Processo Seletivo – Intensivo Maker | IoT

## Etapa Prática – Sistemas Embarcados

Bem-vindo(a) à **etapa prática do processo seletivo para o Intensivo Maker | IoT**.

Esta atividade tem como objetivo avaliar suas competências em **Sistemas Embarcados**, com foco em **organização de projeto, lógica de firmware e simulação de hardware**, a partir da aplicação prática dos conhecimentos adquiridos nos cursos EAD da etapa anterior.

> **Objetivo principal**  
> Avaliar sua capacidade de **planejar, estruturar e desenvolver** uma solução funcional de sistemas embarcados, seguindo boas práticas de engenharia.

---

## Antes de Tudo

Se você **nunca utilizou Git ou GitHub**, não se preocupe.  
Siga atentamente os passos abaixo.

---

### 1 - Criação de Conta no GitHub

1. Acesse: <https://github.com>
2. Clique em **Sign up**
3. Crie sua conta gratuita seguindo as instruções da plataforma

> O GitHub será utilizado para:
>
> - Envio do seu projeto
> - Versionamento do código
> - Correção e validação automática via GitHub Actions

---

### 2 - Instalação do Git

O **Git** é a ferramenta responsável pelo controle de versões do seu código.

### Windows

Baixe e instale o **Git Bash**:  
<https://git-scm.com/downloads>

### Linux / macOS

Verifique se o Git já está instalado:

```bash
git --version
```

> Caso não esteja, instale pelo gerenciador de pacotes do seu sistema.

## Preparando o Ambiente

Para desenvolver o desafio, você deverá criar uma cópia deste repositório no seu GitHub.

### 1 - Fork do Repositório

No canto superior direito desta página, clique em Fork

<img width="219" height="45" alt="image" src="https://github.com/user-attachments/assets/5d629626-513a-445c-ba0f-e5bb3e225187" />

Uma cópia do repositório será criada no seu perfil do GitHub

> O Fork permite que você trabalhe de forma independente, sem alterar o repositório original do processo seletivo.

### 2 - Clone do Repositório

No repositório do seu Fork, clique em **<> Code**

<img width="149" height="52" alt="image" src="https://github.com/user-attachments/assets/abbd331b-a005-4633-89c6-afd16acbe828" />

Copie a URL e execute no terminal:

```bash
git clone https://github.com/SEU_USUARIO/nome-do-repositorio.git
cd nome-do-repositorio
```

> O comando git clone cria uma cópia local do repositório para desenvolvimento.

### 3 - Preparação do Ambiente de Execução

Você pode executar o projeto de duas formas. Escolha apenas uma.

#### Opção A – Ambiente Python Local

**Requisitos:**

- Python 3.10 ou 3.11
- pip

**Instale as dependências:**

```bash
pip install -r requirements.txt
```

#### Opção B – Dev Container (Recomendado)

Este repositório inclui um Dev Container, garantindo um ambiente padronizado.

**Requisitos:**

- VS Code
- Docker instalado
- Extensão Dev Containers

**Passos:**

1. Abra o repositório no VS Code
2. Clique em “Reopen in Container”
3. Aguarde a criação automática do ambiente

> Todas as dependências serão instaladas automaticamente.

## Criando sua API Key do Wokwi

A simulação do projeto será executada automaticamente via GitHub Actions, utilizando o Wokwi CLI.

Para isso, você precisa gerar uma API Key.

1. Acesse: <https://wokwi.com/dashboard/ci>
2. Faça login (Google ou GitHub)
3. Clique em Generate API Token
4. Copie a chave gerada (exemplo: wokwi-xxxxxxxx)

> Importante

- Nunca faça commit dessa chave
- Ela deve ser armazenada apenas como secret no GitHub

## Configurando a API Key no GitHub (Secrets)

**No repositório do seu Fork:**

1. Vá em Settings
2. Acesse Secrets and variables → Actions
3. Clique em New repository secret
4. Nome: WOKWI_API_KEY
5. Valor: sua chave gerada
6. Salve

> As GitHub Actions do template já estão preparadas para usar essa variável automaticamente.

## Desafio Técnico

Você deverá desenvolver um projeto de sistemas embarcados simulados, utilizando Python e Wokwi.

### Estrutura mínima esperada

```text
/project
 ├── src/
 │   └── main.py        # Código principal do projeto
 ├── wokwi.toml         # Configuração da simulação
 ├── diagram.json       # Circuito no Wokwi
 └── README.md          # Explicação do seu projeto
```

> Você pode expandir essa estrutura se desejar, desde que mantenha os arquivos essenciais.

### Escolha do cenário

No diretório "scenarios" existem arquivos .md e pastas referentes a diferentes desafios. Selecione apenas um deles e mantenha apenas a pasta e .md referente ao desafio a ser desenvolvido, deletando os demais. Isso fará com o que o fluxo de testes automáticos selecione o fluxo de acordo com o desafio escolhido.

### Como Desenvolver seu Projeto

O desenvolvimento acontece principalmente nos arquivos abaixo:

#### src/main.py

- Código Python executado na simulação
- Implementa a lógica do sistema embarcado
- Exemplos: controle de LEDs, leitura de sensores, estados, temporizações, etc.

#### diagram.json

- Define o hardware virtual do projeto
- Componentes como:
  - LEDs
  - Botões
  - Sensores
  - Placa microcontroladora

#### wokwi.toml

- Configura a simulação:
  - Tipo de placa
  - Framework
  - Dependências adicionais
 
#### Rodando localmente

Para executar o seu projeto locamente, é necesário preparar a imagem docker local, e após isso
utiliza-la para gerar o arquivo que conterá o seu código para o projeto, para isso, execute os 
seguintes códigos:

1. Prepara a imagem docker (Necessário rodar apenas 1 vez)

```bash
docker build -t esp32-builder -f Dockerfile .
```

2. Prepara o arquivo de memória fs.bin (Necessário a cada iteração)

```bash
docker run --rm -v "$(pwd)/src:/mnt/src" -v "$(pwd):/mnt/out" esp32-builder bash -c "mkdir -p /tmp/fs && cp -r /mnt/src/* /tmp/fs/ && /mklittlefs/mklittlefs -c /tmp/fs -b 4096 -p 256 -s 0x200000 /mnt/out/fs.bin"
```

#### Commit e Push

Após suas alterações:

```bash
git add .
git commit -m "Descrição clara do que foi feito"
git push
```

### Execução Automática (GitHub Actions)

A cada push, o GitHub Actions irá automaticamente:

- Executar o pipeline de build
- Rodar a simulação via Wokwi CLI
- Validar que o projeto executa sem erros

### Caso algo falhe

- Vá até a aba Actions
- Analise os logs da execução
- Corrija e envie novamente

## Critérios de Avaliação

Esta etapa será avaliada considerando:

- Funcionamento correto da simulação
- Código organizado e legível
- Estrutura de arquivos correta
- Uso adequado do Wokwi
- Commits claros e bem descritos
- Projeto executando sem falhas nas Actions

---

## Submissão Final

Após concluir o desenvolvimento:

1. Verifique se o projeto **executa sem erros** nas GitHub Actions
2. Confirme que todos os arquivos obrigatórios estão presentes
3. Copie o link do **seu repositório no GitHub**

Envie o link conforme as orientações do processo seletivo na plataforma do **PNAAT**.

---

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

## Especificação dos Testes Automatizados (Wokwi CI)

Para que o projeto seja validado com sucesso na esteira de integração contínua (CI), o firmware escrito em MicroPython deve interagir corretamente com as leituras dos sensores descritos em cada cenário e enviar as mensagens de status exatas.

### Requisitos Críticos de Implementação

1. **Casamento Exato de Strings:** O Wokwi CI faz uma verificação estrita caractere por caractere. Se houver divergência em maiúsculas/minúsculas, acentuação ou falta de pontuação, o teste irá falhar.
2. **Arquitetura Não-Bloqueante:** Evite o uso de funções bloqueantes. Elas podem fazer com que o firmware perca a janela de tempo em que o simulador altera o peso, quebrando a sincronia do teste automatizado.

---

## Suporte

Em caso de dúvidas:

- Consulte o material dos cursos EAD
- Leia atentamente este README
- Analise os logs das GitHub Actions
- Utilize os canais oficiais para contato com os instrutores
