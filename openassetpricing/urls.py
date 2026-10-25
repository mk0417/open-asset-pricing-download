# Data is from Chen and Zimmermann: https://www.openassetpricing.com/

# Release used by OpenAP() when no release is given
default_release = 202610

# ==========
# All releases are on Hugging Face, one branch (revision) per release
# release<yyyymm>_hf is the branch of the dataset repo below
# ==========
hf_repo_id = 'OpenSourceAP/CrossSection'
hf_url_prefix = f'https://huggingface.co/datasets/{hf_repo_id}/resolve'
hf_api_prefix = f'https://huggingface.co/api/datasets/{hf_repo_id}'

# Version 3.00: data release - 2026.10
# (branch Test-Data-2026.10 has mixed-vintage test data, not for research use;
# reach it with OpenAP(hf_revision='Test-Data-2026.10'))
release202610_hf = 'Data-Release-2026.10'

# Version 2.00: data release - 2025.10
release202510_hf = '2025.10'

# Version 1.41: data release - 2024.10
release202410_hf = '2024.10'

# Version 1.40: data release - 2024.08
release202408_hf = '2024.08'

# Version 1.30: data release - 2023.08
release202308_hf = '2023.08'

# Data release - 2022.04
release202204_hf = '2022.04'

# Version 1.20: data release - 2022.03
release202203_hf = '2022.03'

# Data release - 2021.04
release202104_hf = '2021.04'

# Data release - 2021.03 (only op, placebo_op and firm characteristics)
release202103_hf = '2021.03'

# Releases 2020.05 and 2020.07 are on Hugging Face too, but in an older
# format this package does not read

# Older release names, kept so OpenAP(2023) and OpenAP(2022) still work
release_aliases = {2023: 202308, 2022: 202203}
