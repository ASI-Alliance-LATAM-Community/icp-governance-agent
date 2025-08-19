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
from datetime import datetime, timezone, timedelta
from uuid import uuid4
import os
from dotenv import load_dotenv

load_dotenv()

# ASI1 API settings
ASI1_API_KEY = os.getenv("ASI1_API_KEY")

if not ASI1_API_KEY:
    raise RuntimeError("ASI1_API_KEY not set. Add it to your environment or .env")

ASI1_BASE_URL = "https://api.asi1.ai/v1"
ASI1_HEADERS = {
    "Authorization": f"Bearer {ASI1_API_KEY}",
    "Content-Type": "application/json"
}

BASE_URL = "https://ic-api.internetcomputer.org/api/v3"

HEADERS = {
    "Content-Type": "application/json"
}

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
                "additionalProperties": False
            },
            "strict": True
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
                "additionalProperties": False
            },
            "strict": True
        }
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
                "additionalProperties": False
            },
            "strict": True
        }
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
                "additionalProperties": False
            },
            "strict": True
        }
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
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_ic_proposals",
            "description": "List NNS proposals with optional filters (topic, status, action, etc.) and pagination.",
            "parameters": {
                "type": "object",
                "properties": {
                    "offset": { "type": "integer", "minimum": 0, "description": "Pagination offset (default 0)" },
                    "limit":  { "type": "integer", "minimum": 50, "maximum": 100, "description": "Items per page (default 50)" },
                    "max_proposal_index": { "type": "integer", "description": "Return proposals with index <= this value (page backwards)" },
                    "include_reward_status": {
                        "type": "array",
                        "items": { "type": "string", "enum": ["UNSPECIFIED","ACCEPT_VOTES","READY_TO_SETTLE","SETTLED","INELIGIBLE"] }
                    },
                    "include_topic": {
                        "type": "array",
                        "items": { "type": "string", "enum": [
                        "TOPIC_UNSPECIFIED","TOPIC_NEURON_MANAGEMENT","TOPIC_EXCHANGE_RATE","TOPIC_NETWORK_ECONOMICS",
                        "TOPIC_GOVERNANCE","TOPIC_NODE_ADMIN","TOPIC_PARTICIPANT_MANAGEMENT","TOPIC_SUBNET_MANAGEMENT",
                        "TOPIC_NETWORK_CANISTER_MANAGEMENT","TOPIC_KYC","TOPIC_NODE_PROVIDER_REWARDS",
                        "TOPIC_SNS_DECENTRALIZATION_SALE","TOPIC_IC_OS_VERSION_DEPLOYMENT","TOPIC_IC_OS_VERSION_ELECTION",
                        "TOPIC_SNS_AND_COMMUNITY_FUND","TOPIC_API_BOUNDARY_NODE_MANAGEMENT","TOPIC_SUBNET_RENTAL",
                        "TOPIC_PROTOCOL_CANISTER_MANAGEMENT","TOPIC_SERVICE_NERVOUS_SYSTEM_MANAGEMENT",
                        "TOPIC_SYSTEM_CANISTER_MANAGEMENT","TOPIC_APPLICATION_CANISTER_MANAGEMENT"
                        ] }
                    },
                    "include_status": {
                        "type": "array",
                        "items": { "type": "string", "enum": ["UNKNOWN","UNSPECIFIED","OPEN","REJECTED","ADOPTED","EXECUTED","FAILED"] }
                    },
                    "include_action": {
                        "type": "array",
                        "items": { "type": "string", "enum": [
                        "ApproveGenesisKyc","AddOrRemoveNodeProvider","CreateServiceNervousSystem","ExecuteNnsFunction",
                        "FulfillSubnetRentalRequest","InstallCode","ManageNeuron","ManageNetworkEconomics","Motion",
                        "OpenSnsTokenSwap","RegisterKnownNeuron","RewardNodeProvider","RewardNodeProviders",
                        "SetDefaultFollowees","SetSnsTokenSwapOpenTimeWindow","StopOrStartCanister","UpdateCanisterSettings"
                        ] }
                    },
                    "include_action_nns_function": {
                        "type": "array",
                        "items": { "type": "string" },
                        "description": "NNS function names to include (use values shown by the API UI)."
                    },
                    "manage_neuron_id": { "type": "integer" },
                    "proposer": { "type": "integer" }
                    },
                "required": [],
                "additionalProperties": False
            },
            "strict": True
        }
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
                "additionalProperties": False
            },
            "strict": True
        }
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
                "additionalProperties": False
            },
            "strict": True
        }
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
                "additionalProperties": False
            },
            "strict": True
        }
    },
]

async def call_icp_endpoint(func_name: str, args: dict):
    if func_name == "get_governance_metrics":
        url = f"{BASE_URL}/governance-metrics"
        response = requests.get(url, headers={
            "Content-Type": "application/json"
        })
    elif func_name == "governance_total_locked_e8s":
        url = f"{BASE_URL}/governance-metrics/governance_total_locked_e8s"
        response = requests.get(url, headers={
            "Content-Type": "application/json"
        })
    elif func_name == "get_icp_usd_rate":
        url = f"{BASE_URL}/icp-usd-rate"
        response = requests.get(url, headers={
            "Content-Type": "application/json"
        })
    elif func_name == "get_governance_neurons_total":
        url = f"{BASE_URL}/metrics/governance-neurons-total"
        response = requests.get(url, headers={
            "Content-Type": "application/json"
        })
    elif func_name == "get_governance_voting_power_total":
        url = f"{BASE_URL}/metrics/governance-voting-power-total"
        response = requests.get(url, headers={
            "Content-Type": "application/json"
        })
    elif func_name == "get_ic_proposals":
        url = f"{BASE_URL}/proposals?offset=0&limit=50&format=json"
        response = requests.get(url, headers={
            "Content-Type": "application/json"
        })
    elif func_name == "get_ic_proposals_count":
        url = f"{BASE_URL}/proposals-count"
        response = requests.get(url, headers={
            "Content-Type": "application/json"
        })
    elif func_name == "get_ic_latest_proposal_id":
        url = f"{BASE_URL}/latest-proposal-id"
        response = requests.get(url, headers={
            "Content-Type": "application/json"
        })
    elif func_name == "get_ic_proposals_over_past_7d":
        url = f"{BASE_URL}/proposals-over-past-7d"
        response = requests.get(url, headers={
            "Content-Type": "application/json"
        })
    else:
        raise ValueError(f"Unsupported function call: {func_name}")
    response.raise_for_status()
    return response.json()

async def process_query(query: str, ctx: Context) -> str:
    try:
        # Step 1: Initial call to ASI1 with user query and tools
        initial_message = {
            "role": "user",
            "content": query
        }
        payload = {
            "model": "asi1-mini",
            "messages": [initial_message],
            "tools": tools,
            "temperature": 0.7,
            "max_tokens": 1024
        }
        response = requests.post(
            f"{ASI1_BASE_URL}/chat/completions",
            headers=ASI1_HEADERS,
            json=payload
        )
        response.raise_for_status()
        response_json = response.json()

        # Step 2: Parse tool calls from response
        tool_calls = response_json["choices"][0]["message"].get("tool_calls", [])
        messages_history = [initial_message, response_json["choices"][0]["message"]]

        if not tool_calls:
            return "I couldn't determine what ICP Governance information you're looking for. Please try rephrasing your question."

        # Step 3: Execute tools and format results
        for tool_call in tool_calls:
            func_name = tool_call["function"]["name"]
            arguments = json.loads(tool_call["function"]["arguments"])
            tool_call_id = tool_call["id"]

            ctx.logger.info(f"Executing {func_name} with arguments: {arguments}")

            try:
                result = await call_icp_endpoint(func_name, arguments)
                content_to_send = json.dumps(result)
            except Exception as e:
                error_content = {
                    "error": f"Tool execution failed: {str(e)}",
                    "status": "failed"
                }
                content_to_send = json.dumps(error_content)

            tool_result_message = {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": content_to_send
            }
            messages_history.append(tool_result_message)

        # Step 4: Send results back to ASI1 for final answer
        final_payload = {
            "model": "asi1-mini",
            "messages": messages_history,
            "temperature": 0.7,
            "max_tokens": 1024
        }
        final_response = requests.post(
            f"{ASI1_BASE_URL}/chat/completions",
            headers=ASI1_HEADERS,
            json=final_payload
        )
        final_response.raise_for_status()
        final_response_json = final_response.json()

        # Step 5: Return the model's final answer
        return final_response_json["choices"][0]["message"]["content"]

    except Exception as e:
        ctx.logger.error(f"Error processing query: {str(e)}")
        return f"An error occurred while processing your request: {str(e)}"

agent = Agent(
    name='ICP-governance-agent',
    port=8001,
    mailbox=True
)
chat_proto = Protocol(spec=chat_protocol_spec)

@chat_proto.on_message(model=ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    try:
        ack = ChatAcknowledgement(
            timestamp=datetime.now(timezone.utc),
            acknowledged_msg_id=msg.msg_id
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
                    content=[TextContent(type="text", text=response_text)]
                )
                await ctx.send(sender, response)
            else:
                ctx.logger.info(f"Got unexpected content from {sender}")
    except Exception as e:
        ctx.logger.error(f"Error handling chat message: {str(e)}")
        error_response = ChatMessage(
            timestamp=datetime.now(timezone.utc),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=f"An error occurred: {str(e)}")]
        )
        await ctx.send(sender, error_response)

@chat_proto.on_message(model=ChatAcknowledgement)
async def handle_chat_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Received acknowledgement from {sender} for message {msg.acknowledged_msg_id}")
    if msg.metadata:
        ctx.logger.info(f"Metadata: {msg.metadata}")

agent.include(chat_proto)

if __name__ == "__main__":
    agent.run()
    
    
# GET /api/v3/governance-metrics/{name}
# GET /api/v3/proposals/{proposal_id}
# <tool_call> {"name": "get_ic_proposal_info", "arguments": {"proposal_id": 138051}} </tool_call>