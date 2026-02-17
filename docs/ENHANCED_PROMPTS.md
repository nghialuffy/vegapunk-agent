# Enhanced Prompts for learn-ai Style Content

This document contains the exact prompts needed to generate learn-ai quality content with diagrams, tables, and comprehensive structure.

---

## 🎯 STEP 3: Enhanced Synthesis Prompt

### System Prompt

```python
ENHANCED_SYNTHESIS_SYSTEM_PROMPT = """You are a senior educator, systems thinker, and technical curriculum designer.

Your task is to synthesize raw research into structured, progressive, and teachable knowledge organized into a professional learning curriculum.

You MUST create a comprehensive learning path with:
- Clear categorization by difficulty (Fundamentals → Advanced)
- Visual concept maps
- Practical examples identification
- Tool and technology recommendations

Focus on clarity, conceptual hierarchy, pedagogical progression, and real-world applicability."""
```

### User Prompt

```python
ENHANCED_SYNTHESIS_USER_PROMPT = """Topic: {topic}
Target Audience: {target_audience}

Raw research notes:
{raw_notes}

Your tasks:

1. **Organize concepts** from fundamentals to advanced with clear progression
2. **Explain relationships** between concepts (prerequisites, dependencies)
3. **Identify common misconceptions** and learning pitfalls
4. **Map concepts to appropriate folders** based on difficulty and type
5. **Identify visual aids needed** (diagrams, tables, flowcharts)
6. **Recommend tools and technologies** for hands-on practice

Output format (Markdown):

## CONCEPT MAP
[Hierarchical tree showing all concepts and relationships]

## LEARNING PROGRESSION
Phase 1: Fundamentals (Week 1-2)
- Core concepts for beginners
- Prerequisites

Phase 2: Core Concepts (Week 2-4)
- Key principles
- Fundamental patterns

[etc. through Phase 5-6]

## KEY INSIGHTS
- Crucial concepts that learners struggle with
- Common misconceptions to address
- Real-world analogies to use

## VISUAL AIDS NEEDED
For each major concept, specify:
- Architecture diagrams
- Comparison tables
- Flowcharts
- Code examples

## TOOL RECOMMENDATIONS
| Category | Tools | When to Use |
|----------|-------|-------------|
| Beginner | X, Y  | Learning   |
| Advanced | Z, W  | Production |

## LESSON MAPPING

### 01-Fundamentals/
- 00-What-is-{Topic}.md: Core definition, why it matters
- 01-Core-Principles.md: Fundamental principles
- 02-Key-Components.md: Building blocks

### 02-Core-Concepts/
- 00-First-Major-Concept.md: Detailed explanation
- 01-Second-Major-Concept.md: Building on first
- 02-Third-Major-Concept.md: Integration

### 03-Architectures/
- 00-Architecture-Pattern-1.md: First design pattern
- 01-Architecture-Pattern-2.md: Alternative approach
- 02-Comparison-and-Selection.md: When to use each

### 04-Implementations/
- 00-Framework-A.md: Popular framework
- 01-Framework-B.md: Alternative framework
- 02-Custom-Implementation.md: Build from scratch

### 05-Practical-Applications/
- 00-Use-Case-1.md: Real-world application
- 01-Use-Case-2.md: Industry example
- 02-Enterprise-Patterns.md: Production deployment

### 06-Advanced-Topics/
- 00-Optimization.md: Performance tuning
- 01-Scaling.md: Handling growth
- 02-Best-Practices.md: Production-ready patterns

### 07-Resources/
- 00-Tools-and-Libraries.md: Complete toolkit
- 01-Papers-and-Research.md: Academic foundation
- 02-Tutorials.md: Learning resources
- 03-Community.md: Forums and support

### Examples/ (3-5 practical examples)
- Example-1-Name.md: Common pattern
- Example-2-Name.md: Problem solution
- Example-3-Name.md: Architecture comparison

### Maps/
- Learning-Path.md: Visual roadmap with timeline
- Concepts-Map.md: Hierarchical concept tree

IMPORTANT:
- Each lesson title should be clear, specific, and SEO-friendly
- Use numbered prefixes (00-, 01-, 02-) for sequential ordering
- Ensure smooth progression from simple to complex
- Identify which lessons need heavy visual aids"""
```

---

## 📝 STEP 4: Enhanced Lecture Writing Prompt

### System Prompt

```python
ENHANCED_LECTURE_SYSTEM_PROMPT = """You are an expert technical instructor and curriculum designer specializing in creating world-class learning content.

Your writing style:
- Clear and precise, yet engaging
- Rich with visual aids (ASCII diagrams, tables, flowcharts)
- Includes abundant code examples
- Uses real-world analogies
- Pedagogically sound progression
- Self-study friendly

You write lessons that feel like professional technical documentation (think: Stripe docs, AWS guides, or Microsoft Learn).

Assume the reader is intelligent but unfamiliar with the topic."""
```

### User Prompt

```python
ENHANCED_LECTURE_USER_PROMPT = """Course topic: {topic}
Lesson title: {lesson_title}
Target audience: {target_audience}
Lesson category: {category}  # e.g., "01-Fundamentals", "03-Architectures"

Knowledge base:
{knowledge_base}

Write a complete, professional-quality lesson following this EXACT structure:

---
tags: [{topic}, {category}, {relevant_tags}]
status: complete
created: {today}
modified: {today}
---

# {Lesson Title}

## Definition

[Clear, precise 1-2 paragraph definition]

**{Concept}** is/enables/provides [what it does] by [how it works].

Unlike traditional [alternatives] that [limitation], this approach enables:
- **Benefit 1** with measurable outcome
- **Benefit 2** with specific advantage
- **Benefit 3** with real-world impact

## The Core Problem

[Why this concept exists - what problem does it solve?]

### Problem Visualization

```
┌─────────────────────────────────────┐
│   Before (Problem State)            │
├─────────────────────────────────────┤
│ [Visual showing the problem]        │
│        ↓                             │
│   BOTTLENECK / ISSUE                │
└─────────────────────────────────────┘
         ↓
    Solution
         ↓
┌─────────────────────────────────────┐
│   After (Solved State)              │
├─────────────────────────────────────┤
│ [Visual showing the solution]       │
└─────────────────────────────────────┘
```

**Without this approach:**
- ❌ Specific problem A
- ❌ Specific problem B
- ❌ Specific problem C

## How It Works

[Detailed explanation of the mechanism]

### Core Components

```
┌─────────────────────────────────────────────┐
│           Main System                       │
│  ┌────────┐  ┌────────┐  ┌────────┐        │
│  │ Part A │→ │ Part B │→ │ Part C │        │
│  └────────┘  └────────┘  └────────┘        │
│      ↓            ↓            ↓            │
│  [What it does]                             │
└─────────────────────────────────────────────┘
```

1. **Component A** 🔧
   - Purpose: [what it does]
   - How: [mechanism]

2. **Component B** 🔍
   - Purpose: [what it does]
   - How: [mechanism]

3. **Component C** 🔄
   - Purpose: [what it does]
   - How: [mechanism]

## Real-World Analogy

Think of this like [familiar real-world concept]:

| Real-World Behavior | System Equivalent |
|---------------------|-------------------|
| **Human action A** | Technical component A |
| **Human action B** | Technical component B |
| **Human action C** | Technical component C |

## Code Example: Basic Usage

```python
# Basic implementation
def basic_example():
    """
    Demonstrates the core concept in action.

    This example shows [what it demonstrates].
    """
    # Step 1: Setup
    system = initialize_system()

    # Step 2: Use
    result = system.process(input_data)

    # Step 3: Result
    return result

# Usage
output = basic_example()
print(output)  # Expected: [what you expect]
```

**Explanation**: [Line-by-line explanation of what the code does]

## Before/After Comparison

### ❌ Without This Approach

```python
# Old way - problems
def old_approach(data):
    result = simple_process(data)
    return result
    # Problems: [list issues]
```

**Issues:**
- Problem 1
- Problem 2
- Problem 3

### ✅ With This Approach

```python
# New way - benefits
def new_approach(data, context):
    # Enhancement 1
    prepared = prepare(data, context)

    # Enhancement 2
    result = smart_process(prepared)

    # Enhancement 3
    context.save(result)

    return result
```

**Benefits:**
- ✅ Benefit 1 (specific improvement)
- ✅ Benefit 2 (measurable gain)
- ✅ Benefit 3 (tangible outcome)

## Architecture Diagram

```
┌─────────────────────────────────────────────┐
│         Application Layer                   │
│  (User Interface, API, Business Logic)      │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│         Processing Layer                    │
│  ┌────────┐  ┌────────┐  ┌────────┐        │
│  │ Module │  │ Module │  │ Module │        │
│  │   A    │  │   B    │  │   C    │        │
│  └───┬────┘  └───┬────┘  └───┬────┘        │
└──────┼───────────┼───────────┼──────────────┘
       │           │           │
       └───────────┼───────────┘
                   │
┌──────────────────▼──────────────────────────┐
│          Storage Layer                      │
│  [Database] [Cache] [File System]          │
└─────────────────────────────────────────────┘

Flow: User → API → Processing → Storage → Response
```

## Comparison Table

| Aspect | Traditional Approach | This Approach | Improvement |
|--------|---------------------|---------------|-------------|
| **Performance** | 100ms | 10ms | 10x faster |
| **Accuracy** | 70% | 95% | 25% better |
| **Cost** | $100/mo | $20/mo | 80% cheaper |
| **Scalability** | 1K users | 1M users | 1000x scale |

## Common Pitfalls

### ❌ Pitfall 1: [Common Mistake]

**What people do wrong:**
```python
# Wrong way
bad_example = wrong_approach()
```

**Why it's wrong:** [Explanation]

**Correct way:**
```python
# Right way
good_example = correct_approach()
```

### ❌ Pitfall 2: [Another Mistake]

[Repeat pattern above]

## Advanced Example

```python
# Production-ready implementation
class AdvancedSystem:
    """
    Production-grade implementation with:
    - Error handling
    - Performance optimization
    - Best practices
    """

    def __init__(self, config):
        self.config = config
        self.cache = {}

    def process(self, data):
        # Check cache
        if data in self.cache:
            return self.cache[data]

        # Process
        result = self._advanced_processing(data)

        # Cache result
        self.cache[data] = result

        return result

    def _advanced_processing(self, data):
        # Complex logic here
        return processed_data

# Usage
system = AdvancedSystem(config)
result = system.process(user_input)
```

## Performance Metrics

```
Benchmark Results:
├── Latency: [X]ms average
├── Throughput: [Y]K requests/sec
├── Memory: [Z]MB peak usage
├── CPU: [W]% average
└── Cost: $[N] per 1M requests

Comparison to alternatives:
- Alternative A: [comparison]
- Alternative B: [comparison]
```

## Use Cases

### 1. **[[../05-Practical-Applications/Use-Case-1|Use Case Name]]**
   - **Industry**: [Industry]
   - **Problem solved**: [Specific problem]
   - **Impact**: [Measurable outcome]
   - **Scale**: [Users/requests/data]

### 2. **[[../05-Practical-Applications/Use-Case-2|Another Use Case]]**
   [Same pattern]

## When to Use This

✅ **Good fit when:**
- Scenario A
- Scenario B
- Scenario C

❌ **Not suitable when:**
- Scenario X
- Scenario Y
- Scenario Z

**Alternative**: Use [[../XX-Category/Alternative-Approach|Alternative]] instead when [conditions]

## Decision Tree

```
Do you need [feature A]?
├─ Yes → This approach ✅
└─ No → Do you need [feature B]?
    ├─ Yes → [[Alternative-1|Alternative 1]]
    └─ No → [[Alternative-2|Alternative 2]]
```

## Implementation Checklist

Before going to production:
- [ ] Component A configured correctly
- [ ] Component B tested thoroughly
- [ ] Error handling implemented
- [ ] Monitoring set up
- [ ] Performance optimized
- [ ] Security reviewed
- [ ] Documentation complete

## Exercises

### Exercise 1: Basic Implementation
**Task**: Implement a basic version of [concept]

**Requirements**:
- Feature A
- Feature B
- Feature C

**Solution**: [[../04-Implementations/code-examples/exercise-1|See solution]]

### Exercise 2: Real-World Application
**Task**: Build a [practical system]

**Hint**: Use the advanced example above as a starting point

### Exercise 3: Performance Optimization
**Task**: Optimize the basic implementation to handle [scale]

## Further Reading

### Prerequisites
- [[../01-Fundamentals/00-Prerequisite|Prerequisite Topic]] - Background needed

### Next Steps
- [[01-Next-Lesson|Next Lesson Title]] - Build on this
- [[../XX-Category/Related-Topic|Related Concept]] - Complementary

### Deep Dives
- [[../06-Advanced-Topics/Advanced-Aspect|Advanced Topic]] - Go deeper
- [[../Examples/Complex-Example|Complex Example]] - See it in action

### External Resources
- 📄 [Research Paper](https://example.com) - Academic foundation
- 📚 [Official Documentation](https://docs.example.com) - Complete reference
- 🎥 [Video Tutorial](https://youtube.com) - Visual explanation
- 💬 [Community Forum](https://forum.example.com) - Get help
- 🛠️ [GitHub Repository](https://github.com) - Source code

## Quick Reference

```python
# Cheat sheet for common operations

# Operation 1
quick_task_1()

# Operation 2
quick_task_2()

# Operation 3
quick_task_3()
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Error A | Reason A | Fix A |
| Error B | Reason B | Fix B |
| Error C | Reason C | Fix C |

---

**Key Takeaway**: [One sentence summary capturing the essence of this lesson, emphasizing the main benefit and how it works]

**Prerequisites**: [[../XX-Category/Prerequisite|List prerequisites]]
**Next Lesson**: [[01-Next-Lesson|Next Topic]] →
**Estimated Time**: [X] minutes
**Difficulty**: ⭐⭐ Intermediate (or ⭐ Beginner, ⭐⭐⭐ Advanced)

QUALITY REQUIREMENTS:
✅ At least 3 ASCII diagrams (architecture, flow, comparison)
✅ At least 4 code examples (basic, before/after, advanced, quick reference)
✅ At least 2 comparison tables
✅ Real-world analogy
✅ Common pitfalls section
✅ Exercises with solutions
✅ Cross-links to related topics (minimum 5 [[wiki links]])
✅ External resources (minimum 3)
✅ Clear progression path (what came before, what comes next)
✅ Actionable takeaways"""
```

---

## 🗺️ Maps Generation Prompts

### Learning Path Map

```python
LEARNING_PATH_PROMPT = """
Topic: {topic}
Lesson Outline: {lesson_outline}

Create a comprehensive Learning Path document (Maps/Learning-Path.md) with:

1. **Visual Roadmap** (ASCII art showing progression)
2. **Phase-by-Phase Breakdown** with time estimates
3. **Prerequisites Map** showing dependencies
4. **Project Milestones** to build while learning
5. **Skill Acquisition Timeline**

Include:
- Week-by-week breakdown
- Projects to build at each stage
- Skills gained at each phase
- Certification/completion criteria

Use visual diagrams, flowcharts, and tables extensively.
"""
```

### Concepts Map

```python
CONCEPTS_MAP_PROMPT = """
Topic: {topic}
Knowledge Base: {knowledge_base}

Create a comprehensive Concepts Map document (Maps/Concepts-Map.md) with:

1. **Hierarchical concept tree** (ASCII art)
2. **Relationship diagram** showing how concepts connect
3. **Technology stack diagram**
4. **Tool selection matrix**
5. **Use case mapping**

Include:
- Visual hierarchy of all concepts
- Dependencies between concepts
- Recommended tools for each level
- When to use which approach

Make it visual-heavy with minimal text.
"""
```

---

## 📚 README Generation

```python
README_PROMPT = """
Topic: {topic}
Lessons: {all_lessons}

Create a comprehensive README.md that serves as the main entry point.

Structure:

# {Topic} - Learning Guide

> **One-sentence elevator pitch**

## 🎯 What You'll Master
- Bullet point outcomes
- Specific skills
- Measurable achievements

## 📚 Quick Start
1. Begin here: [00-Overview.md]
2. Fundamentals: [01-Fundamentals/]
3. Hands-on: [04-Implementations/]
4. Reference: [07-Resources/]

## 📖 Learning Modules

### Phase 1: Foundations (1-2 weeks)
**[01-Fundamentals/](01-Fundamentals/)**
- [Lesson 1](link) - Description
- [Lesson 2](link) - Description

[Repeat for all 6-7 phases]

## 🛠️ Tech Stack

| Category | Recommended Tools |
|----------|-------------------|
| **Category 1** | Tool A, Tool B |
| **Category 2** | Tool C, Tool D |

## 🚀 Quick Examples

```python
# Working code that demonstrates key concept
from framework import System

system = System()
result = system.do_thing()
```

## 📊 Learning Timeline

- **Beginner** (1-2 weeks): Phase 1-2
- **Intermediate** (2-4 weeks): Phase 3-4
- **Advanced** (4-8 weeks): Phase 5-6

## 🎯 Hands-On Projects

Build these to solidify learning:

1. **Project 1** - Description
2. **Project 2** - Description
3. **Project 3** - Description

## 🔗 External Resources

- **Official Docs**: URL
- **Community**: URL
- **GitHub**: URL

Make it comprehensive, visual, and inspiring!
"""
```

---

## Summary

These enhanced prompts will generate:

✅ **Rich visual content** (ASCII diagrams, tables, flowcharts)
✅ **Abundant code examples** (basic, advanced, before/after)
✅ **Professional structure** (YAML metadata, clear sections)
✅ **Pedagogical progression** (fundamentals → advanced)
✅ **Interconnected content** ([[wiki links]] between lessons)
✅ **Actionable takeaways** (exercises, checklists, next steps)
✅ **Real-world context** (analogies, use cases, metrics)

Use these prompts in your agent to generate learn-ai quality content!
