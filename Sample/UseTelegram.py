# 텔레그램 메시지 보내기

import os
import sys
import logging
import traceback
# python-telegram-bot 라이브러리 사용시 2.0버전부터는 아래와 같이 asyncio를 인포트해야 한다.
import asyncio
# 공통 모듈 Import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from module import upbit

# -----------------------------------------------------------------------------
# - Name : main
# - Desc : 메인
# -----------------------------------------------------------------------------
if __name__ == '__main__':

    # noinspection PyBroadException
    try:
        # python-telegram-bot 라이브러리 사용시 2.0버전부터는 아래와 같이 asyncio를 사용해야 한다.
        asyncio.run(upbit.send_telegram_message('테스트 메세지 입니다!'))

    except KeyboardInterrupt:
        logging.error("KeyboardInterrupt Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-100)

    except Exception:
        logging.error("Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-200)