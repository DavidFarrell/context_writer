# Blog Writing Tool - Project Context

## Project Overview
We are building a **blog post writing tool** using nbdev and FastHTML. This is NOT a blog rendering platform - it's an internal tool to help compose and manage blog posts through a web interface.

### Core Technologies
- **nbdev**: For literate programming and progressive feature development
- **FastHTML**: Web server framework (Python-only, no JavaScript needed)
- **MonsterUI**: Component library for UI (built on UIKit/FrankenUI)
- **Jupyter Notebooks**: Each notebook implements one feature/module

## Development Philosophy

### Progressive Notebook Development
- Each notebook builds ONE piece of functionality
- Follow the pattern: `01_feature_name.ipynb`, `02_another_feature.ipynb`
- Every notebook should be independently testable
- Use `#| export` to mark code for the library
- Follow Jeremy Howard's testing pattern: function → mock tests → real tests (#| hide)

### Current Project Structure
```
newblog/
├── nbs/              # Notebooks (each adds a feature)
│   ├── index.ipynb   # Project overview & setup
│   ├── 01_*.ipynb    # Feature notebooks (to be created)
│   └── ...
├── newblog/          # Exported Python modules (auto-generated)
├── main.py           # FastHTML server entry point
├── .ruler/           # Always-in-context documentation
└── llm_docs/         # Reference docs (use when needed)
```

## Documentation Strategy

### Context Management
This document, along with all other `.ruler/*.md` files, will be concatenated into your context. You'll see sections for:
- Project context and guidelines (this file)
- FastHTML patterns and MonsterUI components
- API conventions for UI components
- nbdev patterns and testing philosophy

These provide your essential working knowledge for every interaction.

### Additional Reference Documentation (in llm_docs/)

**IMPORTANT: When you encounter something you don't know how to do with FastHTML, MonsterUI, nbdev, or Quarto, ALWAYS check these docs FIRST before inventing solutions or searching the web.**

These files contain authoritative, tested patterns and examples:

- **llm_docs/fast_html_documentation.md**: Complete FastHTML reference (65KB)
  - Use when: Implementing ANY FastHTML feature not covered in the condensed guide
  - Contains: Full API documentation, deployment guides, advanced patterns, authentication, WebSockets, database integration

- **llm_docs/Quarto_and_nbdev.md**: Publishing and documentation details
  - Use when: Setting up documentation, configuring Quarto, publishing workflows, or any nbdev feature beyond basic usage
  - Contains: nbdev publishing pipeline, Quarto configuration, CI/CD setup, testing strategies

**Required workflow when facing unknowns:**
1. Check if the answer is in your current context (from .ruler/)
2. If not, **IMMEDIATELY** read the relevant llm_docs file: `Read("llm_docs/filename.md")`
3. Only if the answer isn't in llm_docs should you search the web or propose a custom solution
4. Never invent FastHTML/MonsterUI/nbdev patterns without checking documentation first

**Common triggers for accessing llm_docs:**
- User asks for ANY feature you're unsure about
- Implementing authentication, WebSockets, or database operations
- Setting up documentation, testing, or CI/CD
- ANY error or unexpected behavior with these frameworks
- Before writing custom code that might have a framework solution

## MCP Servers Available (Usage Hierarchy)

### fasthtml-tester (PRIMARY - Use First for App Testing)
**Custom FastHTML application testing server** - Purpose-built for this project.

**ALWAYS use this first for:**
- Starting/stopping the FastHTML server (`start_app`, `stop_app`)
- Testing the web application (`navigate_to`, `click_element`)
- Checking application status (`get_app_status`)
- Viewing server logs (`get_server_logs`)
- Viewing browser console logs (`get_console_logs`)
- Any interaction with YOUR FastHTML application

This server manages the entire lifecycle of your FastHTML app and provides integrated browser automation specifically tailored for FastHTML development.

### playwright (SECONDARY - Fallback for General Web)
Generic browser automation tool.

**Use ONLY when fasthtml-tester can't handle the task:**
- Browsing external websites
- Complex browser interactions not supported by fasthtml-tester
- Screenshots or visual regression testing
- Multi-tab/window scenarios
- File downloads from external sites

### gpt5-server  
Advanced language model for content generation.

**Use for:**
- Generating blog post content
- Editing suggestions
- Content analysis and improvement
- Summarization tasks

### nano-banana
Image generation service.

**Use for:**
- Creating blog post illustrations
- Generating visual content
- Image editing and variations

## MCP Server Selection Logic

When you need to interact with the web application:
1. **First**: Try using `fasthtml-tester` MCP server
2. **If that fails or is insufficient**: Fall back to `playwright`
3. **Never**: Use playwright for basic app testing when fasthtml-tester can do it

Example decision flow:
- "Test the blog editor" → Use `fasthtml-tester`
- "Check if the form submits" → Use `fasthtml-tester`
- "Look at the server logs" → Use `fasthtml-tester`
- "Browse to Stack Overflow" → Use `playwright`
- "Take a screenshot of the app" → Try `fasthtml-tester` first, then `playwright` if needed

## Development Guidelines

1. **Start with the notebook**: Always implement features in a notebook first
2. **Test inline**: Write tests immediately after each function (nbdev style)
3. **Export regularly**: Run `nbdev_export()` to keep Python modules in sync
4. **Single file server**: Keep FastHTML server code in `main.py` when possible
5. **Component reuse**: Leverage MonsterUI components before writing custom HTML
6. **Progressive enhancement**: Build features incrementally, one notebook at a time

## Current Task Focus
We're in the early stages. Priority is setting up:
1. Basic FastHTML server structure
2. Initial notebook for data models (blog post structure)
3. Simple UI for creating/editing posts
4. Storage mechanism (likely SQLite via FastLite)

## Key Decisions Made
- Using nbdev (not plain Python) for development
- FastHTML/MonsterUI for all UI (no separate frontend framework)
- Notebooks as primary development environment
- Tool for writing posts, not publishing them
- Progressive feature addition via numbered notebooks

## What NOT to Do
- Don't create a blog rendering/publishing system
- Don't add JavaScript unless absolutely necessary
- Don't create multiple Python files when one notebook will do
- Don't skip inline testing in notebooks
- Don't mix multiple features in one notebook

---

Remember: This tool helps WRITE blog posts through a web interface. The actual blog rendering/publishing is a separate concern not addressed by this project.

<Claude Guidance>
<Writing FastHTML>
# FastHTML Development Guide

## Framework Philosophy

FastHTML is designed for simplicity and developer experience in Python web development:

- **Simplicity over Complexity**: Minimal abstractions between Python and HTML
- **Developer Experience**: Fast feedback loops and intuitive APIs
- **Progressive Enhancement**: Build apps that work everywhere, enhance where possible
- **Python-First**: Leverage Python's strengths instead of fighting against them

## Project Structure

**IMPORTANT**: Prefer single-file applications. Only add files when there's massive benefit.

```
fasthtml-app/
├── main.py           # Main application file (preferred: everything here)
├── components/       # Reusable UI components (only if necessary)
├── routes/          # Route handlers (only for very large apps)
├── static/          # Static assets
├── models/          # Data models (only if complex)
└── README.md        # Project documentation
```

## Core Patterns

### Application Setup

```python
from fasthtml.common import *
from monsterui.all import *

app, rt = fast_app(hdrs=Theme.blue.headers())
```

### Routing

#### Basic Route
```python
@rt
def index():
    return Container(H1("Title"), content)
```

#### Parameterized Routes
```python
@rt
def detail(item_id: str):
    # Access via: detail.to(item_id="123")
    pass

@rt
def action(parent_id: str, child_id: int, action_type: str):
    # Access via: action.to(parent_id="x", child_id=1, action_type="update")
    pass
```

### Database (FastLite)

#### Table Definition
```python
class Record:
    parent_id: str
    child_id: int
    content: str
    metadata: str
    status: str

db = Database('app.db')
db.records = db.create(Record, pk=('parent_id', 'child_id'), transform=True)
```

#### CRUD Operations
```python
# Create
new_record = db.records.insert(Record(...))
# Note: insert() returns the dataclass instance, convert to dict if needed:
# new_record_dict = new_record.__dict__

# Read
record = db.records[parent_id, child_id]  # Single record (may return dataclass)
records = list(db.records.rows_where('parent_id=?', [parent_id]))  # Query
unique_items = list(db.records.rows_where(select='distinct parent_id, content'))  # Distinct

# Update - IMPORTANT: Handle dataclass objects properly
record = db.records[id]
# Convert dataclass to dict for modification
record_dict = record.__dict__ if hasattr(record, '__dict__') else record
record_dict['field'] = new_value
db.records.update(record_dict)

# Delete
db.records.delete(record_id)
```

### HTMX Integration

#### Auto-Save Input
```python
Input(value=record['field'], 
      name='field',
      hx_post=update.to(id=record_id),
      hx_trigger='change')
```

#### Button with Target Update
```python
Button("Action",
       hx_post=process.to(id=item_id, action="approve"),
       hx_target="#result-123",
       cls=ButtonT.primary)
```

#### Dynamic Content Updates
```python
@rt
def update_section(item_id: str, value: str):
    # Process and return HTML to replace target
    return render_updated_content(item_id)
```

## Component Patterns

### Tables from Data
```python
# Build table data
body = []
for item in items:
    body.append({
        'Column1': item['field'],
        'Column2': A("Link", href=detail.to(id=item['id'])),
        'Column3': interactive_component(item)
    })

# Create table
TableFromDicts(['Column1', 'Column2', 'Column3'], body)
```

### Layout Composition
```python
Container(
    H1("Page Title"),
    Card(render_md(content)),  # Card with markdown
    DivLAligned(button1, button2)  # Aligned buttons
)
```

### Interactive Toggle Buttons
```python
def toggle_buttons(parent_id: str, item_id: int = None):
    target_id = f"#toggle-{parent_id}-{item_id}" if item_id else f"#toggle-{parent_id}"
    current_state = db.records[parent_id, item_id].status
    
    def create_button(label: str):
        return Button(label,
            hx_post=update_state.to(parent_id=parent_id, item_id=item_id, state=label.lower()),
            hx_target=target_id,
            cls=ButtonT.primary if current_state == label.lower() else ButtonT.secondary,
            submit=False)
    
    return DivLAligned(
        create_button("Option1"), 
        create_button("Option2"),
        id=target_id[1:])  # Remove # for element id
```

## Styling Reference

### Theme Application
```python
fast_app(hdrs=Theme.blue.headers())
```

### Common Style Classes
- **Buttons**: `ButtonT.primary`, `ButtonT.secondary`, `ButtonT.ghost`
- **Text**: `TextT.muted`, `TextT.sm`, `TextT.bold`
- **Links**: `AT.primary`, `AT.muted`, `AT.reset`
- **Cards**: `CardT.hover`, `CardT.primary`
- **Layout**: `Container`, `DivLAligned`, `DivCentered`, `DivFullySpaced`

## Common Techniques

### Dynamic URLs with Parameters
```python
A("Link Text", 
  cls=AT.primary, 
  href=route_func.to(param1=value1, param2=value2))
```

### Conditional Styling
```python
cls=ButtonT.primary if condition else ButtonT.secondary
```

### HTMX Target IDs
```python
target_id = f"#component-{parent_id}-{child_id}"  # For hx_target
id=target_id[1:]  # For element id (remove #)
```

### Markdown Rendering
```python
render_md(text.replace('\\n', '\n'))
```

## Request Handling

### POST Route Pattern
```python
@rt
def update_field(parent_id: str, child_id: int, field_name: str):
    # FastHTML auto-converts form data to function parameters
    record = Record(parent_id=parent_id, child_id=child_id, field_name=field_name)
    db.records.update(record)
    return render_updated_component()  # Return HTML for HTMX
```

### Component Factory Pattern
```python
def create_interactive_element(data):
    """Reusable component factory."""
    return Component(
        property1=data['field1'],
        property2=data['field2'],
        hx_post=action.to(id=data['id']),
        hx_target=f"#element-{data['id']}")
```

## Best Practices

### Core Principles
1. **URL Generation**: Always use `.to()` method for parameterized routes
2. **Database Keys**: Use compound primary keys for hierarchical data
3. **HTMX Triggers**: `'change'` for inputs, default click for buttons
4. **Target IDs**: Prefix with `#` in hx_target, remove for element id
5. **Component Reuse**: Create factory functions for repeated UI patterns
6. **State Management**: Database as single source of truth
7. **Response Patterns**: Return only updated HTML for HTMX requests
8. **Database Objects**: Always convert dataclass instances to dicts when modifying
9. **HTMX Targets**: Ensure target elements always exist in the DOM

### Component-First Development

```python
# ❌ BAD: Inline everything
@rt
def index():
    return Main(*[Card(H1("Title"), P("Content"), cls="py-6 border-b mb-4") for t,c in items])

# ✅ GOOD: Reusable components
def ContentCard(title, content):
    return Card(title, content, cls="py-6 border-b mb-4")

@rt
def index():
    return Main(*[ContentCard(*item) for item in items])
```

### HTMX Best Practices
- Use `hx_` attributes for dynamic behavior
- Keep responses minimal (return only what changes)
- Use semantic HTML elements
- Let server handle state

## Server Startup

```python
serve()  # Start the FastHTML server
```
</Writing FastHTML>
<Monster UI - for FastHTML>
# MonsterUI Component Library Reference

## Overview

MonsterUI is FastHTML's component library built on top of UIKit and FrankenUI, providing pre-built, customizable UI components following modern design principles.

**Key Principles:**
- Built on UIKit and FrankenUI foundation
- Works seamlessly with Tailwind CSS
- Use Tailwind for spacing (margin, padding, gap)
- Use MonsterUI components for everything else when possible

## Core Import Pattern

```python
from fasthtml.common import *
from monsterui.all import *
from fasthtml.svg import *  # If using icons

# Standard app initialization with theme
app, rt = fast_app(hdrs=Theme.blue.headers())
```

## Component API Reference

### Style Enums

#### Text Styling
- **`TextT`**: Text styles (paragraph, lead, meta, gray, italic, xs, sm, lg, xl, light, normal, medium, bold, extrabold, muted, primary, secondary, success, warning, error, info, left, right, center, justify, start, end, top, middle, bottom, truncate, break_, nowrap, underline, highlight)

#### Button Styling  
- **`ButtonT`**: Button styles (default, ghost, primary, secondary, destructive, text, link, xs, sm, lg, xl, icon)

#### Container Sizing
- **`ContainerT`**: Container max widths (xs, sm, lg, xl, expand)

#### Section Styling
- **`SectionT`**: Section styles (default, muted, primary, secondary, xs, sm, lg, xl, remove_vertical)

#### Link Styling
- **`AT`**: Link/anchor styles (muted, text, reset, primary, classic)

#### List Styling
- **`ListT`**: List styles (disc, circle, square, decimal, hyphen, bullet, divider, striped)

#### Label Styling
- **`LabelT`**: Label/pill styles (primary, secondary, destructive)

#### Navigation Styling
- **`NavT`**: Navigation styles (default, primary, secondary)
- **`ScrollspyT`**: Scrollspy styles (underline, bold)

#### Card Styling
- **`CardT`**: Card styles (default, primary, secondary, destructive, hover)

#### Table Styling
- **`TableT`**: Table styles (divider, striped, hover, sm, lg, justify, middle, responsive)

### Core Components

#### Layout Components

- **`Container`**: Main content wrapper for large sections
- **`Section`**: Section with styling and margins
- **`Grid`**: Responsive grid layout with smart defaults
- **`Button`**: Styled button (defaults to submit for forms)

#### Flexbox Layout Helpers
- **`DivFullySpaced`**: Flex container with maximum space between items
- **`DivCentered`**: Flex container with centered items
- **`DivLAligned`**: Flex container with left-aligned items  
- **`DivRAligned`**: Flex container with right-aligned items
- **`DivVStacked`**: Flex container with vertically stacked items

### Form Components

#### Basic Form Elements
- **`Form`**: Form with default spacing between elements
- **`Fieldset`**: Styled fieldset container
- **`Legend`**: Styled legend for fieldsets
- **`Input`**: Styled text input
- **`TextArea`**: Styled textarea
- **`Radio`**: Styled radio button
- **`CheckboxX`**: Styled checkbox
- **`Range`**: Styled range slider
- **`Switch`**: Toggle switch component
- **`Select`**: Dropdown select with optional search
- **`Upload`**: File upload component
- **`UploadZone`**: Drag-and-drop file zone

#### Form Labels & Combos
- **`FormLabel`**: Styled form label
- **`Label`**: Pill-style labels (FrankenUI)
- **`LabelInput`**: Label + Input combo with proper spacing/linking
- **`LabelSelect`**: Label + Select combo with proper spacing/linking  
- **`LabelRadio`**: Label + Radio combo with proper spacing/linking
- **`LabelCheckboxX`**: Label + Checkbox combo with proper spacing/linking
- **`LabelTextArea`**: Label + TextArea combo with proper spacing/linking

#### Form Helpers
- **`Options`**: Wrap items into Option elements for Select
- **`UkFormSection`**: Form section with title and description

### Navigation Components

- **`NavBar`**: Responsive navigation bar with mobile menu support
- **`NavContainer`**: Navigation list container (for sidebars)
- **`NavParentLi`**: Navigation item with nested children
- **`NavDividerLi`**: Navigation divider item
- **`NavHeaderLi`**: Navigation header item
- **`NavSubtitle`**: Navigation subtitle element
- **`NavCloseLi`**: Navigation item with close button
- **`DropDownNavContainer`**: Dropdown menu container

### Modal & Dialog Components

- **`Modal`**: Modal dialog with proper structure
- **`ModalTitle`**: Modal title element
- **`ModalCloseButton`**: Button that closes modal via JS

### Data Display Components

- **`Card`**: Card with header, body, and footer sections
- **`Table`**: Basic table component
- **`TableFromLists`**: Create table from list of lists
- **`TableFromDicts`**: Create table from list of dictionaries (recommended)

### Icons & Avatars

- **`UkIcon`**: Lucide icon component
- **`UkIconLink`**: Clickable icon link
- **`DiceBearAvatar`**: Generated avatar from DiceBear API

### Utility Functions

- **`render_md`**: Render markdown content with proper styling
- **`apply_classes`**: Apply classes to HTML string


## Common Component Patterns

### Card with Content

```python
def Tags(cats): return DivLAligned(map(Label, cats))

Card(
    DivLAligned(
        A(Img(src="https://picsum.photos/200/200?random=12", style="width:200px"),href="#"),
        Div(cls='space-y-3 uk-width-expand')(
            H4("Creating Custom FastHTML Tags for Markdown Rendering"),
            P("A step by step tutorial to rendering markdown in FastHTML using zero-md inside of DaisyUI chat bubbles"),
            DivFullySpaced(map(Small, ["Isaac Flath", "20-October-2024"]), cls=TextT.muted),
            DivFullySpaced(
                Tags(["FastHTML", "HTMX", "Web Apps"]),
                Button("Read", cls=(ButtonT.primary,'h-6'))))),
    cls=CardT.hover)
```

### Form with Grid Layout

```python
relationship = ["Parent",'Sibling', "Friend", "Spouse", "Significant Other", "Relative", "Child", "Other"]
Div(cls='space-y-4')(
    DivCentered(
        H3("Emergency Contact Form"),
        P("Please fill out the form completely", cls=TextPresets.muted_sm)),
    Form(cls='space-y-4')(
        Grid(LabelInput("First Name",id='fn'), LabelInput("Last Name",id='ln')),
        Grid(LabelInput("Email",     id='em'), LabelInput("Phone",    id='ph')),
        H3("Relationship to patient"),
        Grid(*[LabelCheckboxX(o) for o in relationship], cols=4, cls='space-y-3'),
        LabelInput("Address",        id='ad'),
        LabelInput("Address Line 2", id='ad2'),
        Grid(LabelInput("City",      id='ct'), LabelInput("State",    id='st')),
        LabelInput("Zip",            id='zp'),
        DivCentered(Button("Submit Form", cls=ButtonT.primary))))
```

### Navigation Bar

```python
NavBar(
    A(Input(placeholder='search')), 
    A(UkIcon("rocket")), 
    A('Page1',href='/rt1'), 
    A("Page2", href='/rt3'),
    brand=DivLAligned(Img(src='/api_reference/logo.svg'),UkIcon('rocket',height=30,width=30)))
```

## Quick Reference Guide

### Application Setup

```python
from fasthtml.common import *
from monsterui.all import *

# Basic app setup with theme
app, rt = fast_app(hdrs=Theme.blue.headers())

# With additional features
app, rt = fast_app(hdrs=Theme.blue.headers(), pico=False, live=True, HighlightJS=True)
```

### Database Pattern (FastLite)

```python
from pathlib import Path

# Define data models as simple classes
class Query:
    id: int          # Primary key
    query_text: str
    created_at: str

# Create database and tables
db = database(Path("myapp.db"))
db.queries = db.create(Query, pk='id')

# CRUD operations
db.queries.insert(Query(query_text="test", created_at=datetime.now().isoformat()))
db.queries('query_text=?', ["test"])  # Query with conditions
db.q("SELECT * FROM query WHERE id=?", [1])  # Raw SQL when needed
```

### Routing Pattern

```python
@rt
def index():
    return layout(content)

@rt 
def view_item(item_id: int):
    return layout(item_details)

# Route with parameters
@rt
def save_data(query_id: str, result_id: str, rating: int = 0):
    # FastHTML auto-converts form data to function parameters
    return response
```

### HTMX Integration

```python
# Form submission
Form(
    Input(id="query"),
    Button("Submit"),
    hx_post=search,              # POST to search route
    hx_target="#results",        # Update #results div
    hx_swap="innerHTML"          # Replace content
)

# Dynamic updates
Button("Save", 
    hx_post=save_eval.to(query_id=1, result_id=2),  # Pass parameters
    hx_swap="none")  # No DOM update
```

### UI Components

#### Layout Components
```python
# Navigation
NavBar(
    A("Home", href="/"),
    A("About", href="/about"),
    brand=H3("My App"),
    sticky=True
)

# Container layouts
Container(content)                    # Standard container
DivFullySpaced(left, right)          # Flexbox space-between
DivLAligned(icon, text)              # Left-aligned flex
DivRAligned(buttons)                 # Right-aligned flex
DivCentered(content)                 # Centered content
```

#### Forms
```python
# Styled form inputs
LabelInput("Name", id="name", placeholder="Enter name")
LabelSelect(Option("A"), Option("B"), label="Choose", id="choice")
LabelTextArea("Notes", id="notes", rows="3")
LabelCheckboxX("Agree", id="agree")
LabelRadio("Option 1", name="group", value="1")

# Form structure
Form(
    Grid(
        Div(LabelInput(...)),
        Div(LabelSelect(...)),
        cols=2
    ),
    Button("Submit", cls=ButtonT.primary)
)
```

#### Data Display
```python
# Cards
Card(
    content,
    header=(H3("Title"), Subtitle("Description")),
    footer=Button("Action")
)

# Tables from dictionaries
headers = ["Name", "Email", "Actions"]
rows = [
    {"Name": "John", "Email": "john@example.com", "Actions": A("Edit")}
]
TableFromDicts(headers, rows)

# Custom table rendering
def cell_render(col, val):
    match col:
        case "Actions": return Td(Button("Edit"))
        case _: return Td(val)

TableFromDicts(headers, data, body_cell_render=cell_render)
```

#### Modals & Dropdowns
```python
# Modal
Modal(
    Div(
        ModalTitle("Create Item"),
        Form(...),
        DivRAligned(
            ModalCloseButton("Cancel"),
            ModalCloseButton("Save", cls=ButtonT.primary)
        )
    ),
    id="create-modal"
)

# Dropdown
DropDownNavContainer(
    NavCloseLi(A("Option 1")),
    NavCloseLi(A("Option 2"))
)
```

### Common Patterns

#### Page Layout Pattern
```python
def layout(content):
    return Div(
        NavBar(...),
        Container(content),
        cls="min-h-screen"
    )

@rt
def index():
    return layout(
        H1("Welcome"),
        Grid(cards, cols_lg=3)
    )
```

#### Search/Filter Pattern
```python
def search_form():
    return Form(
        LabelInput("Query", id="query"),
        LabelSelect(...options..., id="filter"),
        Button("Search"),
        hx_post=search,
        hx_target="#results"
    )

@rt
def search(query: str, filter: str):
    results = perform_search(query, filter)
    return Div(
        *[ResultCard(r) for r in results],
        id="results"
    )
```

#### CRUD Operations Pattern
```python
# Create
@rt
def create_item(name: str, description: str):
    item = db.items.insert(Item(name=name, description=description))
    return Success("Item created")

# Read
@rt
def view_items():
    items = db.items()  # Get all
    return Grid(*[ItemCard(i) for i in items])

# Update
@rt
def update_item(item_id: int, **kwargs):
    db.items.update(item_id, **kwargs)
    return Success("Updated")

# Delete
@rt
def delete_item(item_id: int):
    db.items.delete(item_id)
    return Success("Deleted")
```

#### File Upload Pattern
```python
# Reading files in artifacts
content = await window.fs.readFile('filename.csv', {'encoding': 'utf8'})

# Processing CSV files
import Papa from 'papaparse'
parsed = Papa.parse(content, {
    header: True,
    dynamicTyping: True,
    skipEmptyLines: True
})
```

### Styling

#### Theme Classes
- **ButtonT**: `primary`, `ghost` - Button styles
- **TextT**: `muted`, `error`, `sm` - Text styles
- **CardT**: `hover` - Card hover effects
- **NavT**: `primary`, `secondary` - Navigation styles
- **ContainerT**: `xl` - Container sizes

#### Common CSS Classes
- `space-y-4` - Vertical spacing
- `w-full` - Full width
- `gap-4` - Grid gap
- `mt-4`, `mb-6` - Margins
- `rounded-md` - Border radius

### Best Practices

1. Use styled MonsterUI components over raw HTML when available
2. Leverage HTMX for dynamic updates without full page reloads
3. Use FastLite for simple database operations
4. Match route parameters to form field names for automatic binding
5. Compose layouts with reusable functions
6. Use Grid/Flex helpers (DivFullySpaced, DivCentered, etc.) for consistent layouts
7. Prefer dictionaries for table data with TableFromDicts
8. Keep forms simple with Label* components that combine labels and inputs

### Quick Start Template

```python
from fasthtml.common import *
from monsterui.all import *
from datetime import datetime

app, rt = fast_app(hdrs=Theme.blue.headers())

# Database setup
db = database("app.db")
db.items = db.create(Item, pk='id')

# Layout wrapper
def layout(content):
    return Div(
        NavBar(A("Home", href="/"), brand=H3("My App")),
        Container(content)
    )

# Main route
@rt
def index():
    items = db.items()
    return layout(
        H1("Items"),
        Grid(*[ItemCard(i) for i in items])
    )

serve()
```

## Complete Table Example

```python
"""FrankenUI Tasks Example built with MonsterUI (original design by ShadCN)"""

from fasthtml.common import *
from monsterui.all import *
from fasthtml.svg import *
import json

app, rt = fast_app(hdrs=Theme.blue.headers())

def LAlignedCheckTxt(txt): return DivLAligned(UkIcon(icon='check'), P(txt, cls=TextPresets.muted_sm))

with open('data/status_list.json', 'r') as f: data     = json.load(f)
with open('data/statuses.json',    'r') as f: statuses = json.load(f)

def _create_tbl_data(d):
    return {'Done': d['selected'], 'Task': d['id'], 'Title': d['title'], 
            'Status'  : d['status'], 'Priority': d['priority'] }
    
data = [_create_tbl_data(d)  for d in data]
page_size = 15
current_page = 0
paginated_data = data[current_page*page_size:(current_page+1)*page_size]

priority_dd = [{'priority': "low", 'count': 36 }, {'priority': "medium", 'count': 33 }, {'priority': "high", 'count': 31 }]

status_dd = [{'status': "backlog", 'count': 21 },{'status': "todo", 'count': 21 },{'status': "progress", 'count': 20 },{'status': "done",'count': 19 },{'status': "cancelled", 'count': 19 }]

def create_hotkey_li(hotkey): return NavCloseLi(A(DivFullySpaced(hotkey[0], Span(hotkey[1], cls=TextPresets.muted_sm))))

hotkeys_a = (('Profile','⇧⌘P'),('Billing','⌘B'),('Settings','⌘S'),('New Team',''))
hotkeys_b = (('Logout',''), )

avatar_opts = DropDownNavContainer(
    NavHeaderLi(P('sveltecult'),NavSubtitle('leader@sveltecult.com')),
    NavDividerLi(),
    *map(create_hotkey_li, hotkeys_a),
    NavDividerLi(),
    *map(create_hotkey_li, hotkeys_b),)

def CreateTaskModal():
    return Modal(
        Div(cls='p-6')(
            ModalTitle('Create Task'),
            P('Fill out the information below to create a new task', cls=TextPresets.muted_sm),
            Br(),
            Form(cls='space-y-6')(
                Grid(Div(Select(*map(Option,('Documentation', 'Bug', 'Feature')), label='Task Type', id='task_type')),
                     Div(Select(*map(Option,('In Progress', 'Backlog', 'Todo', 'Cancelled', 'Done')), label='Status', id='task_status')),
                     Div(Select(*map(Option, ('Low', 'Medium', 'High')), label='Priority', id='task_priority'))),
                TextArea(label='Title', placeholder='Please describe the task that needs to be completed'),
                DivRAligned(
                    ModalCloseButton('Cancel', cls=ButtonT.ghost),
                    ModalCloseButton('Submit', cls=ButtonT.primary),
                    cls='space-x-5'))),
        id='TaskForm')

page_heading = DivFullySpaced(cls='space-y-2')(
            Div(cls='space-y-2')(
                H2('Welcome back!'),P("Here's a list of your tasks for this month!", cls=TextPresets.muted_sm)),
            Div(DiceBearAvatar("sveltcult",8,8),avatar_opts))

table_controls =(Input(cls='w-[250px]',placeholder='Filter task'),
     Button("Status"),
     DropDownNavContainer(map(NavCloseLi,[A(DivFullySpaced(P(a['status']), P(a['count'])),cls='capitalize') for a in status_dd])), 
     Button("Priority"),
     DropDownNavContainer(map(NavCloseLi,[A(DivFullySpaced(LAlignedCheckTxt(a['priority']), a['count']),cls='capitalize') for a in priority_dd])),
     Button("View"),
     DropDownNavContainer(map(NavCloseLi,[A(LAlignedCheckTxt(o)) for o in ['Title','Status','Priority']])),
     Button('Create Task',cls=(ButtonT.primary, TextPresets.bold_sm), data_uk_toggle="target: #TaskForm"))

def task_dropdown():
    return Div(Button(UkIcon('ellipsis')),
               DropDownNavContainer(
                   map(NavCloseLi,[
                       *map(A,('Edit', 'Make a copy', 'Favorite')),
                        A(DivFullySpaced(*[P(o, cls=TextPresets.muted_sm) for o in ('Delete', '⌘⌫')]))])))                        
def header_render(col):
    match col:
        case "Done":    return Th(CheckboxX(), shrink=True)
        case 'Actions': return Th("",          shrink=True)
        case _:         return Th(col,         expand=True)

def cell_render(col, val):
    def _Td(*args,cls='', **kwargs): return Td(*args, cls=f'p-2 {cls}',**kwargs)
    match col:
        case "Done": return _Td(shrink=True)(CheckboxX(selected=val))
        case "Task":  return _Td(val, cls='uk-visible@s')  # Hide on small screens
        case "Title": return _Td(val, cls='font-medium', expand=True)
        case "Status" | "Priority": return _Td(cls='uk-visible@m uk-text-nowrap capitalize')(Span(val))
        case "Actions": return _Td(task_dropdown(), shrink=True)
        case _: raise ValueError(f"Unknown column: {col}")

task_columns = ["Done", 'Task', 'Title', 'Status', 'Priority', 'Actions']

tasks_table = Div(cls='mt-4')(
    TableFromDicts(
        header_data=task_columns,
        body_data=paginated_data,
        body_cell_render=cell_render,
        header_cell_render=header_render,
        sortable=True,
        cls=(TableT.responsive, TableT.sm, TableT.divider)))


def footer():
    total_pages = (len(data) + page_size - 1) // page_size
    return DivFullySpaced(
        Div('1 of 100 row(s) selected.', cls=TextPresets.muted_sm),
        DivLAligned(
            DivCentered(f'Page {current_page + 1} of {total_pages}', cls=TextT.sm),
            DivLAligned(*[UkIconLink(icon=i,  button=True) for i in ('chevrons-left', 'chevron-left', 'chevron-right', 'chevrons-right')])))

tasks_ui = Div(DivFullySpaced(DivLAligned(table_controls), cls='mt-8'), tasks_table, footer())

@rt
def index(): return Container(page_heading, tasks_ui, CreateTaskModal())

serve()
```
</Monster UI - for FastHTML>
<NBDEV Notebook Best Practices>
# Notebook Best Practices: Jeremy Howard's nbdev Philosophy

> A comprehensive guide to writing effective Jupyter notebooks following Jeremy Howard's literate programming principles

This document outlines the key principles and practices for creating high-quality Jupyter notebooks based on Jeremy Howard's nbdev methodology and years of experience with notebook-driven development.

## Core Philosophy: Literate Programming

Jeremy Howard advocates for **literate programming** - the idea that code should be written primarily for humans to read, with execution by computers being secondary. Notebooks excel at this because they combine:

- **Code** - The implementation
- **Documentation** - Explanations and context  
- **Examples** - Working demonstrations
- **Tests** - Validation and edge cases

## Essential Principles

### 1. Functions First, Widgets Second

**Always build and test core functions before creating interactive interfaces.**

```python
# ✅ GOOD: Build function first
def calculate_roi(revenue: float, cost: float) -> float:
    """Calculate return on investment as a percentage."""
    return (revenue - cost) / cost * 100

# Test immediately
result = calculate_roi(1200, 1000)
assert result == 20.0
print(f"ROI: {result}%")

# Interactive demo comes last (optional)
from ipywidgets import interact
interact(calculate_roi, revenue=(0, 10000, 100), cost=(0, 5000, 100))
```

```python
# ❌ AVOID: Starting with widgets before building functions
# Don't build functionality inside widget callbacks
```

### 2. Small, Focused Functions

**Each function should do one thing well and be immediately testable.**

```python
# ✅ GOOD: Small, focused function
def extract_domain(url: str) -> str:
    """Extract domain from a URL."""
    from urllib.parse import urlparse
    return urlparse(url).netloc

# Test immediately
test_url = "https://api.example.com/v1/data"
domain = extract_domain(test_url)
assert domain == "api.example.com"
print(f"Domain: {domain}")
```

```python
# ❌ AVOID: Large functions that do multiple things
def process_api_data_and_send_emails_and_log_everything(data):
    # 50+ lines of mixed concerns
    pass
```

### 3. Immediate Testing and Demonstration

**Every function should be followed immediately by working examples and tests.**

**CRITICAL JEREMY HOWARD PATTERN - MUST FOLLOW EXACTLY:**

```
Function Definition (#| export)
    ↓
Mock Tests (clean examples for documentation)
    ↓  
Hidden Real API Test (#| hide - immediate validation)
    ↓
[Next Function...]
```

**❌ NEVER DO THIS (violates nbdev philosophy):**
```
Function 1 definition
Mock tests for Function 1
Function 2 definition  
Mock tests for Function 2
Function 3 definition
Mock tests for Function 3
[GIANT BLOB OF ALL REAL API TESTS AT END] ← WRONG!
```

**✅ ALWAYS DO THIS (Jeremy Howard's way):**
```
Function 1 definition (#| export)
Mock tests for Function 1
Real API test for Function 1 (#| hide)

Function 2 definition (#| export)
Mock tests for Function 2  
Real API test for Function 2 (#| hide)

Function 3 definition (#| export)
Mock tests for Function 3
Real API test for Function 3 (#| hide)
```

```python
#| export
def validate_email(email: str) -> bool:
    """Check if email format is valid."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# Immediate testing with assertions
from fastcore.test import test_eq

test_eq(validate_email("user@example.com"), True)
test_eq(validate_email("invalid-email"), False)
test_eq(validate_email(""), False)

print("✅ Email validation function working correctly")

# Show practical examples
emails = ["john@example.com", "invalid", "test@domain.org"]
for email in emails:
    status = "✅" if validate_email(email) else "❌"
    print(f"{status} {email}")
```

### 4. Progressive Building

**Build complexity gradually, with each step building on the previous.**

```python
# Step 1: Simple function
def make_request(url: str) -> dict:
    """Make a basic HTTP request."""
    import requests
    response = requests.get(url)
    return response.json()

# Test Step 1
test_data = make_request("https://httpbin.org/json")
print("✅ Basic request working")

# Step 2: Add error handling
def make_safe_request(url: str) -> dict:
    """Make HTTP request with error handling."""
    try:
        import requests
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Test Step 2
result = make_safe_request("https://invalid-url.com")
assert "error" in result
print("✅ Error handling working")

# Step 3: Add authentication (builds on previous steps)
def make_authenticated_request(url: str, token: str) -> dict:
    """Make authenticated request using previous function."""
    import requests
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
```

## Notebook Structure Standards

### 1. Title and Metadata

Start every notebook with clear metadata:

```markdown
# API Client Implementation

> A step-by-step implementation of a robust API client

This notebook demonstrates how to build a production-ready API client following best practices for error handling, authentication, and testing.
```

### 2. Imports and Setup

Keep imports clean and organized:

```python
#| default_exp api_client

# Standard library
import os
from typing import Dict, List, Optional, Any
from datetime import datetime

# Third party
import requests
import pandas as pd

# Testing
from fastcore.test import test_eq, test_ne

# Local imports (if any)
from myproject.utils import helper_function
```

### 3. Function Organization

Each major functionality should follow this pattern:

```markdown
## Authentication

Let's start with a simple authentication class:
```

```python
#| export
class APIAuth:
    """Simple API authentication handler."""
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    @property
    def headers(self) -> Dict[str, str]:
        """Return authentication headers."""
        return {"Authorization": f"Bearer {self.api_key}"}

# Test immediately
auth = APIAuth("test-key-123")
expected = {"Authorization": "Bearer test-key-123"}
test_eq(auth.headers, expected)
print("✅ Authentication class working")
```

### 4. Export Management

Always include export cell at the end:

```python
#| hide
import nbdev
nbdev.nbdev_export()
```

## Testing Best Practices

### 1. Use fastcore.test Functions

```python
from fastcore.test import test_eq, test_ne, test_close, test_is

# Equality testing
test_eq(calculate_tax(100, 0.1), 10.0)

# Inequality testing  
test_ne(process_data([]), None)

# Float comparison with tolerance
test_close(calculate_pi(), 3.14159, eps=1e-4)

# Identity testing
test_is(get_singleton(), get_singleton())
```

### 2. Test Edge Cases

```python
def safe_divide(a: float, b: float) -> Optional[float]:
    """Safely divide two numbers."""
    if b == 0:
        return None
    return a / b

# Test normal cases
test_eq(safe_divide(10, 2), 5.0)
test_eq(safe_divide(7, 3), 7/3)

# Test edge cases
test_eq(safe_divide(5, 0), None)  # Division by zero
test_eq(safe_divide(0, 5), 0.0)   # Zero dividend
test_eq(safe_divide(-10, 2), -5.0) # Negative numbers

print("✅ All edge cases handled correctly")
```

### 3. Document Error Cases

```python
def parse_config(config_str: str) -> Dict[str, Any]:
    """Parse configuration string to dictionary."""
    import json
    try:
        return json.loads(config_str)
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON: {e}"}

# Test success case
valid_json = '{"key": "value", "number": 42}'
result = parse_config(valid_json)
test_eq(result, {"key": "value", "number": 42})

# Test error case
invalid_json = '{"incomplete": json'
result = parse_config(invalid_json)
assert "error" in result
print("✅ Error handling documented and tested")
```

## Advanced Patterns

### 1. Use show_doc for Class Methods

```python
from nbdev.showdoc import show_doc

class DataProcessor:
    """Process and analyze data efficiently."""
    
    def clean_data(self, data: List[Dict]) -> List[Dict]:
        """Remove invalid entries and normalize data."""
        # Implementation here
        pass
    
    def analyze_trends(self, data: List[Dict]) -> Dict[str, float]:
        """Analyze trends in the cleaned data."""
        # Implementation here  
        pass

# Document methods individually
show_doc(DataProcessor.clean_data)
show_doc(DataProcessor.analyze_trends)
```

### 2. Use Patch for Method Extension

```python
from fastcore.basics import patch

@patch
def to_summary(self: DataProcessor) -> str:
    """Generate a summary report of the processor state."""
    return f"DataProcessor with {len(self.data)} records"

# Test the patched method
processor = DataProcessor()
processor.data = [{"a": 1}, {"b": 2}]
test_eq(processor.to_summary(), "DataProcessor with 2 records")
```

### 3. Rich Display for Objects

```python
class APIResponse:
    def __init__(self, data: dict, status_code: int):
        self.data = data
        self.status_code = status_code
    
    def _repr_markdown_(self) -> str:
        """Rich display in notebooks."""
        return f"""
**API Response**
- Status Code: `{self.status_code}`
- Data Keys: `{list(self.data.keys())}`
- Success: {'✅' if self.status_code == 200 else '❌'}
"""

# When displayed in notebook, shows formatted markdown
response = APIResponse({"users": [1, 2, 3]}, 200)
response  # Rich display automatically shown
```

## Cross-Platform Import Resolution

### 1. Required Path Setup for All Notebooks

For notebooks to work across different environments (Mac Jupyter, Docker, etc.), always include path setup at the beginning of imports:

```python
#| export
from __future__ import annotations

import sys
import os

# Add project root to path so we can import awin_pubkit modules
if '..' not in sys.path:
    sys.path.insert(0, '..')
if '.' not in sys.path:
    sys.path.insert(0, '.')

# Then proceed with regular imports
from typing import Any, Dict, List, Optional
from awin_pubkit.core import AwinClient
```

**Why this is needed:**
- Jupyter notebooks don't automatically include project directory in Python path
- Different platforms (macOS vs Docker) may have different path resolution behavior
- Virtual environments may not be detected consistently by notebook kernels
- This ensures reliable imports regardless of execution environment

**Pattern for all future notebooks:**
1. Always include the path setup code at the top of imports cell
2. Include it in the `#| export` cell so it's available in generated modules
3. Test imports work from the `nbs/` directory before proceeding
4. This pattern works across Mac, Linux, Docker, and other environments

## API Integration and Real Data Testing

### 1. Dual Testing Pattern for API Functions

When building functions that interact with external APIs, use a two-tier testing approach:

```python
# 1. Mock/Unit Tests (exported to docs)
# Test immediately with predictable mock data
class MockClient:
    def request(self, method, path):
        return {"accounts": [{"accountId": 12345, "accountType": "publisher"}]}

mock_client = MockClient()
result = get_publisher_ids(mock_client)
test_eq(len(result), 1)
print("✅ Function logic working correctly")
```

```python
#| hide
# 2. Real API Tests (hidden from docs)
# Validate with actual API integration

try:
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    api_token = os.getenv('API_TOKEN')
    if api_token:
        real_client = APIClient(api_token)
        real_result = get_publisher_ids(real_client)
        print(f"✅ Found {len(real_result)} real accounts")
        print("✅ Real API integration working")
    else:
        print("ℹ️ Skipping real API test (API_TOKEN not set)")
        
except Exception as e:
    print(f"⚠️ Real API test note: {e}")
```

**Benefits of this pattern**:
- Documentation shows clean, predictable examples
- Hidden tests prove functions work with real APIs
- Graceful degradation when credentials unavailable
- Security best practices (no credentials in published docs)

### 2. API Response Structure Validation

Never assume API response structures. Always validate actual responses:

```python
# ❌ Dangerous assumption
def get_data(client):
    data = client.request("/endpoint")
    if not isinstance(data, list):  # Wrong assumption!
        return []
    return data

# ✅ Proper validation
def get_data(client):
    data = client.request("/endpoint")
    # Validate actual structure
    if isinstance(data, dict) and 'items' in data:
        return data['items']
    elif isinstance(data, list):
        return data
    return []
```

**Best practices**:
- Test with real API responses to understand actual structure
- Handle multiple possible response formats gracefully
- Document the expected API response format in comments
- Update specifications when API structure assumptions are wrong

### 3. Environment Configuration for API Testing

Use `.env` files with `python-dotenv` for secure credential management:

```python
#| hide
# Standard pattern for API testing
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

api_token = os.getenv('API_TOKEN')
if not api_token:
    print("ℹ️ Skipping API tests (API_TOKEN not set in .env)")
    return

# Proceed with real API testing...
```

**Security benefits**:
- Credentials stay out of notebooks and repositories
- Easy to manage different environments (dev/staging/prod)
- Graceful fallback when credentials unavailable
- Consistent credential management across project

## Common Anti-Patterns to Avoid

### ❌ Don't Mix Imports and Logic

```python
# BAD
import pandas as pd
df = pd.read_csv("data.csv")  # Don't mix with imports
import numpy as np
```

```python
# GOOD
import pandas as pd
import numpy as np

# Separate cell for logic
df = pd.read_csv("data.csv")
```

### ❌ Don't Create Massive Functions

```python
# BAD
def do_everything(data):
    # 100+ lines of mixed functionality
    # Data cleaning
    # API calls  
    # Email sending
    # Logging
    # Analysis
    pass
```

```python
# GOOD
def clean_data(data): pass
def call_api(endpoint): pass  
def send_notification(message): pass
def log_activity(action): pass
def analyze_results(results): pass
```

### ❌ Don't Skip Documentation

```python
# BAD
def calc(x, y, z):
    return (x * y) / z if z != 0 else None
```

```python
# GOOD
def calculate_efficiency_ratio(revenue: float, costs: float, time_hours: float) -> Optional[float]:
    """Calculate efficiency ratio as revenue per cost per hour.
    
    Args:
        revenue: Total revenue generated
        costs: Total costs incurred
        time_hours: Time spent in hours
        
    Returns:
        Efficiency ratio or None if time_hours is zero
        
    Example:
        >>> calculate_efficiency_ratio(1000, 500, 10)
        2.0
    """
    if time_hours == 0:
        return None
    return revenue / costs / time_hours
```

## Collaboration Best Practices

### 1. Use nbdev Hooks

```bash
# Install git hooks to clean notebooks
nbdev_install_hooks
```

This automatically:
- Cleans notebook metadata on save
- Resolves merge conflicts at cell level
- Keeps notebooks lightweight and mergeable

### 2. Consistent Cell Organization

```python
# Standard pattern for each major function:

# 1. Function definition with #| export
#| export
def my_function(param: int) -> str:
    """Function description."""
    return str(param * 2)

# 2. Immediate testing
test_eq(my_function(5), "10")
test_eq(my_function(0), "0")

# 3. Usage examples
examples = [1, 2, 3, 4, 5]
results = [my_function(x) for x in examples]
print(f"Results: {results}")

# 4. Edge case testing
test_eq(my_function(-1), "-2")  # Negative input
```

### 3. Clear Section Headers

Use markdown headers to create clear notebook structure:

```markdown
# Main Topic

## Subtopic 1: Basic Implementation

### Helper Functions

### Main Functions  

### Testing

## Subtopic 2: Advanced Features

### Error Handling

### Performance Optimization
```

## Summary

Following Jeremy Howard's nbdev philosophy creates notebooks that are:

- **Educational**: Easy to learn from with clear progression
- **Maintainable**: Small functions with immediate tests
- **Professional**: Production-ready code with comprehensive documentation  
- **Collaborative**: Clean, mergeable notebooks with consistent patterns

The key is treating notebooks as the authoritative source of both code and documentation, where every function is immediately demonstrated and tested in context.

Remember: **Functions First, Widgets Second** - build robust functionality before creating interactive interfaces, and always test immediately after implementation.
</NBDEV Notebook Best Practices>

</Claude Guidance>