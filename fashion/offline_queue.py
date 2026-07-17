"""
Offline Queue
=============
Offline-first request queue for the Fashion AI app.

When the device has no internet connectivity, user requests are stored
in a local queue (JSON file or in-memory).  When connectivity is restored,
the queue is flushed and processed in order.

This module implements the Python / backend side of the offline story.
The frontend Service Worker handles the browser-side caching.

Usage
-----
    from fashion.offline_queue import OfflineQueue

    queue = OfflineQueue(persist_path="data/offline_queue.jsonl")

    # Enqueue when offline
    queue.enqueue(request_type="tutor_chat", payload={"message": "How do I sew darts?"})

    # Process when back online
    results = queue.flush(processor_fn=my_agent_function)
"""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class QueuedRequest:
    id: str
    request_type: str           # "tutor_chat" | "copilot" | "pattern" | "image_analysis"
    payload: dict[str, Any]
    created_at: float
    status: str = "pending"     # "pending" | "processing" | "done" | "failed"
    result: dict | None = None
    attempts: int = 0
    last_attempt: float | None = None
    error: str | None = None


# ---------------------------------------------------------------------------
# Queue
# ---------------------------------------------------------------------------

@dataclass
class OfflineQueue:
    """
    Offline-first request queue with JSON-lines persistence.

    Parameters
    ----------
    persist_path : path to JSONL file for persistent queue storage.
                   If None, operates in-memory only.
    max_retries  : maximum attempts before marking a request as failed.
    """
    persist_path: str | None = None
    max_retries: int = 3
    _queue: list[QueuedRequest] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.persist_path:
            self._load()

    # -----------------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------------

    def enqueue(
        self,
        request_type: str,
        payload: dict[str, Any],
        request_id: str | None = None,
    ) -> QueuedRequest:
        """
        Add a request to the offline queue.

        Parameters
        ----------
        request_type : type of request ("tutor_chat", "copilot", etc.)
        payload      : request data (will be sent to processor when online)
        request_id   : optional client-generated ID for deduplication

        Returns
        -------
        QueuedRequest that was enqueued
        """
        req = QueuedRequest(
            id=request_id or str(uuid.uuid4())[:8],
            request_type=request_type,
            payload=payload,
            created_at=time.time(),
        )
        # Deduplicate by ID
        if not any(r.id == req.id for r in self._queue):
            self._queue.append(req)
            if self.persist_path:
                self._append_to_file(req)
        return req

    def flush(
        self,
        processor_fn: Callable[[str, dict], dict] | None = None,
    ) -> list[QueuedRequest]:
        """
        Process all pending requests in the queue.

        Parameters
        ----------
        processor_fn : function(request_type, payload) → result_dict
                       If None, requests are marked as done with a stub result.

        Returns
        -------
        List of processed QueuedRequest objects
        """
        pending = [r for r in self._queue if r.status == "pending"]
        processed = []

        for req in pending:
            req.status = "processing"
            req.attempts += 1
            req.last_attempt = time.time()

            try:
                if processor_fn:
                    req.result = processor_fn(req.request_type, req.payload)
                else:
                    req.result = {"status": "ok", "note": "processed (stub)"}
                req.status = "done"
            except Exception as exc:  # noqa: BLE001
                req.error = str(exc)
                if req.attempts >= self.max_retries:
                    req.status = "failed"
                else:
                    req.status = "pending"  # will retry next flush

            processed.append(req)

        if self.persist_path:
            self._rewrite_file()

        return processed

    def pending_count(self) -> int:
        return sum(1 for r in self._queue if r.status == "pending")

    def all_requests(self, status: str | None = None) -> list[QueuedRequest]:
        if status:
            return [r for r in self._queue if r.status == status]
        return list(self._queue)

    def clear_done(self) -> int:
        """Remove completed requests from the queue. Returns count removed."""
        before = len(self._queue)
        self._queue = [r for r in self._queue if r.status != "done"]
        if self.persist_path:
            self._rewrite_file()
        return before - len(self._queue)

    def status_summary(self) -> dict[str, Any]:
        """Summary of queue state — useful for UI status indicators."""
        counts = {"pending": 0, "processing": 0, "done": 0, "failed": 0}
        for r in self._queue:
            counts[r.status] = counts.get(r.status, 0) + 1
        return {
            "total": len(self._queue),
            **counts,
            "has_pending": counts["pending"] > 0,
        }

    def export_for_sync(self) -> list[dict[str, Any]]:
        """
        Export pending requests as JSON-serializable dicts.
        Used by the frontend to sync with the server when connectivity returns.
        """
        return [
            asdict(r) for r in self._queue if r.status == "pending"
        ]

    # -----------------------------------------------------------------------
    # Persistence
    # -----------------------------------------------------------------------

    def _append_to_file(self, req: QueuedRequest) -> None:
        Path(self.persist_path).parent.mkdir(parents=True, exist_ok=True)  # type: ignore[arg-type]
        with open(self.persist_path, "a") as f:  # type: ignore[arg-type]
            f.write(json.dumps(asdict(req)) + "\n")

    def _rewrite_file(self) -> None:
        Path(self.persist_path).parent.mkdir(parents=True, exist_ok=True)  # type: ignore[arg-type]
        with open(self.persist_path, "w") as f:  # type: ignore[arg-type]
            for req in self._queue:
                f.write(json.dumps(asdict(req)) + "\n")

    def _load(self) -> None:
        path = Path(self.persist_path)  # type: ignore[arg-type]
        if not path.exists():
            return
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                req = QueuedRequest(**data)
                # Only reload non-done requests (done ones are stale)
                if req.status != "done":
                    self._queue.append(req)
            except (json.JSONDecodeError, TypeError):
                continue


# ---------------------------------------------------------------------------
# Connectivity helpers
# ---------------------------------------------------------------------------

def is_online(host: str = "8.8.8.8", port: int = 53, timeout: float = 2.0) -> bool:
    """
    Check internet connectivity by attempting a TCP connection.

    Uses DNS (port 53) as the test target — lightweight and reliable.
    """
    import socket
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except OSError:
        return False


def sync_if_online(
    queue: OfflineQueue,
    processor_fn: Callable[[str, dict], dict],
) -> dict[str, Any]:
    """
    Check connectivity and flush the queue if online.

    Returns a summary dict for logging/display.
    """
    online = is_online()
    if not online:
        return {
            "online": False,
            "pending": queue.pending_count(),
            "flushed": 0,
            "message": f"{queue.pending_count()} request(s) queued — will sync when online",
        }

    processed = queue.flush(processor_fn=processor_fn)
    done = sum(1 for r in processed if r.status == "done")
    failed = sum(1 for r in processed if r.status == "failed")

    return {
        "online": True,
        "flushed": len(processed),
        "done": done,
        "failed": failed,
        "message": f"Synced {done} request(s) successfully",
    }


# ---------------------------------------------------------------------------
# Quick demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        tmp_path = f.name

    queue = OfflineQueue(persist_path=tmp_path)

    print("=== Offline Queue Demo ===\n")

    # Simulate offline requests
    r1 = queue.enqueue("tutor_chat", {"message": "How do I sew invisible zipper?"})
    r2 = queue.enqueue("tutor_chat", {"message": "What is a dart?"})
    r3 = queue.enqueue("copilot", {"description": "Ankara blazer, size 12"})

    print(f"Queued {queue.pending_count()} requests")
    print("Status:", queue.status_summary())

    # Simulate coming back online and flushing
    def mock_processor(req_type: str, payload: dict) -> dict:
        return {"response": f"[mock response for {req_type}]", "payload": payload}

    processed = queue.flush(processor_fn=mock_processor)
    print(f"\nFlushed {len(processed)} requests:")
    for r in processed:
        print(f"  [{r.id}] {r.request_type} → {r.status}")

    cleared = queue.clear_done()
    print(f"\nCleared {cleared} done requests")
    print("Final status:", queue.status_summary())

    os.unlink(tmp_path)
