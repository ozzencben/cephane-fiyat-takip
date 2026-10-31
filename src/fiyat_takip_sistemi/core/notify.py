import os
import sys
from typing import Any, Dict, List, Optional

import httpx
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

MAX_TELEGRAM_MESSAGE_LENGTH = 4096


def format_tr_price(val: Optional[float]) -> str:
    if val is None:
        return "-"
    s = f"{val:,.2f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def get_all_telegram_chat_ids(token: Optional[str] = None) -> List[str]:
    """
    Hem .env içindeki TELEGRAM_CHAT_ID değerini hem de @Cep-haneFiyatTakipBot botuna
    /start veya mesaj yazan tüm aktif kullanıcıların chat_id değerlerini toplar.
    Böylece Serdar Bey kendi telefonundan bota /start yazdığında bildirimler anında ona da gider.
    """
    bot_token = token or TELEGRAM_TOKEN
    chat_ids: List[str] = []
    if TELEGRAM_CHAT_ID:
        chat_ids.append(str(TELEGRAM_CHAT_ID))

    if not bot_token:
        return chat_ids

    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    try:
        resp = httpx.get(url, timeout=15.0)
        if resp.status_code == 200:
            updates = resp.json().get("result", [])
            for upd in updates:
                chat = (
                    upd.get("message", {}).get("chat", {})
                    or upd.get("edited_message", {}).get("chat", {})
                    or upd.get("channel_post", {}).get("chat", {})
                )
                cid = chat.get("id")
                if cid and str(cid) not in chat_ids:
                    chat_ids.append(str(cid))
    except Exception as e:
        print(f"⚠️ Telegram getUpdates uyarısı: {e}")

    return chat_ids


def get_telegram_chat_id(token: Optional[str] = None) -> Optional[str]:
    ids = get_all_telegram_chat_ids(token)
    return ids[-1] if ids else None


def format_daily_notification_message(
    llm_report: str, critical_alerts: List[Dict[str, Any]]
) -> str:
    """
    Cep-Hane Teknoloji Satın Alma Müdürlüğü için Telegram sabah brifingi formatı:
    LLM yönetici özeti + en kritik 3 pazaryeri/satıcı fiyat uyarısı ve Havale dip sınır analizi.
    """
    clean_report = (
        llm_report.strip()
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    sections = [
        "📱 <b>CEP-HANE TEKNOLOJİ — GÜNLÜK FİYAT VE REKABET BRİFİNGİ</b>",
        "──────────────────────────────",
        clean_report,
        "\n🚨 <b>ÖNE ÇIKAN KRİTİK PAZARYERİ &amp; SATICI UYARILARI (İLK 3)</b>",
        "──────────────────────────────",
    ]

    for idx, alert in enumerate(critical_alerts[:3], 1):
        urun = str(alert.get("urun", "Bilinmeyen Ürün")).replace("<", "&lt;").replace(">", "&gt;")
        rakip = str(alert.get("rakip", "Rakip")).replace("<", "&lt;").replace(">", "&gt;")
        bizim_fiyat = alert.get("bizim_fiyat", 0.0)
        rakip_fiyat = alert.get("rakip_fiyat", 0.0)
        dip_sinir = alert.get("havale_dip_siniri")
        oneri = str(alert.get("oneri", "Aksiyon önerisi yok")).replace("<", "&lt;").replace(">", "&gt;")
        durum = str(alert.get("durum", "")).replace("<", "&lt;").replace(">", "&gt;")

        dip_line = f" | Havale Dip: {format_tr_price(dip_sinir)} TL" if dip_sinir else ""

        sections.append(
            f"<b>{idx}. {urun}</b>\n"
            f"   • Kanal / Satıcı: <b>{rakip}</b>\n"
            f"   • Cep-Hane: {format_tr_price(bizim_fiyat)} TL | Rakip: {format_tr_price(rakip_fiyat)} TL{dip_line}\n"
            f"   • Durum: {durum}\n"
            f"   • 💡 <i>{oneri}</i>\n"
        )

    full_message = "\n".join(sections)

    if len(full_message) > MAX_TELEGRAM_MESSAGE_LENGTH:
        full_message = (
            full_message[: MAX_TELEGRAM_MESSAGE_LENGTH - 40]
            + "\n\n... [Mesaj sınırı aşıldığı için kısaltıldı]"
        )

    return full_message


def send_telegram_message(
    text: str,
    chat_id: Optional[str] = None,
    token: Optional[str] = None,
    parse_mode: str = "HTML",
) -> bool:
    """
    Bota kayıtlı tüm aktif kullanıcılara (veya belirtilen chat_id'ye) Telegram mesajı gönderir.
    """
    bot_token = token or TELEGRAM_TOKEN
    if not bot_token:
        print("❌ Hata: TELEGRAM_TOKEN .env dosyasında bulunamadı!")
        return False

    target_ids = [str(chat_id)] if chat_id else get_all_telegram_chat_ids(bot_token)
    if not target_ids:
        print("❌ Hata: TELEGRAM_CHAT_ID tespit edilemedi. Lütfen @Cep-haneFiyatTakipBot botuna /start yazın!")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    any_success = False

    for target_chat_id in target_ids:
        payload = {
            "chat_id": target_chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True,
        }
        try:
            resp = httpx.post(url, json=payload, timeout=20.0)
            if resp.status_code == 200:
                print(f"✓ Telegram bildirimi başarıyla gönderildi! (Chat ID: {target_chat_id})")
                any_success = True
            else:
                print(f"❌ Telegram gönderimi başarısız (HTTP {resp.status_code}): {resp.text}")
                if parse_mode == "HTML":
                    payload["parse_mode"] = ""
                    retry_resp = httpx.post(url, json=payload, timeout=20.0)
                    if retry_resp.status_code == 200:
                        print(f"✓ Düz metin formatında iletildi (Chat ID: {target_chat_id}).")
                        any_success = True
        except Exception as e:
            print(f"❌ Telegram bağlantı hatası ({target_chat_id}): {e}")

    return any_success
