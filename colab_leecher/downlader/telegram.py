# copyright 2023 © Xron Trix | https://github.com/Xrontrix10


import logging
from datetime import datetime
from os import path as ospath
from colab_leecher import colab_bot
from colab_leecher.utility.handler import cancelTask
from colab_leecher.utility.variables import Transfer, Paths, Messages, BotTimes
from colab_leecher.utility.helper import speedETA, getTime, sizeUnit, status_bar


async def media_Identifier(link):
    """
    解析Telegram链接并获取消息
    支持格式:
    1. 公开频道: https://t.me/channel_username/message_id
    2. 私有频道: https://t.me/c/channel_id/message_id
    """
    try:
        parts = link.split("/")
        
        # 验证基本链接格式
        if len(parts) < 5 or parts[2] != "t.me":
            raise ValueError(f"无效的Telegram链接格式: {link}")
        
        # 判断链接类型并解析
        if parts[3] == "c":  # 私有频道格式: t.me/c/channel_id/message_id
            if len(parts) < 6:
                raise ValueError(f"私有频道链接格式错误: {link}")
            
            channel_id = "-100" + parts[4]  # 私有频道需要添加-100前缀
            message_id = int(parts[5])
            logging.info(f"解析私有频道 - 频道ID: {channel_id}, 消息ID: {message_id}")
            
        else:  # 公开频道格式: t.me/channel_username/message_id
            channel_username = parts[3]  # 频道用户名
            message_id = int(parts[4])   # 消息ID
            channel_id = channel_username  # 公开频道直接使用用户名
            logging.info(f"解析公开频道 - 频道: @{channel_username}, 消息ID: {message_id}")
        
        # 获取消息
        logging.info(f"正在获取消息: {channel_id}/{message_id}")
        message = await colab_bot.get_messages(channel_id, message_id)
        
        # 检查消息是否成功获取
        if message is None:
            error_msg = f"无法获取消息 - 频道: {channel_id}, 消息ID: {message_id}"
            logging.error(error_msg)
            await cancelTask(error_msg)
            return None, None
        
        # 提取媒体对象
        media = (
            message.document
            or message.photo
            or message.video
            or message.audio
            or message.voice
            or message.video_note
            or message.sticker
            or message.animation
            or None
        )
        
        if media is None:
            error_msg = f"消息中没有可下载的媒体文件 - 频道: {channel_id}, 消息ID: {message_id}"
            logging.error(error_msg)
            await cancelTask(error_msg)
            return None, None
        
        # 记录成功信息
        media_type = type(media).__name__
        file_size = getattr(media, 'file_size', 0)
        logging.info(f"成功获取媒体 - 类型: {media_type}, 大小: {file_size} bytes")
        
        return media, message
        
    except ValueError as e:
        logging.error(f"链接格式错误: {e}")
        await cancelTask(str(e))
        return None, None
        
    except Exception as e:
        # 提供更详细的错误信息
        if "CHAT_ID_INVALID" in str(e):
            error_msg = f"无法访问频道。可能原因:\n1. 频道不存在或已被删除\n2. 机器人未加入该频道\n3. 频道为私有且无访问权限\n链接: {link}"
        elif "MESSAGE_ID_INVALID" in str(e):
            error_msg = f"消息ID无效或消息已被删除 - 消息ID: {message_id}\n链接: {link}"
        elif "CHANNEL_INVALID" in str(e):
            error_msg = f"频道无效 - {channel_id}\n链接: {link}"
        else:
            error_msg = f"获取消息失败: {e}\n链接: {link}"
        
        logging.error(error_msg)
        await cancelTask(error_msg)
        return None, None


async def download_progress(current, total):
    speed_string, eta, percentage = speedETA(start_time, current, total)

    await status_bar(
        down_msg=Messages.status_head,
        speed=speed_string,
        percentage=percentage,
        eta=getTime(eta),
        done=sizeUnit(sum(Transfer.down_bytes) + current),
        left=sizeUnit(Transfer.total_down_size),
        engine="Pyrogram 💥",
    )


async def TelegramDownload(link, num):
    global start_time
    
    # 获取媒体信息
    media, message = await media_Identifier(link)
    
    # 检查是否成功获取到媒体和消息
    if media is None or message is None:
        logging.error(f"无法下载Telegram消息: {link}")
        return  # 已在media_Identifier中处理了错误，直接返回
    
    # 获取文件名
    if hasattr(media, "file_name") and media.file_name:
        name = media.file_name
    else:
        # 为没有文件名的媒体生成默认名称
        media_type = type(media).__name__.lower()
        file_ext = {
            'photo': '.jpg',
            'video': '.mp4', 
            'audio': '.mp3',
            'voice': '.ogg',
            'animation': '.gif',
            'sticker': '.webp',
            'document': ''
        }.get(media_type, '')
        name = f"telegram_media_{num}{file_ext}"
    
    Messages.status_head = f"<b>📥 DOWNLOADING FROM » </b><i>🔗Link {str(num).zfill(2)}</i>\n\n<code>{name}</code>\n"
    start_time = datetime.now()
    file_path = ospath.join(Paths.down_path, name)
    
    try:
        # 下载文件
        logging.info(f"开始下载文件: {name} ({getattr(media, 'file_size', 0)} bytes)")
        await message.download(
            progress=download_progress, 
            in_memory=False, 
            file_name=file_path
        )
        Transfer.down_bytes.append(getattr(media, 'file_size', 0))
        logging.info(f"文件下载完成: {file_path}")
        
    except Exception as e:
        error_msg = f"下载文件失败: {e}\n文件: {name}"
        logging.error(error_msg)
        await cancelTask(error_msg)
