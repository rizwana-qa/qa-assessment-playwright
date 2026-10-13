# QA Automation Assessment

Automated tests for the mock data quality app, written with Playwright (Python, sync API) and pytest.

## Requirements

- Python 3.10 or newer
- The assessment app files (`index.html`, `vf-container.html`, `app.html`) in a folder named `app`

## Setup

```
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Run

1. Serve the app. In the `app` folder run:
   ```
   python -m http.server 8080
   ```
2. In a second terminal, in this repository folder, run:
   ```
   python -m pytest -v
   ```

## Tests

1. Navigate to the Data Issues grid and assert 10 issue cards.
2. Check every original row has a non-empty sfid.
3. Select the original value on the 7th card and assert the final row updates.
4. Edit the final row for record `00Qak00000RHtuzEAD` to `123 Test Street`.
5. Checkbox selection counter: 3 selected, then 10 selected, then hidden when cleared.

Each test starts from `http://localhost:8080/index.html` and can run on its own. The app files are not modified.
