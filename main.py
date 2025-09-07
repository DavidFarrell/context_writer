from fasthtml.common import *
from monsterui.all import *

app, rt = fast_app(hdrs=Theme.blue.headers())

@rt
def index():
    return Container(
        H1("Example FastHTML App"),
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