
# StratAI Portal - Google Translate API Setup

This app supports Google Cloud Translate via `google-cloud-translate`.

## Setup

1. Create a project at https://console.cloud.google.com
2. Enable the "Cloud Translation API"
3. Create a Service Account Key (JSON)
4. Store the key locally and define:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="your-key-file.json"
```

5. Install:

```bash
pip install google-cloud-translate
```

Then deploy the app as usual.
