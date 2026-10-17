import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database_connected"] is True
    assert data["model"] == "gemini-3.8-flash"
    assert "KaamSaathi" in data["app"]

def test_serve_index_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "KaamSaathi AI" in response.text
    assert "data-theme" in response.text

def test_earnings_crud_and_session_isolation(client):
    headers_user_a = {"X-Session-ID": "worker_session_alpha_12345"}
    headers_user_b = {"X-Session-ID": "worker_session_beta_67890"}

    # 1. User A creates an earning entry
    payload_a = {
        "date": "2024-10-15",
        "category": "Food Delivery",
        "platform": "Zomato",
        "gross_earnings": 1200.0,
        "tips_incentives": 150.0,
        "expenses": 250.0,
        "notes": "14 orders in peak evening"
    }
    create_resp = client.post("/api/earnings", json=payload_a, headers=headers_user_a)
    assert create_resp.status_code == 201
    entry_a = create_resp.json()
    assert entry_a["id"] is not None
    # Verify strict arithmetic: 1200 + 150 - 250 = 1100
    assert entry_a["net_earnings"] == 1100.0
    entry_a_id = entry_a["id"]

    # 2. User A can retrieve their own entry
    get_resp_a = client.get(f"/api/earnings/{entry_a_id}", headers=headers_user_a)
    assert get_resp_a.status_code == 200
    assert get_resp_a.json()["platform"] == "Zomato"

    # 3. User B CANNOT view or access User A's entry (Isolation check)
    get_resp_b = client.get(f"/api/earnings/{entry_a_id}", headers=headers_user_b)
    assert get_resp_b.status_code == 404

    # 4. User B's earnings list must NOT contain User A's record
    list_b = client.get("/api/earnings", headers=headers_user_b).json()
    assert len(list_b) == 0

    # 5. User B CANNOT delete User A's entry
    del_b = client.delete(f"/api/earnings/{entry_a_id}", headers=headers_user_b)
    assert del_b.status_code == 404

    # 6. User A updates their own entry (fuel cost increased by 50)
    update_resp = client.put(f"/api/earnings/{entry_a_id}", json={"expenses": 300.0}, headers=headers_user_a)
    assert update_resp.status_code == 200
    # Net: 1200 + 150 - 300 = 1050
    assert update_resp.json()["net_earnings"] == 1050.0

    # 7. User A's summary reflects the net calculation
    summary_a = client.get("/api/earnings/summary", headers=headers_user_a).json()
    assert summary_a["all_time"]["total_net"] == 1050.0

    # 8. User A deletes their entry
    del_a = client.delete(f"/api/earnings/{entry_a_id}", headers=headers_user_a)
    assert del_a.status_code == 200
    assert client.get(f"/api/earnings/{entry_a_id}", headers=headers_user_a).status_code == 404

def test_welfare_schemes_list_and_search(client):
    resp = client.get("/api/welfare")
    assert resp.status_code == 200
    schemes = resp.json()
    assert len(schemes) >= 5

    # Filter by category
    resp_cat = client.get("/api/welfare?category=Food%20Delivery")
    assert resp_cat.status_code == 200
    assert any("e-Shram" in s["name"] for s in resp_cat.json())

    # Filter by state
    resp_state = client.get("/api/welfare?location=Rajasthan")
    assert resp_state.status_code == 200
    assert any("Rajasthan" in s["name"] for s in resp_state.json())

def test_safety_guides_and_categories(client):
    resp = client.get("/api/safety/categories")
    assert resp.status_code == 200
    cats = resp.json()
    assert "Food Delivery" in cats
    assert "Cab/Ride-hailing" in cats

    guide_resp = client.get("/api/safety/Food%20Delivery")
    assert guide_resp.status_code == 200
    guide = guide_resp.json()
    assert "emergency_numbers" in guide
    assert len(guide["categories"]) >= 3

def test_missing_credentials_honest_error_handling(client, monkeypatch):
    """Priority 2: When API key is not configured, endpoints must return honest non-200 errors, not fake data."""
    # Temporarily remove GEMINI_API_KEY from settings
    monkeypatch.setenv("GEMINI_API_KEY", "")
    monkeypatch.setenv("GOOGLE_API_KEY", "")

    # 1. Document analysis text must return HTTP 503, NOT a fake success
    doc_resp = client.post("/api/documents/analyze-text", json={
        "document_text": "Clause 1: 15% platform fee deduction applies on all completed trips."
    })
    assert doc_resp.status_code in [502, 503]
    assert "API key" in doc_resp.json()["detail"] or "not configured" in doc_resp.json()["detail"]

    # 2. Grievance drafting must return HTTP 503, NOT a fake canned draft
    grievance_resp = client.post("/api/grievances/draft", json={
        "category": "Delayed or unpaid wages",
        "employer_platform": "DeliveryCo",
        "incident_date": "2024-10-10",
        "incident_details": "Payout of Rs 2000 not credited"
    })
    assert grievance_resp.status_code in [502, 503]
    assert "API key" in grievance_resp.json()["detail"] or "not configured" in grievance_resp.json()["detail"]

    # 3. Chat endpoint must return HTTP 503, NOT HTTP 200 with canned text
    chat_resp = client.post("/api/ai/chat", json={
        "message": "How do I calculate my net take-home earnings?"
    })
    assert chat_resp.status_code == 503
    assert "API key" in chat_resp.json()["detail"] or "not configured" in chat_resp.json()["detail"]

def test_document_upload_size_validation(client):
    """Priority 4: Reject oversized uploads exceeding 5 MB limit."""
    oversized_content = b"A" * (6 * 1024 * 1024) # 6 MB
    files = {"file": ("large_doc.txt", oversized_content, "text/plain")}
    resp = client.post("/api/documents/upload", files=files)
    assert resp.status_code == 413
    assert "exceeds maximum limit" in resp.json()["detail"]

def test_cross_session_isolation_grievances_and_documents(client):
    """Requirement 4: Prove two independent sessions cannot access each other's grievances or document history."""
    headers_user_a = {"X-Session-ID": "worker_alice_session_test_4455"}
    headers_user_b = {"X-Session-ID": "worker_bob_session_test_9988"}

    # 1. User A saves a grievance draft
    save_payload = {
        "category": "Delayed or unpaid wages",
        "employer_platform": "QuickBite Express",
        "incident_date": "2024-10-15",
        "amount_disputed": 1250.0,
        "incident_details": "Weekly payout delayed by 5 days without notification.",
        "generated_draft": "Formal notice of unpaid wage for week ending Oct 15.",
        "language": "en"
    }
    save_resp = client.post("/api/grievances/save", json=save_payload, headers=headers_user_a)
    assert save_resp.status_code == 201
    grievance_id = save_resp.json()["id"]

    # 2. User B CANNOT read User A's grievance by ID
    get_b = client.get(f"/api/grievances/{grievance_id}", headers=headers_user_b)
    assert get_b.status_code == 404

    # 3. User B's grievance list does NOT contain User A's record
    list_b = client.get("/api/grievances", headers=headers_user_b).json()
    assert all(g["id"] != grievance_id for g in list_b)

    # 4. User A saves a document analysis directly via service
    from app.services.document_service import save_document_analysis
    doc_id = save_document_analysis(
        filename="alice_contract.pdf",
        file_type="application/pdf",
        raw_text="Rider terms with 20% commission",
        analysis={"summary": "Alice confidential rider agreement"},
        session_id="worker_alice_session_test_4455"
    )

    # 5. User B CANNOT read User A's document details
    doc_b = client.get(f"/api/documents/{doc_id}", headers=headers_user_b)
    assert doc_b.status_code == 404

    # 6. User A CAN read their own document details
    doc_a = client.get(f"/api/documents/{doc_id}", headers=headers_user_a)
    assert doc_a.status_code == 200
    assert doc_a.json()["filename"] == "alice_contract.pdf"

def test_rate_limiter_blocks_excessive_ai_requests(client, monkeypatch):
    """Requirement 5: In-memory rate limiter returns 429 when threshold exceeded."""
    from app.services.rate_limiter import ai_rate_limiter
    ai_rate_limiter.reset_all()

    # Mock chat reply so we test the rate limiter without making 20 live network calls
    monkeypatch.setattr(
        "app.routers.ai.generate_chat_reply",
        lambda *args, **kwargs: {"reply": "ok", "language": "en"}
    )

    test_headers = {"X-Session-ID": "spammer_session_test_12345678"}
    
    # Send requests up to limit
    for _ in range(20):
        res = client.post("/api/ai/chat", json={"message": "hello"}, headers=test_headers)
        assert res.status_code == 200
    
    # 21st request should be rejected with 429
    excess_resp = client.post("/api/ai/chat", json={"message": "hello"}, headers=test_headers)
    assert excess_resp.status_code == 429
    assert "Too many AI requests" in excess_resp.json()["detail"]
    assert "Retry-After" in excess_resp.headers

    # Reset limiter so subsequent tests are unaffected
    ai_rate_limiter.reset_all()

def test_document_mandatory_sections_and_questions_to_ask():
    """Verify that document analysis forces 1-2 items for questions_to_ask and missing_info_checklist."""
    from app.services.gemini_service import _ensure_document_mandatory_items

    # Case 1: Payment statement with empty sections
    data_statement = {"summary": "Payment summary for week 42."}
    _ensure_document_mandatory_items(data_statement, doc_type="Payment Statement", language="en")
    
    assert "questions_to_ask" in data_statement
    assert len(data_statement["questions_to_ask"]) >= 1
    assert any("bag deduction" in q.lower() for q in data_statement["questions_to_ask"])
    assert any("platform access fee" in q.lower() for q in data_statement["questions_to_ask"])
    assert len(data_statement["missing_info_checklist"]) >= 1

    # Case 2: Hindi language output
    data_hi = {"summary": "भुगतान विवरण"}
    _ensure_document_mandatory_items(data_hi, doc_type="Salary Slip", language="hi")
    assert len(data_hi["questions_to_ask"]) >= 1
    assert any("कटौती" in q for q in data_hi["questions_to_ask"])
    assert len(data_hi["missing_info_checklist"]) >= 1


