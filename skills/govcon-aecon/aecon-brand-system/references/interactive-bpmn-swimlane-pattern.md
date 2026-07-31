# Interactive BPMN Swimlane Design Pattern

## When to use
Building interactive workflow visualizations that serve as both stakeholder briefings AND implementation specifications. Use when the user says: "make it interactive," "swimlane," "BPMN-style," "clickable workflows," "view controls," "filterable process," "state diagram," or rejects static linear diagrams as "too simple."

## Key principles

### Start from the user's specification, not from assumptions
The user gave this exact spec for a workflow diagram. When they provide this level of detail, build to it directly — don't simplify:

1. **Swimlanes** — horizontal lanes for each role (Manager, System, Justin, Mark, Amyn, IT, Leadership). Each action placed in the lane of the responsible person/system.
2. **BPMN semantics** — rounded rectangles = activities, diamonds = decisions, circles = start/end, clock icons = SLA timers, solid connectors = workflow, dashed = notifications/escalations.
3. **Role colors** — consistent across the entire document. Clay/orange for managers, olive for system, blue for Justin, purple for Mark, amber for Amyn, green for IT, red for leadership.
4. **View controls** — pill buttons that filter the diagram (Full Lifecycle, Internal Employee, Subcontractor, Temporary Consultant, Urgent, Denied, More Info Loop, SLA, Audit Evidence). Clicking highlights relevant path and dims unrelated.
5. **Clickable nodes** — every activity expands into a detail panel with: Owner, Trigger, Inputs, Required Fields, Business Rules, System Actions, Status Transition, Notifications, Records Updated, SLA, Error Handling, Audit Evidence.
6. **Three coordinated views** — not everything in one diagram. Use tabs: Swimlane Workflow, State Transition Diagram, SLA & Escalation.

### State diagrams
When the user asks for a state transition diagram:
- Show every valid status as a colored node
- Group by state type (active/pending/review/warning/bad/done)
- List transitions explicitly
- Purpose: directly implementable as Power Automate conditions
- Every transition writes an audit record

### SLA diagrams
When the user asks for SLA/escalation:
- Show it as a PARALLEL timer on each human approval stage, not as a separate section below
- Standard: 3d→Mark, 5d→Leadership, 7d→Public, 10d→Brian with audit trail
- Urgent: 24h→Mark, 48h→Leadership
- Use timeline bars showing proportional time segments
- Table format: Trigger, Recipient, Channel, Action

## Technical implementation

### Architecture
- Single self-contained HTML file (no external dependencies)
- CSS Grid for swimlane layout
- JavaScript for view filtering and detail panel toggling
- `data-view` attributes on every node for filter targeting
- `data-role` attributes for color assignment
- Overlay + fixed-position detail panel for node expansion

### CSS patterns
```css
/* Lane structure */
.lane { display: flex; border-bottom: 1px solid var(--g200); min-height: 72px; }
.lane-header { width: 160px; flex-shrink: 0; /* role label */ }
.lane-body { flex: 1; display: flex; align-items: center; gap: 0; overflow-x: auto; }

/* Nodes */
.node { cursor: pointer; transition: transform 100ms; }
.node:hover { transform: translateY(-2px); box-shadow: 0 3px 10px rgba(0,0,0,0.1); }
.node.dimmed { opacity: 0.2; pointer-events: none; }
.node.highlighted { opacity: 1; }

/* Decision diamonds */
.decision { width: 36px; height: 36px; transform: rotate(45deg); }
.decision span { transform: rotate(-45deg); /* readable text */ }

/* Connectors */
.connector { width: 20px; height: 2px; background: var(--g300); }
.connector::after { /* arrowhead via border trick */ }
.connector.dashed { /* repeating-linear-gradient for dashed lines */ }
```

### JavaScript patterns
```javascript
// View filtering
function setView(view, btn) {
  // Highlight active button
  // For each [data-view] element:
  //   if views includes selected view OR 'all' → show
  //   else → dim
}

// Detail panel
function openDetail(id) {
  // Lookup node details from data object
  // Build detail-grid HTML
  // Show overlay + panel
}

// Node detail data structure
const nodeDetails = {
  'node-id': {
    title, owner, trigger, inputs, fields, rules,
    actions, status, notify, records, sla, errors, audit
  }
}
```

### Role color palette
```css
--manager: #FFF5F2; --manager-border: #D97757;    /* Clay */
--system: #F5FAF2; --system-border: #788C5D;      /* Olive */
--justin: #F0F4FA; --justin-border: #4A7BBF;      /* Blue */
--mark: #F5F3FF; --mark-border: #8B5CF6;          /* Purple */
--amyn: #FFFBEB; --amyn-border: #B45309;          /* Amber */
--it: #F0FDF4; --it-border: #166534;              /* Green */
--leadership: #FEF2F2; --leadership-border: #991B1B; /* Red */
```

## Pitfalls

- **Don't mix happy path, decisions, and SLA into one linear diagram.** The user explicitly rejected this: "The current graphic looks clean, but it mixes the happy path, decision branches, and SLA escalation into one linear diagram. That makes the process appear simpler than it actually is."
- **Don't put SLA escalation below the process as a separate section.** Integrate it as a parallel timer on each human approval stage.
- **Don't use decorative colors alone — use shape semantics.** Rounded rectangles = activity, diamond = decision, circle = start/end. Color is supplementary, not primary.
- **Provide view controls.** The user wants to filter by path (internal vs sub vs temp vs urgent vs denied vs more info). Build the full diagram once, then use view filtering — don't build separate diagrams for each path.
- **Every activity node must be clickable with full detail.** This serves both executives (browse the overview) and engineers (expand into implementation). The detail panel must include all 12 fields: Owner, Trigger, Inputs, Required Fields, Business Rules, System Actions, Status, Notifications, Records, SLA, Errors, Audit.
- **Use three coordinated diagrams, not one.** Swimlane + State + SLA. Tab between them. Don't force everything into one visualization.
- **Mobile responsiveness.** The default view works at desktop widths. Add `flex-wrap: wrap` and `@media` breakpoints for mobile.
- **Consistent role colors across ALL views.** The same person uses the same color in swimlane, state diagram, and SLA diagram.
- **CSS scope leak when embedding into larger documents.** When merging standalone workflow CSS into a larger HTML document (e.g., embedding the swimlane into a multi-section technical design), loose class selectors like `.decision`, `.node`, `.connector`, `.overlay` will leak into other sections and BREAK existing styling. The `.decision` class from the swimlane (sets `width:36px` + `transform:rotate(45deg)` for diamond nodes) will squash decision-tree elements elsewhere. **Fix:** scope ALL workflow CSS selectors under a parent class (e.g., `.swimlane .decision`, `.swimlane .node`, `.swimlane .connector`) before merging. Rename `.overlay` to `.wf-overlay` to avoid conflicts. This was discovered when the Flow 1 decision tree CSS stopped rendering after embedding the workflow — it took 3 rounds to diagnose.
- **Stale in-line approver references when a role is removed.** When removing a role from the workflow (e.g., removing Amyn from the in-line access flow), ALL derivative artifacts must be updated — not just the primary swimlane diagram. Checklist: list schemas (filled-by columns), flow descriptions (step text), state diagrams (status names), decision trees (branch labels), permission models (role members), JavaScript node detail data (owner/trigger/fields), quick-reference tables (approval chains), and build estimates (hours). Stale references persist across multiple fix rounds because they're easy to miss in a large document. Do a full-text sweep for the removed role name after every diagram change.
- **Nextcloud share links may not resolve via curl.** When a user drops a Nextcloud share URL like `https://cloud.h.porb.dev/f/51970`, curl may return JSON/HTML rather than the image binary. The share token may not map directly to a file path. Instead: find the uploaded file by searching `/data/nextcloud/data/amyn/files/` for recently modified images (`find ... -name "*.png" -newer ...`), then embed as base64. For self-contained HTML deliverables, always use base64 data URLs — never external file references that may break when the document is shared.

## Reference implementation
The complete implementation is at `fcs-process-flows-v3-interactive.html` in the briefings folder. It includes:
- 7-lane swimlane with 25+ interactive nodes
- 12 decision diamonds
- 3 tabbed views (Swimlane / State / SLA)
- 9 path filters
- Full detail data for every node
- Responsive CSS with mobile breakpoints
