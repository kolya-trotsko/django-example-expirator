import time
import schedule
import traceback
import logging

from data.services.update_domains import update_domains

from feature import (
    daily_check_days_left,
    daily_check_whois_trouble,
    daily_check_cf_ns,
    daily_check_binom_allowed
)

from notification.telegram_notification import (
    send_telegram_notification,
    telegram_domain_notifications
)


def handle_exception(func, *args, **kwargs):
    try:
        result = func(*args, **kwargs)
        if result is not None:
            return result
    except Exception as e:
        error_text = f"Error: {str(e)}\n{traceback.format_exc()}"
        send_telegram_notification(text=f"Hi! I am in trouble: {error_text}")
        logging.error(error_text)


def update_all_domains():
    handle_exception(update_domains)


def daily_checks():
    handle_exception(daily_check_days_left)
    handle_exception(daily_check_binom_allowed)
    handle_exception(daily_check_cf_ns)
    handle_exception(daily_check_whois_trouble)


def send_notifications():
    handle_exception(send_telegram_notification)
    handle_exception(telegram_domain_notifications)


def run_tests():
    print("_update_domains")
    update_all_domains()
    print("_daily_check")
    daily_checks()
    print("_notification")
    send_notifications()


def schedule_tasks():
    schedule.every(6).hours.do(update_all_domains)
    schedule.every().day.do(daily_checks)
    schedule.every().day.at("13:00").do(send_notifications)

    while True:
        schedule.run_pending()
        time.sleep(100)


def main():
    run_tests()
    schedule_tasks()


if __name__ == "__main__":
    main()
