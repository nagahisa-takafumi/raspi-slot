import RPi.GPIO as GPIO
import time
import random

LedPins = [17, 27, 22] # LED出力のGPIOピン
SwPin = 26 # スイッチの入力箇所

# ピン番号指定方法選択(.setmode)
GPIO.setmode(GPIO.BCM) # GPIO番号で指定

# LEDピン設定
for LPin in LedPins:
  GPIO.setup(LPin, GPIO.OUT) # LEDピン指定

# インプット指定方法(2種類(pullUp, pullDown))
GPIO.setup(SwPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # スイッチピン

beforeSwState = -1
SlotCount = 0
SlotMax = 0

try:
  while True:
    sw = GPIO.input(SwPin) # スイッチの状態(0:通電, 1:非通電)

    # 押された場合
    if beforeSwState != sw and sw == 0:
      print('押された')
      time.sleep(0.2)
      if random.randint(1, 2) == 2:
        GPIO.output(LedPins[SlotCount], GPIO.HIGH) # 点灯
        SlotMax += 1
      SlotCount += 1

      # リセット
      if SlotCount == 3:
        print('リセット')
        time.sleep(0.2)
        if SlotMax == 3:
          # アタリ
          for i in range(8):
            for Lpin in LedPins:
              GPIO.output(Lpin, GPIO.HIGH) # 点灯
              time.sleep(0.07)
            time.sleep(0.1)
            for Lpin in LedPins:
              GPIO.output(Lpin, GPIO.LOW) # 消灯
            time.sleep(0.1)
        else:
          # ハズレ
          for Lpin in LedPins:
            GPIO.output(Lpin, GPIO.LOW) # 消灯
        SlotCount = 0
        SlotMax = 0

    beforeSwState = sw
except KeyboardInterrupt:
  GPIO.cleanup() # GPIOの解放
