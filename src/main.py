from machine import Pin, I2C
import time

# --------------------------------------------------------------------
# Configuracao de hardware
# --------------------------------------------------------------------

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
MPU_ADDR = 0x68

# botao (porta): pull-up interno, entao pressionado = 0 (LOW), solto = 1 (HIGH)
btn = Pin(4, Pin.IN, Pin.PULL_UP)

# --------------------------------------------------------------------
# Constantes do desafio
# --------------------------------------------------------------------

LIMITE_TEMPO_X = 5000       # 5 segundos com a porta aberta = alarme
LIMITE_VARIACAO_Y = 3.0     # 3 graus de diferenca = alarme termico
TEMPO_CONFIRMACAO_NORMAL = 600  # ms de estabilidade antes de avisar normalizacao

# --------------------------------------------------------------------
# Funcoes do sensor MPU6050
# --------------------------------------------------------------------

def mpu_init():
    i2c.writeto_mem(MPU_ADDR, 0x6B, bytes([0]))

def ler_temperatura():
    dados = i2c.readfrom_mem(MPU_ADDR, 0x41, 2)
    bruto = (dados[0] << 8) | dados[1]
    if bruto > 32767:
        bruto -= 65536
    return (bruto / 340.0) + 36.53

def ler_temperatura_segura(ultima_valida):
    # se o sensor falhar momentaneamente (ex: ruido no I2C), a gente nao
    # quer que o programa inteiro trave/quebre -- usa a ultima leitura
    # boa conhecida e segue o loop normalmente
    try:
        return ler_temperatura()
    except OSError:
        return ultima_valida

# --------------------------------------------------------------------
# Logica de cada parte do sistema (separada em funcoes, cada uma cuida
# de uma coisa so, pra ficar mais facil de ler e de testar)
# --------------------------------------------------------------------

def checar_porta(porta_esta_aberta, agora, porta_aberta_desde, alarme_porta):
    if porta_esta_aberta:
        if porta_aberta_desde is None:
            porta_aberta_desde = agora
        elif not alarme_porta and time.ticks_diff(agora, porta_aberta_desde) >= LIMITE_TEMPO_X:
            alarme_porta = True
            print("ALERTA: Porta aberta por muito tempo!")
    else:
        porta_aberta_desde = None
        alarme_porta = False
    return porta_aberta_desde, alarme_porta

def checar_temperatura(temp_atual, temp_referencia, alarme_temperatura):
    delta = abs(temp_atual - temp_referencia)
    if delta >= LIMITE_VARIACAO_Y:
        if not alarme_temperatura:
            alarme_temperatura = True
            print("ALERTA: Degradacao termica detectada!")
    else:
        if alarme_temperatura:
            alarme_temperatura = False
        temp_referencia = temp_atual
    return temp_referencia, alarme_temperatura

def checar_normalizacao(alarme_porta, alarme_temperatura, agora, estava_em_alarme, normal_desde):
    if not alarme_porta and not alarme_temperatura:
        if estava_em_alarme:
            if normal_desde is None:
                normal_desde = agora
            elif time.ticks_diff(agora, normal_desde) >= TEMPO_CONFIRMACAO_NORMAL:
                print("Status: Sistema Normalizado.")
                estava_em_alarme = False
                normal_desde = None
        else:
            normal_desde = None
    else:
        estava_em_alarme = True
        normal_desde = None
    return estava_em_alarme, normal_desde

# --------------------------------------------------------------------
# Inicializacao
# --------------------------------------------------------------------

mpu_init()
print("Sistema de Monitoramento Inicializado")

time.sleep_ms(300)
temp_referencia = ler_temperatura_segura(25.0)  # 25.0 = valor de segurança caso falhe logo de cara

porta_aberta_desde = None
alarme_porta = False
alarme_temperatura = False
estava_em_alarme = False
normal_desde = None

# --------------------------------------------------------------------
# Loop principal (nao-bloqueante: nada de time.sleep() longo aqui dentro)
# --------------------------------------------------------------------

while True:
    agora = time.ticks_ms()

    porta_esta_aberta = btn.value() == 1
    porta_aberta_desde, alarme_porta = checar_porta(
        porta_esta_aberta, agora, porta_aberta_desde, alarme_porta
    )

    temp_atual = ler_temperatura_segura(temp_referencia)
    temp_referencia, alarme_temperatura = checar_temperatura(
        temp_atual, temp_referencia, alarme_temperatura
    )

    estava_em_alarme, normal_desde = checar_normalizacao(
        alarme_porta, alarme_temperatura, agora, estava_em_alarme, normal_desde
    )

    time.sleep_ms(50)
