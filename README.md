<p align="center">
  <img src="./public/icp-logo.png" alt="Description" width="400"/>
</p>

<h1 align="center">ICP Governance agent</h1>
<p align="center">From ASI LATAM Community 🌎</p>

<div align="center">
  <img src="https://img.shields.io/badge/innovationlab-3D8BD3" alt="tag:innovationlab">
</div>


<h3 align="center">NNS Metrics, Proposals & On-chain State.</h3>
<p align="center">An intelligent agent focused on ICP governance, providing real-time information on proposals, metrics, and more!</p>

## Agent details

- **name**: ICP-Governance-agent
- **Address:** `agent1q0cws9lqyazjhmcth2u4keuk7mhpptg5fvh7wvrkz8j98ls05ftrwgcwc5a`


## 🚀 Getting Started (Local)

### 1) Clone the repository

```bash
git clone https://github.com/ASI-Alliance-LATAM-Community/icp-governance-agent.git

cd icp-governance-agent
```

### 2) Start the local replica and deploy the canister

```bash
dfx start --clean --background

dfx deploy
```

After deployment, grab your canister ID:

```bash
dfx canister id backend
```

Copy the printed canister **ID** and paste it into `fetch/agent.py` for `ICP_CANISTER_ID` (near the “Canister Settings” section).

### 3) Set up the agent environment

```bash
cd fetch/

python3 -m venv .venv

source .venv/bin/activate   # On Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file in `fetch/` and add your ASI1 API key:

```
ASI1_API_KEY=your_api_key_here
```

### 4) Run the agent

```bash
python3 agent.py
```

Tip: When you’re done, stop the local replica with:

```bash
dfx stop
```


## ✨ Features

- Governance and Proposal Queries
- Storage proposals IDs to track in the future
- ICP/USD Price

---

## 🗂 Structure

```
.
└── fetch/
    └── agent.py
    ic/
    └── main.mo
```

## 🧰 ICP API Cheat Sheet

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

### Proposal ID management:

- Add proposal ID 123
- Remove proposal ID 123
- Get my proposal IDs → [1001, 2045, 3077]


## 📄 License

MIT — no warranty.