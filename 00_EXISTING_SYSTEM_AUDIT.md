# Phase 0: Existing System Audit Report

## 1. Audit Overview
This document evaluates the existing Swift Sign Chatbot codebase against the requirements of the Centralized Multi-Client AI Platform[cite: 8, 18].

## 2. Component Classification

| Component | Status | Description / Action |
| :--- | :--- | :--- |
| **FastAPI Core (`main.py`)** | **KEEP** | Standard ASGI foundation with CORS middleware[cite: 6]. |
| **Gemini Integration Layer** | **REFACTOR** | Wrap model calls in an abstract AI provider interface[cite: 18]. |
| **Database Schema (`models.py`)** | **REFACTOR** | Extend `Client` and `KnowledgeChunk` with `Assistant`, `BusinessUnit`, and metadata fields[cite: 13, 20]. |
| **Admin CRUD APIs (`admin.py`)** | **KEEP** | Functional endpoints for knowledge chunk management[cite: 6]. |
| **Floating Chat Widget (`index.html`, `style.css`, `script.js`)** | **KEEP** | Responsive client widget UI communicating with `/api/chat`[cite: 7]. |
| **Client Authentication** | **NEW** | Implement API Key / Token checks instead of trusting raw browser client IDs[cite: 10, 15]. |
| **Information Classification** | **NEW** | Enforce visibility controls (Public, Internal, Confidential)[cite: 13, 14]. |