# Data is from Chen and Zimmermann: https://www.openassetpricing.com/

# Release used by OpenAP() when no release is given
default_release = 202510

# ==========
# Hugging Face releases (2026.10 and later)
# release<yyyymm>_hf is the branch (revision) of the dataset repo below
# ==========
hf_repo_id = 'OpenSourceAP/CrossSection'
hf_url_prefix = f'https://huggingface.co/datasets/{hf_repo_id}/resolve'

# Version 3.00 test release: mixed-vintage data, not for research use.
# When the real release ships, point this at its branch.
release202610_hf = 'Test-Data-2026.10'

# ==========
# Google Drive releases (2025.10 and earlier)
# ==========

# Version 2.00: data release - 2025.10
release202510_url = (
    'https://drive.google.com/drive/folders/1qQDuTsnyvWfEJR6nPBQZ8xxlq6bkLG_y')

# Version 1.41: data release - 2024.10
release202410_url = (
    'https://drive.google.com/drive/folders/1SSoHGbwgyhRwUCzLE0YWvUlS0DjLCd4k')

# Version 1.40: data release - 2024.08
release202408_url = (
    'https://drive.google.com/drive/folders/1-PqsR-tOjv3-U9DRHw85X-VznYlu-Sfc')

# Version 1.30: data release - 2023.08
release2023_url = (
    'https://drive.google.com/drive/folders/1EP6oEabyZRamveGNyzYU0u6qJ-N43Qfq')

# Version 1.20: data release - 2022.03
release2022_url = (
    'https://drive.google.com/drive/folders/1O18scg9iBTiBaDiQFhoGxdn4FdsbMqGo')
