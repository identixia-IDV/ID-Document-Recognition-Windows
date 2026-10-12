"""Document recognition Python kit — ctypes bindings to DocumentRecognitionSDK.dll (lib/cpu/).

Role: thin native API for integrators. ``python server`` calls this package. For a UI, run ``python demo`` (it talks to the server over HTTP).
"""

from __future__ import annotations

import base64
import ctypes
import io
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "lib" / "cpu"
DLL = LIB / "DocumentRecognitionSDK.dll"

os.chdir(ROOT)
os.environ["PATH"] = str(LIB) + os.pathsep + os.environ.get("PATH", "")
if hasattr(os, "add_dll_directory"):
    os.add_dll_directory(str(LIB))

_dll = ctypes.WinDLL(str(DLL))

_dll.DocumentRecognitionSDK_initialize.restype = ctypes.c_int
_dll.DocumentRecognitionSDK_initialize.argtypes = []
_dll.DocumentRecognitionSDK_activate.restype = ctypes.c_int
_dll.DocumentRecognitionSDK_activate.argtypes = [ctypes.c_char_p]
_dll.DocumentRecognitionSDK_getMachineCode.restype = ctypes.c_int
_dll.DocumentRecognitionSDK_getMachineCode.argtypes = [ctypes.c_char_p]
_dll.DocumentRecognitionSDK_documentProcess.restype = ctypes.c_int
_dll.DocumentRecognitionSDK_documentProcess.argtypes = [
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_char_p,
]
_dll.DocumentRecognitionSDK_generalProcess.restype = ctypes.c_int
_dll.DocumentRecognitionSDK_generalProcess.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]


def _opt_sym(name, restype, argtypes):
    fn = getattr(_dll, name, None)
    if fn is None:
        return None
    fn.restype = restype
    fn.argtypes = argtypes
    return fn


_start_new_session = _opt_sym(
    "DocumentRecognitionSDK_startNewSession", ctypes.c_int, [ctypes.c_char_p, ctypes.c_char_p]
)
_start_new_page = _opt_sym(
    "DocumentRecognitionSDK_startNewPage", ctypes.c_int, [ctypes.c_char_p, ctypes.c_char_p]
)
_unload = _opt_sym("DocumentRecognitionSDK_unload", ctypes.c_int, [ctypes.c_char_p])
_get_license_status = _opt_sym(
    "DocumentRecognitionSDK_getLicenseStatus", ctypes.c_int, [ctypes.c_char_p]
)

_MC_BUF = 768
_STATUS_BUF = 512
_OUT_MIN = 1_000_000
_OUT_MAX = 16 * 1024 * 1024
_MAX_IMG = 8 * 1024 * 1024


def _b(v) -> bytes:
    if v is None:
        return b""
    if isinstance(v, bytes):
        return v
    return str(v).encode("utf-8")


def _out(*parts: bytes):
    n = min(max(_OUT_MIN, sum(len(p) for p in parts) * 2 + 262144), _OUT_MAX)
    return ctypes.create_string_buffer(n)


def _fit_b64(image_b64: str, max_bytes: int = _MAX_IMG) -> bytes:
    """JPEG for the engine. PDFs stay as-is. Other image types are converted."""
    raw = _b(image_b64).strip()
    data = base64.b64decode(raw, validate=False)
    if data[:4] == b"%PDF":
        return raw
    if data[:3] == b"\xff\xd8\xff" and len(raw) <= max_bytes:
        return raw
    if (data[:8] == b"\x89PNG\r\n\x1a\n" or data[:2] == b"BM") and len(raw) <= max_bytes:
        return raw
    try:
        from PIL import Image

        img = Image.open(io.BytesIO(data))
        img.load()
        if getattr(img, "n_frames", 1) > 1:
            img.seek(0)
        img = img.convert("RGB")
    except Exception:
        return raw
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue())


def get_machine_code() -> str:
    buf = ctypes.create_string_buffer(_MC_BUF)
    _dll.DocumentRecognitionSDK_getMachineCode(buf)
    return buf.value.decode("utf-8", errors="replace")


def get_license_status() -> dict:
    """Return license capability dict from DocumentRecognitionSDK_getLicenseStatus."""
    fallback = {
        "licensed": False,
        "level": -1,
        "levelName": "None",
        "recognition": False,
        "authenticity": False,
        "label": "No license",
    }
    if _get_license_status is None:
        return fallback
    buf = ctypes.create_string_buffer(_STATUS_BUF)
    if int(_get_license_status(buf)) != 0:
        return fallback
    try:
        data = json.loads(buf.value.decode("utf-8", errors="replace") or "{}")
        return data if isinstance(data, dict) else fallback
    except Exception:  # noqa: BLE001
        return fallback


def activate(license_path: str) -> int:
    return int(_dll.DocumentRecognitionSDK_activate(_b(license_path)))


def init_sdk() -> int:
    return int(_dll.DocumentRecognitionSDK_initialize())


def start_new_session(options: dict | None = None) -> str:
    if _start_new_session is None:
        return '{"msg":"DocumentRecognitionSDK_startNewSession not in this DocumentRecognitionSDK.dll"}'
    opts = options or {"scenario": "FullProcess", "series": False}
    options_b = _b(json.dumps(opts, separators=(",", ":")))
    out = _out(options_b)
    _start_new_session(options_b, out)
    return out.value.decode("utf-8", errors="replace")


def start_new_page(options: dict | None = None) -> str:
    if _start_new_page is None:
        return '{"msg":"DocumentRecognitionSDK_startNewPage not in this DocumentRecognitionSDK.dll"}'
    opts = options or {}
    options_b = _b(json.dumps(opts, separators=(",", ":")))
    out = _out(options_b)
    _start_new_page(options_b, out)
    return out.value.decode("utf-8", errors="replace")


def unload() -> str:
    if _unload is None:
        return '{"msg":"DocumentRecognitionSDK_unload not in this DocumentRecognitionSDK.dll"}'
    out = _out()
    _unload(out)
    return out.value.decode("utf-8", errors="replace")


def document_process(images, rfid: str = "", options: dict | None = None) -> str:
    opts = dict(options or {
        "response": {
            "OCR": "normal",
            "MRZ": "normal",
            "Barcode": "normal",
            "ImageQuality": "normal",
            "Authenticity": "normal",
        }
    })
    items = list(images or [])
    multipage = len(items) >= 2
    if multipage and "multipageProcessing" not in opts:
        opts["multipageProcessing"] = True
    norm = []
    for i, item in enumerate(items):
        if isinstance(item, dict):
            entry = {"image": _fit_b64(item["image"]).decode()}
            if item.get("page_idx") is not None:
                entry["page_idx"] = int(item["page_idx"])
            elif multipage:
                entry["page_idx"] = i
            norm.append(entry)
        else:
            if multipage:
                norm.append({"image": _fit_b64(item).decode(), "page_idx": i})
            else:
                norm.append(_fit_b64(item).decode())
    images_json = _b(json.dumps(norm, separators=(",", ":")))
    options_b = _b(json.dumps(opts, separators=(",", ":")))
    rfid_b = _b(rfid or "")
    out = _out(images_json, rfid_b, options_b)
    _dll.DocumentRecognitionSDK_documentProcess(images_json, rfid_b, options_b, out)
    return out.value.decode("utf-8", errors="replace")


def general_process(image: str, options: dict | None = None) -> str:
    opts = options or {}
    image_b = _fit_b64(image)
    options_b = _b(json.dumps(opts, separators=(",", ":")))
    out = _out(image_b, options_b)
    _dll.DocumentRecognitionSDK_generalProcess(image_b, options_b, out)
    return out.value.decode("utf-8", errors="replace")


_RECOGNITION_RESPONSE = {
    "OCR": "normal",
    "MRZ": "normal",
    "Barcode": "normal",
    "ImageQuality": "normal",
    "Authenticity": "none",
    "RFID": "none",
}

_LIVENESS_RESPONSE = {
    "OCR": "none",
    "MRZ": "none",
    "Barcode": "none",
    "ImageQuality": "none",
    "Authenticity": "normal",
    "RFID": "none",
}


def _forced_process_options(response: dict, extra: dict | None) -> dict:
    opts = dict(extra or {})
    opts.pop("response", None)
    opts["response"] = dict(response)
    return opts


def document_recognition(images, rfid: str = "", extra: dict | None = None) -> str:
    """OCR / MRZ / barcode / image quality only. Authenticity is always off."""
    return document_process(
        images, rfid, _forced_process_options(_RECOGNITION_RESPONSE, extra)
    )


def document_liveness(images, rfid: str = "", extra: dict | None = None) -> str:
    """Authenticity / security only. OCR / MRZ / barcode / image quality are always off."""
    return document_process(
        images, rfid, _forced_process_options(_LIVENESS_RESPONSE, extra)
    )
