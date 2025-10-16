A small Tkinter GUI that simulates a CRM sending an RSign e-signature envelope, then fetches envelope status and signer-entered form data back from the RSign API. It authenticates against RSign, sends from a template/rule with prefilled “CRM_” fields, polls status, and downloads Base64-encoded XML to display parsed values in a read-only window.

# What it does

* Presents a desktop UI with fields for name, email, CRM customer number, contract number, and a free text. Default values are generated for quick demos. 
* Sends an envelope via RSign using a predefined template/rule with control updates. Returns the EnvelopeID and logs progress. 
* Fetches and displays envelope status messages. 
* Downloads signer data as Base64 XML, extracts selected control labels, and shows them in a monospaced, read-only window with timestamps.
  **Takeaway:** It is a complete send-status-collect loop for RSign, wrapped in a simple GUI.

# How it works (flow)

1. User enters data → clicks “Send the contract…”. The app validates inputs, logs them, then calls RSign in a background thread to avoid freezing the UI. EnvelopeID is captured from the API response. 
2. “Seek envelope status…” queries RSign and appends a timestamped status line to the log window.
3. “Import user data…” fetches Base64 XML for that EnvelopeID, parses selected form controls, and renders them in a separate window.
   **Takeaway:** Three buttons map to send, check, and collect.

# Main components

* `main_app.py`: starts Tkinter, instantiates the UI and the log window. 
* `UI_components.py`: the GUI, default values, and button handlers that call event functions. 
* `event_handling.py`: validates input, spawns a worker thread to send the envelope, fetches status, and retrieves user data. 
* `RSignOperations.py`: all RSign API calls, file/Base64 handling, XML parsing, and helper functions. 
* `GettingRSignAuthToken.py`: retrieves and caches AuthToken to `MyAuthToken.txt`. 
* `window_logging.py`: scrolling log window with colored tags and timestamps. 
* `collecting_user_info.py`: read-only viewer window for parsed signer data with timestamps and counters. 
* `InputValidation.py`: simple validators for email, name, number. 
* `file_logging.py`: appends timestamped lines to `operation_log.txt`. 
* `myTestCompany.py`: demo credentials and reference key (staging). **Do not commit real secrets.** 
  **Takeaway:** UI + handlers + API layer + viewers + logging.

# Setup

* Python 3.10+ recommended.
* `pip install requests` (Tkinter ships with most Python builds).
* Place a `Logo.png` next to the scripts for the GUI header. 
* Add a DOCX named `DloadXMLb64.docx` in the working folder if you want the app to auto-create and cache `DloadXMLb64.b64`. 
* Configure RSign sandbox credentials in `myTestCompany.py`. **Use env vars in production.** 
  **Takeaway:** Minimal deps; one logo and one template file are optional but useful.

# Run

```bash
python main_app.py
```

* Press Enter as a shortcut for “Send the contract…”. 
  **Takeaway:** Single entry point.

# Demo steps

* 1. Click **Send the contract…** → watch the log window show “sending” then “envelope sent”, and capture the `EnvelopeID`.
* 2. Click **Seek envelope status…** to append the latest RSign status line. 
* 3. Click **Import user data…** after signing to view parsed control values in the “Collected Information” window.
     **Takeaway:** Three sequential clicks cover the lifecycle.

# RSign endpoints used

* Auth: `POST /api/V1/Authentication/AuthenticateIUser` (token cached to file). 
* Send from rule/template and dynamic envelopes with `TemplateCode`, role mappings, and `UpdateControls`. 
* Status and info: `GetEnvelopeStatus`, `GetEnvelopeStatusInfo`. 
* Data download: `GetDownloadeDataByCode/{EnvelopeID}` (Base64 XML). 
  **Takeaway:** Token → send → status → data.

# Logging and threading

* UI remains responsive; sending runs in a worker thread and communicates back via a `queue.Queue`. 
* Human-readable log window plus file log entries in `operation_log.txt`.
  **Takeaway:** Non-blocking UX with persistent logs.

# Configuration knobs (examples)

* `TemplateCode`, `RoleID`s, subject lines, and control mappings are hardcoded for the demo. Adapt to your template. 
* The list of control labels to extract from XML is set in `event_handling.fetch_user_data()`. 
  **Takeaway:** Change codes and control IDs to match your RSign setup.

# Trade-offs

* Simplicity over abstraction: direct calls keep the demo clear but concentrate config in code. 
* File-based token cache is easy but weaker than OS secrets or env vars. 
* Tkinter is portable but basic; no async/await UI integration. 
  **Takeaway:** Good for demos and labs, not turnkey production.

# Failure modes and caveats

* **Validation bug:** `validate_number` returns `len(number) is not None`, which is always `True` for any string. You’re wrong because the intention was “is numeric” or “length > 0”. Fix: `return number.isdigit() and len(number) > 0`. 
* **Hardcoded secrets:** `myTestCompany.py` contains credentials. Replace with environment variables and never commit real keys. 
* **Template/IDs mismatch:** Wrong `TemplateCode`, `RoleID`, or `ControlID` will cause send/update failures or missing data. 
* **Missing DOCX/B64:** If `DloadXMLb64.docx` is absent, no document is attached for the rule-based send. 
* **No EnvelopeID:** Status/data calls log a guidance line and return early. 
  **Takeaway:** Fix number validation, secure secrets, and align template metadata.

# Extending

* Swap Tkinter for a web UI.
* Move config to `.env` and add structured logging.
* Add retries and explicit error messages per HTTP status. 
  **Takeaway:** The API layer already isolates most functionality.

# File tree (selected)

```
main_app.py
UI_components.py
event_handling.py
RSignOperations.py
GettingRSignAuthToken.py
collecting_user_info.py
window_logging.py
InputValidation.py
file_logging.py
myTestCompany.py
```

**Takeaway:** Each module has a single, clear role.
