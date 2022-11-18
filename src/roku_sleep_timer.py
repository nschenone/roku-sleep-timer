from datetime import datetime, timedelta
from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler
from roku import Roku


class RokuSleepTimer:
    """
    Sleep timer for Roku. Will interact with Roku via Python SDK
    and schedule sleep job using APScheduler. Automatically connects
    to the first Roku it find on the network.
    """

    def __init__(self):
        # Start background scheduler for sleep jobs
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

        # Find first roku on network
        self.discover()
        print(f"Using roku at IP: {self.host}")

    def on(self) -> str:
        """
        Turn TV on via Roku.

        :return: On message
        """
        self.roku.poweron()
        return "on"

    def off(self) -> str:
        """
        Turn TV off via Roku.

        :return: Off message
        """
        self.roku.poweroff()
        return "off"

    def discover(self, timeout: int = 10) -> None:
        """
        Find the first Roku on the network.

        :param timeout: Number of seconds before search times out.
        """
        self.roku = Roku.discover(timeout=timeout)[0]

    def trigger_sleep(self) -> None:
        """
        Sleep mechanism. If an app is open, go to the
        home screen, wait, and power off.
        """
        # Prevents Roku from waking up TV if timer is triggered while TV is off
        if self.roku.active_app.id != "None":
            self.roku.home()

            # Gives enough time to close open apps before turning off
            sleep(2)
        self.roku.poweroff()

    def stop_sleep(self) -> str:
        """
        Stop sleep timer by removing all jobs in scheduler.

        :return: Stop message
        """
        for job in self.scheduler.get_jobs():
            job.remove()
        return "Stopped sleep timer"

    def schedule_sleep(self, minutes: int) -> str:
        """
        Schedule sleep job after the specified number of minutes.

        :param minutes: Number of minutes to wait before sleeping

        :return: Job schedule success message
        """
        self.scheduler.add_job(
            self.trigger_sleep, run_date=(timedelta(minutes=minutes) + datetime.now())
        )
        return (
            f"Started sleep timer for {minutes} minutes. Enjoy the show, sleep tight!"
        )

    @property
    def host(self) -> str:
        """
        Helper to get IP address of Roku device.

        :return: IP address of Roku
        """
        return self.roku.host
