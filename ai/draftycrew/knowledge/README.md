# OpenSCAD Knowledge System for Drafty

## Overview

This knowledge system provides the `cad_generator` agent with comprehensive information about OpenSCAD best practices, common patterns, and validation rules to ensure generated code compiles correctly and follows proper conventions.

## Files Structure

```
knowledge/
├── README.md                           # This file
├── user_preference.txt                 # User preferences (legacy)
├── openscad_best_practices.txt         # Core OpenSCAD syntax and best practices
└── openscad_common_patterns.txt        # Templates and patterns for common objects
```

## Knowledge Base Components

### 1. OpenSCAD Best Practices (`openscad_best_practices.txt`)

Contains comprehensive guidelines for:
- Basic syntax rules (semicolons, indentation, variable declarations)
- Geometric primitives (cube, cylinder, sphere, cone)
- Transformations (translate, rotate, scale, mirror)
- Boolean operations (union, difference, intersection, hull)
- 2D to 3D conversion (linear_extrude, rotate_extrude)
- Common mistakes to avoid
- Parametric design principles
- Module structure guidelines
- Validation rules
- Furniture-specific guidelines
- Error prevention strategies
- Output requirements

### 2. OpenSCAD Common Patterns (`openscad_common_patterns.txt`)

Provides ready-to-use templates for:
- Basic chair template with realistic dimensions
- Table template with proper proportions
- Rounded box pattern with fillets
- Hole pattern arrays
- Chaise lounge pattern (corrected version)
- Validation patterns
- Common transformations
- Texture patterns
- Assembly patterns
- Error correction patterns

## Tools Integration

### 1. OpenSCAD Knowledge Tool (`openscad_knowledge_tool.py`)

**Purpose**: Provides contextual knowledge to the `cad_generator` agent

**Features**:
- Loads knowledge base files dynamically
- Provides specific guidance based on query content
- Covers furniture, syntax, dimensions, and validation topics
- Integrates with CrewAI's tool system

**Usage**: Agent queries this tool before generating code to ensure best practices

### 2. OpenSCAD Validator Tool (`openscad_validator.py`)

**Purpose**: Validates and corrects generated OpenSCAD code

**Features**:
- Automatic correction of common syntax errors
- Fixes missing semicolons
- Converts 2D objects to 3D context
- Validates dimensions and proportions
- Adds missing $fn parameters
- Provides detailed validation reports

**Usage**: Agent uses this tool after generating code to ensure compilation

## Integration with CrewAI

### Agent Configuration

The `cad_generator` agent is configured with both tools:

```python
@agent
def cad_generator(self) -> Agent:
    return Agent(
        config=self.agents_config['cad_generator'],
        verbose=True,
        tools=[openscad_knowledge, openscad_validator],  # Knowledge tools
        llm=gpt4o_llm,
        allow_delegation=False
    )
```

### Workflow

1. **Knowledge Consultation**: Agent queries OpenSCAD Knowledge Base tool
2. **Code Generation**: Agent generates initial OpenSCAD code using GPT-4o
3. **Validation**: Agent uses OpenSCAD Validator tool to check and correct code
4. **Output**: Final validated OpenSCAD code is produced

### Task Configuration

The `generate_cad` task includes explicit workflow instructions:

```
WORKFLOW:
1. FIRST: Use the OpenSCAD Knowledge Base tool to get best practices and patterns
2. SECOND: Generate initial OpenSCAD code following the knowledge base guidelines
3. THIRD: Use the OpenSCAD Validator tool to check and correct any syntax issues
4. FOURTH: Output the final validated OpenSCAD code
```

## Benefits

### 1. Error Prevention
- Prevents common OpenSCAD syntax errors
- Ensures realistic dimensions and proportions
- Avoids 2D objects in 3D context issues

### 2. Quality Improvement
- Consistent code structure and formatting
- Proper use of parametric variables
- Realistic furniture dimensions

### 3. Compilation Success
- Validated code that compiles in OpenSCAD
- Proper use of $fn parameters for smooth objects
- Correct boolean operations

### 4. Maintainability
- Clear, commented code structure
- Parametric design for easy modification
- Follows OpenSCAD best practices

## Usage Examples

### Knowledge Base Query
```
Agent: "I need to generate a chair model. What are the best practices?"
Tool: Provides furniture-specific guidelines, realistic dimensions, and chair templates
```

### Code Validation
```
Agent: "Here's my generated code: [OpenSCAD code]"
Tool: "VALIDATED AND CORRECTED OPENSCAD CODE: [corrected code]"
```

## Future Enhancements

1. **Extended Patterns**: Add more object-specific templates
2. **Advanced Validation**: Implement more sophisticated error detection
3. **Performance Optimization**: Cache frequently used knowledge
4. **User Customization**: Allow user-specific knowledge base additions

## References

- [CrewAI Documentation](https://docs.crewai.com/en/concepts/knowledge)
- [OpenSCAD Documentation](https://openscad.org/documentation.html)
- [CrewAI Tools Documentation](https://docs.crewai.com/en/tools/overview) 