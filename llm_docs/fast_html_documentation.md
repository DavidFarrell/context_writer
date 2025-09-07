FastHTML: A Comprehensive Developer Guide

Introduction

FastHTML is a next-generation web framework for building modern, interactive web applications entirely in Python ￼. It eliminates much of the complexity of traditional web development by allowing developers to define UIs and behavior in pure Python, without requiring extensive JavaScript or templating languages ￼. FastHTML leverages core web technologies under the hood – it’s built on the high-performance ASGI standard (via Starlette and Uvicorn) and uses the HTMX library to enable dynamic behavior – but presents a simplified, Python-first interface to developers ￼ ￼.

Key Features and Benefits: FastHTML addresses common pain points in web development, testing, and performance. Some highlights include ￼ ￼:
	•	Python-only development: Build the frontend and backend in Python – no need for a separate JS framework. This results in lean projects with fewer files and less boilerplate ￼.
	•	Minimal dependencies: FastHTML relies on only a few libraries (Starlette, Uvicorn, HTMX, etc.), reducing maintenance complexity and security surface area ￼.
	•	Unified client/server stack: You use a single language (Python) and framework for both UI and logic, which minimizes context switching and accelerates development ￼.
	•	HTML as Python objects: Every HTML tag is represented as a Python function or class. For example, <div> corresponds to Div(...) and <a> to A(..., href=...) – including support for modern attributes like hx-* for interactivity ￼ ￼. This yields a type-safe, expressive HTML DSL with no new templating syntax to learn.
	•	Asynchronous and high-performance: FastHTML is ASGI-native. It can handle many concurrent connections with low latency by using Python async features and non-blocking I/O ￼. Under heavy load, async frameworks like FastHTML (built on Starlette) outperform traditional sync frameworks ￼. It also supports WebSockets and server-sent events out-of-the-box for real-time features ￼ ￼.
	•	Integrated extras: Common web app needs like authentication, caching, database integration, and custom styling are supported. FastHTML includes a lightweight ORM (fastlite for SQLite), integrates easily with external databases or ORMs, and has built-in support for things like OAuth login and Stripe payments ￼ ￼. It even ships with a default CSS framework (PicoCSS) for quick, clean styling ￼ ￼.

In summary, FastHTML aims to let you create dynamic web interfaces with minimal code while standing on solid foundations (Python, HTML/HTTP, ASGI, HTMX) ￼ ￼. The following sections will guide you through setting up FastHTML, building applications with it, and utilizing its ecosystem of features.

Installation and Setup

FastHTML is a Python library available on PyPI. Install it with pip:

pip install python-fasthtml

This will pull in the fasthtml package and its few dependencies (Starlette, Uvicorn, etc.) ￼. Ensure you have Python 3.7+ installed (we recommend using Python 3.10+). If you’re new to Python, using an environment manager like Miniconda is a good idea for managing dependencies ￼.

After installation, you can verify by importing FastHTML in a Python REPL or script. There is no separate initialization step – FastHTML apps run anywhere Python runs, and no specialized server is required beyond an ASGI server (Uvicorn is included by default) ￼ ￼.

Editor Configuration: Because FastHTML uses some dynamic coding patterns, your IDE or linter might show false errors. For example, the common VS Code/Pylance setup may not understand FastHTML’s syntax and wildcard imports, leading to spurious warnings ￼ ￼. It’s recommended to adjust your editor’s settings to disable certain type checks for FastHTML projects ￼ ￼. In VS Code, for instance, you can add the following to your workspace settings JSON:

"python.analysis.diagnosticSeverityOverrides": {
    "reportWildcardImportFromLibrary": "none",
    "reportGeneralTypeIssues": "none",
    "reportOptionalMemberAccess": "none",
    // ... (disable other false positives as needed)
}

This will prevent misleading error squiggles in FastHTML code. (As an alternative to import *, some developers prefer import fasthtml.common as fh and using fh.ElementName for clarity ￼, but the library is designed so that wildcard imports are safe and convenient, exporting only intended symbols ￼.)

Getting Started: Your First FastHTML App

Let’s jump in with a minimal “Hello, World” app to see FastHTML in action. All you need is a single Python file:

main.py:

from fasthtml.common import *  # Import FastHTML and Starlette essentials
app, rt = fast_app()          # Create a FastHTML app and route shortcut

@rt('/')                      # Define a route for the home page (GET by default)
def index():
    return Div(P('Hello, World!'))
    
serve()  # Run the development server

That’s it! Run this file with python main.py. FastHTML will start Uvicorn for you (on port 5001 by default) and print the local URL ￼ ￼:

INFO:     Uvicorn running on http://127.0.0.1:5001 (Press CTRL+C to quit)
INFO:     Started reloader process...
INFO:     Application startup complete.

Open http://127.0.0.1:5001 in your browser, and you should see a page that says “Hello, World!” ￼. If you edit the code and save, the server will detect the change and auto-reload (thanks to Uvicorn’s reloader) ￼ ￼ – simply refresh the browser to see your updates. FastHTML’s serve() call wraps Uvicorn, so you typically don’t need a separate uvicorn command during development, and you also don’t need to add the if __name__ == "__main__": guard (FastHTML’s serve() handles that internally ￼ ￼).

A quick breakdown of the example:
	•	We import everything from fasthtml.common. This module provides all the key classes and functions (it’s a “meta-package” import for convenience ￼). The wildcard import is intentional to keep code concise – only relevant FastHTML symbols are exposed in __all__ ￼.
	•	app, rt = fast_app() creates a FastHTML application object and a route decorator in one go ￼ ￼. Here app is an instance of FastHTML (which is a subclass of Starlette) ￼, and rt is a shorthand for app.route. You can also create an app with app = FastHTML() and use @app.get(...)/@app.post(...) decorators, but using rt (route) is idiomatic for brevity ￼.
	•	The @rt('/') decorator registers a view function for the root URL /. By default, this will respond to GET requests.
	•	In the index() function, we return a Div component containing a P (paragraph) component with the text “Hello, World!”.
	•	Returning FastHTML components (also called FT components or FastTags) causes them to be rendered to HTML when sending the response ￼ ￼. In this case, the framework will produce an HTML page with our <div><p>Hello, World!</p></div> inside the body (and some default styling applied).
	•	Finally, serve() starts the app. In development it runs Uvicorn with auto-reload and debug output; in production you might run Uvicorn or Gunicorn manually (more on deployment later).

Congratulations – you’ve created your first FastHTML web page! 🎉

Creating HTML Components in Python

One of FastHTML’s core ideas is representing HTML as Python objects. You don’t write HTML strings or templates; instead you compose HTML using Python function calls that mirror HTML tags ￼. This Pythonic HTML abstraction makes your UI code type-safe and easy to refactor ￼.

Basic usage: Each standard HTML tag has a corresponding Python constructor in FastHTML. For example, Div(), P(), A(), Table(), etc. (there are over 150 tags available) ￼. These constructors accept two kinds of arguments:
	•	Positional arguments – interpreted as the tag’s child elements or content (which can be strings or other components) ￼ ￼.
	•	Keyword arguments – interpreted as HTML attributes for that tag ￼. Because Python identifiers can’t contain hyphens or certain reserved words, FastHTML uses a few naming conventions:
	•	Use cls for the class attribute ￼.
	•	Underscores _ in attribute names will be converted to hyphens. For example, hx_get="/data" in Python becomes hx-get="/data" in HTML ￼.
	•	A trailing underscore can be used if an attribute name conflicts with Python keywords (e.g. for_="val" -> for="val"), though some common cases like for are also handled by aliases (e.g. _for) ￼ ￼.
	•	Boolean attributes: use Python booleans True/False. True means include the attribute with no value (HTML shorthand), False means omit it ￼.

Example:

from fasthtml.common import *
page = Html(
    Head(Title('My Page')), 
    Body(
        Div('Some text, ', 
            A('a link', href='https://example.com'), 
            Img(src="https://placehold.co/100"), 
            cls='container')
    )
)
print(to_xml(page))

This Python code builds a simple HTML page structure and uses to_xml() to output it as HTML. The result would be:

<!doctype html>
<html>
  <head>
    <title>My Page</title>
  </head>
  <body>
    <div class="container">
      Some text, <a href="https://example.com">a link</a>
      <img src="https://placehold.co/100">
    </div>
  </body>
</html>

As shown, our Python calls produced the equivalent HTML. Notice how cls='container' became class="container", and the string and nested tags became children inside the <div> ￼ ￼. When you return such components from a FastHTML route, the framework takes care of serializing them to a proper HTTP response.

FastHTML defers HTML serialization until the last moment – your route functions can simply return Python objects (or even tuples of objects), and FastHTML will convert them to an HTML response automatically ￼. This means you can manipulate your UI elements in Python (pass them around, store them, test them) as regular objects. It also means refactoring is safe – if you rename a function parameter or component, references update naturally, unlike string templates ￼. You can even unit-test components by instantiating them and inspecting their properties or HTML, without running a live server ￼.

FT Components: The classes/functions representing HTML tags are often called FastTags or FT components. By convention, they start with a capital letter (PascalCase) – e.g. Div, Span, Input – which makes them visually distinct in code from ordinary variables (a nod to the fast.ai coding style) ￼ ￼. Under the hood, each FT component is essentially a small callable that returns a tuple structure of (tag_name, children, attrs) ￼, but you don’t need to worry about that detail – just call them like you would HTML tags. FastHTML comes with a comprehensive set of tags (almost every HTML5 element, plus a few extras for convenience like Titled and Socials) ￼.

You can create custom components easily by composing existing ones. The simplest way is to define a Python function that returns an FT component or a group of them. For example:

def Card(title, body):
    return Article(
        H2(title, cls="card-title"),
        P(body, cls="card-body"),
        cls="card"
    )
)

This defines a reusable Card component that you can use in your routes like Card("Welcome", "This is a card."). Each instance will produce an <article class="card">...</article> block with a heading and paragraph inside. By encapsulating markup in Python functions, you avoid repetition and ensure consistency across your UI ￼ ￼. Any changes to the component’s implementation will automatically reflect everywhere it’s used.

Note: If you prefer not to pollute the global namespace with import *, you can import the components under a namespace. For example, import fasthtml.ft as ft allows you to write ft.Div(...), ft.H1(...), etc. ￼ ￼. This is purely a stylistic choice – functionally it’s the same.

Routing and Request Handling

Defining URL routes in FastHTML will feel familiar if you’ve used frameworks like FastAPI or Flask. You use Python decorators to map URL paths and HTTP methods to functions. Those functions (view handlers) return the content to send back.

Using the app from earlier, you can add routes in a few ways:

1. Declarative decorators: FastHTML provides app.get(), app.post(), etc., similar to FastAPI. For example:

@app.get("/about")
def about_page():
    return Div(H1("About"), P("This is the about page."))

This registers the function to handle GET requests to /about ￼ ￼. Likewise, use @app.post("/submit") for a POST endpoint, etc. The decorator name corresponds to the HTTP method.

If you are using the rt = app.route shortcut, you can call it with a path and optionally specify methods. By default, @rt('/path') without specifying method will handle both GET and POST for that path (which is convenient for forms – more on that later) ￼ ￼.

2. Automatic route naming: A FastHTML idiom is to use @rt with no path string and let the function name determine the route ￼ ￼. In this mode, the function’s name (converted to lowercase) becomes the URL path, and it will handle both GET and POST by default. For instance:

@rt
def contact():  # will serve at "/contact"
    return Titled("Contact Us", P("Contact form here..."))

@rt
def index():    # the name "index" is special-cased to "/"
    return Titled("Home", P("Welcome to the site!"))

Here, contact() becomes the handler for /contact, and index() maps to / (root) ￼ ￼. This convention lets you avoid repeating URLs in many cases and makes refactoring route names easier. Do note that if you use this style, you must use unique function names (no two handlers with the same name). Under the hood, FastHTML registers these routes on the Starlette app with the given names.

Path Parameters vs Query Parameters: If you need to accept parameters in your route, you have two options:
	•	Path parameters: Include placeholders in the URL path (like /user/{id}) and correspondingly add arguments to the function. This works much like FastAPI’s path parameters ￼. For example:

@rt('/user/{username}')
def profile(username: str):
    return P(f"Profile page of {username}")

Calling /user/alice would pass "alice" as the username argument.

	•	Query parameters: Simply add typed parameters to your function without putting them in the path. FastHTML will automatically parse query strings and form fields to fill these. For example:

@rt
def search(q: str):
    # accessible at /search?q=some+term
    return P(f"You searched for '{q}'")

In FastHTML, using query parameters is often more idiomatic and flexible than complex path hierarchies ￼ ￼. It avoids having to duplicate parameter names in the URL and code. The framework will prefer query args unless you explicitly use a {param} in the route string.

In both cases, type annotations are important – FastHTML uses them to convert the incoming strings to the right Python types (int, float, etc.) and to decide whether to treat a parameter as part of the path or query ￼ ￼. Always annotate your route function parameters (if a parameter is unannotated, it may not be injected).

Example with parameters and testing:

@rt('/greet/{name}')
def greet(name: str, excited: bool = False):
    message = f"Hello, {name}"
    return P(message + ("!!!" if excited else "."))

	•	Visiting /greet/John returns “Hello, John.”
	•	Visiting /greet/Jane?excited=true returns “Hello, Jane!!!” (because excited=true in the query string is parsed as the boolean True).

FastHTML routes are asynchronous by default, meaning you can declare them with async def if you need to perform await operations (database calls, etc.). If your function is async, FastHTML will await it. If it’s sync, FastHTML will run it in a threadpool automatically when needed (inherited Starlette behavior). For simple CPU-bound tasks, regular def is fine.

Accessing Request Data: FastHTML automatically passes the underlying Starlette Request object to your handler if you include a parameter named req (or request) ￼. For example:

@rt
def show_headers(req):
    return Pre(str(req.headers))

Including a request parameter (or any prefix like req) will inject the request. Similarly, to work with cookies or server sessions, you can include a parameter named session (or sess) ￼. FastHTML uses Starlette’s signed cookie-based session middleware by default, so session behaves like a dictionary for per-client data (you can set values and they persist via cookies) ￼ ￼.

There are also convenience functions:
	•	cookie(name, value) to set a cookie value in the response ￼ ￼.
	•	RedirectResponse(url) to redirect the client to a new URL. You can return a Starlette RedirectResponse (or any Starlette Response) directly from a handler and FastHTML will use it as-is ￼.
	•	HTTPException(status_code, detail) can be raised to immediately send an error response (like 404 or 400). This works the same as in FastAPI/Starlette. For example, raise HTTPException(404, "Not found").

Generating URLs: When linking between pages or submitting forms to other routes, you can hardcode paths (e.g. A("Go", href="/some/path")), but FastHTML provides a safer way. Every route function is given a .to() method that generates its URL with query parameters properly encoded ￼ ￼. For example, if you have def toggle(id: int): ..., you can use toggle.to(id=42) which might produce "/toggle?id=42" ￼. This is handy for ensuring URLs stay in sync with your code (especially if you later change a route’s name or signature – your .to() calls will update accordingly).

You can even pass route functions directly as attributes in components, and FastHTML will convert them to their path. For instance, Button("Delete", hx_post=delete_item) will transform to something like <button hx-post="/delete_item">Delete</button> automatically ￼ ￼. (Under the hood, FastHTML detects when a function is used in an attribute and calls .to() on it ￼ ￼.)

Organizing Routes: For larger projects, FastHTML supports grouping routes across files. You can mount sub-apps or use an APIRouter similar to FastAPI’s. One approach is using Starlette’s Mount to attach an app at a subpath ￼ ￼. Another approach is FastHTML’s APIRouter class which lets you define routes in a separate module and then integrate them into the main app ￼ ￼. For example, you might define products_router = APIRouter() in one file, use @products_router for its routes, then do products_router.to_app(app) in your main file ￼ ￼. This attaches all routes from the router into the main app. This is optional, but useful to keep your code modular as your app grows.

Handling Forms and User Input

Dynamic web apps require handling user input – typically via HTML forms or AJAX requests. FastHTML simplifies form handling by binding form fields directly to Python parameters or dataclasses, without requiring separate form-parsing logic.

HTML Forms: You can create forms using FastHTML components. The library provides tags like Form, Input, Textarea, Select, Button, etc., which behave like their HTML counterparts. For example:

form = Form(method="post", action="/submit")(
    Fieldset(
        Label("Name", Input(name="name")),
        Label("Email", Input(name="email", type="email"))
    ),
    Button("Submit", type="submit")
)

This would produce an HTML form with two input fields and a submit button. In FastHTML, a Form(...) component is actually callable – calling it with child components attaches them inside the form (this is a quirk of how FT components can be used either as Form(..., children...) or Form(...)(children...) for readability) ￼ ￼.

Binding form data: On the server side, FastHTML can automatically parse form submissions. If you define your route to accept a dataclass or other structured type, FastHTML will convert form fields into that object for you ￼ ￼. For instance:

from dataclasses import dataclass

@dataclass
class Profile:
    name: str
    email: str
    age: int

@rt('/', methods=['get','post'])
def profile(data: Profile = None):
    if data is None:
        # GET request: show form
        return Form(
            Label("Name", Input(name="name")), 
            Label("Email", Input(name="email", type="email")),
            Label("Age", Input(name="age", type="number")),
            Button("Submit", type="submit"),
            method="post", action="/"
        )
    else:
        # POST request: data is a Profile object parsed from the form
        return Div(
            H1("Profile Submitted"),
            P(f"Name: {data.name}"),
            P(f"Email: {data.email}"),
            P(f"Age: {data.age}")
        )

In this example, when the form is submitted (POST), FastHTML will instantiate a Profile from the form fields (matching by field name) and pass it as the data argument ￼ ￼. If any field is missing or of the wrong type, it might raise a validation error or 400 automatically. Under the hood, FastHTML uses Starlette’s request data parsing to get form inputs and then Pydantic-like logic to create the dataclass instance ￼. This pattern eliminates a lot of boilerplate – you don’t have to manually do request.form() or construct objects by hand.

Form validation: You can always add custom validation logic. If something is wrong with input, you can raise an HTTPException(400, "Error message") to send a 400 Bad Request with an error detail ￼ ￼. For example:

@rt('/register', methods=['post'])
def register(user: UserForm):
    if "@" not in user.email:
        raise HTTPException(status_code=400, detail="Invalid email")
    # ...proceed to create user...
    return P("Thanks for registering!")

If an exception like this is raised, FastHTML (Starlette) will catch it and return an error response with that status code and detail. You can customize exception handling globally as well (for instance, to show a nicer error page) ￼ ￼, but by default a JSON error message or simple text will be returned for such exceptions.

Dynamic interactions (without full page refresh): Often you want to update part of a page in response to input without reloading everything. This is where HTMX comes in, which FastHTML deeply integrates. We’ll cover that in the next section.

Before moving on, note that FastHTML also seamlessly supports JSON input. If you send a JSON payload to a route (e.g. via fetch or client-side script) and your route expects a Pydantic model or dataclass, it can similarly deserialize JSON into that object (since Starlette will populate request.json()). The usage is analogous to form handling.

File uploads: To handle file uploads, use the UploadFile type for your route parameter (just like Starlette/FastAPI) ￼ ￼. For example:

@rt
async def upload(file: UploadFile):
    content = await file.read()  # read file content
    save_path = Path("uploads") / file.filename
    save_path.write_bytes(content)
    return P(f"Uploaded {file.filename} ({file.size} bytes)")

If an <input type="file" name="file"> is present in a form, FastHTML will detect it and provide an UploadFile object. Make sure to mark the handler async for reading/writing files so as not to block other requests ￼ ￼. For multiple file inputs (multiple="true"), use a parameter type list[UploadFile]. FastHTML (via Starlette) will give you a list of files.

Adding Interactivity with HTMX

One of the most powerful aspects of FastHTML is how it enables dynamic, single-page-app-like behavior without writing JavaScript. This is achieved through integration with HTMX, a lightweight JavaScript library that allows HTML elements to send AJAX requests and swap in server responses. FastHTML embraces this “hypermedia” approach: your server can send fragments of HTML to update the page, triggered by user actions, instead of rendering everything upfront or using a heavy client-side framework ￼ ￼.

HTMX attributes: Any FastHTML component supports the special hx_* attributes which correspond to HTMX directives. For instance:
	•	hx_get="/some/url" – when this element is clicked (if it’s e.g. an <a> or <button>), perform an AJAX GET to /some/url and replace the element with the response.
	•	hx_post="/save" – on form submission or click, POST to /save.
	•	hx_target="#result" – designate a target element whose content should be replaced with the response.
	•	hx_swap="outerHTML" – control how the returned fragment is inserted (replace outer HTML, inner HTML, etc.).

You can use these in FastHTML by supplying them as keyword args, e.g. Div("Click me", hx_get="/change") ￼ ￼. Underscores will become hyphens (hx_get -> hx-get in the rendered HTML).

Example – Click to update: Let’s augment our “Hello, World” with a simple interactive behavior. We’ll make the message change when clicked:

@rt('/')
def home():
    # A paragraph that will update itself when clicked
    return P('Hello, World!', id='msg', hx_get="/change")

@rt('/change')
def change_message():
    # Return a new paragraph content
    return P('Nice to be here!', id='msg')

Here, the paragraph has an hx_get="/change" attribute, meaning when you click it, the browser will issue a GET request to /change (via HTMX) and replace the paragraph with whatever HTML is returned ￼ ￼. Our /change route returns a new <p> with the same id. The result: when a user clicks “Hello, World!”, it seamlessly changes to “Nice to be here!” without a full page reload. This works because by default HTMX swaps the target element with the returned snippet (since we didn’t specify hx_target, it targets the element itself).

FastHTML’s response handling is smart about HTMX requests. HTMX sends an HX-Request: true header on AJAX calls; FastHTML detects this and can send HTML partials (fragments) instead of full pages ￼ ￼. In practice, you usually just return the component(s) that need to be updated. If the request is HTMX-driven, FastHTML will skip sending the outer HTML boilerplate, and HTMX will merge the fragment into the page DOM. This makes it trivial to build rich interactions: click a button -> server computes new data -> returns a snippet (like a new table row or a status message) -> page updates in place.

More complex interactions: You can attach HTMX triggers to forms, buttons, links, etc. For example, a common use-case is a form that submits via AJAX and displays a result without redirect:

form = Form(Input(name="term"), Button("Search", type="submit"),
            hx_post="/search", hx_target="#results")

This form will POST to /search and insert the returned snippet into the element with id=“results”. Your /search handler can just return a <div id="results">...</div> with the results. This pattern avoids writing any JS for most interactive behaviors (submitting forms, loading more content, confirmations, etc.).

Client-side scripting: If needed, you can include custom JavaScript. FastHTML provides a Script() component to embed scripts. You can either reference an external script by Script(src="...") or inline code by Script("console.log('hi')") ￼ ￼. For example, to include an external library:

app, rt = fast_app(hdrs=[Script(src="https://cdn.plot.ly/plotly-2.32.0.min.js")])

This adds the Plotly.js library to the page’s <head> on every load ￼ ￼. Then you can return components that use it, or even generate a <Script> on the fly in a route to execute some code (like initializing a chart). As another example, FastHTML’s own documentation shows integration with Fabric.js (for a drawing app) – simply include the library via a script tag and then you can use its API in your HTMX handlers.

Tip: Prefer solving interactions with HTMX and minimal JS when possible. FastHTML strongly encourages server-driven interactions – you often don’t need custom JS for things like showing/hiding elements, refreshing content, etc. In cases where JS is needed (e.g. a custom widget or using a specific JS UI library), you can absolutely include it. Just avoid frameworks that clash with server-driven DOM updates (React/Vue which assume full control of DOM) ￼. Libraries that enhance static HTML (charts, maps, editors) work great with FastHTML.

Handling events: HTMX covers a wide range of events (click, change, etc.). You can also use hx-on attributes to handle client-side events in-line. FastHTML has a shortcut for writing these in Python: use a double underscore in attribute names to indicate event names. For example, hx_on__after_request="this.reset()" in Python will become hx-on-after-request="this.reset()" in HTML, which means “after the HTMX request is completed, run this.reset() on the element” ￼ ￼. This is useful for resetting forms after submission, etc. The FastHTML best practices suggest using the newer HTMX event syntax (with dashes instead of colons) and demonstrate the attribute naming conversion with underscores ￼.

Out-of-band swaps and WebSockets: HTMX supports “out of band” (OOB) responses and a WebSocket extension. FastHTML provides utilities for these advanced cases as well:
	•	If you return a fragment wrapped in a <turbo-stream> or with a specific HX trigger, you can update multiple parts of the page. (Detailed usage is beyond this introduction.)
	•	For WebSockets, FastHTML has built-in support via the @app.ws() decorator and helper functions like setup_ws() to integrate with HTMX’s ws extension ￼ ￼. We’ll touch on WebSockets in a later section.

In short, FastHTML + HTMX lets you build interactive frontends where the server is in control of UI state. You can achieve SPA-like user experiences (e.g. dynamic content loading, infinite scroll, real-time updates) without the complexity of managing a client-side framework.

Database Integration and State Management

Most web apps need to store and retrieve data. FastHTML is database-agnostic – you can use any Python database library or ORM. However, for convenience it includes FastLite, a lightweight ORM designed for SQLite (and potentially other databases via the MiniDataAPI spec) ￼. FastLite allows you to define data models as simple Python classes and get a table interface with minimal code.

Using FastLite (SQLite): FastHTML’s fasthtml.common actually re-exports FastLite utilities for convenience. You can create or connect to a database with database(path) (from fastlite) ￼ ￼, then define classes to represent tables:

from fasthtml.common import *  # includes fastlite
db = database('data/app.db')   # connect to a SQLite database file (it will be created if not exists)

class Todo:
    id: int
    title: str
    done: bool = False

todos = db.create(Todo)  # create table 'todo' if not exists, with columns id, title, done [oai_citation:139‡fastht.ml](http://www.fastht.ml/docs/ref/best_practice.html#:~:text=After%3A) [oai_citation:140‡fastht.ml](http://www.fastht.ml/docs/ref/best_practice.html#:~:text=class%20Todo%3A%20id%3Aint%3B%20task%3Astr%3B%20completed%3Abool%3B,create%28Todo)

A few things happen here:
	•	We declared a simple class Todo with type hints for fields. FastLite interprets this as a schema definition. The optional assignment done: bool = False sets a default value.
	•	db.create(Todo) creates a table based on this class (if it isn’t already created) and returns a table object (todos). The table object can be used as a callable to query all records, or to insert/update/delete records via methods ￼ ￼.
	•	The id field is automatically used as the primary key (since we didn’t specify otherwise). FastLite’s create() is idempotent – if the table exists, it just returns the table object without modifying data ￼ ￼.

Now todos acts like a collection of Todo objects:

todos.insert(title="Write documentation")     # Insert a new todo (returns the new Todo object) [oai_citation:145‡fastht.ml](http://www.fastht.ml/docs/ref/best_practice.html#:~:text=%40rt%20def%20add,isoformat) [oai_citation:146‡fastht.ml](http://www.fastht.ml/docs/ref/best_practice.html#:~:text=return%20todo_item%28todos)
todos.insert(title="Build FastHTML app", done=True)
all_items = todos()                          # Get all todos as a list of Todo objects [oai_citation:147‡fastht.ml](http://www.fastht.ml/docs/ref/concise_guide.html#:~:text=User) [oai_citation:148‡fastht.ml](http://www.fastht.ml/docs/ref/concise_guide.html#:~:text=)
one = todos[1]                               # Fetch todo with primary key 1 [oai_citation:149‡fastht.ml](http://www.fastht.ml/docs/ref/concise_guide.html#:~:text=,user.id) [oai_citation:150‡fastht.ml](http://www.fastht.ml/docs/ref/concise_guide.html#:~:text=Test%20if%20a%20record%20exists,keyword%20on%20primary%20key)
todos.update(id=1, done=True)                # Update fields on todo with id=1 (returns updated object) [oai_citation:151‡fastht.ml](http://www.fastht.ml/docs/ref/concise_guide.html#:~:text=Updates%20,return%20the%20updated%20record) [oai_citation:152‡fastht.ml](http://www.fastht.ml/docs/ref/concise_guide.html#:~:text=user)
if 1 in todos:                               # Check existence by PK [oai_citation:153‡fastht.ml](http://www.fastht.ml/docs/ref/concise_guide.html#:~:text=Test%20if%20a%20record%20exists,keyword%20on%20primary%20key) [oai_citation:154‡fastht.ml](http://www.fastht.ml/docs/ref/concise_guide.html#:~:text=1%20in%20users)
    todos.delete(1)                          # Delete by primary key [oai_citation:155‡fastht.ml](http://www.fastht.ml/docs/ref/concise_guide.html#:~:text=Deleting%20by%20pk%3A) [oai_citation:156‡fastht.ml](http://www.fastht.ml/docs/ref/concise_guide.html#:~:text=users)

FastLite returns dataclass-like objects for each record. In fact, you can get the actual dataclass type via Todo = todos.dataclass(), or define the class with a dataclass decorator from the start. The returned objects support attribute access (e.g. one.title, one.done) and even have nice reprs.

FastLite also provides query helpers:
	•	todos(order_by='name', limit=10, where="done=1") etc., to filter or sort results ￼ ￼.
	•	Parameterized queries: todos("name=?", ("Write documentation",)) as a secure way to query ￼ ￼.
	•	.xtra() to set a default filter on all queries (for multi-tenancy or soft-deletes) ￼ ￼.

For more complex database needs, you might integrate SQLAlchemy or another ORM. FastHTML doesn’t interfere with that – you can use them as you normally would in any async Starlette app. In fact, there’s a companion library fastsql (not detailed here) that helps integrate SQLAlchemy if needed ￼.

Using databases in routes: Because FastHTML routes can be sync or async, you should be mindful of how you access the DB. If using an async database client (like an async ORM or direct async SQL client), declare your route as async def and await the DB calls. If using FastLite (which is sync with a thread-safe SQLite driver) or an ORM like SQLAlchemy (sync), you can use normal functions – just know that heavy queries could benefit from being run in a thread executor. Starlette will by default offload sync route handlers to a thread pool, so it’s usually fine.

Example: Todo list route using FastLite:

@rt
def list_todos():
    items = todos(order_by="id DESC")
    return Ul(*[Li(f"{'✅' if t.done else '🔲'} {t.title}") for t in items])

This route fetches all todos (most recently added first) and returns an unordered list. We use a list comprehension to turn each Todo into an Li element, marking done items with a checkbox character. FastHTML can take an iterable of components directly – we could also do Ul(*map(todo_item_component, items)) without converting to list, since FastHTML will accept a generator or map object and iterate over it ￼ ￼.

Sessions and server state: For small-scale state (like tracking user preferences, or storing non-critical data), you can use FastHTML’s session (which is basically a signed client-side cookie store). Use the session parameter in routes as described earlier to read/write session data ￼ ￼. For example:

@rt
def visit_counter(session):
    session['count'] = session.get('count', 0) + 1
    return P(f"Visit count: {session['count']}")

This will update a counter each time the route is hit. The session data is stored in the user’s cookie (encrypted) up to a certain size.

For anything beyond trivial usage, a real database or cache is recommended (sessions are often just used for auth, etc.). FastHTML doesn’t include a built-in cache/store aside from sessions, but you can use Redis or other systems as you would in any Python web app.

Background Tasks

Sometimes you need to perform work after sending a response – for example, sending an email, processing a file, or any long-running job that the user doesn’t need to wait for. FastHTML provides a simple way to do this via background tasks, leveraging Starlette’s background task support ￼ ￼.

A background task is essentially a function that will run after the response is sent. You attach it to the response, and FastHTML/Starlette will execute it asynchronously.

Example – simple background task:

from starlette.background import BackgroundTask

@rt
def index():
    def count_slowly(n):
        for i in range(n):
            print(i)
            time.sleep(1)
    task = BackgroundTask(count_slowly, n=5)
    return Titled("Background Task Example"), task

In this example, when a user visits the page, they immediately get the response (a title saying “Background Task Example”). Meanwhile, on the server, the count_slowly(5) function will execute in the background, printing numbers 0 to 4 with a delay ￼ ￼. The user doesn’t see this directly, but it could have been something like sending emails or crunching data. Key points:
	•	We created a BackgroundTask object, giving it the function and arguments to execute later ￼ ￼.
	•	We returned a tuple of (FT components, task). FastHTML recognizes this pattern: if the return value of a route is a tuple where one element is a BackgroundTask, it will set up the task to run after sending the response ￼ ￼.
	•	The user’s browser isn’t kept waiting for the task to finish.

This makes the UI snappier for operations that can be deferred. For example, if a user triggers a heavy computation, you might immediately return a page saying “Your request is being processed” and run the computation as a background task, then use some mechanism (email, WebSocket, polling) to inform the user when it’s done ￼ ￼.

More realistic example: Suppose a user uploads a dataset and you need to run analysis on it. You want to acknowledge the upload instantly and process data after. You could do:

@rt
def upload(file: UploadFile, session):
    # Save file to disk
    filepath = save_upload(file)
    # Kick off background processing
    task = BackgroundTask(analyze_file, path=filepath, user=session.get('user_id'))
    return Div(P("File received! Analysis will be ready soon.")), task

Here analyze_file would be a function (maybe defined elsewhere) that takes the file path and does heavy lifting (and perhaps stores results in a database or sends a notification). The response is returned immediately along with the task.

FastHTML’s background tasks are powered by thread or event loop scheduling (Starlette will use an event loop task for async functions or a thread for sync ones). They are not meant as a full-fledged task queue (for very long tasks or tasks that must survive process restarts, you’d use something like Celery or an external job queue). But for moderate tasks, they work great.

Multiple tasks: You can attach multiple background tasks by combining them (Starlette’s BackgroundTasks container can hold several). FastHTML will run all of them. In practice, if you need multiple, you can instantiate tasks = BackgroundTasks() and do tasks.add_task(func1, ...), tasks.add_task(func2, ...) and return that. (Or simply call one task function from another if order/sequencing is needed.) ￼ ￼

WebSockets and Real-Time Updates

FastHTML supports WebSockets to enable truly real-time, bidirectional communication with clients (e.g. chat apps, live dashboards). Under the hood it uses Starlette’s WebSocket support. Additionally, HTMX has an extension for WebSockets which FastHTML can integrate with to do partial page updates over a WebSocket channel.

Basic WebSocket usage: You can define a WebSocket route with the @app.ws(path) decorator. For example:

clients = []  # keep track of connected client WebSocket objects

@app.ws('/ws')
async def websocket_endpoint(ws):
    await ws.accept()
    clients.append(ws)
    try:
        while True:
            msg = await ws.receive_text()
            # Echo the message to all clients
            for client in clients:
                await client.send_text(f"Broadcast: {msg}")
    except WebSocketDisconnect:
        clients.remove(ws)

This low-level example simply echoes any received message to all connected clients (a basic chat broadcast). FastHTML’s FastHTML class inherits Starlette’s WebSocket handling, so this works as it would in Starlette.

However, FastHTML goes further by providing tools to use WebSockets in conjunction with HTMX. HTMX’s ws extension allows you to tie form inputs to WebSocket sends and handle server-sent messages as ordinary DOM swaps. FastHTML can simplify setting that up.

WebSocket with HTMX example: From the documentation, an example of a live updating UI:

app, rt = fast_app(exts='ws')  # enable HTMX WebSocket extension [oai_citation:180‡fastht.ml](http://www.fastht.ml/docs/ref/concise_guide.html#:~:text=,transfer%20app%2C%20rt%20%3D%20fast_app%28exts%3D%27ws) [oai_citation:181‡fastht.ml](http://www.fastht.ml/docs/ref/concise_guide.html#:~:text=app%2C%20rt%20%3D%20fast_app)

@rt
async def index():
    # Render a page with a form that sends via WebSocket and a div for messages
    return Titled('Chat',
        Div(id='messages'),
        Form(Input(id='chat-input'), hx_ws='send', hx_target="#messages", hx_ext="ws")
    )

async def on_connect(send):
    # Function to run on new connection: send welcome
    await send(Div("🔗 Connected", id="messages"))

@app.ws('/ws', on_connect=on_connect)
async def chat_socket(message: str, send):
    # This function is called when a message is sent from client
    await send(Div(f"💬 {message}", id="messages"))

In this conceptual example (not full code), we set up the app with exts='ws' which makes HTMX’s websocket JavaScript available ￼ ￼. The form in the index has hx_ws="send", meaning “on submit, send the input value through WebSocket rather than regular AJAX” ￼. The hx_target="#messages" tells HTMX to put incoming messages into the messages div.

The @app.ws('/ws') route is the WebSocket handler. We passed an on_connect callback to send an initial message to the client upon connection ￼. The handler itself is defined to take message: str and a send function. FastHTML’s WebSocket support can automatically parse JSON messages or plain text into parameters (here we expect a string message). We can then await send(component) to push an update to the client. The FastHTML send will actually queue an out-of-band HTMX swap – effectively sending an HTML fragment that HTMX will insert into the page ￼ ￼. In this case, every time a message is received, we broadcast a new <div> with the message text into the #messages list.

The above pattern enables reactive updates: multiple clients connected to the same WebSocket endpoint can all receive updates (if you store their connections and loop through to send). For example, a collaborative drawing or game could broadcast moves to all players.

Server-Sent Events (SSE): In addition to WebSockets, FastHTML supports HTMX’s SSE extension (server-sent events) for one-way push updates ￼ ￼. SSE is simpler than WebSockets (just server push, no client -> server messages except via normal requests). You can integrate SSE by including the HTMX SSE script and using HtmxResponseHeaders to push events. This is a bit advanced, but know that if you need push but not full duplex, SSE might be an option. FastHTML documentation provides an example where they use setup_sse to stream events.

In summary, FastHTML gives you the tools to make truly real-time apps: whether via polling (simple, with HTMX), WebSockets (for interactive back-and-forth), or SSE. Combined with background tasks or periodic jobs, you can push updates to the UI as they happen. For instance, a live dashboard can be built where the server periodically sends new data points to the front-end via WebSocket, and you update a chart – all in Python aside from perhaps a small JS chart library for rendering ￼ ￼.

Authentication and Security

For authenticating users and protecting routes, FastHTML leverages standard approaches from the Starlette/FastAPI world, and also includes some convenient helpers.

Session-based auth: The simplest form of auth is using sessions (cookies). For example, after a user logs in (via your own logic or OAuth), you could store session['user_id'] = .... Then, to guard routes, you can use a beforeware or decorator that checks for that session value and redirects or denies access if not present.

FastHTML supports beforeware – functions that run before every request or specific routes. You can supply a before=Beforeware(func, skip=[...]) when creating the app ￼ ￼. For example:

from fasthtml.common import Beforeware

def auth_check(req, sess):
    if sess.get('user_id') is None:
        return RedirectResponse('/login', status_code=303)

app, rt = fast_app(before=Beforeware(auth_check, skip=['/login', '/signup', '.*\.css']))

Here, auth_check runs on each request; if no user_id in session, it redirects to login page ￼ ￼. We skip the login and static file routes so those can be accessed freely. This is a simple way to protect many routes at once.

You can also create route-specific decorators for auth. For instance:

from functools import wraps

def require_token(f):
    @wraps(f)
    async def wrapper(req):
        token = req.headers.get("Authorization")
        if token != "SECRET123":
            return Response("Not authorized", status_code=401)
        return await f(req)
    return wrapper

@rt('/secure')
@require_token
async def secure_data(req):
    return P("Sensitive data here.")

This pattern is similar to standard Python decorators – it checks something and either short-circuits or calls the original function ￼ ￼. In this case we looked for a header token. You could adapt it to check session or anything else. FastHTML allows stacking multiple such decorators if needed (just remember to handle async appropriately by making the wrapper async def if the inner function is async, as shown above) ￼ ￼.

OAuth (Social Login): FastHTML includes a module fasthtml.oauth that greatly simplifies implementing OAuth “Login with X” flows for providers like Google, GitHub, Discord, HuggingFace, etc. You can use the provided OAuth client classes and an OAuth helper class.

Basic outline:
	1.	Create an OAuth client instance with your app’s client ID/secret for the provider (e.g. GoogleAppClient(id, secret) ) ￼ ￼.
	2.	Subclass fasthtml.oauth.OAuth and override the get_auth() method to define what to do when a user successfully logs in (e.g. create a user in your database, or decide if the user is allowed) ￼ ￼.
	3.	Instantiate your OAuth subclass with the FastHTML app and the client. This will auto-set up redirect and logout routes and a beforeware that protects routes by default ￼ ￼.
	4.	Provide a login route (where you send users if not logged in) that perhaps just shows a “Log in with X” link, which you can get via oauth_instance.login_link(request) ￼ ￼.

For example (simplified):

from fasthtml.oauth import GitHubAppClient, OAuth as FastHTMLOAuth

client = GitHubAppClient(os.getenv('GH_CLIENT_ID'), os.getenv('GH_CLIENT_SECRET'))

class Auth(FastHTMLOAuth):
    def get_auth(self, info, ident, session, state):
        # This is called after OAuth provider confirms login
        session['user_id'] = info.id  # maybe store GitHub user ID
        return RedirectResponse('/', status_code=303)

oauth = Auth(app, client)

@rt('/login')
def login_page(req):
    return Div(A("Log in with GitHub", href=oauth.login_link(req)))

Once a user clicks the login link, they go through GitHub, and GitHub will redirect back to FastHTML’s built-in /redirect route (provided by Auth(app, client)). The get_auth method is then called with user info; we stored the user and redirected home ￼ ￼. The Auth base class has default behavior that, for example, will redirect any not-logged-in user hitting a protected page to /login automatically ￼ ￼ (this is set up by the internal beforeware when we initialized Auth). There are more details (like logout_path, error handling, state tokens for security, etc.), but the takeaway is: FastHTML makes common OAuth flows very straightforward, often just a few lines of configuration.

CSRF and security considerations: Since FastHTML relies on HTMX and form submissions for state changes, typical CSRF protection might involve setting and checking an anti-CSRF token. Currently, FastHTML doesn’t document a built-in CSRF solution; however, HTMX by default only issues same-site requests, and you can use SameSite cookies for session. If needed, you can manually implement CSRF by adding a hidden token field and verifying it in handlers.

On the plus side, fewer moving parts (no separate front-end forms or complex state) can mean fewer vulnerabilities. Just remain mindful of common issues: validate user input (especially if inserting into the DOM – FastHTML escapes strings by default to prevent injection, unless you wrap content in Safe() or NotStr to deliberately include raw HTML ￼). Also, use HTTPS in production so that cookies and data are secure in transit.

Testing FastHTML Apps

Testing your FastHTML application is straightforward because the framework is built on Starlette, and everything is just Python code (no magic template rendering step). You can use Starlette’s TestClient to simulate requests to your routes in memory ￼ ￼.

Unit testing components: Since FT components are Python objects, you can test them without even running a server. For example, if you have a function Card(title, body) that returns a Div, you can call result = Card("X", "Y") in a test and verify that to_xml(result) produces the expected HTML string, or that result has children of certain types, etc. This is a big advantage over string-templating: you can construct and inspect components directly in tests ￼.

Integration testing with TestClient: The starlette.testclient.TestClient works with FastHTML’s app object. Example:

from starlette.testclient import TestClient

client = TestClient(app)  # `app` is our FastHTML app
resp = client.get("/?q=hello")
assert resp.status_code == 200
assert "Hello" in resp.text

This spins up a lightweight test ASGI server in the same process and sends a GET request to /. The response .text contains the full HTML (or partial HTML if the route returns a fragment). You can test specific behaviors, e.g.:
	•	HTMX requests: Include the header HX-Request: 1 in the client request to simulate an AJAX call. For instance:

resp = client.get("/change", headers={"HX-Request": "1"})

Then resp.text should contain just the snippet (no <html><head> wrapper) that your /change route returns ￼ ￼.

	•	Form submissions: You can simulate POSTing form data by using client.post(url, data={"field": "value"}). Starlette will encode it as form data. If your route expects a dataclass, it will receive the filled object. You can then assert on the response or on side effects (like database changes).
	•	JSON APIs: Similarly, use client.post(url, json={"key": "val"}) if your route consumes JSON.
	•	Sessions/cookies: The TestClient will handle cookies. For example, after one request you can check client.cookies or include cookies in subsequent calls to simulate a logged-in session.

Example test:

def test_todo_creation():
    client = TestClient(app)
    # Simulate adding a todo via form post
    resp = client.post("/add_todo", data={"task": "Buy milk"})
    assert resp.status_code == 200
    # After adding, fetch the list page
    list_resp = client.get("/todos")
    text = list_resp.text
    assert "Buy milk" in text  # the task should appear in the HTML list

This tests that posting the form triggers the creation and that the new item appears in the listing.

Because FastHTML’s app object is a Starlette app, you can also use Starlette’s TestClient context manager to test lifespan events or background tasks. For example, if you want to ensure a background task ran, you might insert a short delay or polling in the test, or better, design the task to signal completion (perhaps by writing to the database which you can then check).

FastHTML doesn’t introduce new testing frameworks; you use standard Python test tools. The key is that since there are no separate front-end codebases or templating systems, you can cover a lot of ground with simple Python tests.

Deployment

FastHTML apps are just Python ASGI applications, which means you have a lot of flexibility in deployment. You can run them on any hosting that supports Python web services. Here are some notes and options:
	•	Uvicorn/Gunicorn: In production, you can treat FastHTML like a Starlette app. For example, using Gunicorn with Uvicorn workers: gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000. This will serve your app on port 8000. Ensure to set appropriate number of workers/threads for your needs.
	•	Railway.app: FastHTML has first-class support for deploying to Railway (a popular cloud hosting). In fact, the FastHTML package comes with a CLI tool to streamline this. After installing the Railway CLI and logging in ￼ ￼, you can simply run:

fh_railway_deploy MyAppName

in your project directory. This command will create or connect to a Railway project, deploy your code, and even set up a persistent volume for data at /app/data by default ￼ ￼. It prints the deployed app URL at the end ￼ ￼. (Note: your main file should be named main.py for this to work by convention ￼.) You can add environment variables (like API keys) on Railway’s dashboard and they’ll be available in os.environ within your app ￼ ￼.

	•	Vercel: You can deploy FastHTML on Vercel via their Python serverless support. Typically you would create a api/index.py (or similar) that exposes the app as a module-level variable. The FastHTML team has mentioned one-click deploys to Vercel as well ￼.
	•	Hugging Face Spaces: FastHTML apps can run on Spaces (which use Gradio/Streamlit under the hood) by selecting a “Python – Starlette” template. The docs include a guide with a template repository ￼. Essentially, as long as you have a app = FastHTML() in a script, Spaces can serve it.
	•	Replit: There is an example Repl you can fork which has FastHTML configured ￼. On Replit, you might need to add a replit.toml or .replit config to specify how to run the app (uvicorn main:app --reload) ￼. Once running, you can use Replit’s web view or deploy feature.
	•	Traditional VPS or servers: Just treat it like any other ASGI app. For instance, using Docker: your Dockerfile would install python-fasthtml and then run Uvicorn. Or using NGINX+Uvicorn on a VM is straightforward.

No matter the platform, remember FastHTML is essentially a Starlette app. So any deployment strategy for Starlette/FastAPI will apply. You may need to configure environment variables like PORT (FastHTML’s serve() respects a PORT env var if provided, otherwise defaults to 5001). On some platforms (like Heroku or Fly.io), ensure you bind to the port they assign.

Static files: By default, FastHTML will serve static files (like CSS/JS/images) that are in your application directory if referenced with standard extensions (e.g. a file style.css in the same folder can be linked and FastHTML/Starlette will serve it) ￼. You can configure the static directory via fast_app(static_path="...") if needed. If deploying to a CDN or separate static host, you might instead build your static assets and serve them externally, but for simplicity, including them in your app should work.

Secrets and config: Use environment variables (accessible via os.environ) for things like database URLs, API keys, etc., and set them in your hosting platform’s configuration. FastHTML itself doesn’t have a special config system – it’s standard Python.

To recap deployment options:
	•	One-click style: Railway, Replit, Spaces, etc., are very quick and FastHTML provides examples for each ￼ ￼.
	•	Cloud VM/Kubernetes: Containerize the app or use a process manager. Since FastHTML apps run on Uvicorn, they are comparable to FastAPI deployment.

Lastly, FastHTML’s footprint is small – apps start fast and can run on modest resources. Just ensure if you use SQLite (FastLite) in a multi-instance environment to be mindful of concurrency (SQLite is file-based; for multiple app instances consider using Postgres or similar via an ORM).

Best Practices and Tips

FastHTML encourages a highly concise and pragmatic coding style (influenced by the fast.ai philosophy). Here are some best practices and tips to write clean FastHTML apps, distilled from the official recommendations and common patterns:
	•	Leverage Pythonic constructs: Write logic in expressions when possible. Use list comprehensions or generator expressions directly in components instead of manual loops. FastHTML components accept iterables, so you can pass a generator to a Div() or Ul() without unpacking it ￼ ￼. For example, Ul(todo_item(t) for t in todos()) is perfectly fine and avoids creating an intermediate list.
	•	Prefer query parameters over path parameters: As discussed, use query strings (?id=42) instead of embedding IDs in the URL path unless there’s a good reason ￼ ￼. It makes routes simpler and more flexible.
	•	Use route function names for routing: Let @rt infer the route name from the function name to reduce repetition. Use index() for the home page route ￼ ￼. This not only saves typing but also means if you rename the function (thus the URL), any route_func.to() links will automatically update.
	•	Use route_func.to(...) for constructing URLs: Never hardcode URLs that include variable parts. The .to() method ensures you build correct links and can catch errors (type checked) at development time ￼ ￼.
	•	Minimize glue code: Many things can be returned directly without extra steps. For example, if a database insert function returns the created object, you can return render_item(db.insert(...)) instead of assigning to a variable and then returning ￼ ￼. If a handler doesn’t need to return anything, you can just perform the action and return None (FastHTML will send an empty 204 or a default response). Avoid writing "return ''" – returning an empty string triggers a plaintext response, whereas None yields no content (which for an HTMX action might be fine) ￼ ￼.
	•	Take advantage of defaults: FastHTML sets smart defaults to reduce boilerplate. For example, the Titled(title, ...) component automatically wraps content in a container and adds an <h1> title – you don’t need to wrap it in a Div or include your own main header ￼ ￼. The serve() function chooses a default host (127.0.0.1) and port (5001) and checks for __main__ internally – so you can just call serve() at the end of your script without the typical if __name__ == "__main__" block ￼ ￼.
	•	Code style considerations: Embrace the concise fastai coding style if you can – it favors fewer lines, use of the ternary operator, and inlining simple logic in returns, which leads to very compact route functions that are still readable ￼ ￼. For example, you might write a whole POST handler in one line:

@rt def delete_item(id: int): todos.delete(id)

This is clear enough (perform deletion, return nothing which implies success). Use comments or docstrings to clarify if needed, but avoid overly verbose constructs when a simple one-liner will do.

	•	Avoid unnecessary work on each request: If you have expensive computations that don’t depend on user input (e.g. loading a ML model, or a large data file), do it at startup time (outside of route functions) rather than on every request. You can leverage FastHTML’s startup event (since it’s Starlette-based) or simply initialize above in the script.
	•	Use MonsterUI and PicoCSS for styling: Before writing lots of custom CSS, see if the built-in PicoCSS (included by default) covers your needs with its minimalist style. For more complex UI, FastHTML’s MonsterUI extension provides a set of pre-built components and Tailwind-based styles (similar to shadcn/UI library) ￼ ￼. MonsterUI can be installed and used to get things like theming, modal dialogs, etc., without much effort. This keeps you in Python land for UI components instead of writing raw CSS/JS.
	•	POST for state-changing actions: FastHTML by default only allows GET and POST methods (it doesn’t have built-in decorators for PUT/DELETE) – the philosophy is to use GET for reading data and POST for any action that changes state ￼ ￼. Even for things like deletion, using hx-post (with maybe a hidden _method=DELETE if you want to signal it) is preferred over custom verbs. This keeps things simple and aligns with HTML forms (which only support GET/POST).
	•	Real-time updates: If building apps that auto-update (dashboards, games), consider using WebSockets which FastHTML supports natively. This avoids hacks with long-polling. The framework’s integration with HTMX’s ws extension means you can often push updates by simply calling await send(Component) in your Python code and let the front-end update elegantly ￼ ￼.
	•	Study the examples: The FastHTML team provides many example apps (to-do list, chat, games, etc.) in the [fasthtml-examples GitHub repo] ￼. These are gold mines for learning idiomatic usage. They also have an Idiomatic FastHTML App which is a heavily commented reference project ￼. Reading through those can inspire patterns for structuring larger applications.

By following these practices, you’ll write FastHTML code that is not only concise and fast, but also clear and maintainable. Remember that FastHTML is young and evolving – keep an eye on the official docs and community for new patterns and updates. The goal is to remove ceremony and let you focus on your app’s logic ￼ ￼, leveraging smart defaults and Python’s strengths wherever possible.

Conclusion and Next Steps

FastHTML offers a refreshing approach to web development: it lets you build everything from simple pages to complex interactive apps using just Python. In this guide, we covered the full landscape – from basic routing and HTML generation to advanced topics like WebSockets and background tasks. You should now be equipped to start developing with FastHTML, even if you had never heard of it before.

As you proceed, here are some final pointers:
	•	Explore the official examples and source: The creators provide example projects (e.g. a Chatbot app, Pictionary game, To-do app) ￼. Try running those to see FastHTML in action. The FastHTML GitHub repository also includes notebook-based development – many features are developed and demonstrated in Jupyter notebooks, which can be enlightening to read ￼.
	•	Join the community: There is an official FastHTML Discord channel ￼ where you can ask questions, and a growing ecosystem of third-party tutorials and components ￼. Since FastHTML is rapidly evolving (as of 2024-2025), engaging with the community can help you stay up-to-date and get help.
	•	Keep an eye on updates: Not all features are fully documented yet, and new ones are being added. The FastHTML team has noted that things like deeper integrations and more components (MonsterUI, etc.) are on the way ￼. Watch Jeremy Howard’s announcements and the fast.ai forums for news.
	•	Think in terms of hypermedia: If you come from a React or traditional MVC background, there is a mindset shift – instead of building JSON APIs and heavy clients, you’re often sending HTML from the server in small pieces. Embrace it! It can drastically simplify development and debugging (what you see in the browser is exactly what the server sent). And performance can be surprisingly good since modern browsers and networks handle many small requests efficiently ￼.

We hope this guide has made you comfortable with FastHTML. You’ve seen how to set up routes, create interfaces, handle user input, connect a database, secure your app, test it, and deploy it. With these tools, you can quickly prototype and build full-featured web applications. As the FastHTML motto suggests, it’s “the fastest way to create a real web application” ￼ – so go build something awesome with it!

Happy coding with FastHTML! 🚀

Sources: The information and examples in this document were drawn from the official FastHTML documentation ￼ ￼, tutorials, and community resources, as well as third-party guides (e.g. DataCamp’s FastHTML tutorial) ￼ ￼. For further reading, visit the FastHTML official docs and the FastHTML GitHub repo.