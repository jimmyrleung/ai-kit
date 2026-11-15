---
name: ui-process
description: "Step-by-step process to build UI with intent and avoid the so-called AI slop. It goes through a series of steps to make sure the agents have enough context and the right references, and only then it builds the UI proposal. Use whenever building a new UI or re-designing an existing UI."
---

# ui-process

Goal: goes through a series of steps so that AI agents have enough context and the right references before proposing a given UI.

## Approach

The UI process goes through the following steps, in order:

1. **Gather context and interview the user**: 

- Read all inputs and references provided by the user
- Interview the user on anything that is not completely clear - do not make assumptions
- Ensure you understand what the ask is
- Once everything is clear, confirm with the user both of you are aligned. You can only proceed when both are aligned.

2. **Research**: with clear context on what needs to be done, plan a research on references. Be careful with the sources, try to stick with authoritative sources, well-known references, overall good practices, etc. Confirm the plan with the user before applying it.

- Research here includes finding relevant references for our context, especially when it comes to UI and UX.
- For UI, make sure to research places like Dribbble, Pinterest, showcases from famous libs like Tailwind, etc.

3. **Branding alignment**: in this step there's a few scenarios that can happen.

- We're building new design or re-designing when branding already exists: in that case, we should iterate on the context gathered + research results and make sure we add branding alignment
- We're building new design or re-designing and there's no sense of branding yet: in that case, based on the context gathered + research results, we should launch a brand building process (purpose, strategy, target, competitors, positioning, identity, etc.)
- We're building new design or re-designing and branding is not needed: we accept that the gathered context and research results are enough to proceed to the next step

4. **Design System**: Based on the gathered context, relevant research results, branding (when applicable), proceed to building the Design System that will be the foundation for the UI to be built. Iterate on that with the user until the user approves the Design System.

- Must read the [Skill references] section on this step if not yet.

5. **Components library**: From the design system, build the components library that will be used to build high-fidelity prototypes. You can also build some UI references or test pages so the user sees not only the components itself, but also how they could be used.

- Must read the [Skill references] section on this step if not yet.

## Skill references

Especially on steps 4 and 5 of the approach, it is highly recommended that you incorporate the `taste-skill` and `impeccable` to the process and even use them as reference for building the UI. They are consolidated skills for minimizing the so-called AI-slop. Pick one (the best that applies to that process) and proceed.

- `taste-skill`: `https://github.com/Leonxlnx/taste-skill/tree/main`
- `impeccable`: `https://github.com/pbakaus/impeccable`

## Output guidance

As the final result of that UI process, it is expected that the user get the following set of artifacts:

- Context file which has all the context not only for their initial ask, but also of this entire process.
- Research file + artifacts, with everything that was research and conclusions.
- Branding file + artifacts, with everything related to the branding process.
- Design system artifacts documenting the design system built
- Components library artifacts, documenting the components library that was built

The user should be able to point any agents and/or any tools like Claude Design, Open Design, etc. to the output as the source of truth for building the prototype.
