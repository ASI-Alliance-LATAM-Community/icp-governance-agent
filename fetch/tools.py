from typing import List, Dict, Any

TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "get_governance_metrics",
            "description": "Fetch Internet Computer governance metrics from ic-api.internetcomputer.org (no parameters).",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "governance_total_locked_e8s",
            "description": "Gets the total amount of e8s locked in ICP governance.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_icp_usd_rate",
            "description": "Fetch the latest ICP/USD rate from Internet Computer API.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_governance_neurons_total",
            "description": "Fetch time-series of total governance neurons from Internet Computer API.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_governance_voting_power_total",
            "description": "Fetch time-series of total governance voting power from the Internet Computer API.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_ic_proposals",
            "description": "List NNS proposals with optional filters (topic, status, action, etc.) and pagination.",
            "parameters": {
                "type": "object",
                "properties": {
                    "offset": {
                        "type": "integer",
                        "minimum": 0,
                        "description": "Pagination offset (default 0)",
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 50,
                        "maximum": 100,
                        "description": "Items per page (default 50)",
                    },
                    "max_proposal_index": {
                        "type": "integer",
                        "description": "Return proposals with index <= this value (page backwards)",
                    },
                    "include_reward_status": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": [
                                "UNSPECIFIED",
                                "ACCEPT_VOTES",
                                "READY_TO_SETTLE",
                                "SETTLED",
                                "INELIGIBLE",
                            ],
                        },
                    },
                    "include_topic": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": [
                                "TOPIC_UNSPECIFIED",
                                "TOPIC_NEURON_MANAGEMENT",
                                "TOPIC_EXCHANGE_RATE",
                                "TOPIC_NETWORK_ECONOMICS",
                                "TOPIC_GOVERNANCE",
                                "TOPIC_NODE_ADMIN",
                                "TOPIC_PARTICIPANT_MANAGEMENT",
                                "TOPIC_SUBNET_MANAGEMENT",
                                "TOPIC_NETWORK_CANISTER_MANAGEMENT",
                                "TOPIC_KYC",
                                "TOPIC_NODE_PROVIDER_REWARDS",
                                "TOPIC_SNS_DECENTRALIZATION_SALE",
                                "TOPIC_IC_OS_VERSION_DEPLOYMENT",
                                "TOPIC_IC_OS_VERSION_ELECTION",
                                "TOPIC_SNS_AND_COMMUNITY_FUND",
                                "TOPIC_API_BOUNDARY_NODE_MANAGEMENT",
                                "TOPIC_SUBNET_RENTAL",
                                "TOPIC_PROTOCOL_CANISTER_MANAGEMENT",
                                "TOPIC_SERVICE_NERVOUS_SYSTEM_MANAGEMENT",
                                "TOPIC_SYSTEM_CANISTER_MANAGEMENT",
                                "TOPIC_APPLICATION_CANISTER_MANAGEMENT",
                            ],
                        },
                    },
                    "include_status": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": [
                                "UNKNOWN",
                                "UNSPECIFIED",
                                "OPEN",
                                "REJECTED",
                                "ADOPTED",
                                "FAILED",
                                "EXECUTED",
                            ],
                        },
                    },
                    "include_action": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": [
                                "ApproveGenesisKyc",
                                "AddOrRemoveNodeProvider",
                                "CreateServiceNervousSystem",
                                "ExecuteNnsFunction",
                                "FulfillSubnetRentalRequest",
                                "InstallCode",
                                "ManageNeuron",
                                "ManageNetworkEconomics",
                                "Motion",
                                "OpenSnsTokenSwap",
                                "RegisterKnownNeuron",
                                "RewardNodeProvider",
                                "RewardNodeProviders",
                                "SetDefaultFollowees",
                                "SetSnsTokenSwapOpenTimeWindow",
                                "StopOrStartCanister",
                                "UpdateCanisterSettings",
                            ],
                        },
                    },
                    "include_action_nns_function": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "NNS function names to include (use values shown by the API UI).",
                    },
                    "manage_neuron_id": {"type": "integer"},
                    "proposer": {"type": "integer"},
                },
                "required": [],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_ic_proposals_count",
            "description": "Get the total number of Internet Computer governance proposals.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_ic_latest_proposal_id",
            "description": "Get the latest Internet Computer governance proposal ID. This is useful for fetching the most recent proposal details.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_ic_proposals_over_past_7d",
            "description": "Get the number of IC governance proposals over the past 7 days and the delta vs the previous 7 days.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_ic_proposal_info",
            "description": "Get details of a specific ICP governance proposal by ID.",
            "parameters": {
                "type": "object",
                "properties": {"proposal_id": {"type": "integer"}},
                "required": ["proposal_id"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_proposal_id",
            "description": "Store a proposal ID in the user's list",
            "parameters": {
                "type": "object",
                "properties": {"proposal_id": {"type": "integer"}},
                "required": ["proposal_id"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remove_proposal_id",
            "description": "Remove a proposal ID from the user's list",
            "parameters": {
                "type": "object",
                "properties": {"proposal_id": {"type": "integer"}},
                "required": ["proposal_id"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_proposal_ids",
            "description": "Get the current list of proposal IDs stored by the user",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]