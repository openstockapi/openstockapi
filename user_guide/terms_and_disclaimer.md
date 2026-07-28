# ⚖️ Terms of Service & Disclaimer

Thank you for using **OpenStockAPI**. This open-source library connects directly to public APIs of various financial institutions, stock brokerages, cryptocurrency exchanges, and mutual fund platforms.

By integrating or using this library, you acknowledge and agree to the following terms, disclaimers, and guidelines regarding third-party data compliance.

---

## 1. General Disclaimer

*   **Educational and Research Purpose:** OpenStockAPI is an open-source, non-commercial project developed solely for educational, research, and personal development purposes. The project does not provide commercial data redistribution services.
*   **No Financial Advice:** All information and data retrieved through this library are for informational purposes only. The developers and contributors do not assume any responsibility for investment decisions, financial losses, or legal liabilities arising from the use of this data.
*   **Data Accuracy and Latency:** Data is fetched directly from third-party systems. We do not guarantee the accuracy, completeness, timeliness, or continuity of the data. Data may be delayed, rate-limited, or suspended at any time based on the policies of individual providers.

---

## 2. Third-Party Data Compliance (ToS)

Data providers (including stock brokerages, fund managers, and digital asset exchanges) enforce their own Terms of Service (ToS). When using OpenStockAPI, you are indirectly interacting with these endpoints and must adhere to the following rules:

### 2.1 Personal and Non-Commercial Use Only
Most financial data providers specify that:
*   Market data, financial statements, and company details are provided exclusively for the personal, non-commercial use of the client/user.
*   Repackaging, commercializing, or redistributing this data to third parties without the prior written consent of the original data provider is strictly prohibited.

### 2.2 Fair Use & Rate Limiting
Making excessive or rapid requests (scraping/spamming) can be considered a Denial of Service (DoS) attack or resource abuse:
*   **Rate Limiting:** Please respect the built-in rate-limiting tiers of OpenStockAPI or implement custom request throttling/delay in your applications.
*   **Caching:** Actively cache static or historical data (such as company profiles or historical financial reports) rather than sending repeated API requests.
*   **System Integrity:** Avoid infinite loops that execute continuous API calls without a cooldown period.

### 2.3 Technical and Security Risks
*   **Endpoint Stability:** Providers reserve the right to alter their API structure, headers, payload requirements, or block incoming IP addresses without prior notice.
*   **Authentication & Security:** For endpoints requiring credentials or API keys, you are solely responsible for securing your configuration. OpenStockAPI does not store, transmit, or monitor your private keys or credentials (all operations execute locally).

---

## 3. Specific Asset Class Compliance

As the project expands, please refer to the corresponding sub-folder documentation for specific compliance guidelines:
*   **Vietnam Stock Market:** Refer to [Vietnam Stock Terms and Disclaimer](./vn_stock/terms_and_disclaimer.md) for details on TCBS, Vietcap, KB Securities, DNSE, and Fmarket.
*   **Global Markets / Crypto / Forex:** Refer to the respective guides in those sub-folders when they are introduced.

---

## 4. Limitation of Liability

Under no circumstances shall the developers or contributors of OpenStockAPI be liable for any direct, indirect, incidental, special, or consequential damages resulting from the use or inability to use this software, even if advised of the possibility of such damages.
