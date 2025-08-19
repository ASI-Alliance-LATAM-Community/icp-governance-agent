<p align="center">
  <img src="./public/icp-logo.png" alt="Description" width="400"/>
</p>

<h1 align="center">ICP Governance agent</h1>

<div align="center">
  <img src="https://img.shields.io/badge/innovationlab-3D8BD3" alt="tag:innovationlab">
</div>

<h3 align="center">NNS Metrics, Proposals & On-chain State.</h3>
<p align="center">An intelligent agent focused on ICP governance, providing real-time information on proposals, metrics, and more!</p>

## Agent details

- **Address:** `agent1q0cws9lqyazjhmcth2u4keuk7mhpptg5fvh7wvrkz8j98ls05ftrwgcwc5a`

## ✨ Features

- Governance and Proposal Queries
- ICP/USD Price

---

## 🗂 Structure

```
.
└── fetch/
    └── agent.py
```

## 🧰 API Cheat Sheet

| Endpoint                                               | Purpose                   |
| ------------------------------------------------------ | ------------------------- |
| `/api/v3/icp-usd-rate`                                 | Latest ICP-USD            |
| `/metrics/governance-neurons-total`                    | Total neurons             |
| `/metrics/governance-voting-power-total`               | Voting power              |
| `/metrics/governance_not_dissolving_neurons_e8s_1year` | Buckets by dissolve delay |
| `/proposals`                                           | Proposals list + filters  |
| `/proposals-count`                                     | Count                     |
| `/latest-proposal-id`                                  | Latest id                 |
| `/proposals-over-past-7d`                              | 7-day totals              |

---

## 💡 Suggested questions

Use natural language—**ICP Governance agent** will map these to the right NNS endpoints and your on-chain prefs.

### Quick status

* What’s the **latest NNS proposal ID**?
* How many **proposals exist in total**?
* How many **proposals were submitted in the last 7 days**, and what’s the change vs the previous week?
* What’s the **current ICP/USD rate**?

### Browse proposals

* Show the **latest 20 proposals**.
* List **OPEN proposals** only.
* Filter proposals by **topic**: Governance, IC OS Version Deployment, Network Canister Management, etc.
* Filter proposals by **action**: `InstallCode`, `ExecuteNnsFunction`, `ManageNeuron`, etc.
* Show proposals from **proposer ID 52**.
* Paginate proposals: **offset 50, limit 50**.
* For proposal **138051**, show the **summary, tally, and status**.

### Metrics & trends

* What’s the **total number of neurons** right now?
* What’s the **total voting power** right now?
* Give me the **non-dissolving neurons** breakdown by **dissolve delay buckets** (0–12m, 12–24m, …).
* Plot the **voting power** time series with **step=7200** over the **last 24 hours**.
* From **start=<ts> to end=<ts>**, chart **total neurons** with a 2-hour step.

### My on-chain prefs (canister)

* **Set my preferred filters** to topic Governance and status OPEN.
* **Remember** that I last saw proposal **138051**.
* What’s my **current stored state** (prefs, last seen proposal, webhook)?
* **Set a webhook** to `https://example.com/webhook` for new proposals.
* **Clear my webhook** and keep the filters.

### Automation loop prompts

* Check if there are **new proposals since my last seen** and then **update** my last seen ID.
* Fetch only **proposals newer than 138000** and **summarize by topic**.
* Compare **this week’s proposal count vs last week** and give me the delta.


## 📄 License

MIT — no warranty.