import pytest
from playwright.sync_api import sync_playwright, expect

URL = "http://localhost:8080/index.html"


@pytest.fixture
def app():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL)
        page.get_by_role("button", name="Got it").click()
        frame = page.frame_locator("#outerFrame").frame_locator("#appFrame")
        yield frame
        browser.close()


@pytest.fixture
def cards(app):
    app.locator("#solveBtn").click()
    cards = app.locator(".issue-card")
    expect(cards).to_have_count(10, timeout=10000)
    return cards


def test_navigate_to_grid(cards):
    expect(cards).to_have_count(10)


def test_original_rows_have_sfid(cards):
    for i in range(cards.count()):
        sfid = cards.nth(i).locator('tr[data-row-type="original"] td').last
        expect(sfid).not_to_be_empty()


def test_select_original_value(cards):
    card = cards.nth(6)
    original = card.locator('tr[data-row-type="original"] td.cell-issue span').inner_text()
    card.locator('input[type="radio"][value="original"]').check()
    expect(card.locator('tr[data-row-type="final"] .cell-editable')).to_have_text(original)


def test_edit_final_row(app, cards):
    card = app.locator('[data-record-id="00Qak00000RHtuzEAD"]')
    card.locator(".cell-editable").click()
    box = card.locator("input.inline-edit-input")
    box.fill("")
    box.fill("123 Test Street")
    box.press("Enter")
    expect(card.locator(".cell-editable")).to_have_text("123 Test Street")


def test_checkbox_selection_count(app, cards):
    boxes = app.locator(".issue-checkbox")
    for i in (0, 2, 4):
        boxes.nth(i).check()
    bar = app.locator("#confirmBar")
    expect(bar).to_contain_text("3 issue(s) selected")
    app.locator("#selectAll").check()
    expect(bar).to_contain_text("10 issue(s) selected")
    app.locator("#selectAll").uncheck()
    expect(bar).not_to_be_visible()
