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

from tools import TOOLS as tools
from dotenv import load_dotenv

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

# ICP API settings
BASE_URL = "https://ic-api.internetcomputer.org/api/v3"
HEADERS = {"Content-Type": "application/json"}

# Canister Settings
ICP_NETWORK = "local"
ICP_CANISTER_ID = "uxrrr-q7777-77774-qaaaq-cai"
CANISTER_BASE_URL = "http://127.0.0.1:4943"

iden = Identity()
client = Client(url=CANISTER_BASE_URL if ICP_NETWORK == "local" else "https://ic0.app")
ic_agent = IcAgent(iden, client)

CANISTER_TOOL_NAMES = {
    "add_proposal_id",
    "remove_proposal_id",
    "get_proposal_ids",
}

ICP_TOOL_NAMES = {
    "get_governance_metrics",
    "governance_total_locked_e8s",
    "get_icp_usd_rate",
    "get_governance_neurons_total",
    "get_governance_voting_power_total",
    "get_ic_proposals",
    "get_ic_proposals_count",
    "get_ic_latest_proposal_id",
    "get_ic_proposals_over_past_7d",
    "get_ic_proposal_info",
}


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

        resp = requests.post(
            f"{ASI1_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {ASI1_API_KEY}", "Content-Type": "application/json"},
            json=payload,
        )
        resp.raise_for_status()
        response_json = resp.json()

        model_msg = response_json["choices"][0]["message"]
        tool_calls = model_msg.get("tool_calls", [])
        messages_history = [initial_message, model_msg]

        if not tool_calls:
            return "No matching tool function found."

        for tool_call in tool_calls:
            func_name = tool_call["function"]["name"]
            arguments = json.loads(tool_call["function"]["arguments"] or "{}")
            tool_call_id = tool_call["id"]

            try:
                if func_name in CANISTER_TOOL_NAMES:
                    result = await call_canister_endpoint(func_name, arguments, ctx)
                elif func_name in ICP_TOOL_NAMES:
                    result = await call_icp_endpoint(func_name, arguments)
                else:
                    raise ValueError(f"Unsupported tool: {func_name}")

                content_to_send = json.dumps(result)

            except Exception as e:
                ctx.logger.error(f"Tool execution failed for {func_name}: {e}")
                content_to_send = json.dumps(
                    {"error": format_error_response(e), "status": "failed", "tool": func_name}
                )

            messages_history.append(
                {"role": "tool", "tool_call_id": tool_call_id, "content": content_to_send}
            )

        final_payload = {
            "model": "asi1-mini",
            "messages": messages_history,
            "temperature": 0.7,
            "max_tokens": 2048,
        }
        final_response = requests.post(
            f"{ASI1_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {ASI1_API_KEY}", "Content-Type": "application/json"},
            json=final_payload,
        )
        final_response.raise_for_status()
        return final_response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        ctx.logger.error(f"Error processing query: {e}")
        return f"An error occurred: {e}"


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
