# Contributing to OpenStockAPI

Thank you for your interest in contributing to OpenStockAPI! We welcome contributions from the community to make this financial data plane better for everyone.

By contributing to this project, you agree to abide by our Code of Conduct and to sign our Contributor License Agreement (CLA) before your pull request can be merged.

---

## 1. Contributor License Agreement (CLA)

To protect the project, its users, and you as a contributor, we require all contributors to accept our **Contributor License Agreement (CLA)**. 

### Why is this required?
OpenStockAPI uses a dual-licensing model (AGPL-3.0 and Commercial). The CLA transfers or grants necessary copyright rights to the project owners, allowing us to:
*   Defend the open-source version of the project under AGPL-3.0.
*   Provide commercial licensing options to enterprise partners who cannot use copyleft licenses.

### How to sign?
We use an automated **CLA Assistant** bot. Once you open a Pull Request, the bot will automatically check if you have signed the CLA. If not, it will post a link in the PR comments for you to sign electronically in a single click using your GitHub account.

You can read the full terms of the agreement in [CLA.md](CLA.md).

---

## 2. How to Contribute

### Step 1: Find or Create an Issue
*   Check the [Issue Tracker](https://github.com/yourusername/openstockapi/issues) for existing bugs, feature requests, or improvements.
*   If you want to add a new provider or suggest a change that doesn't have an issue yet, please open a new issue first to discuss it with the maintainers.

### Step 2: Set Up Your Development Environment
1.  **Fork** the repository on GitHub.
2.  **Clone** your fork locally:
    ```bash
    git clone https://github.com/yourusername/openstockapi.git
    cd openstockapi
    ```
3.  Install dependencies including development tools:
    ```bash
    pip install -e .[dev,pandas]
    ```

### Step 3: Make Your Changes
1.  Create a feature branch:
    ```bash
    git checkout -b feature/your-feature-name
    ```
2.  Implement your changes. Ensure you adhere to the project's code style (Python 3.10+, typing hints, clear docstrings).
3.  Keep existing comments and docstrings intact.

### Step 4: Test Your Changes
Before submitting your changes, run unit tests to verify that nothing is broken:
```bash
pytest
```


### Step 5: Submit a Pull Request
1.  Push your feature branch to your fork:
    ```bash
    git push origin feature/your-feature-name
    ```
2.  Open a Pull Request (PR) from your fork's feature branch to the `main` branch of the official OpenStockAPI repository.
3.  Provide a clear description of the changes and link any related issues.
4.  Complete the electronic CLA signature via the automated comment link in your PR.
