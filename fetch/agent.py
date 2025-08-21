import requests
import json
from uagents_core.contrib.protocols.chat import (
    chat_protocol_spec,
    ChatMessage,
    ChatAcknowledgement,
    TextContent,
    StartSessionContent,
)
from uagents import Agent, Context, Protocol
from datetime import datetime, timezone
from uuid import uuid4
import os
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent as IcAgent
from ic.candid import Types, encode
from dotenv import load_dotenv
from ic.candid import Types

load_dotenv()

# ASI1 API settings
ASI1_API_KEY = os.getenv("ASI1_API_KEY")

if not ASI1_API_KEY:
    raise RuntimeError("ASI1_API_KEY not set. Add it to your environment or .env")

ASI1_BASE_URL = "https://api.asi1.ai/v1"
ASI1_HEADERS = {
    "Authorization": f"Bearer {ASI1_API_KEY}",
    "Content-Type": "application/json",
}

BASE_URL = "https://ic-api.internetcomputer.org/api/v3"

HEADERS = {"Content-Type": "application/json"}

# Canister Settings
ICP_NETWORK = "local"
ICP_CANISTER_ID = "uxrrr-q7777-77774-qaaaq-cai"
DFX_CANISTER_NAME = "backend"
CANISTER_BASE_URL = "http://127.0.0.1:4943"

iden = Identity()
client = Client(url=CANISTER_BASE_URL if ICP_NETWORK == "local" else "https://ic0.app")
ic_agent = IcAgent(iden, client)

CANISTER_HEADERS = {
    "Host": f"{ICP_CANISTER_ID}.localhost",
    "Content-Type": "application/cbor",
}

proposal_id_type = Types.Nat
proposal_ids_type = Types.Vec(Types.Nat)

tools = [
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
                                "EXECUTED",
                                "FAILED",
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


async def call_canister_endpoint(func_name: str, args: dict, ctx: Context):
    def _normalize_nat(a) -> int:
        v = a.get("proposal_id") if isinstance(a, dict) else a
        if v is None:
            raise ValueError("proposal_id is missing")
        return int(v)

    try:
        ctx.logger.debug(
            f"[CALL] Function={func_name!r}, Raw args={args!r}, Type={type(args)}"
        )

        if func_name == "add_proposal_id":
            pid = _normalize_nat(args)
            ctx.logger.info(f"Adding proposal ID {pid}")
            encoded = encode([{"type": Types.Nat, "value": pid}])
            _ = ic_agent.update_raw(ICP_CANISTER_ID, "addProposalId", encoded)
            return {"status": "ok"}

        elif func_name == "remove_proposal_id":
            pid = _normalize_nat(args)
            ctx.logger.info(f"Removing proposal ID {pid}")
            encoded = encode([{"type": Types.Nat, "value": pid}])
            _ = ic_agent.update_raw(ICP_CANISTER_ID, "removeProposalId", encoded)
            return {"status": "ok"}

        elif func_name == "get_proposal_ids":
            empty_args = encode([])
            result_bytes = ic_agent.query_raw(
                ICP_CANISTER_ID, "getProposalIds", empty_args
            )
            ctx.logger.info(f"[RESULT] Decoded proposal IDs: {result_bytes}")
            return {"status": "ok", "proposal_ids": result_bytes}

        else:
            raise ValueError(f"Unsupported canister function: {func_name}")

    except Exception as e:
        ctx.logger.error(f"Canister call failed: {e}")
        raise


def format_error_response(error: Exception) -> str:
    """Format error messages for user display"""
    error_str = str(error)
    if "CanisterId" in error_str:
        return (
            "⚠️ There was an issue with the canister identification.\n\n"
            "Technical Details:\n"
            f"- Error: {error_str}\n"
            "- This might be due to an incorrect canister ID format\n\n"
            "Suggested Actions:\n"
            "1. Verify the canister ID is correct\n"
            "2. Check that the canister is deployed\n"
            "3. Try `dfx canister id backend` to get the correct ID"
        )
    else:
        return (
            "⚠️ An error occurred while accessing your preferences:\n\n"
            f"{error_str}\n\n"
            "You can try:\n"
            "1. Waiting a few moments and trying again\n"
            "2. Checking if the canister is running"
        )


def validate_canister_response(response: dict) -> bool:
    """Validate that the canister response has the expected structure"""
    if not isinstance(response, dict):
        return False

    required_fields = ["prefs", "created_at_ns", "updated_at_ns"]
    return all(field in response for field in required_fields)


async def call_icp_endpoint(func_name: str, args: dict):
    if func_name == "get_governance_metrics":
        url = f"{BASE_URL}/governance-metrics"
        response = requests.get(url, headers={"Content-Type": "application/json"})
    elif func_name == "governance_total_locked_e8s":
        url = f"{BASE_URL}/governance-metrics/governance_total_locked_e8s"
        response = requests.get(url, headers={"Content-Type": "application/json"})
    elif func_name == "get_icp_usd_rate":
        url = f"{BASE_URL}/icp-usd-rate"
        response = requests.get(url, headers={"Content-Type": "application/json"})
    elif func_name == "get_governance_neurons_total":
        url = f"{BASE_URL}/metrics/governance-neurons-total"
        response = requests.get(url, headers={"Content-Type": "application/json"})
    elif func_name == "get_governance_voting_power_total":
        url = f"{BASE_URL}/metrics/governance-voting-power-total"
        response = requests.get(url, headers={"Content-Type": "application/json"})
    elif func_name == "get_ic_proposals":
        url = f"{BASE_URL}/proposals?offset=0&limit=50&format=json"
        response = requests.get(url, headers={"Content-Type": "application/json"})
    elif func_name == "get_ic_proposals_count":
        url = f"{BASE_URL}/proposals-count"
        response = requests.get(url, headers={"Content-Type": "application/json"})
    elif func_name == "get_ic_latest_proposal_id":
        url = f"{BASE_URL}/latest-proposal-id"
        response = requests.get(url, headers={"Content-Type": "application/json"})
    elif func_name == "get_ic_proposals_over_past_7d":
        url = f"{BASE_URL}/proposals-over-past-7d"
        response = requests.get(url, headers={"Content-Type": "application/json"})
    elif func_name == "get_ic_proposal_info":
        url = f"{BASE_URL}/proposals/{args['proposal_id']}"
        response = requests.get(url, headers={"Content-Type": "application/json"})
    else:
        raise ValueError(f"Unsupported function call: {func_name}")
    response.raise_for_status()
    return response.json()


async def process_query(query: str, ctx: Context) -> str:
    try:
        initial_message = {"role": "user", "content": query}
        payload = {
            "model": "asi1-mini",
            "messages": [initial_message],
            "tools": tools,
            "temperature": 0.7,
            "max_tokens": 2048,
        }
        response = requests.post(
            f"{ASI1_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {ASI1_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        response.raise_for_status()
        response_json = response.json()

        tool_calls = response_json["choices"][0]["message"].get("tool_calls", [])
        messages_history = [initial_message, response_json["choices"][0]["message"]]

        if not tool_calls:
            return "No matching tool function found."

        for tool_call in tool_calls:
            func_name = tool_call["function"]["name"]
            arguments = json.loads(tool_call["function"]["arguments"])
            tool_call_id = tool_call["id"]

        try:
            result = await call_canister_endpoint(func_name, arguments, ctx)
            content_to_send = json.dumps(result)
        except Exception as e:
            ctx.logger.error(f"Tool execution failed: {str(e)}")
            content_to_send = json.dumps(
                {"error": format_error_response(e), "status": "failed"}
            )

        messages_history.append(
            {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": content_to_send,
            }
        )

        final_payload = {
            "model": "asi1-mini",
            "messages": messages_history,
            "temperature": 0.7,
            "max_tokens": 2048,
        }
        final_response = requests.post(
            f"{ASI1_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {ASI1_API_KEY}",
                "Content-Type": "application/json",
            },
            json=final_payload,
        )
        final_response.raise_for_status()
        return final_response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        ctx.logger.error(f"Error processing query: {str(e)}")
        return f"An error occurred: {str(e)}"


agent = Agent(name="ICP-governance-agent", port=8001, mailbox=True)
chat_proto = Protocol(spec=chat_protocol_spec)


@chat_proto.on_message(model=ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    try:
        ack = ChatAcknowledgement(
            timestamp=datetime.now(timezone.utc), acknowledged_msg_id=msg.msg_id
        )
        await ctx.send(sender, ack)

        for item in msg.content:
            if isinstance(item, StartSessionContent):
                ctx.logger.info(f"Got a start session message from {sender}")
                continue
            elif isinstance(item, TextContent):
                ctx.logger.info(f"Got a message from {sender}: {item.text}")
                response_text = await process_query(item.text, ctx)
                ctx.logger.info(f"Response text: {response_text}")
                response = ChatMessage(
                    timestamp=datetime.now(timezone.utc),
                    msg_id=uuid4(),
                    content=[TextContent(type="text", text=response_text)],
                )
                await ctx.send(sender, response)
            else:
                ctx.logger.info(f"Got unexpected content from {sender}")
    except Exception as e:
        ctx.logger.error(f"Error handling chat message: {str(e)}")
        error_response = ChatMessage(
            timestamp=datetime.now(timezone.utc),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=f"An error occurred: {str(e)}")],
        )
        await ctx.send(sender, error_response)


@chat_proto.on_message(model=ChatAcknowledgement)
async def handle_chat_acknowledgement(
    ctx: Context, sender: str, msg: ChatAcknowledgement
):
    ctx.logger.info(
        f"Received acknowledgement from {sender} for message {msg.acknowledged_msg_id}"
    )
    if msg.metadata:
        ctx.logger.info(f"Metadata: {msg.metadata}")


agent.include(chat_proto)

if __name__ == "__main__":
    agent.run()
