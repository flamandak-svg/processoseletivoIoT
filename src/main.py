from machine import Pin, I2C
import time

# --------------------------------------------------------------------
# Configuracao de hardware
# --------------------------------------------------------------------

# I2C nos pinos padrao do ESP32 (SDA=21, SCL=22), onde o MPU6050 esta ligado
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
MPU_ADDR = 0x68

# botao (porta): pull-up interno, entao pressionado = 0 (LOW), solto = 1 (HIGH)
btn = Pin(4, Pin.IN, Pin.PULL_UP)

# --------------------------------------------------------------------
# Funcoes do sensor MPU6050
# --------------------------------------------------------------------

def mpu_init():
    # registrador de power management, escrever 0 "acorda" o sensor
    i2c.writeto_mem(MPU_ADDR, 0x6B, bytes([0]))

def ler_temperatura():
    # le os 2 bytes do registrador de temperatura (0x41 e 0x42)
    dados = i2c.readfrom_mem(MPU_ADDR, 0x41, 2)
    bruto = (dados[0] << 8) | dados[1]
    if bruto > 32767:
        bruto -= 65536
    # formula padrao do datasheet do MPU6050 pra converter em graus C
    temp_c = (bruto / 340.0) + 36.53
    return temp_c

# --------------------------------------------------------------------
# Constantes do desafio
# --------------------------------------------------------------------

LIMITE_TEMPO_X = 5000       # 5 segundos com a porta aberta = alarme
LIMITE_VARIACAO_Y = 3.0     # 3 graus de diferenca = alarme termico

# --------------------------------------------------------------------
# Variaveis de estado
# --------------------------------------------------------------------

porta_aberta_desde = None   # guarda o tempo (ticks_ms) de quando a porta abriu
alarme_porta = False
alarme_temperatura = False
temp_referencia = None
estava_em_alarme = False   # controla se ja estava em algum alarme, pra so avisar 1x a normalizacao
normal_desde = None        # marca quando o sistema voltou a ficar seguro, pra confirmar antes de avisar

# --------------------------------------------------------------------
# Inicializacao
# --------------------------------------------------------------------

mpu_init()
print("Sistema de Monitoramento Inicializado")

# pequena pausa pra dar tempo do cenario de teste configurar o sensor
# antes da gente fixar a "temperatura de referencia" inicial
time.sleep_ms(300)
temp_referencia = ler_temperatura()

# --------------------------------------------------------------------
# Loop principal (nao-bloqueante: nada de time.sleep() aqui dentro)
# --------------------------------------------------------------------

while True:
    agora = time.ticks_ms()

    # porta: pino em LOW (0) = pressionado = fechada. HIGH (1) = solta = aberta
    porta_esta_aberta = btn.value() == 1

    # --- logica da porta ---
    if porta_esta_aberta:
        if porta_aberta_desde is None:
            porta_aberta_desde = agora
        elif not alarme_porta and time.ticks_diff(agora, porta_aberta_desde) >= LIMITE_TEMPO_X:
            alarme_porta = True
            print("ALERTA: Porta aberta por muito tempo!")
    else:
        porta_aberta_desde = None
        alarme_porta = False

    # --- logica da temperatura ---
    temp_atual = ler_temperatura()
    delta = abs(temp_atual - temp_referencia)

    if delta >= LIMITE_VARIACAO_Y:
        if not alarme_temperatura:
            alarme_temperatura = True
            print("ALERTA: Degradacao termica detectada!")
    else:
        # se estabilizou de novo, atualiza a referencia e limpa o alarme
        if alarme_temperatura:
            alarme_temperatura = False
        temp_referencia = temp_atual

    # --- normalizacao: só quando as duas condicoes estao ok ao mesmo tempo ---
    # espera 600ms de estabilidade antes de avisar, pra dar tempo do teste
    # automatico "ouvir" a mensagem (evita o texto sumir cedo demais)
    if not alarme_porta and not alarme_temperatura:
        if estava_em_alarme:
            if normal_desde is None:
                normal_desde = agora
            elif time.ticks_diff(agora, normal_desde) >= 600:
                print("Status: Sistema Normalizado.")
                estava_em_alarme = False
                normal_desde = None
        else:
            normal_desde = None
    else:
        estava_em_alarme = True
        normal_desde = None

    time.sleep_ms(50)  # pequena pausa entre leituras, nao afeta o timing dos testes
