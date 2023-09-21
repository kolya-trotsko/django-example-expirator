import traceback
import logging
import time
import datetime
import telebot
from setting.config import TG_TOKEN, TG_CHATID
from data.db.get_db_domains import get_db_domains_daysleft_notification
from data.db.get_db_notifications import get_db_notifications
from data.db.update_db_notifications import update_db_notifications


bot = telebot.TeleBot(TG_TOKEN)

def send_telegram_notification(id=TG_CHATID, text="Hello, I am fine!"):
    try:
        bot.send_message(id, text)
        time.sleep(5)
    except Exception as e:
        error_text = f"Error sending telegram notification: {str(e)}"
        logging.error(error_text)

def get_domains_notification():
    data = {}
    domains = get_db_domains_daysleft_notification()
    notifications = get_db_notifications()
    five_days_ago = str(datetime.date.today() - datetime.timedelta(days=5))
    
    for domain in domains:
        if notifications.get(domain["domain_name"], False):
            domain_days_left = notifications[domain["domain_name"]].get("domain_days_left", five_days_ago)
        else:
            domain_days_left = five_days_ago

        last_notification_date = datetime.datetime.strptime(domain_days_left, "%Y-%m-%d").date()
        if (datetime.datetime.now().date() - last_notification_date).days >= 5:
            binom_exists = domain['binom_exists']
            if binom_exists in data:
                data[binom_exists].append(domain)
            else:
                data[binom_exists] = [domain]
    return data

def format_domain_notification_text(domain):
    text = f"Domain: {domain['domain_name']}\n" \
           f"❌ Expires in: {domain['days_left']} days\n" \
           f"Clicks 60 days: {domain['days_clicks_60']}\n"\
           f"CF: {domain['cloudflare_acc']}\n" \
           f"NS: {domain['name_servers']}\n" \
           f"Registrar: {domain['registrar']}\n" \
           f"Registrar acc: {domain['registrar_acc']}\n"

    return text

def telegram_domain_notifications():
    domains = get_domains_notification()

    for binom, domain_list in domains.items():
        try:
            text = f"binom: {binom}\n"
            for domain in domain_list:
                formatted_domain_text = format_domain_notification_text(domain)
                if len(text) + len(formatted_domain_text) <= 2048:
                    text += formatted_domain_text
                    update_db_notifications({"domain": domain['domain_name'], "domain_days_left": datetime.datetime.now().date()})

            if domain_list and domain_list[0]['binom_owner'] is not None:
                text += f"\n{domain_list[0]['binom_owner']}"

            send_telegram_notification(TG_CHATID, text)

        except Exception as e:
            error_text = f"Error: {str(e)}\n{traceback.format_exc()}"
            logging.error(error_text)
