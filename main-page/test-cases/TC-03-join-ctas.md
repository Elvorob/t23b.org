# Test Cases: TC-03 — Join CTAs (Become a Boy Scout / Become a Cub Scout)

**Test Case:** TC-03 (Join CTAs)  
**Scope:** https://www.t23b.org/

---

## TC-03-01: Become a Boy Scout block is visible

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Homepage loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open `https://www.t23b.org/`. | Page loads. |
| 2 | Locate element containing text "Become a Boy Scout". | Element is present and visible. |

**Automation notes:** Contains text "Become a Boy Scout" or use aria-label/heading if available.

---

## TC-03-02: Become a Cub Scout block is visible

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Homepage loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open `https://www.t23b.org/`. | Page loads. |
| 2 | Locate element containing text "Become a Cub Scout". | Element is present and visible. |

**Automation notes:** Same approach as TC-03-01.

---

## TC-03-03: Boy Scout block shows contact name and contact method

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Homepage loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Within "Become a Boy Scout" block, locate contact name. | At least one name (e.g., "Sherman Wong") is present. |
| 2 | Within same block, locate contact method: email or phone. | At least one of: clickable email link or visible phone number (digits present). |

**Automation notes:** Email may be obfuscated; assert presence of mailto link or element with phone digits. Do not assert raw email string if masked.

---

## TC-03-04: Cub Scout block shows contact name and contact method

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Homepage loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Within "Become a Cub Scout" block, locate contact name. | At least one name is present. |
| 2 | Within same block, locate contact method: email or phone. | At least one of: email link or phone number with digits. |

**Automation notes:** Same as TC-03-03 for Cub Scout block.

---

## TC-03-05: Learn more link in Boy Scout block goes to How to Join

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Homepage loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Within "Become a Boy Scout" block, locate link with text "Learn more". | Link is present. |
| 2 | Get link `href` or click and get current URL. | URL contains "how-to-join" or equivalent path. |

**Automation notes:** `a[href*="how-to-join"]` within Boy Scout section; or click and assert final URL.

---

## TC-03-06: Learn more link in Cub Scout block goes to How to Join

| Field | Value |
|-------|--------|
| **Priority** | High |
| **Preconditions** | Homepage loads. |

**Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Within "Become a Cub Scout" block, locate link with text "Learn more". | Link is present. |
| 2 | Get link `href` or click and get current URL. | URL contains "how-to-join" or equivalent path. |

**Automation notes:** Same as TC-03-05 for Cub Scout block.
