import os

from flask import Flask

from roku_sleep_timer import RokuSleepTimer

app = Flask(__name__)
sleep_timer = RokuSleepTimer()


@app.route("/")
def home() -> str:
    """
    Test connection to app.

    :return: Successful connection message
    """
    return "Connected"


@app.route("/host")
def host() -> str:
    """
    Get IP address of Roku.

    :return: IP address of Roku
    """
    return sleep_timer.host


@app.route("/on")
def on() -> str:
    """
    Turn TV on via Roku.

    :return: On message
    """
    return sleep_timer.on()


@app.route("/off")
def off() -> str:
    """
    Turn TV off via Roku.

    :return: Off message
    """
    return sleep_timer.off()


@app.route("/discover")
def discover() -> str:
    """
    Reset Roku connection to re-find first
    Roku on the network.

    :return: IP address of Roku
    """
    sleep_timer.discover()
    return sleep_timer.host


@app.route("/start/<int:minutes>")
def schedule_sleep(minutes: int):
    """
    Schedule sleep job after the specified number of minutes.

    :param minutes: Number of minutes to wait before sleeping

    :return: Job schedule success message
    """
    return sleep_timer.schedule_sleep(minutes=minutes)


@app.route("/stop")
def stop_sleep() -> str:
    """
    Stop sleep timer by removing all jobs in scheduler.

    :return: Stop message
    """
    return sleep_timer.stop_sleep()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("FLASK_PORT")))
