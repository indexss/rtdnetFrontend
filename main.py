from fastapi.responses import FileResponse
from fastapi import Header
from typing import Optional
import os
from fastapi import HTTPException

@app.get("/videos/{video_name}")
async def get_video(video_name: str, range: Optional[str] = Header(None)):
    video_path = f"/root/m2changenewfastapi/api/videos/{video_name}"
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="视频文件不存在")
    
    return FileResponse(
        path=video_path,
        media_type="video/mp4",  # 设置正确的 MIME 类型
        filename=video_name,  # 设置下载时的文件名
        headers={
            "Accept-Ranges": "bytes",
            "Content-Disposition": f"inline; filename={video_name}"
        }
    ) 