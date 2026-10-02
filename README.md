# Household Carbon Footprint & Target Tracker

Software Engineering coursework project based on **BPS61 -- Household
Carbon Footprint & Target Tracker**.

The project documents the analysis, requirements, UML modelling,
Jira-based project management, and software architecture/design work for
the system.

## Project Structure

``` text
.
├── lab2/
│   └── Lab 2 files
│
├── lab3/
│   └── Lab 3 files
│
├── 61_SE_Lab1_SE_Problem Statement...
│   └── Problem Statement
│
├── Household Carbon Footprint - Use ...
│   └── UML Use Case Diagram
│
├── Requirements_Table.docx
│   └── Requirements document
│
└── README.md
```

## Problem Statement

### Household Carbon Footprint & Target Tracker

The system helps a resident record household consumption, calculate
monthly carbon emissions, view carbon-footprint information, set
reduction targets, and track progress toward those targets.

### Main Functional Requirements

-   **FR-001 -- Calculate Monthly CO₂e**
    -   Calculate monthly carbon emissions from electricity and
        transport data.
-   **FR-002 -- Record Monthly Consumption**
    -   Enter and save monthly utility and commute data.
-   **FR-003 -- View Carbon Footprint**
    -   View monthly and historical CO₂e values.
-   **FR-004 -- Set Reduction Target**
    -   Set and update a carbon-reduction target and target period.
-   **FR-005 -- Track Reduction Progress**
    -   Track progress toward the reduction target.

### Non-Functional Requirements

-   **NFR-001 -- Interactive Performance**
    -   Annual milestone and historical graphs should render quickly and
        remain responsive.
-   **NFR-002 -- Authentication and Authorization**
    -   Household carbon-footprint and consumption data should be
        accessible only to authenticated and authorized users.

## UML Modelling

The project includes a UML Use Case Diagram showing the major actors and
system use cases.

### Actors

-   **Resident**
-   **Sustainability Coach**

### Major Use Cases

-   Record Monthly Consumption
-   Calculate Monthly CO₂e
-   View Carbon Footprint
-   Set/Update Reduction Target
-   Track Reduction Progress
-   View Historical Comparison

The use case model also represents the relevant `<<include>>` and
`<<extend>>` relationships.

## Lab 2 -- Jira

Lab 2 demonstrates project management using Jira.

Three Jira spaces/projects were created:

1.  **Scrum**
2.  **Kanban**
3.  **Bug Tracking**

The Jira work items were created from the functional and non-functional
requirements of BPS61.

The Kanban/Scrum work included:

-   Epics
-   User stories
-   Functional requirements
-   Non-functional requirements
-   Backlog management
-   Sprint/workflow tracking

The Bug Tracking project contains defect reports related to the system.

## Lab 3 -- Software Architecture & Design

Lab 3 extends the BPS61 project into software architecture and
component-level design.

The selected architecture is:

> **Layered Architecture**

The component design separates the system into presentation, business,
and data responsibilities.

### Main Components

-   **Resident Interface**
-   **Consumption Manager**
-   **CO₂e Calculator**
-   **Footprint Monitor**
-   **Target & Progress Manager**
-   **Carbon Data Store**

The component diagram defines interfaces between these components and
represents the flow of consumption, carbon-footprint, historical,
target, and stored-data information.

## Repository Contents

  Item                        Description
  --------------------------- --------------------------------------------
  `lab2/`                     Lab 2 Jira-related deliverables
  `lab3/`                     Lab 3 architecture and design deliverables
  Problem Statement           Original BPS61 problem statement
  UML Use Case Diagram        Use case model for the system
  `Requirements_Table.docx`   Requirements documentation
  `README.md`                 Project documentation

## Project Identifier

**BPS Number:** BPS61

**Project:** Household Carbon Footprint & Target Tracker
