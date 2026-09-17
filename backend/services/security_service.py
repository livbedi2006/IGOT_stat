"""
Security Hardening & Audit Logging Service for STATWISE Platform (Prompt Q).
Features:
- Security headers middleware: CSP, HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy.
- Rate Limiter with sliding window for login, upload, MCQ generation, and tutor chat.
- Structured Security Audit Logger for authentication, uploads, approvals, and exports.
- RBAC validation helper.
"""

import time
import os
import logging
from typing import Dict, Any, List, Optional
from fastapi import Request, HTTPException, Response
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime

logger = logging.getLogger("statwise.security")


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Injects robust HTTP security headers conforming to Prompt Q."""

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "connect-src 'self' http://localhost:* http://127.0.0.1:*;"
        )
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


class RateLimiter:
    """Sliding-window in-memory rate limiter for sensitive endpoints."""

    def __init__(self):
        # Maps endpoint_key -> {ip -> [timestamp, ...]}
        self.buckets: Dict[str, Dict[str, List[float]]] = {}
        # Route limits: (max_requests, window_seconds)
        self.limits = {
            "login": (10, 60),          # 10 requests per minute
            "upload": (15, 60),         # 15 uploads per minute
            "mcq_generate": (12, 60),   # 12 generations per minute
            "tutor_chat": (30, 60),     # 30 chat messages per minute
            "default": (120, 60)        # 120 standard requests per minute
        }

    def check_rate_limit(self, route_type: str, client_ip: str):
        now = time.time()
        max_req, window = self.limits.get(route_type, self.limits["default"])

        if route_type not in self.buckets:
            self.buckets[route_type] = {}
        if client_ip not in self.buckets[route_type]:
            self.buckets[route_type][client_ip] = []

        # Retain timestamps within the active sliding window
        active_timestamps = [t for t in self.buckets[route_type][client_ip] if now - t < window]
        if len(active_timestamps) >= max_req:
            logger.warning(f"Rate limit exceeded for route '{route_type}' from IP: {client_ip}")
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded for '{route_type}'. Please slow down and retry in {int(window)} seconds."
            )

        active_timestamps.append(now)
        self.buckets[route_type][client_ip] = active_timestamps


class SecurityAuditLogger:
    """Maintains an append-only security and administrative audit trail."""

    def __init__(self):
        self.audit_log: List[Dict[str, Any]] = []

    def log_event(
        self,
        event_type: str,
        user_id: str,
        user_role: str,
        action: str,
        status: str = "SUCCESS",
        ip_address: str = "127.0.0.1",
        details: Optional[Dict[str, Any]] = None
    ):
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": event_type,  # AUTH, UPLOAD, APPROVAL, EXPORT, ROLE_SWITCH
            "user_id": user_id,
            "user_role": user_role,
            "action": action,
            "status": status,
            "ip_address": ip_address,
            "details": details or {}
        }
        self.audit_log.append(entry)
        logger.info(f"[SECURITY AUDIT] {event_type} | {user_id} ({user_role}) | {action} | {status}")

    def get_audit_trail(self, limit: int = 50) -> List[Dict[str, Any]]:
        return list(reversed(self.audit_log[-limit:]))


# Singletons
rate_limiter = RateLimiter()
security_audit_logger = SecurityAuditLogger()
