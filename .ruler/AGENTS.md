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