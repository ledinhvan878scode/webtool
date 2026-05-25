import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import datetime

HISTORY_FILE = "inputs_history.txt"


# 记录输入
def log_input(user_id: int, text: str):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] User {user_id}: {text}\n")


# 执行系统命令
def run_cmd(cmd: list):
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=8)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error: {e}"


# /ping 命令
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = " ".join(context.args)
    log_input(update.effective_user.id, f"/ping {user_input}")

    if not user_input:
        await update.message.reply_text("用法: /ping <host>")
        return

    output = run_cmd(["ping", "-c", "4", user_input])
    await update.message.reply_text(f"Ping 结果:\n{output}")


# /dig 命令
async def dig(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = " ".join(context.args)
    log_input(update.effective_user.id, f"/dig {user_input}")

    if not user_input:
        await update.message.reply_text("用法: /dig <domain>")
        return

    output = run_cmd(["dig", user_input])
    await update.message.reply_text(f"Dig 结果:\n{output}")


# /host 命令
async def host(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = " ".join(context.args)
    log_input(update.effective_user.id, f"/host {user_input}")

    if not user_input:
        await update.message.reply_text("用法: /host <domain>")
        return

    output = run_cmd(["host", user_input])
    await update.message.reply_text(f"Host 查询结果:\n{output}")

# /whois 命令
async def whois(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = " ".join(context.args)
    log_input(update.effective_user.id, f"/whois {user_input}")

    if not user_input:
        await update.message.reply_text("用法: /whois <domain>")
        return

    output = run_cmd(["whois", user_input])

    # Telegram 单条消息有长度限制
    if len(output) > 4000:
        output = output[:4000] + "\n\n[输出过长，已截断]"

    await update.message.reply_text(f"Whois 查询结果:\n{output}")

async def traceroute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = " ".join(context.args)
    log_input(update.effective_user.id, f"/traceroute {user_input}")

    if not user_input:
        await update.message.reply_text("用法: /traceroute <host>")
        return

    output = run_cmd(["traceroute", user_input])
    await update.message.reply_text(f"Traceroute 结果:\n{output}")

async def nslookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = " ".join(context.args)
    log_input(update.effective_user.id, f"/nslookup {user_input}")

    if not user_input:
        await update.message.reply_text("用法: /nslookup <domain>")
        return

    output = run_cmd(["nslookup", user_input])
    await update.message.reply_text(f"Nslookup 结果:\n{output}")

# 普通消息处理
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    log_input(update.effective_user.id, text)
    await update.message.reply_text(f"你发送了: {text}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_input(update.effective_user.id, "/start")
    await update.message.reply_text("欢迎使用网络工具 Bot！可用命令:\n/ping\n/dig\n/host traceroute nslookup 其他的暂时没有更新 因为是免费公益所以 ")


def main():
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("dig", dig))
    app.add_handler(CommandHandler("host", host))
    app.add_handler(CommandHandler("traceroute", traceroute))
    app.add_handler(CommandHandler("nslookup", nslookup))
    app.add_handler(CommandHandler("whois", whois))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling()


if __name__ == "__main__":
    main()
