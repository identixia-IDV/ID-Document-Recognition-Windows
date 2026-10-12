<div align="center">
<img alt="Identixia" src="https://raw.githubusercontent.com/identixia-IDV/identixia-assets/main/brand/logo.png" width="320"/>

<a href="https://identixia.com"><img src="https://img.shields.io/badge/Website-0F766E?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Website" /></a>
<a href="https://docs.identixia.com"><img src="https://img.shields.io/badge/Docs-0F766E?style=for-the-badge&logo=gitbook&logoColor=white" alt="Docs" /></a>
<a href="https://huggingface.co/Identixia"><img src="https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" alt="Hugging Face" /></a>
<a href="https://hub.docker.com/u/identixia"><img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Hub" /></a>
<a href="https://playground.identixia.com/"><img src="https://img.shields.io/badge/Playground-0F766E?style=for-the-badge&logo=cloudplayground&logoColor=white" alt="Playground" /></a>
</div>

<div align="center">

# <img src="https://cdn.simpleicons.org/windows/0078D4" width="32" height="32" alt="" /> ID Document Recognition SDK for Windows — HTTP API Demo | Identixia

</div>

Integrate **ID document recognition and OCR** with the **Identixia Windows SDK**. This repository provides a self-hosted Windows HTTP API for reading passports, national ID cards, and driver licenses. Extract identity fields using optical character recognition (OCR), read the machine-readable zone (MRZ), and decode supported document barcodes. This recognition-only sample does not include document liveness checks.

Use the sample to build document capture and data extraction into customer onboarding, Know Your Customer (KYC), and electronic KYC (eKYC) workflows. Processing runs on your own server; images are not sent to the Identixia cloud.

> For setup, integration, and API guides, see the [ID Document Recognition SDK documentation for Windows](https://docs.identixia.com). This page covers the sample repository.

## <img src="https://api.iconify.design/lucide/clipboard-list.svg?color=%230F766E" width="24" height="24" alt="" /> SDK overview

Start the server and request its machine code using `GET /api/machinecode`. Send that code to [contact@identixia.com](mailto:contact@identixia.com) to request a license for this machine. Apply the returned key using the activation instructions below.

| Topic | Basic information |
| --- | --- |
| **Product** | On-premise **document recognition** for Windows |
| **Runtime** | Download the runtime zip from [Releases](https://github.com/identixia-IDV/ID-Document-Recognition-Windows/releases/latest) |
| **Privacy** | Document images stay on your host — no Identixia cloud |

---

## <img src="https://api.iconify.design/lucide/package.svg?color=%230F766E" width="24" height="24" alt="" /> SDK installation

Download [`documentrecognition-liveness-windows.zip`](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows/releases/latest) from the [ID-Document-Recognition-Liveness-Detection-Windows Releases](https://github.com/identixia-IDV/ID-Document-Recognition-Liveness-Detection-Windows/releases/latest). Unzip it into `lib/cpu/`. The files should sit in that folder, not inside an extra directory.

Unzip **directly** into `lib\cpu\`.

---

## <img src="https://api.iconify.design/lucide/terminal.svg?color=%230F766E" width="24" height="24" alt="" /> Quick start

### <img src="https://img.shields.io/badge/-1-0F766E?style=for-the-badge" alt="" /> Run the server

```bash
git clone https://github.com/identixia-IDV/ID-Document-Recognition-Windows.git
cd ID-Document-Recognition-Windows
pip install -r requirements.txt
python run_server.py
```

Copy `.env.example` to `.env` and edit the settings for your installation: `PORT`, `LICENSE`, `API_BASE`, and `DEMO_PORT`. Environment variables already set in the shell take precedence over values in `.env`.

### <img src="https://img.shields.io/badge/-2-0F766E?style=for-the-badge" alt="" /> Get a license

```bash
curl -s http://127.0.0.1:14101/api/machinecode
```

The JSON response contains your machine code in `data.machinecode`. This value identifies the machine for licensing.

Email the machine code and the product you want to use to [contact@identixia.com](mailto:contact@identixia.com) to request a license key.

### <img src="https://img.shields.io/badge/-3-0F766E?style=for-the-badge" alt="" /> Activate / license

Replace `YOUR_KEY` in the request below with the license key issued for this machine. The activation endpoint saves the key to the server’s `.env` file and attempts to initialize the SDK. For a local installation, you can also set `LICENSE=YOUR_KEY` in the repository’s `.env` file and restart the server.

```bash
curl -s -X POST http://127.0.0.1:14101/api/activate -H "Content-Type: application/json" -d "{\"license\":\"YOUR_KEY\"}"
```

### <img src="https://img.shields.io/badge/-4-0F766E?style=for-the-badge" alt="" /> Check that it is running

```bash
curl -s http://127.0.0.1:14101/api/health
```

### <img src="https://img.shields.io/badge/-5-0F766E?style=for-the-badge" alt="" /> Try the API

Process a document through the recognize / process endpoints after activation. See [docs](https://docs.identixia.com).

---

## <img src="https://api.iconify.design/lucide/list-checks.svg?color=%230F766E" width="24" height="24" alt="" /> Features

| Capability | What it does |
| --- | --- |
| **OCR / MRZ / barcode** | Read identity fields from ID documents |
| **HTTP API** | Local on-premise service |

---

## <img src="https://api.iconify.design/lucide/pc-case.svg?color=%230F766E" width="24" height="24" alt="" /> System requirements

| | |
| --- | --- |
| API port | **14101** |
| Gradio demo port | **14201** |
| Runtime download | [Releases](https://github.com/identixia-IDV/ID-Document-Recognition-Windows/releases/latest) |

---

## <img src="https://api.iconify.design/lucide/app-window.svg?color=%230F766E" width="24" height="24" alt="" /> Gradio demo

Keep the API running, then open a second terminal in the repository folder.

```bash
pip install -r requirements-demo.txt
python run_demo.py
```

Open http://127.0.0.1:14201

## <img src="https://api.iconify.design/lucide/braces.svg?color=%230F766E" width="24" height="24" alt="" /> API

HTTP API on port **14106**. For image-processing requests, encode the JPEG image as base64 and include it in the JSON request body.

| Call | Route |
| --- | --- |
| Health | `GET /api/health` |
| Machine code | `GET /api/machinecode` |
| Activate | `POST /api/activate` with a JSON body containing your license key: `{"license":"YOUR_KEY"}` |
| Process | `POST /api/document/process` |

Returns identity, fields, and images. Document liveness is not in this build.

```bash
curl -s http://127.0.0.1:14106/api/health
```

---

## <img src="https://api.iconify.design/lucide/layers.svg?color=%230F766E" width="24" height="24" alt="" /> SDKs for other platforms

| | Platform | Repo |
| --- | --- | --- |
| <img src="https://cdn.simpleicons.org/android/3DDC84" width="18" height="18" alt="" /> | Android | [ID-Document-Recognition-Android](https://github.com/identixia-IDV/ID-Document-Recognition-Android) |
| <img src="https://cdn.simpleicons.org/apple/000000" width="18" height="18" alt="" /> | iOS | [ID-Document-Recognition-iOS](https://github.com/identixia-IDV/ID-Document-Recognition-iOS) |
| <img src="https://cdn.simpleicons.org/flutter/02569B" width="18" height="18" alt="" /> | Flutter | [ID-Document-Recognition-Flutter](https://github.com/identixia-IDV/ID-Document-Recognition-Flutter) |
| <img src="https://cdn.simpleicons.org/react/61DAFB" width="18" height="18" alt="" /> | React Native | [ID-Document-Recognition-React-Native](https://github.com/identixia-IDV/ID-Document-Recognition-React-Native) |
| <img src="https://cdn.simpleicons.org/ionic/3880FF" width="18" height="18" alt="" /> | Ionic Capacitor | [ID-Document-Recognition-Ionic-Capacitor](https://github.com/identixia-IDV/ID-Document-Recognition-Ionic-Capacitor) |
| <img src="https://cdn.simpleicons.org/apachecordova/E8E8E8" width="18" height="18" alt="" /> | Ionic Cordova | [ID-Document-Recognition-Ionic-Cordova](https://github.com/identixia-IDV/ID-Document-Recognition-Ionic-Cordova) |
| <img src="https://cdn.simpleicons.org/windows/0078D4" width="18" height="18" alt="" /> | Windows ← this repo | [ID-Document-Recognition-Windows](https://github.com/identixia-IDV/ID-Document-Recognition-Windows) |
| <img src="https://cdn.simpleicons.org/docker/2496ED" width="18" height="18" alt="" /> | Linux / Docker | [ID-Document-Recognition-Docker](https://github.com/identixia-IDV/ID-Document-Recognition-Docker) |

---

## <img src="https://api.iconify.design/lucide/mail.svg?color=%230F766E" width="24" height="24" alt="" /> Contact

<div align="center">

<a href="mailto:contact@identixia.com"><img alt="Email contact@identixia.com" src="https://img.shields.io/badge/Email-contact%40identixia.com-0F766E?style=for-the-badge&logo=gmail&logoColor=white" /></a>
<a href="https://wa.me/17018854218"><img alt="WhatsApp +1 (701) 885-4218" src="https://img.shields.io/badge/WhatsApp-%2B1_(701)_885--4218-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" /></a>
<a href="https://t.me/identixia"><img alt="Telegram @identixia" src="https://img.shields.io/badge/Telegram-%40identixia-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" /></a>

</div>

---
