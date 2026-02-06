# ADR-001: Next.js Web App Architecture

**Status**: Accepted
**Date**: 2026-02-04

## Context

The need to transition from a CLI-based todo application to a web-based application as part of Phase II of the 5-phase evolution plan. The constitution specifies that Phase II requires a Full-Stack Web App with Next.js frontend and FastAPI backend. The existing CLI application provides the functional requirements that need to be translated to a web interface.

## Decision

We will implement a full-stack web application using the following technology stack:

**Frontend**: Next.js 14 with App Router
- Framework: Next.js 14.x with App Router for file-based routing
- Language: TypeScript 5.3 for type safety
- Styling: Tailwind CSS for utility-first styling approach
- State Management: React state for client-side state and SWR for server state

**Backend**: FastAPI with SQLModel
- Framework: FastAPI 0.104.x for high-performance API with automatic documentation
- Language: Python 3.11
- ORM: SQLModel for database modeling (combines SQLAlchemy and Pydantic)
- Database: Neon DB (PostgreSQL-compatible serverless database)

**Architecture Pattern**: Separated frontend and backend applications communicating via REST API

## Alternatives Considered

1. **React + Vite + Express**:
   - Pros: Well-established ecosystem, simpler setup
   - Cons: Less integrated than Next.js, missing SSR capabilities, not compliant with constitution requirements

2. **Remix + Prisma**:
   - Pros: Strong server-client integration, excellent performance
   - Cons: More complex than required, not specifically mentioned in constitution

3. **SvelteKit + Hono**:
   - Pros: Lightweight, modern framework
   - Cons: Different ecosystem from constitution requirements, less mainstream

4. **Vue + Nuxt + Supabase**:
   - Pros: Alternative full-stack solution
   - Cons: Constitution specifically mentions Next.js for Phase II

## Consequences

**Positive**:
- Aligns with constitution requirements for Phase II
- Next.js provides excellent developer experience with built-in optimizations
- FastAPI provides automatic API documentation and type validation
- SQLModel bridges the gap between database models and API schemas
- Neon DB offers serverless scaling capabilities
- Clear separation of concerns between frontend and backend

**Negative**:
- Requires managing two separate applications
- Additional complexity compared to monolithic solution
- Need to coordinate deployments between frontend and backend

## References

- Plan: specs/003-web-todo-app/plan.md
- Research: specs/003-web-todo-app/research.md
- Data Model: specs/003-web-todo-app/data-model.md
- API Contract: specs/003-web-todo-app/contracts/tasks-api-contract.md
- Constitution: .specify/memory/constitution.md (Section 82-87)