# Day 45 Notes

## LangChain Tools

Tools are functions wrapped with:

@tool

Benefits:

- Metadata
- Descriptions
- Argument schemas
- Agent compatibility

Examples:

@tool
def get_time():
    pass

@tool
def get_date():
    pass

@tool
def multiply(a, b):
    pass

Invocation:

tool.invoke({})