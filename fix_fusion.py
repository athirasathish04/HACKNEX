from pathlib import Path

p = Path("ai/analysis/multimodal_fusion.py")
s = p.read_text(encoding="utf-8-sig")

if "def build_multimodal_fusion" not in s:
    s += '''

def build_multimodal_fusion(video_analysis, audio_analysis):
    return fuse_audio_video(video_analysis, audio_analysis)
'''

p.write_text(s, encoding="utf-8")

print("build_multimodal_fusion compatibility wrapper added.")
