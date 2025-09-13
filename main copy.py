from fasthtml.common import *
from monsterui.all import *

# Import from our nbdev package!
from context_writer.core import get_secret_word, AppConfig




app, rt = fast_app(hdrs=Theme.blue.headers())

# Create an instance of our config
config = AppConfig("Context Writer App")

@rt
def index():
    # Use the secret word from our nbdev package
    secret = get_secret_word()
    
    return Container(
        H1(config.get_title()),  # Uses the title from our nbdev class
        Subtitle(f"Secret Word: {secret}"),  # Shows the secret word directly
        Card(
            H3("Package Info"),
            *[P(f"{k}: {v}") for k, v in config.get_info().items()]
        ),
        Subtitle("To show how you can control it with MCP"),
        P("Steps:"),
        Ol(
            Li("Install fastmcp python library"),
            Li("Install the mcp server in claude code using fastmcp `fastmcp install claude-code --server-spec mcp_server.py`"),
            Li("Open claude code and do `/mcp` to verify it's connected"),
            Li("Ask claude code to `Try to start the app with the tool, press the button, and then get the broser console log of what the error is`")
        ),
        Button("Example Broken Button", hx_get="/aroute", hx_target="#broken-content"),
    )

@rt
def aroute():
    return Div("Something went wrong")

serve()