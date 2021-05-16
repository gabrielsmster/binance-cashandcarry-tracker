import robrisa as rbs

def lambda_handler(event, context):
    print("iniciando")

    robrisa = rbs.RobrisaContangoReader(pair_code='BTCUSD', target=0.3)

    futuresInfo = robrisa.check_premium()

    if futuresInfo != []:
        robrisa.connect_to_client('telegram')
        for info in futuresInfo:
            robrisa.notify_telegram_group(info)

    print('OK')