import threading
import time
from datetime import timedelta, timezone, datetime
from typing import Optional

import jwt
from passlib.context import CryptContext

from src.core.settings import settings

context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class SnowflakeIDGenerator:
    """
    雪花算法ID生成器（64位）
    结构：1位符号位（固定0） + 41位时间戳（毫秒级） + 10位机器ID + 12位序列号
    """

    def __init__(self, machine_id: int, datacenter_id: int = 0, start_time: Optional[float] = None):
        """
        初始化生成器
        :param machine_id: 机器ID（0-31，占5位，可扩展）
        :param datacenter_id: 数据中心ID（0-31，占5位，可扩展）
        :param start_time: 起始时间戳（毫秒），默认2020-01-01 00:00:00
        """
        # 校验机器ID和数据中心ID（共10位，最大1023）
        if machine_id < 0 or machine_id > 31:
            raise ValueError("机器ID必须在0-31之间")
        if datacenter_id < 0 or datacenter_id > 31:
            raise ValueError("数据中心ID必须在0-31之间")

        # 常量定义
        self.EPOCH = start_time or 1577808000000  # 2020-01-01 00:00:00的毫秒级时间戳
        self.MACHINE_ID_BITS = 5  # 机器ID位数
        self.DATACENTER_ID_BITS = 5  # 数据中心ID位数
        self.SEQUENCE_BITS = 12  # 序列号位数（支持同一毫秒内生成4096个ID）

        # 位移参数
        self.MACHINE_ID_SHIFT = self.SEQUENCE_BITS
        self.DATACENTER_ID_SHIFT = self.SEQUENCE_BITS + self.MACHINE_ID_BITS
        self.TIMESTAMP_SHIFT = self.SEQUENCE_BITS + self.MACHINE_ID_BITS + self.DATACENTER_ID_BITS

        # 最大取值计算（位运算）
        self.MAX_MACHINE_ID = (1 << self.MACHINE_ID_BITS) - 1  # 31
        self.MAX_DATACENTER_ID = (1 << self.DATACENTER_ID_BITS) - 1  # 31
        self.MAX_SEQUENCE = (1 << self.SEQUENCE_BITS) - 1  # 4095

        # 初始化参数
        self.machine_id = machine_id
        self.datacenter_id = datacenter_id
        self.last_timestamp = -1  # 上一次生成ID的时间戳
        self.sequence = 0  # 序列号（同一毫秒内递增）
        self.lock = threading.Lock()  # 线程锁（保证多线程安全）

    def _get_current_timestamp(self) -> int:
        """获取当前毫秒级时间戳"""
        return int(time.time() * 1000)

    def _wait_for_next_millisecond(self, last_timestamp: int) -> int:
        """等待到下一毫秒（解决时钟回拨或同一毫秒内序列号用尽的问题）"""
        timestamp = self._get_current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._get_current_timestamp()
        return timestamp

    def generate_id(self) -> int:
        """生成唯一ID"""
        with self.lock:  # 确保多线程环境下的安全性
            current_timestamp = self._get_current_timestamp()

            # 处理时钟回拨（当前时间小于上一次生成ID的时间）
            if current_timestamp < self.last_timestamp:
                # 回拨时间较短（<10ms）则等待，否则抛出异常
                if self.last_timestamp - current_timestamp < 10:
                    current_timestamp = self._wait_for_next_millisecond(self.last_timestamp)
                else:
                    raise RuntimeError(f"时钟回拨异常，差值：{self.last_timestamp - current_timestamp}ms")

            # 同一毫秒内，序列号递增
            if current_timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.MAX_SEQUENCE
                # 序列号用尽，等待下一毫秒
                if self.sequence == 0:
                    current_timestamp = self._wait_for_next_millisecond(self.last_timestamp)
            else:
                # 新的毫秒，序列号重置为0
                self.sequence = 0

            # 更新上一次时间戳
            self.last_timestamp = current_timestamp

            # 拼接64位ID（位运算）
            id = (
                    ((current_timestamp - self.EPOCH) << self.TIMESTAMP_SHIFT)  # 时间戳部分
                    | (self.datacenter_id << self.DATACENTER_ID_SHIFT)  # 数据中心ID部分
                    | (self.machine_id << self.MACHINE_ID_SHIFT)  # 机器ID部分
                    | self.sequence  # 序列号部分
            )
            return id


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return context.hash(password)


def create_access_token(data: dict, expire_minutes: timedelta):
    expire = datetime.now(timezone.utc) + expire_minutes
    to_encode = {"exp": expire, **data}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except Exception as e:
        print(f"验证错误: {str(e)}")
        return None


id_generator = SnowflakeIDGenerator(machine_id=1, datacenter_id=0)
if __name__ == '__main__':
    print(id_generator.generate_id())
    # print(get_password_hash('123456'))
    # token = create_access_token({"username": "admin"}, timedelta(seconds=10))
    # print(token)
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTM2ODk5NDEsInVpZCI6IjBlYzdkMmZmLThjMTUtNDRiZS04NDkzLTM3MTNmMTRkODI4MCIsInJvbGUiOjF9.8_RN8mXjhjes5Trgbvp2u6O4WtyEl3Gbu9NAFwLLcmI"
    # print(verify_token(token))
