# Feature: [Component Name]

> **Feature Type**: UI Component Addition
>
> **Instructions**: This template is pre-filled for adding a new UI component. Customize the bracketed sections.

## Definition

Create a new [React/Vue/etc.] component `[ComponentName]` that allows users to [perform what action or see what information].

**User Story**: As a [user type], I want to [do something] so that [achieve goal].

**Visual Reference**: [Link to Figma/design/mockup if available]

---

## Relevant Files/Flows

- `src/components/` - Existing components directory
- `src/pages/[PageName].tsx` - Page where component will be used
- `src/hooks/[useHookName].ts` - Custom hooks (if needed)
- `src/api/[resource].ts` - API calls for data fetching
- `src/styles/` - Styling approach (CSS modules, Tailwind, styled-components)
- `src/types/[Type].ts` - TypeScript types/interfaces

---

## Expected Output

**Current State**:

- [What UI exists now?]
- [How do users currently accomplish this task?]

**Future State**:

- New `[ComponentName]` component available
- Component displays [what content]
- Users can interact by [describe interactions]
- Component appears on [which pages/contexts]

---

## Acceptance Criteria

- [ ] Component renders correctly with provided props
- [ ] Component handles loading state appropriately
- [ ] Component handles error state with user-friendly message
- [ ] Component handles empty/no-data state
- [ ] All interactive elements are accessible (keyboard navigation, ARIA labels)
- [ ] Component is responsive (mobile, tablet, desktop)
- [ ] Component follows design system/style guide
- [ ] Component has appropriate prop types/TypeScript interfaces
- [ ] Component is testable (React Testing Library, etc.)

---

## Component Specification

### Props Interface

```typescript
interface [ComponentName]Props {
  // Required props
  requiredProp: string;
  anotherRequired: number;

  // Optional props
  optionalProp?: boolean;
  onAction?: (data: ActionData) => void;

  // Styling
  className?: string;
  variant?: 'primary' | 'secondary' | 'danger';
}
```

### Component States

- Loading: Data is being fetched
- Success: Data loaded and displayed
- Error: Error occurred, show error message with retry option
- Empty: No data available, show empty state message

### User Interactions

- Click [element]: [What happens]
- Hover [element]: [Visual feedback]
- Keyboard navigation: [Tab order, Enter/Space handling]
- Form submission (if applicable): [Validation, submission, feedback]

### Example Usage

```typescript
import { [ComponentName] } from '@/components/[ComponentName]';

function ParentComponent() {
  return (
    <[ComponentName]
      requiredProp="value"
      anotherRequired={123}
      onAction={(data) => console.log(data)}
      variant="primary"
    />
  );
}
```

## Design Specifications

### Layout

- Width: [full-width / fixed width / max-width]
- Height: [auto / fixed / min-height]
- Padding/Margins: [Specify or "follow design system"]
- Grid/Flexbox: [Layout approach]

### Colors

- Background: [Color/token]
- Text: [Color/token]
- Borders: [Color/token]
- Hover states: [Color changes]

### Typography

- Font size: [Size or token]
- Font weight: [Weight]
- Line height: [Height]

### Spacing

- Use design system tokens: spacing-[xs|sm|md|lg|xl]

### Responsive Breakpoints

- Mobile (< 640px): [Behavior]
- Tablet (640px - 1024px): [Behavior]
- Desktop (> 1024px): [Behavior]

## Constraints

- Performance: Component should render in < [X]ms
- Bundle Size: Keep component size minimal (use code splitting if large)
- Browser Support: [Chrome, Firefox, Safari, Edge - latest 2 versions]
- Accessibility: WCAG 2.1 Level AA compliance
- Design System: Must use existing design tokens/components where possible

## Edge Cases

- Component receives invalid props → Show error boundary or fallback UI
- Data fetch fails → Show error message with retry button
- Very long text content → Truncate with ellipsis or wrap appropriately
- Empty array/no data → Show empty state with helpful message
- Slow network → Show loading indicator after [X]ms delay
- Component unmounts during async operation → Clean up to prevent memory - leaks
- [Add more edge cases specific to your component]

## Dependencies

- UI Library: [React, Vue, etc. - version]
- Component Library: [Material-UI, Ant Design, shadcn/ui, etc.]
- State Management: [Redux, Context, Zustand - if needed]
- Data Fetching: [React Query, SWR, useEffect - approach]
- Styling: [Tailwind, styled-components, CSS modules]
- Icons: [Icon library being used]

## Accessibility Requirements

- [ ] All interactive elements keyboard accessible
- [ ] Proper ARIA labels/roles where needed
- [ ] Focus indicators visible
- [ ] Color contrast meets WCAG AA (4.5:1 for normal text)
- [ ] Screen reader friendly (test with NVDA/JAWS/VoiceOver)
- [ ] No keyboard traps
- [ ] Form fields have associated labels

## Testing Requirements

Unit Tests:

- Component renders without crashing
- Props are passed correctly
- State changes work as expected
- Event handlers are called correctly

Integration Tests:

- Component works within parent context
- Data fetching and display works
- Error handling works

Visual Regression (if applicable):

- Component looks correct in different states
- Responsive behavior works

## Additional Context

Similar Components: [Reference existing components with similar patterns]
Animation/Transitions: [Any animations needed? Duration, easing]
Performance Considerations:

- Will this component render frequently? → Use React.memo/useMemo
- Large lists? → Use virtualization (react-window, etc.)

## Clarifications

[Leave empty - agent will populate]
