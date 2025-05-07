# 🤖 AI Interview Coach

> An AI-powered interview practice assistance that simulates real-world job interviews, gives feedback and helps users to prepare with confidence.


## Structure of Application

```mermaid
flowchart TD

A[🤖 AI Interview Coach]
M[Structured Conversation]
T[Tools]
P[Prompt Template]
S[Structured Output]
F[Final Result]

A --> M
M -- We can use Few-Shot Prompting for better result. -->
P --> T --> S --> F
```