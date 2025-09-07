from fastmcp import FastMCP
import asyncio
import time
import os
from playwright.async_api import async_playwright

mcp = FastMCP("ApplicationServer")

# Global variables to store the process and logs
app_process = None
server_logs = asyncio.Queue()
console_logs = []
browser = None
page = None
playwright = None

async def capture_output(process):
    """Capture output from a subprocess."""
    async for line in process.stdout:
        if line:
            await server_logs.put(line.decode('utf-8').rstrip())
    
    async for line in process.stderr:
        if line:
            await server_logs.put(line.decode('utf-8').rstrip())

async def setup_browser_console_capture():
    """Setup browser with console log capturing."""
    global browser, page, playwright, console_logs
    
    # Launch playwright and browser
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    
    # Clear previous console logs
    console_logs.clear()
    
    # Add console event listener
    def handle_console_message(msg):
        log_entry = {
            "level": msg.type,
            "message": msg.text,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "url": page.url,
            "args": [str(arg) for arg in msg.args]
        }
        console_logs.append(log_entry)
        # Keep only last 100 logs
        if len(console_logs) > 100:
            console_logs.pop(0)
    
    page.on("console", handle_console_message)
    
    # Also capture page errors
    def handle_page_error(error):
        log_entry = {
            "level": "error",
            "message": f"Page Error: {error}",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "url": page.url,
            "args": []
        }
        console_logs.append(log_entry)
    
    page.on("pageerror", handle_page_error)
    
    return True

@mcp.tool
async def start_app() -> str:
    """Starts the fasthtml application subprocess."""
    global app_process
    
    if app_process and app_process.returncode is None:
        return "App is already running."
    
    # Start the FastHTML app
    app_process = await asyncio.create_subprocess_exec(
        "python", "main.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    # Start task to capture output
    asyncio.create_task(capture_output(app_process))
    
    await asyncio.sleep(2)  # Give the server time to start
    
    # Setup browser for console capture
    if await setup_browser_console_capture():
        return "App started successfully. Server is running on http://localhost:5001 with browser console capture enabled."
    else:
        return "App started successfully. Server is running on http://localhost:5001 (browser console capture failed to initialize)."

@mcp.tool
async def stop_app() -> str:
    """Stops the fasthtml application."""
    global app_process, browser, playwright
    
    if app_process and app_process.returncode is None:
        app_process.terminate()
        await app_process.wait()
        app_process = None
    
    # Close browser if open
    if browser:
        await browser.close()
        browser = None
    
    if playwright:
        await playwright.stop()
        playwright = None
    
    if app_process is None:
        return "App stopped successfully."
    else:
        return "App is not running."

@mcp.tool
async def get_console_logs() -> str:
    """Gets the browser console logs from the fasthtml application."""
    global console_logs
    
    if not app_process or app_process.returncode is not None:
        return "App is not running. Start the app first to capture console logs."
    
    if not console_logs:
        return "No browser console logs captured yet. Use navigate_to() to visit pages and generate logs."
    
    # Format logs for display
    formatted_logs = []
    for log in console_logs[-20:]:  # Last 20 logs
        formatted_logs.append(
            f"[{log.get('timestamp', 'N/A')}] [{log.get('level', 'log').upper()}] {log.get('message', '')} - {log.get('url', '')}"
        )
    
    return "\n".join(formatted_logs)

@mcp.tool
async def navigate_to(path: str = "/") -> str:
    """Navigate the browser to a specific path in the application."""
    global page
    
    if not app_process or app_process.returncode is not None:
        return "App is not running. Start the app first."
    
    if not page:
        return "Browser is not initialized. Restart the app."
    
    try:
        url = f"http://localhost:5001{path}"
        await page.goto(url, wait_until="networkidle")
        await asyncio.sleep(1)  # Give time for any async operations
        return f"Navigated to {url}"
    except Exception as e:
        return f"Failed to navigate: {str(e)}"

@mcp.tool
async def get_server_logs() -> str:
    """Gets the application server logs from the fasthtml application."""
    logs = []
    
    # Get all available logs from the queue
    while not server_logs.empty():
        try:
            logs.append(await server_logs.get())
        except:
            break
    
    if not logs:
        if app_process and app_process.returncode is None:
            return "No new server logs. Server is running."
        else:
            return "No server logs. Server is not running."
    
    return "\n".join(logs[-50:])  # Return last 50 lines

@mcp.tool
async def get_app_status() -> str:
    """Gets the current status of the fasthtml application."""
    if app_process and app_process.returncode is None:
        browser_status = "Browser console capture enabled" if browser and page else "Browser not initialized"
        return f"App is running (PID: {app_process.pid}). {browser_status}"
    return "App is not running"

@mcp.tool
async def click_element(selector: str) -> str:
    """Click an element on the page using a CSS selector."""
    global page
    
    if not app_process or app_process.returncode is not None:
        return "App is not running. Start the app first."
    
    if not page:
        return "Browser is not initialized. Restart the app."
    
    try:
        await page.click(selector)
        await asyncio.sleep(0.5)  # Give time for any async operations
        return f"Clicked element: {selector}"
    except Exception as e:
        return f"Failed to click element '{selector}': {str(e)}"

if __name__ == "__main__":
    mcp.run()