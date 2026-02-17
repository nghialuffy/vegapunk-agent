# Quick Implementation Guide

How to upgrade your agent to generate learn-ai style content.

## 📋 Files to Modify

### 1. **src/nodes/setup_node.py**

**Current**: Creates simple `lessons/` directory

**Change to**: Create full hierarchical structure

```python
def create_enhanced_directory_structure(topic: str, base_path: Path) -> dict:
    """Create learn-ai style directory structure"""

    # Sanitize topic name for folder
    topic_slug = topic.lower().replace(' ', '-')
    repo_path = base_path / topic_slug

    # Create main directory
    repo_path.mkdir(exist_ok=True)

    # Create subdirectories
    subdirs = {
        'fundamentals': '01-Fundamentals',
        'core': '02-Core-Concepts',
        'architectures': '03-Architectures',
        'implementations': '04-Implementations',
        'applications': '05-Practical-Applications',
        'advanced': '06-Advanced-Topics',
        'resources': '07-Resources',
        'examples': 'Examples',
        'maps': 'Maps',
    }

    paths = {'root': str(repo_path)}

    for key, dirname in subdirs.items():
        path = repo_path / dirname
        path.mkdir(exist_ok=True)
        paths[key] = str(path)

    # Create code-examples subdirectory
    (repo_path / '04-Implementations' / 'code-examples').mkdir(exist_ok=True)

    return paths
```

---

### 2. **src/prompts.py**

**Replace existing prompts** with enhanced versions from `ENHANCED_PROMPTS.md`

```python
# Copy the entire ENHANCED_SYNTHESIS_SYSTEM_PROMPT
SYNTHESIS_SYSTEM_PROMPT = """You are a senior educator..."""

# Copy the entire ENHANCED_SYNTHESIS_USER_PROMPT
SYNTHESIS_USER_PROMPT_TEMPLATE = """Topic: {topic}..."""

# Copy the entire ENHANCED_LECTURE_SYSTEM_PROMPT
LECTURE_SYSTEM_PROMPT = """You are an expert technical instructor..."""

# Copy the entire ENHANCED_LECTURE_USER_PROMPT
LECTURE_USER_PROMPT_TEMPLATE = """Course topic: {topic}..."""
```

---

### 3. **src/models.py**

**Add new fields** to AgentState:

```python
class AgentState(TypedDict):
    # Existing fields
    topic: str
    target_audience: str
    repo_info: Dict[str, Any]
    research_sources: List[Dict[str, str]]
    raw_notes: str
    knowledge_base: str
    lesson_outline: List[str]
    lessons: Dict[str, str]
    github_repo_url: str

    # NEW: Enhanced structure support
    lesson_categories: Dict[str, List[str]]  # Maps category to lesson titles
    examples: Dict[str, str]  # Example filename -> content
    maps: Dict[str, str]  # Map filename -> content
    readme_content: str  # Main README
    overview_content: str  # 00-Overview.md
```

---

### 4. **src/nodes/synthesis_node.py**

**Update to extract categorized lessons**:

```python
def synthesis_node(state: AgentState) -> dict:
    # ... existing code ...

    # Call Claude with enhanced prompt
    knowledge_base = call_claude(system_prompt, user_prompt, ...)

    # Extract categorized lesson outline
    lesson_categories = extract_lesson_categories(knowledge_base)
    # Returns: {
    #   "01-Fundamentals": ["00-What-is-X", "01-Principles"],
    #   "02-Core-Concepts": ["00-Concept-A", "01-Concept-B"],
    #   ...
    # }

    return {
        "knowledge_base": knowledge_base,
        "lesson_categories": lesson_categories
    }

def extract_lesson_categories(synthesis_output: str) -> Dict[str, List[str]]:
    """Extract categorized lessons from synthesis output"""
    categories = {}
    current_category = None

    for line in synthesis_output.split('\n'):
        # Look for category headers like "### 01-Fundamentals/"
        if line.startswith('### ') and '/' in line:
            current_category = line.strip('# /').strip()
            categories[current_category] = []

        # Look for lesson items like "- 00-Lesson-Name.md:"
        elif current_category and line.strip().startswith('-'):
            # Extract lesson title
            lesson = line.split(':')[0].strip('- ').replace('.md', '')
            categories[current_category].append(lesson)

    return categories
```

---

### 5. **src/nodes/writing_node.py**

**Update to write to categorized folders**:

```python
def writing_node(state: AgentState) -> dict:
    # ... existing setup ...

    lesson_categories = state['lesson_categories']
    repo_info = state['repo_info']

    lessons = {}

    for category, lesson_titles in lesson_categories.items():
        # Get the directory for this category
        category_key = category.split('-')[0]  # "01" -> "fundamentals"
        category_map = {
            '01': 'fundamentals',
            '02': 'core',
            '03': 'architectures',
            '04': 'implementations',
            '05': 'applications',
            '06': 'advanced',
            '07': 'resources'
        }

        lessons_dir = Path(repo_info[category_map.get(category_key, 'fundamentals')])

        for lesson_title in lesson_titles:
            # Write lesson to appropriate category folder
            lesson_key = f"{category}/{lesson_title}"

            # Truncate knowledge base if needed
            truncated_kb, _ = smart_truncate_for_prompt(...)

            # Generate lesson with category context
            system_prompt, user_prompt = format_lecture_prompt(
                topic=topic,
                lesson_title=lesson_title,
                target_audience=target_audience,
                knowledge_base=truncated_kb,
                category=category  # NEW: Pass category for context
            )

            lesson_content = call_claude(system_prompt, user_prompt, ...)

            # Save to category folder
            lesson_path = lessons_dir / f"{lesson_title}.md"
            lesson_path.write_text(lesson_content, encoding='utf-8')

            lessons[lesson_key] = lesson_content

    return {"lessons": lessons}
```

---

### 6. **Add New Nodes**

#### 6a. **src/nodes/examples_node.py** (NEW FILE)

```python
"""Generate practical examples for Examples/ directory"""

from src.models import AgentState
from src.tools.llm_client import call_claude

def examples_node(state: AgentState) -> dict:
    """Generate 3-5 practical examples"""

    topic = state['topic']
    knowledge_base = state['knowledge_base']

    prompt = f"""
    Topic: {topic}

    Create 3-5 practical examples for the Examples/ directory.
    Each should demonstrate a real-world pattern or solution.

    Format each as a complete markdown file with:
    - YAML frontmatter
    - Problem description
    - Solution with code
    - Architecture diagram
    - Explanation

    Output as:
    ## EXAMPLE 1: Filename.md
    [full content]

    ## EXAMPLE 2: Filename.md
    [full content]
    ...
    """

    examples_content = call_claude(system_prompt, prompt, max_tokens=16000)

    # Parse examples
    examples = parse_examples(examples_content)

    # Write to Examples/ directory
    examples_dir = Path(state['repo_info']['examples'])
    for filename, content in examples.items():
        (examples_dir / filename).write_text(content, encoding='utf-8')

    return {"examples": examples}
```

#### 6b. **src/nodes/maps_node.py** (NEW FILE)

```python
"""Generate visual learning maps"""

from src.models import AgentState
from src.tools.llm_client import call_claude

def maps_node(state: AgentState) -> dict:
    """Generate Learning-Path.md and Concepts-Map.md"""

    topic = state['topic']
    lesson_categories = state['lesson_categories']

    # Generate Learning Path
    learning_path_prompt = f"""
    Topic: {topic}
    Lessons: {lesson_categories}

    Create a visual Learning-Path.md with:
    - ASCII roadmap
    - Week-by-week breakdown
    - Project milestones
    - Skill acquisition timeline
    """

    learning_path = call_claude(system_prompt, learning_path_prompt, ...)

    # Generate Concepts Map
    concepts_map_prompt = f"""
    Topic: {topic}

    Create a Concepts-Map.md with:
    - Hierarchical tree (ASCII)
    - Relationship diagram
    - Technology stack
    - Tool selection matrix
    """

    concepts_map = call_claude(system_prompt, concepts_map_prompt, ...)

    # Write to Maps/ directory
    maps_dir = Path(state['repo_info']['maps'])
    (maps_dir / 'Learning-Path.md').write_text(learning_path, encoding='utf-8')
    (maps_dir / 'Concepts-Map.md').write_text(concepts_map, encoding='utf-8')

    return {"maps": {"Learning-Path.md": learning_path, "Concepts-Map.md": concepts_map}}
```

#### 6c. **src/nodes/readme_node.py** (NEW FILE)

```python
"""Generate comprehensive README and Overview"""

from src.models import AgentState
from src.tools.llm_client import call_claude

def readme_node(state: AgentState) -> dict:
    """Generate README.md and 00-Overview.md"""

    topic = state['topic']
    lesson_categories = state['lesson_categories']

    # Generate README
    readme_prompt = f"""
    Topic: {topic}
    All Lessons: {lesson_categories}

    Create a comprehensive README.md with:
    - 🎯 What You'll Master
    - 📚 Quick Start
    - 📖 Learning Modules (all phases)
    - 🛠️ Tech Stack table
    - 🚀 Quick code examples
    - 📊 Timeline
    - 🎯 Projects
    """

    readme = call_claude(system_prompt, readme_prompt, max_tokens=16000)

    # Generate Overview
    overview_prompt = f"""
    Create 00-Overview.md as a detailed learning roadmap...
    """

    overview = call_claude(system_prompt, overview_prompt, max_tokens=16000)

    # Write files
    repo_root = Path(state['repo_info']['root'])
    (repo_root / 'README.md').write_text(readme, encoding='utf-8')
    (repo_root / '00-Overview.md').write_text(overview, encoding='utf-8')

    return {"readme_content": readme, "overview_content": overview}
```

---

### 7. **src/graph.py**

**Update the graph to include new nodes**:

```python
def build_graph():
    graph = StateGraph(AgentState)

    # Existing nodes
    graph.add_node("setup", setup_node)
    graph.add_node("research", research_node)
    graph.add_node("synthesis", synthesis_node)
    graph.add_node("writing", writing_node)

    # NEW nodes
    graph.add_node("examples", examples_node)
    graph.add_node("maps", maps_node)
    graph.add_node("readme", readme_node)

    graph.add_node("publish", publish_node)

    # Define flow
    graph.set_entry_point("setup")
    graph.add_edge("setup", "research")
    graph.add_edge("research", "synthesis")
    graph.add_edge("synthesis", "writing")
    graph.add_edge("writing", "examples")    # NEW
    graph.add_edge("examples", "maps")       # NEW
    graph.add_edge("maps", "readme")         # NEW
    graph.add_edge("readme", "publish")

    return graph.compile()
```

---

## 🚀 Quick Start

### Minimal Changes (1 hour)

Just want to get started quickly?

1. **Update prompts** in `src/prompts.py` with enhanced versions
2. **Test existing agent** - see if output improves with better prompts alone

### Medium Changes (1 day)

Want categorized folders?

1. Do minimal changes above
2. **Update `setup_node.py`** to create folder hierarchy
3. **Update `synthesis_node.py`** to extract categories
4. **Update `writing_node.py`** to write to correct folders

### Full Implementation (1 week)

Want the complete learn-ai experience?

1. Do medium changes above
2. **Add new nodes**: examples, maps, readme
3. **Update graph.py** to include new flow
4. **Test thoroughly** with a real topic

---

## ✅ Testing Checklist

After implementing:

- [ ] Run with a test topic (e.g., "API Design")
- [ ] Verify folder structure created correctly
- [ ] Check lessons have YAML frontmatter
- [ ] Verify ASCII diagrams present
- [ ] Check code examples exist
- [ ] Verify cross-links work
- [ ] Test README completeness
- [ ] Verify Examples/ has content
- [ ] Check Maps/ directory populated
- [ ] Push to GitHub and verify rendering

---

## 🎯 Expected Result

After full implementation, running:

```bash
python main.py
```

Should create:

```
outputs/api-design/
├── README.md                     ✅ 500+ lines, comprehensive
├── 00-Overview.md               ✅ Full learning roadmap
├── 01-Fundamentals/
│   ├── 00-What-is-API-Design.md ✅ Diagrams + code
│   ├── 01-REST-Principles.md    ✅ Tables + examples
│   └── 02-HTTP-Fundamentals.md
├── 02-Core-Concepts/
│   ├── 00-Resources-and-Endpoints.md
│   └── 01-Request-Response.md
├── [more folders...]
├── Examples/
│   ├── Simple-REST-API.md       ✅ Working code
│   ├── GraphQL-vs-REST.md       ✅ Comparison
│   └── API-Versioning.md
└── Maps/
    ├── Learning-Path.md         ✅ Visual roadmap
    └── API-Concepts-Map.md      ✅ Hierarchy
```

Every file should be **production-quality** with diagrams, code, and professional structure!

---

**Need help?** Check the detailed docs:
- `CONTENT_STRUCTURE_PLAN.md` - Full planning document
- `ENHANCED_PROMPTS.md` - Exact prompts to use
- `STRUCTURE_COMPARISON.md` - Visual before/after
