import gradio as gr
from app.agent.calendar_agent import calendar_agent

def run_calendar_agent(user_input, history):
    messages = []

    for turn in history:
        if isinstance(turn, (list, tuple)):
            if len(turn) >= 1 and turn[0]:
                messages.append({"role": "user", "content": turn[0]})
            if len(turn) >= 2 and turn[1]:
                messages.append({"role": "assistant", "content": turn[1]})
        elif isinstance(turn, dict):
            role = turn.get("role")
            content = turn.get("content")
            if role and content:
                messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_input})

    response = calendar_agent.invoke({"messages": messages})
    last_message = response["messages"][-1]

    if isinstance(last_message.content, list):
        return last_message.content[0].get("text", "")

    return last_message.content

iface = gr.ChatInterface(
    fn=run_calendar_agent,
    title="🗓️ AI Calendar Assistant",
    description="Ask the AI Calendar Assistant to help you manage your calendar."
)

if __name__ == "__main__":
    iface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        
    )
