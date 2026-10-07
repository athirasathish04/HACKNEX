from pathlib import Path

p = Path("ai/analysis/forensic_report.py")
s = p.read_text(encoding="utf-8-sig")

start = s.index("def build_forensic_report")

new_function = r'''
def build_forensic_report(file_path: str):
    from ai.analysis.engine import analyze_input

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    analysis = analyze_input(str(path))
    media_type = analysis.get("media_type")

    report = {
        "title": "TRUTHSCAN Multimodal Digital Forensics Report",
        "filename": path.name,
        "media_type": media_type,
        "decision": {},
        "why": [],
        "where": [],
        "when": None,
        "robustness": {
            "status": "not_run",
            "note": "Robustness testing can be run separately from the main analysis."
        },
        "limitations": []
    }

    if media_type == "image":
        authenticity = analysis.get("authenticity", {})

        report["decision"] = {
            "status": authenticity.get("risk_level", "inconclusive"),
            "score": authenticity.get("score"),
            "confidence": authenticity.get("confidence"),
            "interpretation": authenticity.get("interpretation")
        }

        deepfake = analysis.get("deepfake", {})
        predictions = deepfake.get("predictions", [])

        if predictions:
            fake_prediction = next(
                (
                    item for item in predictions
                    if str(item.get("label", "")).lower() in
                    ["fake", "fake_image", "deepfake"]
                ),
                None
            )

            real_prediction = next(
                (
                    item for item in predictions
                    if str(item.get("label", "")).lower() in
                    ["real", "real_image"]
                ),
                None
            )

            if fake_prediction:
                report["why"].append({
                    "signal": "AI Deepfake Detector",
                    "finding": (
                        f"Model classified the image as fake-leaning "
                        f"with score {fake_prediction.get('score')}"
                    )
                })

            if real_prediction:
                report["why"].append({
                    "signal": "AI Deepfake Detector",
                    "finding": (
                        f"Real-class score: {real_prediction.get('score')}"
                    )
                })

        ela = analysis.get("ela", {})
        if ela:
            report["why"].append({
                "signal": "Error Level Analysis",
                "finding": (
                    f"Maximum compression difference: "
                    f"{ela.get('max_difference')}"
                )
            })

        anomaly = analysis.get("anomaly", {})
        if anomaly:
            candidates = anomaly.get("candidate_regions", [])

            report["why"].append({
                "signal": "Local Anomaly Detection",
                "finding": (
                    f"{len(candidates)} candidate anomalous region(s) detected"
                )
            })

            for region in candidates[:5]:
                report["where"].append({
                    "x": region.get("x"),
                    "y": region.get("y"),
                    "width": region.get("width"),
                    "height": region.get("height"),
                    "ratio": region.get("ratio")
                })

        metadata = analysis.get("metadata", {})

        if metadata:
            report["why"].append({
                "signal": "Metadata",
                "finding": (
                    "Embedded metadata detected"
                    if metadata
                    else "No embedded metadata detected"
                )
            })
        else:
            report["why"].append({
                "signal": "Metadata",
                "finding": "No embedded metadata detected"
            })

        pixel = analysis.get("pixel", {})
        if pixel:
            report["why"].append({
                "signal": "Pixel Consistency",
                "finding": (
                    f"Mean brightness: {pixel.get('mean_brightness')}, "
                    f"standard deviation: {pixel.get('std_brightness')}"
                )
            })

        report["limitations"] = [
            "The authenticity score is an evidence-fusion score, not a calibrated probability.",
            "AI detector scores are model outputs and are not proof by themselves.",
            "ELA and anomaly detection identify forensic indicators, not definitive manipulation.",
            "Absence of metadata does not prove that an image is fake."
        ]

    elif media_type == "video":
        temporal = analysis.get("temporal_analysis", {})
        suspicious_frames = analysis.get("suspicious_frames", [])
        audio = analysis.get("audio_analysis", {})
        fusion = analysis.get("multimodal_fusion", {})

        average_score = temporal.get("average_fake_score")

        if suspicious_frames:
            status = "suspicious"
        elif average_score is not None and average_score >= 0.55:
            status = "suspicious"
        else:
            status = "inconclusive"

        report["decision"] = {
            "status": status,
            "score": average_score,
            "confidence": (
                "high" if suspicious_frames
                else "medium" if average_score is not None
                else "low"
            ),
            "interpretation": (
                "Video-level evidence shows potentially manipulated visual content."
                if status == "suspicious"
                else "Available video evidence is inconclusive."
            )
        }

        report["why"].append({
            "signal": "Temporal Visual Analysis",
            "finding": (
                f"Average fake score: {average_score}; "
                f"maximum: {temporal.get('maximum_fake_score')}; "
                f"variation: {temporal.get('variation')}"
            )
        })

        if suspicious_frames:
            report["why"].append({
                "signal": "Suspicious Frames",
                "finding": f"{len(suspicious_frames)} suspicious frame(s) detected"
            })

        report["when"] = temporal.get("strongest_timestamp")

        for frame in suspicious_frames[:10]:
            report["where"].append({
                "timestamp": frame.get("timestamp"),
                "timestamp_seconds": frame.get("timestamp_seconds"),
                "fake_score": frame.get("fake_score")
            })

        if audio:
            report["why"].append({
                "signal": "Audio Analysis",
                "finding": (
                    f"Audio status: {audio.get('status')}; "
                    f"signal present: {audio.get('signal_present')}"
                )
            })

        if fusion:
            report["why"].append({
                "signal": "Multimodal Fusion",
                "finding": fusion.get("interpretation")
            })

        report["limitations"] = [
            "Video model scores are not calibrated probabilities.",
            "Frame-level visual detection is evidence, not definitive proof.",
            "Audio analysis cannot establish lip-sync consistency without temporal speech and facial-motion analysis.",
            "Different compression levels and recording conditions can affect forensic signals."
        ]

    elif media_type == "audio":
        audio = analysis.get("audio_analysis", {})

        status = audio.get("status", "inconclusive")

        report["decision"] = {
            "status": status,
            "score": None,
            "confidence": "medium" if status == "analyzed" else "low",
            "interpretation": audio.get("interpretation")
        }

        report["why"].append({
            "signal": "Audio Signal Analysis",
            "finding": (
                f"Mean RMS: {audio.get('mean_rms')}; "
                f"silence ratio: {audio.get('silence_ratio')}; "
                f"zero-crossing rate: {audio.get('mean_zcr')}"
            )
        })

        report["limitations"] = [
            "Acoustic features are forensic indicators and do not prove voice cloning.",
            "No dedicated voice-cloning classifier is currently used in this report.",
            "Recording quality, compression and background noise can affect acoustic measurements."
        ]

    else:
        report["decision"] = {
            "status": "inconclusive",
            "score": None,
            "confidence": "low",
            "interpretation": "Unsupported media type."
        }

    return report
'''

p.write_text(s[:start] + new_function.lstrip(), encoding="utf-8")
print("Forensic report evidence expansion applied.")
