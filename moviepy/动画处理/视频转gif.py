#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/13 20:47
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : 视频转gif.py
# @version : Python 2.7.6
#import imageio
#imageio.plugins.ffmpeg.download()
import moviepy.editor as mpy

#视频文件的本地路径
content = mpy.VideoFileClip("11.mp4")
# 剪辑78分55秒到79分6秒的片段。注意：不使用resize则不会修改清晰度
c1 = content.subclip((0,1),(0,5))
# 将片段保存为gif图到python的默认路径，可保存到"C:\Users\Administrator\Desktop"
c1.write_gif("gav.gif", fps=10)
